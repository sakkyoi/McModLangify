from typer import Typer
import importlib
import inspect
from dotenv import load_dotenv

import commands

load_dotenv()

app = Typer()

for command in commands.__all__:
    app.command()(getattr(commands, command))


if __name__ == '__main__':
    app()
