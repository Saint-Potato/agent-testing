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
    
    # Get network timeout from environment variable, defaulting to DEFAULT_TIMEOUT from src/constants.py.
    # The Snowflake Connectivity & Timeout Runbook recommends a minimum of 10 seconds and a default of 30 seconds.
    network_timeout = int(os.getenv("SNOWFLAKE_NETWORK_TIMEOUT", str(DEFAULT_TIMEOUT)))

    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        network_timeout=network_timeout
    )
    return conn
