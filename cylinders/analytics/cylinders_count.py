import calendar
from datetime import date

from psycopg2.extensions import connection

from cylinders import config
from cylinders.services.db_connection import connect_pg


def count_cylinders_day(conn: connection, day: date) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
                SELECT SUM(bp."Количество")
                FROM "Баллоны в партиях" bp 
                    INNER JOIN "Партии" p
                    ON p.id = bp."ID партии"
                WHERE p."Партия" = %s
            """,
            (day, ))
        return cur.fetchone()[0]


def get_count_cylinders(month: int, year: int):
    with connect_pg(config.db_config) as conn:
        sum_ = 0
        for day in range(calendar.monthrange(year, month)[1]):
            date_ = date(year, month, day + 1)
            count = count_cylinders_day(conn, date_)
            sum_ += count or 0
            # print(date_, count)
        print(month, sum_)


if __name__ == "__main__":
    for i in range(1, 12):
        get_count_cylinders(i, 2024)
