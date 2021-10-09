from cylinders.models.batch.batch_base import BatchBaseModel


class BatchPostgresModel(BatchBaseModel):
    SQL_BATCH = """
        SELECT
            id,
            trim(Серия) AS "Серия сырья",
            to_char(Партии.Партия, 'DDMMYY') || COALESCE(Суфикс, '') AS "Партия",
            to_char(Партии.Партия, 'DD.MM.YY') AS "Дата изготовления",
            to_char(Партии.Партия + interval '18 mons', 'DD.MM.YY') AS "Срок годности",
            Партии.passport_no as "№ Паспорта" ,
            Партии.Партия || COALESCE(Суфикс, '') AS "sort_date"

        FROM "Партии"
        ORDER BY "sort_date" DESC
        LIMIT %s 
        OFFSET %s;
    """
    SQL_ADD_BATCH = """
        INSERT INTO "Партии"
        ("Серия", "Партия", "Суфикс", "Показать", passport_no)
        VALUES (%s, %s, %s, True, %s);
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
    SQL_DELETE_BATCH_BY_ID = """
        DELETE
        FROM "Баллоны в партиях"
        WHERE "Баллоны в партиях"."ID партии" = %s;
        DELETE FROM "Партии" WHERE "id" = %s
    """

    def get_headers(self):
        return [column.name for column in self.cur.description]
