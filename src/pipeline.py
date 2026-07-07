from src.db.snowflake_connector import get_snowflake_connection
from src.utils import parse_records
from src.db.queries import GET_RAW_EVENTS
import logging

logger = logging.getLogger(__name__)

def run_data_pipeline():
    logger.info("Starting pipeline run...")
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()

        # Corrected: Use the correct table name and query from queries.py
        cursor.execute(GET_RAW_EVENTS, (100,))

        records = cursor.fetchall()
        parsed = parse_records(records)
        logger.info(f"Processed {len(parsed)} records successfully.")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        raise
