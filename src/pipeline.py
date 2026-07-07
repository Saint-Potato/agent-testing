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

        # FIX: Use the correct, centralized query from src/db/queries.py
        # The original query had a typo ('raw_eventss') and was hardcoded.
        # GET_RAW_EVENTS targets 'events_staging' and selects 'id, raw_payload'
        # which aligns with parse_records expectations.
        cursor.execute(GET_RAW_EVENTS, (100,))

        records = cursor.fetchall()
        parsed = parse_records(records)
        logger.info(f"Processed {len(parsed)} records successfully.")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        raise
