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
    
    # The network_timeout was previously hardcoded to 1 second, causing connection failures.
    # It is now configurable via SNOWFLAKE_NETWORK_TIMEOUT environment variable, 
    # defaulting to DEFAULT_TIMEOUT (30 seconds) from src/constants.py.
    snowflake_timeout = int(os.getenv("SNOWFLAKE_NETWORK_TIMEOUT", DEFAULT_TIMEOUT))
    
    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        network_timeout=snowflake_timeout
    )
    return conn
