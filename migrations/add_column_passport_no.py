from psycopg2.extensions import connection
from loguru import logger

from migrations.common import get_query_check_column


def upgrade(con: connection):
    with con.cursor() as cur:
        cur.execute(get_query_check_column("Партии", "passport_no"))
        if cur.fetchone()[0]:
            logger.debug("column exists, no upgrade need")
            return
        cur.execute(
            """
            ALTER TABLE public."Партии"
            ADD COLUMN passport_no integer;
            """
        )
        con.commit()
        logger.info("column passport_no was added to table")
