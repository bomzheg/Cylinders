from cylinders.models.batch.batch_base import BatchBaseModel


class BatchSqliteModel(BatchBaseModel):
    SQL_BATCH = """
        SELECT
            "id",
            trim(Серия) AS "Серия сырья",
            cast(strftime('%d%m', DATE(Партия)) AS TEXT) ||
                cast(strftime('%Y', DATE(Партия)) % 2000 AS TEXT) ||
                ifnull(Суфикс, "")
                AS "Партия",
            strftime('%d.%m.%Y', DATE(Партия)) AS "Дата изготовления",
            strftime('%d.%m.%Y', DATE(Партия, '+18 months')) AS " Срок годности",
            date(Партия) || ifnull(Суфикс, "") AS "sort_date"
    
        FROM "Партии"
        ORDER BY "sort_date" DESC
        LIMIT ? 
        OFFSET ?;
    """
    SQL_ADD_BATCH = """
        INSERT INTO "Партии"
        ("Серия", "Партия", "Суфикс", "Показать")
        VALUES (?, ?, ?, 1);
    """
    SQL_UPDATE_SERIA = """
        UPDATE "Партии" 
        SET "Серия" = ?
        WHERE id = ?;
    """
    SQL_BATCH_COUNT = """
        SELECT count(id)
        FROM "Партии"
    """

    def get_headers(self):
        return [column[0] for column in self.cur.description]
