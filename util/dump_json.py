import pathlib
import json


def dump_json(data: dict, path: pathlib.Path):
    json.dump(data, path.open("w", encoding="utf-8"), ensure_ascii=False, indent=4)
