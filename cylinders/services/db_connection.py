import sqlite3
import typing
from pathlib import Path

import psycopg2
from psycopg2.extensions import connection

from cylinders.config import DBConfig


def connect_pg(db_config: DBConfig) -> connection:
    return psycopg2.connect(
        host=db_config.pg_host,
        port=db_config.pg_port,
        user=db_config.pg_login,
        password=db_config.pg_password,
        dbname=db_config.pg_db_name)


def connect_sqlite(sqlite_path: typing.Union[Path, str]):
    return sqlite3.connect(sqlite_path)


def connect_db(db_config: DBConfig):
    if db_config.db_type == 'postgres':
        return connect_pg(db_config)
    elif db_config.db_type == 'sqlite':
        return connect_sqlite(db_config.sqlite_path)
    else:
        raise ValueError("Incorrect DB_TYPE. must be 'postgres' or 'sqlite', "
                         f"got {db_config.db_type}")
