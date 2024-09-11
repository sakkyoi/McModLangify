import os
import pathlib
import typer
from typing_extensions import Annotated
import deepl as deepl_api
from tqdm import tqdm

from util import walker, load_json, dump_json


def deepl(
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
        source_locale_deepl: Annotated[
            str,
            typer.Argument(
                help="The language code of the source locale in DeepL. "
                     "see: https://developers.deepl.com/docs/resources/supported-languages"
            )
        ],
        target_locale: Annotated[
            str,
            typer.Argument(
                help="The locale of the target files."
            )
        ],
        target_locale_deepl: Annotated[
            str,
            typer.Argument(
                help="The language code of the target locale in DeepL. "
                     "see: https://developers.deepl.com/docs/resources/supported-languages"
            )
        ],
        target: Annotated[
            pathlib.Path,
            typer.Argument(
                help="The directory to save the converted files."
            )
        ] = "./converted",
        api_key: Annotated[
            str,
            typer.Option(
                help="The API key for DeepL API. (can be set as an environment variable DEEPL_API_KEY)"
            )
        ] = "",
):
    # check if the API key is provided, if not, check the environment variable
    if not api_key:
        api_key = os.environ.get("DEEPL_API_KEY")

    # check again cause the environment variable might be empty
    if not api_key:
        raise ValueError("API key is not provided.")

    translater = deepl_api.Translator(api_key)

    for file in tqdm(walker(source), desc="Converting files"):
        # skip files that are not source locale
        if file.stem != source_locale:
            continue

        # load the json file
        data = load_json(file)

        # convert the data value by value
        for k, v in tqdm(data.items(), desc=f"Converting {file.name}"):
            data[k] = translater.translate_text(v, source_lang=source_locale_deepl, target_lang=target_locale_deepl)

        # construct the target path and create the directory if it doesn't exist
        new_file = target / file.relative_to(source).with_name(file.name.replace(source_locale, target_locale))
        new_file.parent.mkdir(parents=True, exist_ok=True)

        # write the file
        dump_json(data, new_file)
