import logging

from src.db.postgres_connector import get_postgres_connection

logger = logging.getLogger(__name__)


def run_daily_sync():
    logger.info("Starting daily sync job...")

    conn = get_postgres_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, customer_name, email
        FROM customers
    """)

    rows = cursor.fetchall()

    synced_records = []

    for row in rows:
        # Intentional Bug: row is a tuple, but accessed like a dictionary
        synced_records.append({
            "id": row["id"],
            "name": row["customer_name"],
            "email": row["email"]
        })

    logger.info(f"Successfully synced {len(synced_records)} records.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    run_daily_sync()
