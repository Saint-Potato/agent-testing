import os
import logging
import snowflake.connector

logger = logging.getLogger(__name__)

def get_snowflake_connection():
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    
    # Fetch network timeout from environment variable, default to 60 seconds
    # The previous hardcoded value of 1 second was causing connection timeouts.
    snowflake_network_timeout = int(os.getenv("SNOWFLAKE_NETWORK_TIMEOUT", "60"))

    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        network_timeout=snowflake_network_timeout
    )
    return conn
