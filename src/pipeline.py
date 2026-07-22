import time
import logging

from src.db.snowflake_connector import get_snowflake_connection
from src.config import Config
from src.utils import parse_records

logger = logging.getLogger(__name__)


def get_snowflake_connection_with_retry():
    """Attempt to obtain a Snowflake connection with exponential back-off retry.

    Retries up to Config.MAX_RETRIES times (default 3, env-overridable via
    MAX_RETRIES). Uses exponential back-off: 2s, 4s, 8s between attempts.
    Raises the last encountered exception if all attempts are exhausted.
    """
    last_exc = None
    for attempt in range(1, Config.MAX_RETRIES + 1):
        try:
            logger.info(
                f"Snowflake connection attempt {attempt}/{Config.MAX_RETRIES}"
            )
            return get_snowflake_connection()
        except Exception as exc:
            last_exc = exc
            wait = 2 ** attempt  # exponential back-off: 2s, 4s, 8s
            logger.warning(
                f"Connection attempt {attempt}/{Config.MAX_RETRIES} failed: {exc}. "
                f"Retrying in {wait}s..."
            )
            if attempt < Config.MAX_RETRIES:
                time.sleep(wait)

    raise last_exc


def run_data_pipeline():
    logger.info("Starting pipeline run...")
    conn = None
    cursor = None
    try:
        conn = get_snowflake_connection_with_retry()
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
