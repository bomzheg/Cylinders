"""
Данный модуль предназначен для класса представляющего модель данных о баллонах в партии
"""

from PySide2.QtCore import *

SQL_CYLINDERS = """
    SELECT
        "СоотношениеОбъёмов"."id",
        "Баллоны в партиях"."ID партии",
        CASE WHEN "СоотношениеОбъёмов"."Колличество в связке" = 1
            THEN CAST ("СоотношениеОбъёмов"."Объём баллона, л" AS FLOAT) || ' л.'
            ELSE "СоотношениеОбъёмов"."Колличество в связке" || ' ×' 
                                    || CAST ("СоотношениеОбъёмов"."Объём баллона, л" AS FLOAT) || ' л.'
        END AS "Формула упаковки",
        "СоотношениеОбъёмов"."Давление, ат",
        "Баллоны в партиях"."Количество"
    FROM "СоотношениеОбъёмов"
    LEFT OUTER JOIN "Баллоны в партиях"
        ON "СоотношениеОбъёмов"."id" = "Баллоны в партиях"."ID баллона"
        AND "Баллоны в партиях"."ID партии" = %s ;
        """
SQL_CYLINDERS_UPDATE = """
    INSERT INTO "Баллоны в партиях"
    ("ID партии", "ID баллона", "Количество")
    VALUES (%s, %s, %s)
    ON CONFLICT("ID партии", "ID баллона") DO UPDATE SET "Количество" = %s;
    """
SQL_SUM_CYLINDERS = """
    SELECT
        SUM("Количество")
    FROM "Баллоны в партиях"
    WHERE "ID партии" = %s AND "ID баллона" != 100;
        """


class CylindersModel(QAbstractTableModel):
    """
    Класс представляющий модель данных о баллонах в партии
    """
    EDITABLE_COLS = (4,)

    def __init__(self, cur, conn, parent=None):
        super(CylindersModel, self).__init__(parent)
        self.current_batch_id = 0
        self.cur = cur
        self.conn = conn
        self._array_data = []
        self.headers = []
        self.sum = 0
        self.refresh()

    def change_batch_id(self, new_id: int):
        """
        изменить текущий номер серии и отобразить данные о баллонах для этой серии
        :param new_id: новый номер серии
        """
        self.current_batch_id = new_id
        self.refresh()

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

        flags = super(CylindersModel, self).flags(index)
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
        if value == "" and self.data(self.index(index.row(), 4)) in (0, '0', ''):
            return True
        id_cyl = self._array_data[index.row()][0]
        try:
            self.set_count(id_cyl, self.current_batch_id, int(value))
        except ValueError:
            return False
        else:
            self.refresh()
            return True

    def refresh(self):
        """
        обновляет содержимое модели с действующим номером партии
        :return: None
        """
        self.cur.execute(SQL_CYLINDERS, (self.current_batch_id,))
        self.beginResetModel()
        self.headers = [column.name for column in self.cur.description]
        self._array_data = [list(row) for row in self.cur]
        self.endResetModel()
        self.sum = self.cur.execute(SQL_SUM_CYLINDERS, (self.current_batch_id,))

        self.sum = self.cur.fetchone()[0]

    def set_count(self, id_cyl, id_batch, count):
        """
        внести новые данные о баллонах в серии
        :param id_cyl: id баллона
        :param id_batch: id серии
        :param count: количество данных баллонов в данной серии
        :return: True если выполнено успешно, False если были ошибки
        """
        self.cur.execute(SQL_CYLINDERS_UPDATE, (id_batch, id_cyl, count, count))
        self.conn.commit()
        return
