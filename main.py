from typer import Typer
import importlib
import inspect

import commands

app = Typer()

for command in commands.__all__:
    for _, obj in inspect.getmembers(importlib.import_module(f"commands.{command}"), inspect.isfunction):
        app.command()(obj)


if __name__ == '__main__':
    app()
