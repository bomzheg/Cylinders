import sqlite3
from pathlib import Path
from psycopg2.extensions import connection

from cylinders.services.db_connection import connect_pg
from cylinders.config import DBConfig

TABLES = ("Партии", "СоотношениеОбъёмов", "Баллоны в партиях")
SQL_BATCHS = """
    CREATE TABLE "Партии" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Серия varchar(10) NOT NULL,
        Партия date NOT NULL,
        Суфикс varchar(5) NULL,
        Показать boolean NULL DEFAULT True
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


def get_sqlite_conn(dump_path: Path):
    return sqlite3.connect(dump_path)


def get_cylinders_from_pg(conn: connection):
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM "СоотношениеОбъёмов"')
        data = []
        for cylinder_info in cur.fetchall():
            cylinder_info = list(cylinder_info)
            cylinder_info[1] = float(cylinder_info[1])
            cylinder_info[3] = float(cylinder_info[3])
            cylinder_info[6] = float(cylinder_info[6])
            data.append(cylinder_info)
        cur.close()

    return data


def get_batchs_info_from_pg(conn: connection):
    batchs = []
    with conn.cursor() as batch_cur, conn.cursor() as cylinder_cur:
        batch_cur.execute(
            f"SELECT id, Серия, Партия, Суфикс, Показать FROM Партии;"
        )
        for id_, *row_batch in batch_cur:
            row_batch = list(row_batch)
            cylinder_cur.execute('''
                        SELECT  
                            "ID баллона", 
                            "Количество" 
                        FROM "Баллоны в партиях"
                        WHERE "ID партии" = %s;''',
                                 (id_,)
                                 )
            cylinder_data = cylinder_cur.fetchall()
            batch = {'batch': row_batch, 'cylinders': cylinder_data}
            batchs.append(batch)
    return batchs


def get_data_from_pg(db_config: DBConfig):
    with connect_pg(db_config) as conn:
        cylinders = get_cylinders_from_pg(conn)
        batchs = get_batchs_info_from_pg(conn)
    return {'cylinders': cylinders, 'batchs': batchs}


def insert_data_in_sqlite(dump_path, data):
    with get_sqlite_conn(dump_path) as conn:
        cur = conn.cursor()
        for cylinder_info in data['cylinders']:
            cur.execute(
                """
                    INSERT INTO "СоотношениеОбъёмов" VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                cylinder_info
            )
        conn.commit()
        for batch in data['batchs']:
            cur.execute(
                """
                    INSERT INTO "Партии" (Серия, Партия, Суфикс, Показать) VALUES (?, ?, ?, ?);
                """,
                batch['batch']
            )
            cur.execute('SELECT id FROM "Партии" WHERE rowid=last_insert_rowid();')
            id_ = cur.fetchone()[0]
            for cylinder in batch['cylinders']:
                cur.execute(
                    """
                        INSERT INTO "Баллоны в партиях" VALUES (?, ?, ?);
                    """,
                    [id_, *cylinder]
                )
        conn.commit()


def backup_pg(db_config: DBConfig):
    drop_tables_sqlite(db_config.dump_sqlite_path)
    create_tables_sqlite(db_config.dump_sqlite_path)
    data = get_data_from_pg(db_config)
    insert_data_in_sqlite(db_config.dump_sqlite_path, data)


def drop_tables_sqlite(dump_path):
    with get_sqlite_conn(dump_path) as conn:
        cur = conn.cursor()
        for table in TABLES:
            cur.execute(f'DROP TABLE IF EXISTS "{table}";')
        conn.commit()
        cur.close()


def create_tables_sqlite(dump_path):
    with get_sqlite_conn(dump_path) as conn:
        cur = conn.cursor()
        cur.execute(SQL_BATCHS)
        cur.execute(SQL_CYLINDERS)
        cur.execute(SQL_MANY)
        conn.commit()
        cur.close()


if __name__ == '__main__':
    from cylinders.config import config
    backup_pg(config.db_config)
