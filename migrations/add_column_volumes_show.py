from psycopg2.extensions import connection
from loguru import logger

from migrations.common import get_query_check_column


def upgrade(con: connection):
    with con.cursor() as cur:
        cur.execute(get_query_check_column("СоотношениеОбъёмов", "show"))
        if cur.fetchone()[0]:
            logger.debug("column show exists, no upgrade need")
            return
        cur.execute(
            """
            ALTER TABLE public."СоотношениеОбъёмов"
            ADD COLUMN show boolean DEFAULT true
            """
        )
        cur.execute(
            """
            UPDATE public."СоотношениеОбъёмов"
            SET show = false
            WHERE id = 100;
            """
        )
        con.commit()
        logger.info("column show added")
