from datetime import date

from cylinders import config
from cylinders.services.db_connection import connect_pg


if __name__ == '__main__':
    with connect_pg(config.db_config) as conn, conn.cursor() as cur:

        cur.execute("""
        UPDATE "Партии"
        SET "Партия" = %s
        WHERE id = %s
        """, (date(2020, 10, 24), 1459))
        conn.commit()
