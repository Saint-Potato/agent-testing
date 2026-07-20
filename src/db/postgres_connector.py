import os
import time
import logging
import psycopg2

from src.config import Config

logger = logging.getLogger(__name__)


def get_postgres_connection():
    connect_timeout = int(os.getenv("PGCONNECT_TIMEOUT", "30"))
    last_exc = None

    for attempt in range(1, Config.MAX_RETRIES + 1):
        try:
            conn = psycopg2.connect(
                host=os.getenv("PGHOST"),
                database=os.getenv("PGDATABASE"),
                user=os.getenv("PGUSER"),
                password=os.getenv("PGPASSWORD"),
                connect_timeout=connect_timeout
            )
            logger.info(f"PostgreSQL connection established on attempt {attempt}.")
            return conn
        except psycopg2.OperationalError as exc:
            last_exc = exc
            logger.warning(
                f"PostgreSQL connection attempt {attempt}/{Config.MAX_RETRIES} failed: {exc}. "
                f"{'Retrying in 5 seconds...' if attempt < Config.MAX_RETRIES else 'No more retries.'}"
            )
            if attempt < Config.MAX_RETRIES:
                time.sleep(5)

    raise ConnectionError(
        f"Failed to connect to PostgreSQL after {Config.MAX_RETRIES} attempts."
    ) from last_exc
