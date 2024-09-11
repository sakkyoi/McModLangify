import pathlib
import typer
from typing_extensions import Annotated
from zipfile import ZipFile
from tqdm import tqdm
import re

re_pattern = re.compile(r"assets/.*?/lang/.*?\.json")


def extract(
        source: Annotated[
            pathlib.Path,
            typer.Argument(
                help="The source file or directory to extract language files from."
            )
        ],
        target: Annotated[
            pathlib.Path,
            typer.Argument(
                help="The directory to extract the language files to."
            )
        ] = "./extracted"
):
    # check path type and get jar files
    if source.is_dir():
        # glob all jar files in the directory
        jar_files = list(source.glob("*.jar"))

        # check if there are jar files
        if not len(jar_files):
            raise FileNotFoundError("No jar files found in the source directory")

        print(f"Found {len(jar_files)} mods")
    elif source.is_dir() and source.suffix == ".jar":
        # just return the file as a list
        jar_files = [source]
    else:
        # raise error if the file or directory does not exist
        raise FileNotFoundError("Source file or directory does not exist ")

    # extract the language files
    for jar_file in tqdm(jar_files, desc=f"Extracting mods"):
        # open the jar file
        z = ZipFile(jar_file, "r")
        # get the list of files in the jar
        name_list = z.namelist()

        for name in name_list:
            # skip files that do not match the pattern
            if not re_pattern.match(name):
                continue

            # read the file
            zf = z.read(name)

            # construct the target path and create the directory if it doesn't exist
            file_path = target / name
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # write the file
            with open(file_path, "wb") as file:
                file.write(zf)
