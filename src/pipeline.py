import time
import logging

from src.db.snowflake_connector import get_snowflake_connection
from src.config import Config
from src.utils import parse_records

logger = logging.getLogger(__name__)


def get_snowflake_connection_with_retry(max_retries=None, base_delay=2):
    """Attempt to establish a Snowflake connection with exponential backoff.

    Args:
        max_retries: Maximum number of connection attempts. Defaults to
            Config.MAX_RETRIES.
        base_delay: Base delay in seconds for exponential backoff.

    Returns:
        An open Snowflake connection object.

    Raises:
        The last exception raised after all attempts are exhausted.
    """
    if max_retries is None:
        max_retries = Config.MAX_RETRIES

    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            return get_snowflake_connection()
        except Exception as exc:
            last_exc = exc
            if attempt == max_retries:
                logger.error(
                    f"All {max_retries} connection attempts failed. "
                    f"Last error: {exc}"
                )
                raise
            delay = base_delay * (2 ** (attempt - 1))
            logger.warning(
                f"Connection attempt {attempt}/{max_retries} failed: {exc}. "
                f"Retrying in {delay}s..."
            )
            time.sleep(delay)


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
