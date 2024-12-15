from pathlib import Path

from loguru import logger


def upgrade(load_volumes: str, con):

    volumes_file = Path(load_volumes)
    if not volumes_file.exists() or not volumes_file.is_file():
        raise ValueError(f"volume file is {volumes_file} but it's not a file or not exists")
    with volumes_file.open(mode="r", encoding="utf8") as f:
        headers = f.readline().strip().split(";")
        assert headers[0] == "id"
        assert headers[1] == "Объём баллона, л"
        assert headers[2] == "Давление, ат"
        assert headers[3] == "Объём газа, м3"
        assert headers[4] == "Температура, °С"
        assert headers[5] == "Колличество в связке"
        assert headers[6] == "Объём газа в одном баллоне, м3"
        with con.cursor() as cur:
            ids = []
            for line in f:
                vol = line.strip().split(";")
                requested_id = int(vol[0])
                ids.append(requested_id)
                cur.execute("""
                    SELECT id FROM public."СоотношениеОбъёмов"
                    WHERE id = %s
                """, (requested_id,))

                fetched_id = cur.fetchone()
                if fetched_id and fetched_id[0] == requested_id:
                    logger.info(f"found id {requested_id}")
                    cur.execute("""
                        UPDATE public."СоотношениеОбъёмов"
                        SET 
                            "Объём баллона, л" = %(volume_cylinder)s,
                            "Давление, ат" = %(pressure)s,
                            "Объём газа, м3" = %(volume_gase)s,
                            "Температура, °С" = %(temperature)s,
                            "Колличество в связке" = %(count)s,
                            "Объём газа в одном баллоне, м3" = %(volume_pack)s
                        WHERE id = %(id)s
                        """,
                        {
                            "id": requested_id,
                            "volume_cylinder": vol[1],
                            "pressure": vol[2],
                            "volume_gase": vol[3],
                            "temperature": vol[4],
                            "count": vol[5],
                            "volume_pack": vol[6],
                    })
                else:
                    logger.info(f"not found id {requested_id}")
                    cur.execute("""
                        INSERT INTO public."СоотношениеОбъёмов" (
                            "id",
                            "Объём баллона, л",
                            "Давление, ат",
                            "Объём газа, м3",
                            "Температура, °С",
                            "Колличество в связке",
                            "Объём газа в одном баллоне, м3"
                        )
                        VALUES (
                            %(id)s,
                            %(volume_cylinder)s,
                            %(pressure)s,
                            %(volume_gase)s,
                            %(temperature)s,
                            %(count)s,
                            %(volume_pack)s
                        )
                        """,
                        {
                            "id": requested_id,
                            "volume_cylinder": vol[1],
                            "pressure": vol[2],
                            "volume_gase": vol[3],
                            "temperature": vol[4],
                            "count": vol[5],
                            "volume_pack": vol[6],
                        })
            assert len(ids) == len(set(ids))
            cur.execute("""
                SELECT id from public."СоотношениеОбъёмов"
                WHERE NOT (id = ANY(%(ids)s))
            """, {"ids": ids})
            founded = cur.fetchall()
            logger.info(f"found ids that should be deleted {founded}")
            con.commit()
