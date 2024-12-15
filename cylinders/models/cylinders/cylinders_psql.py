from cylinders.models.cylinders.cylinders_base import CylindersBaseModel


class CylindersPostgresModel(CylindersBaseModel):
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
            AND "Баллоны в партиях"."ID партии" = %s 
        WHERE "СоотношениеОбъёмов".show
        ORDER BY "СоотношениеОбъёмов"."id"
        
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

    def get_headers(self):
        return [column.name for column in self.cur.description]
