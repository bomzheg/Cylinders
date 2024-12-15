from pathlib import Path


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
                    print(f"found id {requested_id}")
                else:
                    print(f"not found id {requested_id}")
            assert len(ids) == len(set(ids))
            cur.execute("""
                SELECT id from public."СоотношениеОбъёмов"
                WHERE NOT (id = ANY(%(ids)s))
            """, {"ids": ids})
            founded = cur.fetchall()
            print(f"found ids that should be deleted {founded}")
            # con.commit()
