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
    
    # Retrieve network_timeout from environment variable or use a default.
    # The default is sourced from src.constants.DEFAULT_TIMEOUT (30 seconds).
    # This addresses the BUG where network_timeout was hardcoded to 1 second.
    try:
        network_timeout = int(os.getenv("SNOWFLAKE_NETWORK_TIMEOUT", str(DEFAULT_TIMEOUT)))
    except ValueError:
        logger.warning(f"Invalid SNOWFLAKE_NETWORK_TIMEOUT environment variable. Using default: {DEFAULT_TIMEOUT} seconds.")
        network_timeout = DEFAULT_TIMEOUT

    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        network_timeout=network_timeout
    )
    return conn
