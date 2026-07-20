import os
import logging
import snowflake.connector

logger = logging.getLogger(__name__)

def get_snowflake_connection():
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")

    logger.info("Initializing Snowflake connection...")

    # Intentional bug: timeout is passed as a string instead of an integer.
    # The connector later fails while processing the timeout configuration.
    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        network_timeout="1 second"
    )

    return conn
