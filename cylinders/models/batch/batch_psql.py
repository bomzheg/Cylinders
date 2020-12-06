from cylinders.models.batch.batch_base import BatchBaseModel


class BatchPostgresModel(BatchBaseModel):
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
        OFFSET %s;
    """
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

    def get_headers(self):
        return [column.name for column in self.cur.description]
