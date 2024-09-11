import pathlib


def walker(source: pathlib.Path):
    file_list = []
    for root, _, files in source.walk():
        for file in files:
            file_list.append(root / file)

    return file_list
