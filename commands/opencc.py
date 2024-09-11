import pathlib
import typer
from typing_extensions import Annotated
from opencc import OpenCC
import json
from tqdm import tqdm

from util.walker import walker


def opencc(
        source: Annotated[
            pathlib.Path,
            typer.Argument(
                help="The directory extracted by extract command."
            )
        ],
        source_locale: Annotated[
            str,
            typer.Argument(
                help="The locale of the source files."
            )
        ],
        target_locale: Annotated[
            str,
            typer.Argument(
                help="The locale of the target files."
            )
        ],
        target: Annotated[
            pathlib.Path,
            typer.Argument(
                help="The directory to save the converted files."
            )
        ] = "./converted",
        config: Annotated[
            str,
            typer.Option(
                help=f"The configuration file for OpenCC. Available presets: https://github.com/BYVoid/"
                     f"OpenCC?tab=readme-ov-file#%E9%A0%90%E8%A8%AD%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6"
                     f", or use custom configuration file."
            )
        ] = "s2twp.json",
):
    cc = OpenCC(config)

    for file in tqdm(walker(source), desc="Converting files"):
        # skip files that are not source locale
        if file.stem != source_locale:
            continue

        # load the json file
        try:
            data = json.loads(file.read_bytes())
        except json.JSONDecodeError as e:
            # tell the user which file is invalid and what is the error, then break the loop
            print(f"{file}: {e}")
            print("Run validate-json command to check for errors first, fix them before continuing.")
            break

        # convert the data value by value
        for k, v in tqdm(data.items(), desc=f"Converting {file.name}"):
            data[k] = cc.convert(v)

        # construct the target path and create the directory if it doesn't exist
        new_file = target / file.relative_to(source).with_name(file.name.replace(source_locale, target_locale))
        new_file.parent.mkdir(parents=True, exist_ok=True)

        # write the file
        json.dump(data, new_file.open("w", encoding="utf-8"), ensure_ascii=False, indent=4)
