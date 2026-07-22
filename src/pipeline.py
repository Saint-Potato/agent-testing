import time
import logging

from src.config import Config
from src.db.snowflake_connector import get_snowflake_connection
from src.utils import parse_records

logger = logging.getLogger(__name__)


def run_data_pipeline():
    logger.info("Starting pipeline run...")

    conn = None
    last_exc = None

    # Attempt to establish a Snowflake connection with exponential backoff.
    # MAX_RETRIES is read from the environment via Config (default: 3).
    for attempt in range(1, Config.MAX_RETRIES + 1):
        try:
            conn = get_snowflake_connection()
            break
        except Exception as e:
            last_exc = e
            wait = 2 ** attempt
            logger.warning(
                f"Snowflake connection attempt {attempt}/{Config.MAX_RETRIES} "
                f"failed: {e}. Retrying in {wait}s..."
            )
            time.sleep(wait)

    if conn is None:
        logger.error(
            f"All {Config.MAX_RETRIES} Snowflake connection attempts failed."
        )
        raise last_exc

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM raw_events LIMIT 100")
        records = cursor.fetchall()
        parsed = parse_records(records)
        logger.info(f"Processed {len(parsed)} records successfully.")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        raise e
    finally:
        try:
            conn.close()
        except Exception:
            pass
