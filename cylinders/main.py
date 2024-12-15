import ctypes
import os
import sys
from pathlib import Path

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication
from loguru import logger

from cylinders.config import config, Config
from cylinders.services.db_connection import connect_pg
from cylinders.windows import BatchWindow
from migrations import add_column_passport_no, load_volumes


def logger_setup(log_file: Path):
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger.add(
        sink=log_file,
        format='{time} - {name} - {level} - {message}',
        level="DEBUG"
    )


def main():
    logger_setup(config.log_file)

    logger.info("Program started")

    try:
        show_window(config)
    except Exception as e:
        logger.exception(e)
        exit()


def show_window(current_config: Config):
    if os.name == 'nt':
        # fix app icon in task bar
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("bomzheg.batchs")

    current_config.dumps_path.mkdir(parents=True, exist_ok=True)

    add_column_passport_no.upgrade(connect_pg(current_config.db_config))
    if current_config.load_volumes:
        load_volumes.upgrade(current_config.load_volumes, connect_pg(current_config.db_config))


    app = QApplication([])
    app.setWindowIcon(QIcon(str(config.icon)))
    application = BatchWindow(
        db_config=current_config.db_config,
        dumps_path=current_config.dumps_path,
        rzn_login=current_config.rzn_login,
        headless_send=current_config.headless_send,
    )
    application.show()
    application.setWindowIcon(QIcon(str(current_config.icon)))

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
