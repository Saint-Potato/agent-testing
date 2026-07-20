import os
import logging
import time
import snowflake.connector

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
                network_timeout=Config.SNOWFLAKE_NETWORK_TIMEOUT  # integer seconds, default 30s per runbook
            )
            logger.info(f"Snowflake connection established on attempt {attempt}/{Config.MAX_RETRIES}.")
            return conn
        except Exception as exc:
            last_exc = exc
            logger.warning(
                f"Snowflake connection attempt {attempt}/{Config.MAX_RETRIES} failed: {exc}"
            )
            if attempt < Config.MAX_RETRIES:
                backoff = 5 * attempt
                logger.info(f"Retrying Snowflake connection in {backoff}s...")
                time.sleep(backoff)

    logger.error(
        f"Snowflake connection failed after {Config.MAX_RETRIES} attempts. Last error: {last_exc}"
    )
    raise ConnectionError(
        f"Unable to connect to Snowflake after {Config.MAX_RETRIES} attempts."
    ) from last_exc
