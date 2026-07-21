import os


class Config:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    # Enforce runbook minimum of 10 seconds; default is 30 seconds.
    SNOWFLAKE_NETWORK_TIMEOUT = max(10, int(os.getenv('SNOWFLAKE_NETWORK_TIMEOUT', '30')))
