import os
import typing
from pathlib import Path
from typing import NamedTuple

from dotenv import load_dotenv

app_dir = Path(__file__).parent.parent
load_dotenv(str(app_dir / '.env'))


class DBConfig(NamedTuple):
    dump_sqlite_path: Path = None
    pg_host: str = None
    pg_port: int = None
    pg_login: str = None
    pg_password: str = None
    pg_db_name: str = None
    sqlite_path: Path = None
    db_type: str = None


class RZNLogin(NamedTuple):
    login: str
    password: str


class RelatorioDocuments(NamedTuple):
    template: Path
    destination: Path


class Config(NamedTuple):
    app_dir: Path
    icon: Path
    db_config: DBConfig
    name_cylinders: typing.Dict[bool, str]
    log_file: Path
    dumps_path: Path
    rzn_login: RZNLogin
    headless_send: bool
    passport: RelatorioDocuments
    sticker: RelatorioDocuments
    many_stickers: RelatorioDocuments
    title_page: RelatorioDocuments
    load_volumes: typing.Optional[str]


icon = app_dir / "icons" / "icon.ico"

SQLITE_PATH = Path(os.getenv("SQLITE_PATH", default=r'c:\Users\Public\Python\WeatherDiary.db'))
DUMP_SQLITE_PATH = Path(os.getenv("DUMP_SQLITE_PATH", default=""))
DB_IP = os.getenv("DB_IP", default='192.168.1.39')
DB_PORT = int(os.getenv("DB_PORT", default=5432))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", default='batchs')
DB_TYPE = os.getenv("DB_TYPE", default='postgres')

db_config = DBConfig(
    dump_sqlite_path=DUMP_SQLITE_PATH,
    pg_host=DB_IP,
    pg_port=DB_PORT,
    pg_login=DB_USER,
    pg_password=DB_PASSWORD,
    pg_db_name=DB_NAME,
    sqlite_path=SQLITE_PATH,
    db_type=DB_TYPE,
)

name_cylinders = {True: "Баллоны", False: "Моноблоки"}

PRINT_LOG = app_dir / 'log' / 'print.log'

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

rzn_login = RZNLogin(
    login=LOGIN,
    password=PASSWORD
)

TEMPLATE_DIR = Path(os.getenv("TEMPLATE_DIR", default=app_dir / "templates"))
DESTINATION_DIR = Path(os.getenv("DESTINATION_DIR", default=r'c:\Users\Public\Подготовленные документы'))

TEMPLATE_PASSPORT = TEMPLATE_DIR / 'Шаблон паспорта КГМ.odt'
DESTINATION_PASSPORT = DESTINATION_DIR / 'паспорт КГМ.odt'

TEMPLATE_STICKER = TEMPLATE_DIR / 'Шаблон Этикетка.odt'
DESTINATION_STICKER = DESTINATION_DIR / 'Образцы этикеток.odt'

TEMPLATE_TITLE_PAGE = TEMPLATE_DIR / 'Шаблон титульного листа.odt'
DESTINATION_TITLE_PAGE = DESTINATION_DIR / 'Титульный.odt'

TEMPLATE_MANY_STICKER = TEMPLATE_DIR / 'Шаблон Этикеток на всю серию.odt'
DESTINATION_MANY_STICKER = DESTINATION_DIR / 'Этикетки на всю серию.odt'

LOAD_VOLUMES = os.getenv("LOAD_VOLUMES", None)


config = Config(
    app_dir=app_dir,
    icon=icon,
    db_config=db_config,
    name_cylinders=name_cylinders,
    log_file=PRINT_LOG,
    dumps_path=Path(os.getenv("DUMP_PATH", default=app_dir / "dumps")),
    rzn_login=rzn_login,
    headless_send=bool(int(os.getenv("HEADLESS_SELENIUM", default=1))),
    passport=RelatorioDocuments(TEMPLATE_PASSPORT, DESTINATION_PASSPORT),
    sticker=RelatorioDocuments(TEMPLATE_STICKER, DESTINATION_STICKER),
    many_stickers=RelatorioDocuments(TEMPLATE_MANY_STICKER, DESTINATION_MANY_STICKER),
    title_page=RelatorioDocuments(TEMPLATE_TITLE_PAGE, DESTINATION_TITLE_PAGE),
    load_volumes=LOAD_VOLUMES,
)
