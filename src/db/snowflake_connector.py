import os
import logging
import snowflake.connector

logger = logging.getLogger(__name__)

def get_snowflake_connection():
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    
    # Get network timeout from environment variable, default to 30 seconds if not set
    try:
        network_timeout = int(os.getenv("SNOWFLAKE_NETWORK_TIMEOUT", "30"))
    except ValueError:
        logger.warning("Invalid SNOWFLAKE_NETWORK_TIMEOUT environment variable. Using default of 30 seconds.")
        network_timeout = 30

    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        network_timeout=network_timeout
    )
    return conn
