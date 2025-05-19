from calendar import Calendar, monthrange
from datetime import date

import psycopg2.extras
from psycopg2.extensions import cursor

from cylinders import config
from cylinders.services.db_connection import connect_pg


def cylinders_day_count(cur: cursor, day_from: date, day_to: date):
    cur.execute(
        """
            SELECT 
                so."Колличество в связке", 
                so."Объём баллона, л", 
                so."Давление, ат",  
                SUM(bp."Количество")
            FROM "Баллоны в партиях" bp 
            INNER JOIN "Партии" p
                ON p.id = bp."ID партии"
            INNER JOIN "СоотношениеОбъёмов" so 
                ON bp."ID баллона" = so.ID
            WHERE p."Партия" BETWEEN %s AND %s
            GROUP BY so.ID
        """,
        (day_from, day_to, ))


def get_count_cylinders_by_weaks(month: int, year: int):
    with connect_pg(config.db_config) as conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        text_result = f"Отгружено баллонов в {month}.{year}:"
        for monday, *_, sunday in Calendar().monthdatescalendar(year, month):
            cylinders_day_count(cur, monday, sunday)
            text_result += f"\nНа конец недели {sunday}:\n"
            week_total_cylinders = 0
            for cylinder in cur:
                if cylinder['Количество в связке'] > 1:
                    monoblock_modifier = f"{cylinder['Количество в связке']}*"
                else:
                    monoblock_modifier = ""
                text_result += (
                    f"{monoblock_modifier}{cylinder['Объём баллона, л']} л "
                    f"({cylinder['Давление, ат']} ат.): {cylinder['sum']}\n"
                )
                week_total_cylinders += cylinder['sum']
            text_result += f"Итого за неделю баллонов: {week_total_cylinders}\n"
        return text_result


def get_count_cylinders(month: int, year: int):
    with connect_pg(config.db_config) as conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        text_result = f"Отгружено баллонов в {month}.{year}:"
        _, last_month_day = monthrange(year, month)
        start_date = date(year, month, 1)
        end_date = date(year, month, last_month_day)
        cylinders_day_count(cur, start_date, end_date)
        text_result += f"\n{year}-{month}:\n"
        total_cylinders = 0
        for cylinder in cur:
            if cylinder['Количество в связке'] > 1:
                monoblock_modifier = f"{cylinder['Количество в связке']}*"
            else:
                monoblock_modifier = ""
            text_result += (
                f"{monoblock_modifier}{cylinder['Объём баллона, л']} л "
                f"({cylinder['Давление, ат']} ат.): {cylinder['sum']}\n"
            )
            total_cylinders += cylinder['sum']
        text_result += f"Итого за месяц баллонов: {total_cylinders}\n"
        return text_result

if __name__ == "__main__":
    for i in range(1, 12):
        print(get_count_cylinders(i, 2024))
