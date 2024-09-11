import pathlib
import json
import typer
from typing_extensions import Annotated
from tqdm import tqdm

from util import walker


def validate_json(
        source: Annotated[
            pathlib.Path,
            typer.Argument(
                help="The directory extracted by extract command."
            )
        ],
        source_locale: Annotated[
            str,
            typer.Argument(
                help="The locale of the source files to validate. If not specified, all files will be validated."
            )
        ] = "",
):
    errors = []

    for file in tqdm(walker(source), desc="Validating files"):
        # skip files that are not source locale
        if source_locale != "" and file.stem != source_locale:
            continue

        # trying to open the file and check if it's a valid json file
        try:
            json.loads(file.read_bytes())
        except json.JSONDecodeError as e:
            errors.append(f"{file}: {e}")

    # print report
    if errors:
        print("=== Errors ===")

        for error in errors:
            print(error)

        print("=== End of Errors ===")
        print(f"Found {len(errors)} errors, please fix them before continuing.")
