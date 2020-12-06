from cylinders.models.cylinders.cylinders_base import CylindersBaseModel


class CylindersSqliteModel(CylindersBaseModel):

    SQL_CYLINDERS = """
        SELECT
            "СоотношениеОбъёмов"."ID",
            "Баллоны в партиях"."ID партии",
            CASE WHEN "СоотношениеОбъёмов"."Колличество в связке" == 1
                THEN "СоотношениеОбъёмов"."Объём баллона, л" || " л."
                ELSE "СоотношениеОбъёмов"."Колличество в связке" || "×" || "СоотношениеОбъёмов"."Объём баллона, л" || " л."
            END AS "Формула упаковки",
            "СоотношениеОбъёмов"."Давление, ат",
            "Баллоны в партиях"."Количество"
        FROM "СоотношениеОбъёмов"
        LEFT OUTER JOIN "Баллоны в партиях"
            ON "СоотношениеОбъёмов"."ID" = "Баллоны в партиях"."ID баллона"
            AND "Баллоны в партиях"."ID партии" = ? ;
    """
    SQL_CYLINDERS_UPDATE = """
        INSERT INTO "Баллоны в партиях"
        ("ID партии", "ID баллона", "Количество")
        VALUES (?, ?, ?)
        ON CONFLICT("ID партии", "ID баллона") DO UPDATE SET "Количество" = ?;
    """
    SQL_SUM_CYLINDERS = """
        SELECT
            SUM("Количество")
        FROM "Баллоны в партиях"
        WHERE "ID партии" = ? AND "ID баллона" != 100;
    """

    def get_headers(self):
        return [column[0] for column in self.cur.description]
