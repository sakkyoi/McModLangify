import pathlib
import json


def load_json(file: pathlib.Path) -> dict:
    # load the json file
    try:
        data = json.loads(file.read_bytes())
    except json.JSONDecodeError as e:
        raise RuntimeError(f"json.JSONDecodeError: {file}: {e} \n"
                           f"Run validate-json command to check for errors first, fix them before continuing.")

    return data
