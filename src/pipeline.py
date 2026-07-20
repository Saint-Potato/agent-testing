import time
import logging

from src.db.snowflake_connector import get_snowflake_connection
from src.utils import parse_records
from src.config import Config

logger = logging.getLogger(__name__)


def run_data_pipeline():
    logger.info("Starting pipeline run...")
    last_exc = None

    for attempt in range(1, Config.MAX_RETRIES + 1):
        conn = None
        cursor = None
        try:
            conn = get_snowflake_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM raw_events LIMIT 100")

            records = cursor.fetchall()

            # records is a list of tuples returned by fetchall(); use len() to get the count
            logger.info(f"Fetched {len(records)} records from Snowflake.")

            parsed = parse_records(records)
            logger.info(f"Processed {len(parsed)} records successfully.")
            return  # success — exit retry loop

        except Exception as e:
            last_exc = e
            logger.warning(
                f"Pipeline attempt {attempt}/{Config.MAX_RETRIES} failed: {e}"
            )
            if attempt < Config.MAX_RETRIES:
                backoff = 2 ** attempt
                logger.info(f"Retrying pipeline in {backoff}s...")
                time.sleep(backoff)

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

    logger.error(
        f"Pipeline execution failed after {Config.MAX_RETRIES} attempts. Last error: {last_exc}"
    )
    raise last_exc
