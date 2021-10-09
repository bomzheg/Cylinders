"""
Модуль управляющий окном с сериями
"""
import sqlite3
from datetime import date, datetime
import threading
from pathlib import Path
from time import sleep

from PySide2.QtCore import *
from PySide2.QtGui import QCursor
from PySide2.QtWidgets import *
from loguru import logger

from cylinders.config import RZNLogin, DBConfig
from cylinders.models.batch import BatchBaseModel, BatchPostgresModel, BatchSqliteModel
from cylinders.models.cylinders import CylindersBaseModel, CylindersPostgresModel, CylindersSqliteModel
from cylinders.windows.batch_ui import Ui_BatchWindow
from cylinders.services.rzn_sender import RZNLiquid
from cylinders.services import batch_info
from cylinders.services.db_connection import connect_db
from cylinders.export_data import backup_pg


class BatchWindow(QMainWindow):
    """
    Класс основного окна о сериях и баллонах
    """

    def __init__(
            self,
            db_config: DBConfig,
            dumps_path: Path,
            rzn_login: RZNLogin,
            headless_send: bool,
            *args,
            **kwargs
    ):
        super(BatchWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_BatchWindow()
        self.ui.setupUi(self)
        self.db_config = db_config

        self.conn = connect_db(self.db_config)
        self.rzn_login = rzn_login
        self.headless = headless_send
        self.sqlBatchModel: BatchBaseModel
        self.CylinderModel: CylindersBaseModel
        if self.db_config.db_type == "postgres":
            self.cur = self.conn.cursor()
            self.sqlBatchModel = BatchPostgresModel(cur=self.cur, conn=self.conn, parent=self)
            self.CylinderModel = CylindersPostgresModel(cur=self.cur, conn=self.conn, parent=self)
        elif self.db_config.db_type == "sqlite":
            self.conn.row_factory = sqlite3.Row
            self.cur = self.conn.cursor()
            self.sqlBatchModel = BatchSqliteModel(cur=self.cur, conn=self.conn, parent=self)
            self.CylinderModel = CylindersSqliteModel(cur=self.cur, conn=self.conn, parent=self)
        else:
            raise ValueError("Incorrect DB_TYPE. must be 'postgres' or 'sqlite', "
                             f"got {self.db_config.db_type}")
        self.show_version_db()
        self.ui.CylindersView.setModel(self.CylinderModel)
        self.qsortBatch = QSortFilterProxyModel(self)
        self.qsortBatch.setSourceModel(self.sqlBatchModel)
        self.ui.BatchView.setModel(self.qsortBatch)
        self.ui.BatchView.resizeColumnsToContents()
        # TODO сделать изменение TableView с баллонами когда изменятся текущая ячейка а не выделенная
        # self.ui.BatchView.currentChanged.connect(self.show_cylinders_info)
        self.ui.BatchView.selectionModel().selectionChanged.connect(self.batch_selection_changed)

        self.ui.SeriaEdit.setText(self.sqlBatchModel.get_seria())
        self.ui.PartiaEdit.setDate(QDate().currentDate())
        self.ui.SufixEdit.setText(self.get_new_suffix())
        self.ui.PassportNoEdit.setText(str(self.get_new_passport_no()))

        self.ui.docsGb.format_type = QButtonGroup(self)
        self.ui.docsGb.format_type.addButton(self.ui.oldFormat_rb)
        self.ui.docsGb.format_type.addButton(self.ui.newFormat_rb)
        self.data_by_button = {
            self.ui.newFormat_rb: False,
            self.ui.oldFormat_rb: True
        }

        last_batch_id = self.sqlBatchModel.get_batch_id()
        self.show_cylinders_info(last_batch_id)
        # # self.batch_selection_changed()

        self.ui.BatchView.selectRow(0)
        self.ui.addBatchButton.clicked.connect(self.add_batch)
        self.ui.CreatePassportButton.clicked.connect(self.create_passport)
        self.ui.CreateEtiketkaButton.clicked.connect(self.create_sticker)
        self.ui.CreateTitulnButton.clicked.connect(self.create_title_page)
        self.ui.CreateManyEtiketkaButton.clicked.connect(self.create_many_sticker)
        self.ui.submit_button.clicked.connect(self.send_liquid_batch)
        self.batch_context_menu = self.create_context_menu()
        self.batch_context_menu_delete_action = self.create_delete_action()
        self.last_context_menu_pos: QPoint = QPoint()
        logger.info("первичная настрока окна завершена")

        self.back_up_tread = threading.Thread(target=self.back_up, kwargs=dict(dumps_path=dumps_path))
        logger.info("запуск бекапа..")
        self.back_up_tread.start()

    def create_context_menu(self) -> QMenu:
        self.ui.BatchView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.BatchView.customContextMenuRequested.connect(self.show_context_menu)
        context_menu = QMenu(self)
        return context_menu

    def create_delete_action(self) -> QAction:
        delete = self.batch_context_menu.addAction('Удалить серию')  # noqa arg_2 not filled
        delete.triggered.connect(self.delete_context_menu_handler)
        return delete

    def show_context_menu(self, point: QPoint):
        self.last_context_menu_pos = point
        batch_id = self.get_batch_id_by_point(point)
        serial = self.sqlBatchModel.get_partia_by_id(batch_id)
        self.batch_context_menu_delete_action.setText(
            f"Удалить серию {serial} с id {batch_id}"
        )
        self.batch_context_menu.move(QCursor.pos())
        self.batch_context_menu.show()

    def delete_context_menu_handler(self):
        batch_id = self.get_batch_id_by_point(self.last_context_menu_pos)
        logger.warning("deleting batch with id = {}", batch_id)
        self.sqlBatchModel.delete_batch_by_id(batch_id)
        logger.warning("deleted batch with id = {}", batch_id)

    def get_batch_id_by_point(self, menu_pos: QPoint) -> int:
        model_index: QModelIndex = self.ui.BatchView.indexAt(menu_pos)
        index = self.sqlBatchModel.get_batch_id(model_index.row())
        return index

    def show_version_db(self):
        if self.db_config.db_type == "sqlite":
            sql = "SELECT sqlite_version();"
        else:
            sql = "SELECT version();"
        self.cur.execute(sql)
        self.ui.statusbar.showMessage(self.cur.fetchone()[0])

    def get_new_suffix(self):
        try:
            last_date = datetime.strptime(self.sqlBatchModel.get_partia_date(), '%d.%m.%y').date()
        except Exception as e:
            last_date = self.ui.PartiaEdit.date()
            logger.exception(e)
        if last_date != date.today():
            return 'а'
        else:
            return 'б'

    def get_new_passport_no(self):
        return (self.sqlBatchModel.get_passport_no() or 0) + 1

    def batch_selection_changed(self):
        """
        метод реакции на изменение текущей (выделенной) ячейки
        так же отображающий в Label сведения о серии
        :return: None
        """
        row = self.get_current_row()
        ser_id = self.get_current_batch_id()
        logger.debug('Выделена новая область, обновляем данные по составу серии')
        if ser_id != self.sqlBatchModel.get_batch_id(row):
            logger.error(
                "ser_id={ser_id}, batch_id={ser_id}, не равны, а должны быть.",
                ser_id=ser_id,
                batch_id=self.sqlBatchModel.get_batch_id(row)
            )
        logger.debug("ser_id={ser_id}".format(ser_id=ser_id))
        seria = self.sqlBatchModel.get_seria(row)
        partia = self.sqlBatchModel.get_partia(row)
        partia_date = self.sqlBatchModel.get_partia_date(row)
        self.show_cylinders_info(ser_id)
        self.ui.CaptionCylinderslabel.setText(f"Сведения о серии id: {ser_id}, номер серии: {seria},"
                                              f"номер партии: {partia}, дата изготовления: {partia_date},"
                                              f"кол-во: {self.CylinderModel.sum} б.")

    def get_current_batch_id(self):
        """
        возвращает ID серии выделенной пользователем
        :return: batch_id - id текущей серии
        """
        row = self.get_current_row()
        return self.sqlBatchModel.get_batch_id(row)

    def get_current_row(self):
        """

        :return: текущая строка
        """
        return self.ui.BatchView.currentIndex().row()

    def show_cylinders_info(self, ser_id: int):
        """
        метод изменяющий данные в TableView для отображения баллонов из новой серии
        :param ser_id: новый id серии
        :return: None
        """
        self.CylinderModel.change_batch_id(ser_id)
        self.ui.CylindersView.resizeColumnsToContents()

    def get_selected_rows(self):
        rows = sorted(
            {index.row() for index in self.ui.BatchView.selectedIndexes()},
            key=lambda x: -x
        )
        return rows

    def get_selected_batch_ids(self):
        rows = self.get_selected_rows()
        batch_ids = []
        for row in rows:
            batch_ids.append(self.sqlBatchModel.get_batch_id(row))
        logger.info("Выбраны серии: " + ', '.join(map(str, batch_ids)))
        return batch_ids

    def create_passport(self):
        """
        Метод создания паспорта по текущей серии
        :return: None
        """
        logger.info("Подготавливаем паспорта")
        batch_ids = self.get_selected_batch_ids()

        try:
            batch_info.generate_passport(
                batch_ids=batch_ids,
                old_passport=self.data_by_button[self.ui.docsGb.format_type.checkedButton()]
            )
        except Exception as e:
            self.ui.statusbar.showMessage("Ошибка при подготовке документа: " + str(e))
            logger.exception(e)
        else:
            self.ui.statusbar.showMessage("Документ создан успешно")

    def create_sticker(self):
        """
        Метод создания этикетки по текущей серии
        :return: None
        """
        logger.info("Подготавливаем образцы этикеток")
        batch_ids = self.get_selected_batch_ids()

        try:
            batch_info.generate_sticker(
                batch_ids=batch_ids,
                old_passport=self.data_by_button[self.ui.docsGb.format_type.checkedButton()]
            )
        except Exception as e:
            self.ui.statusbar.showMessage("Ошибка при подготовке документа: " + str(e))
            logger.exception(e)
        else:
            self.ui.statusbar.showMessage("Документ создан успешно")

    def create_title_page(self):
        logger.info("Подготавливаем титульные листы")
        batch_ids = self.get_selected_batch_ids()

        try:
            batch_info.generate_title_page(
                batch_ids=batch_ids,
                old_passport=self.data_by_button[self.ui.docsGb.format_type.checkedButton()]
            )
        except Exception as e:
            self.ui.statusbar.showMessage("Ошибка при подготовке документа: " + str(e))
            logger.exception(e)
        else:
            self.ui.statusbar.showMessage("Документ создан успешно")

    def create_many_sticker(self):
        logger.info("Подготавливаем много этикеток для наклейки на все баллоны")
        batch_ids = self.get_selected_batch_ids()

        try:
            batch_info.generate_many_sticker(
                batch_ids=batch_ids,
                old_passport=self.data_by_button[self.ui.docsGb.format_type.checkedButton()]
            )
        except Exception as e:
            self.ui.statusbar.showMessage("Ошибка при подготовке документа: " + str(e))
            logger.exception(e)
        else:
            self.ui.statusbar.showMessage("Документ создан успешно")

    def add_batch(self):
        """
        метод добавления ещё одной серии, данные о которой внесены пользователем
        :return: None
        """
        logger.info("Добавляем серию")
        seria = self.ui.SeriaEdit.text()
        partia = date(*self.ui.PartiaEdit.date().getDate())
        suffix = self.ui.SufixEdit.text()
        passport_no = self.ui.PassportNoEdit.text()
        try:
            self.sqlBatchModel.add_batch(seria, partia, suffix, passport_no)
        except Exception as e:
            logger.exception(e)
            self.ui.statusbar.showMessage("Ошибка при вставке серии: " + str(e))

    def send_liquid_batch(self):
        """
        метод для отправки серии КЖМ
        """
        with RZNLiquid(
                login=self.rzn_login.login,
                password=self.rzn_login.password,
                headless=self.headless
        ) as rzn_sender:
            rzn_sender.save_new_batch(self.ui.line_edit_batch.text(), int(self.ui.line_edit_count.text()))
            sleep(5)

    def closeEvent(self, event):
        self.cur.close()
        self.conn.close()
        if self.back_up_tread.is_alive():
            logger.info("окно закрывается, а бекап не завершён. ждём.")
            self.back_up_tread.join()
        event.accept()

    def back_up(self, dumps_path: Path):
        logger.info("начат процесс сохранения базы данных")
        backup_db_config = DBConfig(
            dump_sqlite_path=get_path_dump(dumps_path),
            pg_host=self.db_config.pg_host,
            pg_port=self.db_config.pg_port,
            pg_login=self.db_config.pg_login,
            pg_password=self.db_config.pg_password,
            pg_db_name=self.db_config.pg_db_name,
        )
        backup_pg(backup_db_config)
        logger.info("завершён процесс сохранения базы данных")


def get_path_dump(dump_dir: Path):
    today_damp = dump_dir / f"{date.today().isoformat()}.db"
    dumps = [dump for dump in dump_dir.glob('*.db')]
    if today_damp in dumps:
        return today_damp
    if len(dumps) > 2:
        dumps.sort()
        dumps[0].unlink()
    return today_damp
