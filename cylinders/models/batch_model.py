from PySide2.QtCore import *
from psycopg2.extensions import cursor, connection
from datetime import date
from loguru import logger
# TODO добавить возможность редактировать партию, суффикс, а так же удалять серии (если есть не нулевое
#  количество баллонов - выдать ошибку
SQL_BATCH = """
    SELECT
        id,
        trim(Серия) AS "Серия сырья",
        to_char(Партии.Партия, 'DDMMYY') || COALESCE(Суфикс, '') AS "Партия",
        to_char(Партии.Партия, 'DD.MM.YY') AS "Дата изготовления",
        to_char(Партии.Партия + interval '18 mons', 'DD.MM.YY') AS "Срок годности",
        Партии.Партия || COALESCE(Суфикс, '') AS "sort_date"
    FROM "Партии"
    ORDER BY "sort_date" DESC
    LIMIT %s 
    OFFSET %s;"""
LIMIT_BATCH = 50
SQL_ADD_BATCH = """
    INSERT INTO "Партии"
    ("Серия", "Партия", "Суфикс", "Показать")
    VALUES (%s, %s, %s, True);
"""
SQL_UPDATE_SERIA = """
    UPDATE "Партии" 
    SET "Серия" = %s
    WHERE id = %s;
"""
SQL_BATCH_COUNT = """
    SELECT count(id)
    FROM "Партии"
"""


class BatchModel(QAbstractTableModel):
    EDITABLE_COLS = (1,)

    def __init__(self, cur: cursor, conn: connection, parent=None):
        super(BatchModel, self).__init__(parent)
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
        self.cur.execute(SQL_BATCH, (LIMIT_BATCH + self.offset, 0))
        self.beginResetModel()
        self.headers = [column.name for column in self.cur.description]
        self._array_data = [list(row) for row in self.cur]
        self.endResetModel()

    # noinspection PyPep8Naming
    def canFetchMore(self, parent: QModelIndex) -> bool:
        return len(self._array_data) < self.batch_count - 1

    # noinspection PyPep8Naming
    def fetchMore(self, parent: QModelIndex):
        self.offset += LIMIT_BATCH
        self.cur.execute(SQL_BATCH, (LIMIT_BATCH, self.offset))
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

        flags = super(BatchModel, self).flags(index)
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

    def add_batch(self, seria: str, partia: date, suffix: str):
        """
        Метод добавляющий данные о новой серии
        :param seria: номер серии сырья
        :param partia: номер партии (только дата)
        :param suffix: суфикс номера партии
        :return: True в случае успеха, False в случае неудачи
        """
        self.cur.execute(SQL_ADD_BATCH, (seria, partia, suffix))
        self.conn.commit()
        self.refresh()

    def update_seria(self, id_batch: int, seria: str):
        logger.debug(f"Для серии {id_batch} обновлена серия сырья: {seria}")
        self.cur.execute(SQL_UPDATE_SERIA, (seria, id_batch))
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

    def get_partia_date(self, index: int = 0):
        """
        Возвращает номер партии (только дата) по переданному индексу
        :param index: номер записи в модели (нулевая запись - самая новая)
        :return: номер партии (только дата)
        """
        return self._array_data[index][3]

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
        self.cur.execute(SQL_BATCH_COUNT)
        return self.cur.fetchone()[0]
