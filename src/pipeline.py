import time
import logging

from src.config import Config
from src.db.snowflake_connector import get_snowflake_connection
from src.utils import parse_records

logger = logging.getLogger(__name__)


def run_data_pipeline():
    logger.info("Starting pipeline run...")
    conn = None
    cursor = None
    last_exc = None

    for attempt in range(1, Config.MAX_RETRIES + 1):
        try:
            conn = get_snowflake_connection()
            break
        except Exception as e:
            last_exc = e
            wait = 2 ** attempt  # exponential backoff: 2s, 4s, 8s
            logger.warning(
                f"Snowflake connection attempt {attempt}/{Config.MAX_RETRIES} failed: {e}. "
                f"Retrying in {wait}s..."
            )
            time.sleep(wait)
    else:
        logger.error("All Snowflake connection attempts exhausted.")
        raise last_exc

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM raw_events LIMIT 100")

        records = cursor.fetchall()

        # records is a list of tuples returned by fetchall(); use len() to get the count
        logger.info(f"Fetched {len(records)} records from Snowflake.")

        parsed = parse_records(records)
        logger.info(f"Processed {len(parsed)} records successfully.")

    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}", exc_info=True)
        raise
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
