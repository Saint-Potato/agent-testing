import os
import logging
import snowflake.connector
from src import constants

logger = logging.getLogger(__name__)

def get_snowflake_connection():
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    
    # Determine network timeout, defaulting to constants.DEFAULT_TIMEOUT (30 seconds)
    # if SNOWFLAKE_NETWORK_TIMEOUT environment variable is not set.
    network_timeout_val = int(os.getenv("SNOWFLAKE_NETWORK_TIMEOUT", str(constants.DEFAULT_TIMEOUT)))

    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        network_timeout=network_timeout_val
    )
    return conn
