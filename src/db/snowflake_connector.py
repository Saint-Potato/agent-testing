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
    
    # Retrieve network_timeout from environment variable, defaulting to DEFAULT_TIMEOUT from constants
    network_timeout_seconds = int(os.getenv("SNOWFLAKE_NETWORK_TIMEOUT", DEFAULT_TIMEOUT))
    
    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        network_timeout=network_timeout_seconds
    )
    return conn
