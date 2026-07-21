import os
import logging
import time
import snowflake.connector
from src.config import Config

logger = logging.getLogger(__name__)

RETRY_BACKOFF_SECONDS = 5


def get_snowflake_connection():
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")

    logger.info("Initializing Snowflake connection...")

    last_exc = None
    for attempt in range(1, Config.MAX_RETRIES + 1):
        try:
            conn = snowflake.connector.connect(
                user=user,
                password=password,
                account=account,
                warehouse=warehouse,
                network_timeout=Config.SNOWFLAKE_NETWORK_TIMEOUT  # integer seconds, e.g. 30
            )
            logger.info("Snowflake connection established successfully.")
            return conn
        except Exception as e:
            last_exc = e
            logger.warning(
                f"Snowflake connection attempt {attempt}/{Config.MAX_RETRIES} failed: {e}. "
                f"Retrying in {RETRY_BACKOFF_SECONDS * attempt}s..."
            )
            time.sleep(RETRY_BACKOFF_SECONDS * attempt)

    logger.error("All Snowflake connection attempts exhausted.")
    raise ConnectionError(
        f"Failed to connect to Snowflake after {Config.MAX_RETRIES} attempts. "
        f"Last error: {last_exc}"
    ) from last_exc
