from psycopg2.extensions import connection
from loguru import logger

from migrations.common import get_numeric_precision


def upgrade(con: connection):
    update_volume(con)
    update_pack_volume(con)
    con.commit()
    logger.info("columns with numeric type changed")


def update_volume(con):
    with con.cursor() as cur:
        cur.execute(get_numeric_precision("СоотношениеОбъёмов", "Объём газа, м3"))
        precision, scale = cur.fetchone()
        if precision == 7 and scale == 3:
            logger.debug("column Объём газа, м3 correct, no upgrade need")
            return
        cur.execute(
            """
            ALTER TABLE public."СоотношениеОбъёмов"
            ALTER COLUMN "Объём газа, м3" TYPE NUMERIC(7, 3)
            """
        )


def update_pack_volume(con):
    with con.cursor() as cur:
        cur.execute(get_numeric_precision("СоотношениеОбъёмов", "Объём газа в одном баллоне, м3"))
        precision, scale = cur.fetchone()
        if precision == 5 and scale == 3:
            logger.debug("column Объём газа в одном баллоне, м3 correct, no upgrade need")
            return
        cur.execute(
            """
            ALTER TABLE public."СоотношениеОбъёмов"
            ALTER COLUMN "Объём газа в одном баллоне, м3" TYPE NUMERIC(5, 3)
            """
        )
