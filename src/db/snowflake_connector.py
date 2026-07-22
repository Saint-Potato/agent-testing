import os
import logging
import time
import snowflake.connector
from snowflake.connector.errors import OperationalError

from src.config import Config

logger = logging.getLogger(__name__)


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
                network_timeout=Config.SNOWFLAKE_NETWORK_TIMEOUT  # integer seconds, default 30 via env var
            )
            logger.info(f"Snowflake connection established on attempt {attempt}.")
            return conn
        except (OperationalError, Exception) as exc:
            last_exc = exc
            wait = 5
            logger.warning(
                f"Snowflake connection attempt {attempt}/{Config.MAX_RETRIES} failed: {exc}. "
                f"Retrying in {wait}s..."
            )
            if attempt < Config.MAX_RETRIES:
                time.sleep(wait)

    logger.error("All Snowflake connection attempts exhausted.")
    raise ConnectionError(
        f"Failed to connect to Snowflake after {Config.MAX_RETRIES} attempts. "
        f"Last error: {last_exc}"
    ) from last_exc
