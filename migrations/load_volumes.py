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
            pass
