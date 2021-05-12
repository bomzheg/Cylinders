import sqlite3
from sqlite3 import Connection
from pathlib import Path

import psycopg2
import psycopg2.extras

from cylinders.config import DBConfig
from cylinders.services.db_connection import connect_pg

TABLES = ("Партии", "СоотношениеОбъёмов", "Баллоны в партиях")
SQL_BATCHS = """
    CREATE TABLE "Партии" (
        id SERIAL PRIMARY KEY NOT NULL,
        Серия varchar(10) NOT NULL,
        Партия date NOT NULL,
        Суфикс varchar(5) NULL,
        Показать boolean NULL DEFAULT True,
        passport_no integer
    );
    """
SQL_CYLINDERS = """
    CREATE TABLE "СоотношениеОбъёмов"  (
        ID SERIAL PRIMARY KEY NOT NULL,
        "Объём баллона, л" numeric(4,2) NOT NULL,
        "Давление, ат" smallint NOT NULL,
        "Объём газа, м3" numeric(7,2) NOT NULL,
        "Температура, °С" smallint NOT NULL,
        "Колличество в связке" smallint NOT NULL,
        "Объём газа в одном баллоне, м3" numeric(5,2) NOT NULL
    );
    """
SQL_MANY = """
    CREATE TABLE "Баллоны в партиях" (
        "ID партии" integer NOT NULL,
        "ID баллона" integer NOT NULL,
        "Количество" integer NOT NULL,
        PRIMARY KEY ("ID партии", "ID баллона")
    );
"""


def get_sqlite_conn(sqlite_path: Path):
    return sqlite3.connect(sqlite_path)


def get_cylinders_from_sqlite(conn: Connection):
    cur = conn.cursor()
    cur.execute('SELECT * FROM "СоотношениеОбъёмов"')
    data = cur.fetchall()
    cur.close()
    return data


def get_batchs_info_from_sqlite(conn: Connection):
    batchs = []
    batch_cur = conn.cursor()
    cylinder_cur = conn.cursor()
    batch_cur.execute(
        f"SELECT id, Серия, Партия, Суфикс, Показать, passport_no FROM 'Партии';"
    )
    for id_, *row_batch in batch_cur:
        row_batch = list(row_batch)
        row_batch[0] = row_batch[0].strip()
        row_batch[-2] = bool(row_batch[-2])
        cylinder_cur.execute('''
                    SELECT  
                        "ID баллона", 
                        "Количество" 
                    FROM "Баллоны в партиях"
                    WHERE "ID партии" = ?;''',
                             (id_,)
                             )
        cylinder_data = cylinder_cur.fetchall()
        batch = {'batch': row_batch, 'cylinders': cylinder_data}
        batchs.append(batch)
    cylinder_cur.close()
    batch_cur.close()
    return batchs


def get_data_from_sqlite(sqlite_path: Path):
    if not (sqlite_path.is_file() or sqlite_path.exists()):
        raise ValueError(
            "In $DUMP_SQLITE_PATH not path to file. "
            "please make sure that its path referer to sqlite dump "
            f'now it is "{sqlite_path}"')
    with get_sqlite_conn(sqlite_path) as conn:
        cylinders = get_cylinders_from_sqlite(conn)
        batchs = get_batchs_info_from_sqlite(conn)
    return {'cylinders': cylinders, 'batchs': batchs}


def insert_data_in_pg(db_config: DBConfig, data):
    with connect_pg(db_config) as conn, conn.cursor() as cur:
        psycopg2.extras.execute_values(
            cur,
            """
                INSERT INTO "СоотношениеОбъёмов" VALUES %s;
            """,
            data['cylinders']
        )
        conn.commit()
        for batch in data['batchs']:
            cur.execute(
                """
                    INSERT INTO "Партии" 
                    (Серия, Партия, Суфикс, Показать, passport_no) 
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """,
                batch['batch']
            )
            id_ = cur.fetchone()[0]
            for cylinder in batch['cylinders']:
                cur.execute(
                    """
                        INSERT INTO "Баллоны в партиях" VALUES (%s, %s, %s);
                    """,
                    [id_, *cylinder]
                )
        conn.commit()


def main(db_config: DBConfig):
    data = get_data_from_sqlite(db_config.dump_sqlite_path)
    insert_data_in_pg(db_config, data)


def drop_tables_pg(db_config: DBConfig):
    with connect_pg(db_config) as conn, conn.cursor() as cur:
        for table in TABLES:
            cur.execute(f'DROP TABLE IF EXISTS "{table}";')
        conn.commit()


def create_tables_pg(db_config: DBConfig):
    with connect_pg(db_config) as conn, conn.cursor() as cur:
        cur.execute(SQL_BATCHS)
        cur.execute(SQL_CYLINDERS)
        cur.execute(SQL_MANY)
        conn.commit()


def load_to_pg(db_config: DBConfig):
    drop_tables_pg(db_config)
    create_tables_pg(db_config)
    main(db_config)


if __name__ == '__main__':
    from cylinders.config import config
    load_to_pg(config.db_config)
