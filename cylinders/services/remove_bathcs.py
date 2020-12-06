from psycopg2.extensions import connection

from cylinders import config
from cylinders.services.db_connection import connect_pg


def remove_batch(conn: connection, seria: str):
    with conn.cursor() as cur:
        cur.execute(
            """
                DELETE
                FROM "Баллоны в партиях"
                WHERE "Баллоны в партиях"."ID партии" IN (
                    SELECT id 
                    FROM "Партии"
                    WHERE "Серия" = %s
                )
            """,
            (seria, ))
        cur.execute('''DELETE FROM "Партии" WHERE "Серия" = %s;''', (seria, ))


def rm_marked_batches():
    with connect_pg(config.db_config) as conn:
        remove_batch(conn, 'удалить')
        conn.commit()


if __name__ == '__main__':
    rm_marked_batches()
