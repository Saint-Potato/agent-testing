import os
import logging
import snowflake.connector

from src.constants import DEFAULT_TIMEOUT

logger = logging.getLogger(__name__)


def get_snowflake_connection():
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")

    # Validate network_timeout is a safe integer before attempting connection.
    network_timeout = DEFAULT_TIMEOUT
    if not isinstance(network_timeout, int) or network_timeout < 10:
        raise ValueError(
            f"network_timeout must be an integer >= 10, got {network_timeout!r}"
        )

    logger.info("Initializing Snowflake connection...")

    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        network_timeout=network_timeout  # integer 30, per runbook guidance
    )

    return conn
