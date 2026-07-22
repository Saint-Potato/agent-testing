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
                network_timeout=Config.SNOWFLAKE_NETWORK_TIMEOUT  # integer seconds, default 30
            )
            logger.info(
                f"Snowflake connection established on attempt {attempt} "
                f"(network_timeout={Config.SNOWFLAKE_NETWORK_TIMEOUT}s)."
            )
            return conn
        except OperationalError as exc:
            last_exc = exc
            backoff = 5 * attempt
            logger.warning(
                f"Snowflake connection attempt {attempt}/{Config.MAX_RETRIES} failed: {exc}. "
                f"Retrying in {backoff}s..."
            )
            if attempt < Config.MAX_RETRIES:
                time.sleep(backoff)

    raise ConnectionError(
        f"Failed to establish Snowflake connection after {Config.MAX_RETRIES} attempts. "
        f"Last error: {last_exc}"
    )
