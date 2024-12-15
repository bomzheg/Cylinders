from pathlib import Path
from typing import Union

from loguru import logger
from psycopg2.extensions import cursor
from relatorio.templates.opendocument import Template

from cylinders.config import config
from cylinders.services.db_connection import connect_pg


# noinspection PyPep8Naming
def convert_pressure_at2MPa(pressure_at: float) -> float:
    """
    Конвертирует давление из технических атмосфер в мегапаскали
    :param pressure_at: давление в технических атмосферах
    :return: давление в мегапаскалях
    """
    g = 9.80665  # acceleration of gravity
    cm2_in_m2 = 100  # in 1 square meter 100 square centimeters
    return round(pressure_at * g / cm2_in_m2, 1)


def get_batch_info(cur: cursor, batch_id):
    """
    Получает данные о серии и упаковывает их в словарь
    """
    cur.execute(
        """
        SELECT
            "Серия",
            "Партия",
            "Суфикс",
            to_char(Партии.Партия + interval '18 mons', 'DD.MM.YY') AS "Срок годности",
            passport_no AS "№ паспорта"
        FROM "Партии"
        WHERE "Партии"."id" = %s;
        """,
        (batch_id,)
    )
    ser, date_, suffix, srok, passport_no = cur.fetchone()
    suffix = "" if suffix is None else suffix
    part = str(date_.strftime('%d%m%y')) + suffix
    date_ = str(date_.strftime('%d.%m.%Y'))
    rez_batch = {
        'date': date_,
        'seria': ser,
        'partia': part,
        'srok': srok,
        'passport_no': passport_no,
    }
    return rez_batch


def get_cylinders_info(cur: cursor):
    """
    Получает данные о типах баллонов и упаковывает их в словарь
    """
    cur.execute(
        """
        SELECT
            "id",
            CAST ("Объём баллона, л" AS FLOAT) || '',
            "Давление, ат",
            "Объём газа, м3",
            "Температура, °С",
            "Колличество в связке",
            "Объём газа в одном баллоне, м3"
        FROM "СоотношениеОбъёмов"
        WHERE "id" != 100;
        """
    )
    cylinders = {}
    for id_, volume, pressure, gaz_count, temperature, count_in_mono, gaz_count_in_mono in cur:
        cylinders[id_] = {
            'volume': volume if count_in_mono == 1 else "{}×{}".format(count_in_mono, volume),
            'volume_single': volume,
            'pressure': convert_pressure_at2MPa(pressure),
            'pressure_at': pressure,
            'gaz_count': gaz_count,
            'temperature': temperature,
            'count_in_mono': count_in_mono,
            'gaz_count_in_mono': gaz_count_in_mono,
            'count': "нет",
            'count_': 0
        }

    return cylinders


def set_cylinders_count(cur: cursor, cylinders: dict, batch_id: int):
    """
    Получает данные о количествах баллонов и записывает их в переданный словарь
    """
    cur.execute(
        """
        SELECT
            "СоотношениеОбъёмов"."id",
            "Баллоны в партиях"."Количество",
            "СоотношениеОбъёмов"."Колличество в связке"
        FROM "СоотношениеОбъёмов"
        LEFT OUTER JOIN "Баллоны в партиях"
            ON "СоотношениеОбъёмов"."id" = "Баллоны в партиях"."ID баллона"
            AND "Баллоны в партиях"."ID партии" = %s
            AND "Баллоны в партиях"."ID баллона" != 100;
        """,
        (batch_id,)
    )

    for id_, count, count_in_mono in cur:
        if count_in_mono == 1:
            unit = "б"
        else:
            unit = "моноб"
        if count is not None and count != 0:
            cylinders[id_]['count'] = f"{count} {unit}."
            cylinders[id_]['count_'] = count
        else:
            try:
                del cylinders[id_]
            except KeyError:
                pass


def convert_cylinders_to_tree(cylinders: dict) -> dict:
    """
    конвертирует словарь из словаря по ID упаковки в словарь по давлению и типу
    """
    rez_tree = {}
    for id_ in cylinders:
        pressure = cylinders[id_]['pressure']
        if pressure not in rez_tree:
            rez_tree[pressure] = {}
        single = cylinders[id_]['count_in_mono'] == 1
        if single not in rez_tree[pressure]:
            rez_tree[pressure][single] = {}
        rez_tree[pressure][single][id_] = cylinders[id_]
    return rez_tree


def get_all_info_about_batch(cur: cursor, batch_id: int) -> dict:
    """
    Получает всю известную информацю по серии
    :rtype: dict
    """
    rez_batch = get_batch_info(cur, batch_id)
    cylinders = get_cylinders_info(cur)
    set_cylinders_count(cur, cylinders, batch_id)
    cylinders_tree = convert_cylinders_to_tree(cylinders)

    rez_batch['cilgroups'] = []
    for pressure in cylinders_tree:
        for single in cylinders_tree[pressure]:
            rez_batch['cilgroups'].append({
                'name': config.name_cylinders[single],
                'pressure': pressure,
                'cils': [dict_ for id_, dict_ in cylinders_tree[pressure][single].items()]
            })
    return rez_batch


def write_data_to_odt(*, data: dict, template_odt: Union[str, Path], destination_odt: Union[str, Path]):
    """
    запись данных из переданного словаря в ODT файл по заданному шаблону
    """
    basic = Template(source='', filepath=template_odt)
    open(destination_odt, 'wb').write(basic.generate(o=data).render().getvalue())


def generate_data_batch_list(batch_ids: list):
    # TODO конфиг на подключение или даже сразу коннект нужно получать из вызывающей функции а не хардкодить тут
    with connect_pg(config.db_config) as conn, conn.cursor() as cur:
        data = {'batchs': []}
        for batch_id in batch_ids:
            temp_data = get_all_info_about_batch(cur=cur, batch_id=batch_id)
            data['batchs'].append(temp_data)

    return data


def generate_passport(batch_ids: list):
    data = generate_data_batch_list(batch_ids=batch_ids)

    write_data_to_odt(
        data=data,
        template_odt=config.passport.template,
        destination_odt=config.passport.destination,
    )


def generate_sticker(batch_ids: list):
    data = generate_data_batch_list(batch_ids=batch_ids)

    write_data_to_odt(
        data=data,
        template_odt=config.sticker.template,
        destination_odt=config.sticker.destination,
    )


def generate_title_page(batch_ids: list):
    data = generate_data_batch_list(batch_ids=batch_ids)

    write_data_to_odt(
        data=data,
        template_odt=config.title_page.template,
        destination_odt=config.title_page.destination,
    )


def generate_many_sticker(batch_ids: list):
    data = generate_data_batch_list(batch_ids=batch_ids)

    write_data_to_odt(
        data=data,
        template_odt=config.many_stickers.template,
        destination_odt=config.many_stickers.destination,
    )


if __name__ == "__main__":
    try:
        generate_passport(batch_ids=[1104, 1102])
    except Exception as e:
        logger.exception(e)
        exit()
