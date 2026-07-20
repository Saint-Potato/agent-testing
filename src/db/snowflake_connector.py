import os
import logging
import time
import snowflake.connector

from src.constants import DEFAULT_TIMEOUT
from src.config import Config

logger = logging.getLogger(__name__)


def get_snowflake_connection():
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")

    last_exc = None
    for attempt in range(1, Config.MAX_RETRIES + 1):
        try:
            conn = snowflake.connector.connect(
                user=user,
                password=password,
                account=account,
                warehouse=warehouse,
                network_timeout=DEFAULT_TIMEOUT  # 30 seconds per runbook recommendation
            )
            logger.info(f"Snowflake connection established on attempt {attempt}.")
            return conn
        except Exception as exc:
            last_exc = exc
            logger.warning(
                f"Snowflake connection attempt {attempt}/{Config.MAX_RETRIES} failed: {exc}. "
                f"{'Retrying in 5 seconds...' if attempt < Config.MAX_RETRIES else 'No more retries.'}"
            )
            if attempt < Config.MAX_RETRIES:
                time.sleep(5)

    raise ConnectionError(
        f"Failed to connect to Snowflake after {Config.MAX_RETRIES} attempts."
    ) from last_exc
