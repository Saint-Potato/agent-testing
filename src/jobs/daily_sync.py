import logging
import psycopg2.extras

from src.db.postgres_connector import get_postgres_connection

logger = logging.getLogger(__name__)


def run_daily_sync():
    logger.info("Starting daily sync job...")

    conn = None
    cursor = None

    try:
        conn = get_postgres_connection()
        # Use RealDictCursor so rows can be accessed by column name
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute("""
            SELECT id, customer_name, email
            FROM customers
        """)

        rows = cursor.fetchall()

        synced_records = []

        for row in rows:
            synced_records.append({
                "id": row["id"],
                "name": row["customer_name"],
                "email": row["email"]
            })

        logger.info(f"Successfully synced {len(synced_records)} records.")

    except Exception as exc:
        logger.error(f"Daily sync job failed: {exc}", exc_info=True)
        raise

    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


if __name__ == "__main__":
    run_daily_sync()
