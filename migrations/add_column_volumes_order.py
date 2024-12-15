from psycopg2.extensions import connection
from loguru import logger

from migrations.common import get_query_check_column


def upgrade(con: connection):
    with con.cursor() as cur:
        cur.execute(get_query_check_column("СоотношениеОбъёмов", "order_"))
        if cur.fetchone()[0]:
            logger.debug("column order exists, no upgrade need")
            return
        cur.execute(
            """
            ALTER TABLE public."СоотношениеОбъёмов"
            ADD COLUMN order_ integer DEFAULT 9999;
            """
        )
        con.commit()
        logger.info("column order added")
