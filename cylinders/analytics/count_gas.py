import typing
import calendar
from datetime import date
from typing import Tuple

from psycopg2.extensions import cursor, connection

from cylinders import config
from cylinders.services.db_connection import connect_pg


def get_butchs_month(cur: cursor, month_number: int, year: int) -> typing.List[int]:
    cur.execute(
        """
        SELECT id
        FROM "Партии"
        WHERE date_part('month', "Партия") = %s and date_part('year', "Партия") = %s
        """,
        (month_number, year)
    )
    return [row[0] for row in cur.fetchall()]


def get_batch_m3_count(cur: cursor, batch_id: int) -> float:
    cur.execute(
        """
        SELECT sum(so."Объём газа, м3" * bp."Количество")
        FROM "Партии" p 
        INNER JOIN "Баллоны в партиях" bp 
            ON p.id = bp."ID партии" 
        INNER JOIN "СоотношениеОбъёмов" so 
            ON bp."ID баллона" = so.ID
        WHERE p.id = %s
        """,
        (batch_id, )
    )
    return cur.fetchone()[0]


def get_batch_m3_count_day(cur: cursor, day: date) -> float:
    cur.execute(
        """
        SELECT sum(so."Объём газа, м3" * bp."Количество")
        FROM "Партии" p 
        INNER JOIN "Баллоны в партиях" bp 
            ON p.id = bp."ID партии" 
        INNER JOIN "СоотношениеОбъёмов" so 
            ON bp."ID баллона" = so.ID
        WHERE p."Партия" = %s
        """,
        (day, )
    )
    return cur.fetchone()[0]


def count_m3_gaz_month(conn: connection, month_number: int, year: int) -> float:
    with conn.cursor() as cur:
        batchs = get_butchs_month(cur, month_number, year)
        s = 0
        for batch_id in batchs:
            count_m3 = get_batch_m3_count(cur, batch_id)
            if count_m3 is not None:
                s += count_m3
        return s


def print_m3_gaz_year(year: int):
    with connect_pg(config.db_config) as conn:
        for i in range(1, 13):
            print(i, count_m3_gaz_month(conn, i, year))


def get_100_id(conn: connection):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT p."Партия"
            FROM "Партии" p 
            INNER JOIN "Баллоны в партиях" bp 
                ON p.id = bp."ID партии" 
            WHERE bp."ID баллона" = 100 AND bp."Количество" > 0
            ORDER BY p."Партия"
            """
        )
        return cur.fetchall()


def get_count_gas(month: int, year: int) -> typing.List[Tuple[date, float]]:
    with connect_pg(config.db_config) as conn, conn.cursor() as cur:
        result = []
        for day in range(calendar.monthrange(year, month)[1]):
            date_ = date(year, month, day + 1)
            count = get_batch_m3_count_day(cur, date_)
            result.append((date_, count))
    return result


def get_summary_month(month: int, year: int):
    print(f"{month}.{year}", sum([count for _, count in get_count_gas(month, year) if count is not None]))


def print_month_gaz(data: typing.List[Tuple[date, float]]):
    print("\n".join(map(lambda t: f"{t[0].isoformat()} {t[1]}" , data)))


if __name__ == "__main__":
    print_month_gaz(get_count_gas(5,2021))
    get_summary_month(5, 2021)
