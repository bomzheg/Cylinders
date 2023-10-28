from PySide2.QtCore import *
from datetime import date
from loguru import logger


class BatchBaseModel(QAbstractTableModel):
    EDITABLE_COLS = (1,)
    SQL_BATCH = ""
    LIMIT_BATCH = 50
    SQL_BATCH_COUNT = ""
    SQL_ADD_BATCH = ""
    SQL_UPDATE_SERIA = ""
    SQL_DELETE_BATCH_BY_ID = ""

    def __init__(self, cur, conn, parent=None):
        super(BatchBaseModel, self).__init__(parent)
        self.cur = cur
        self.conn = conn
        self._array_data = []
        self.headers = []
        self.offset = 0
        self.batch_count = self.get_batch_count()
        self.refresh()

    def refresh(self):
        """
        Получает данные о сериях
        """
        self.cur.execute(self.SQL_BATCH, (self.LIMIT_BATCH + self.offset, 0))
        self.beginResetModel()
        self.headers = self.get_headers()
        self._array_data = [list(row) for row in self.cur]
        self.endResetModel()

    def get_headers(self):
        raise NotImplemented

    # noinspection PyPep8Naming
    def canFetchMore(self, parent: QModelIndex) -> bool:
        return len(self._array_data) < self.batch_count - 1

    # noinspection PyPep8Naming
    def fetchMore(self, parent: QModelIndex):
        self.offset += self.LIMIT_BATCH
        self.cur.execute(self.SQL_BATCH, (self.LIMIT_BATCH, self.offset))
        self.beginResetModel()
        self._array_data.extend(self.cur.fetchall())
        self.endResetModel()

    # noinspection PyPep8Naming
    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._array_data)

    # noinspection PyPep8Naming
    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._array_data[0])

    def data(self, index: QModelIndex, role=None):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self._array_data[index.row()][index.column()]

    # noinspection PyPep8Naming
    def headerData(self, col: int, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[col]
        return None

    def flags(self, index: QModelIndex):
        """
        Переопределённый метод возвращающий список флагов.
        для столбца который можно редактировать добавляется соответствующий флаг
        :param index:
        :return: флаги как родительский класс, если можно редактировать столбец добавлен флаг редактирования
        """

        flags = super(BatchBaseModel, self).flags(index)
        if index.column() in self.EDITABLE_COLS:
            flags |= Qt.ItemIsEditable
        return flags

    # noinspection PyPep8Naming
    def setData(self, index: QModelIndex, value, role=None):
        """
        Переопределённый метод изменения данных в ячейке
        :param index:
        :param value: значение которое нужно записать
        :param role:
        :return: True если выполнено успешно, False если были ошибки
        """
        if index.column() not in self.EDITABLE_COLS:
            return False
        if value == "" or value == self._array_data[index.row()][index.column()]:
            return False
        id_batch = self._array_data[index.row()][0]
        try:
            self.update_seria(id_batch, value)
        except ValueError:
            return False
        except Exception as e:
            logger.exception(e)
            raise
        else:
            self.refresh()
            self.batch_count = self.get_batch_count()
            return True

    def add_batch(self, seria: str, partia: date, suffix: str, passport_no):
        """
        Метод добавляющий данные о новой серии
        :param seria: номер серии сырья
        :param partia: номер партии (только дата)
        :param suffix: суфикс номера партии
        :param passport_no: номер паспорта
        :return: True в случае успеха, False в случае неудачи
        """
        self.cur.execute(self.SQL_ADD_BATCH, (seria, partia, suffix, passport_no))
        self.conn.commit()
        self.refresh()

    def update_seria(self, id_batch: int, seria: str):
        logger.debug(f"Для серии {id_batch} обновлена серия сырья: {seria}")
        self.cur.execute(self.SQL_UPDATE_SERIA, (seria, id_batch))
        self.conn.commit()

    def get_batch_id(self, index: int = 0):
        """
        Возвращает id серии по переданному индексу
        :param index: номер записи в модели (нулевая запись - самая новая)
        :return: id серии
        """
        return self._array_data[index][0]

    def get_seria(self, index: int = 0):
        """
        Возвращает номер серии по переданному индексу
        :param index: номер записи в модели (нулевая запись - самая новая)
        :return: номер серии
        """
        return self._array_data[index][1]

    def get_partia_by_id(self, batch_id: int) -> str:
        return self._array_data[self.get_index_by_id(batch_id)][2]

    def get_index_by_id(self, batch_id: int) -> int:
        return list(map(
            lambda x: x[0],
            self._array_data
        )).index(batch_id)

    def get_partia_date(self, index: int = 0):
        """
        Возвращает номер партии (только дата) по переданному индексу
        :param index: номер записи в модели (нулевая запись - самая новая)
        :return: номер партии (только дата)
        """
        return self._array_data[index][3]

    def get_passport_no(self, index: int = 0):
        """
        Возвращает номер паспорта по переданному индексу
        :param index: номер записи в модели (нулевая запись - самая новая)
        :return: номер паспорта
        """
        return self._array_data[index][5]

    def get_partia(self, index: int = 0):
        """
        Возвращает номер партии по переданному индексу
        :param index: номер записи в модели (нулевая запись - самая новая)
        :return: номер партии
        """
        return self._array_data[index][2]

    def get_suffix(self, index: int = 0):
        """
        Возвращает суфикс партии по переданному индексу
        :param index: номер записи в модели (нулевая запись - самая новая)
        :return: суфикс партии
        """
        last_char = self.get_partia(index)[-1]
        if last_char.isalpha():
            return last_char
        return ""

    def get_batch_count(self):
        self.cur.execute(self.SQL_BATCH_COUNT)
        return self.cur.fetchone()[0]

    def delete_batch_by_id(self, id_: int):
        self.cur.execute(self.SQL_DELETE_BATCH_BY_ID, (id_, id_))
        self.conn.commit()
        self.refresh()
