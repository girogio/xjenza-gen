import re
import shutil
from os import path

import typer
from rich import print
from rich.prompt import Prompt
from typing_extensions import Annotated

from xjenza_gen.article import Article, Author
from xjenza_gen.latex import LatexEngine

app = typer.Typer()


@app.command()
def new(
    name: Annotated[str, typer.Argument(..., help="Name of the project")] = "",
):
    print("\n:sparkles: [green]Creating a new Xjenza article... \n")

    if not name:
        name = Prompt.ask("[blue]Project name", default="xjenza_article")
        print()

    regex_name = r"^[a-zA-Z0-9_-]*$"

    if not name.strip() or not re.match(regex_name, name):
        print(
            f"[red]:x: Project name '{name}' is invalid. Please use only alphanumeric characters, dashes and underscores."
        )

        raise typer.Exit(1)

    latex = copy_skel(name, debug=False)

    einstein = Author(
        "Albert",
        "Einstein",
        "albert@einstein.de",
        "Department of Physics, Faculty of Science, University of Malta, Malta",
    ).corresponding()

    article = Article(
        "Some article",
        "shorter title",
        2022,
        [einstein],
        "Abstract goes here",
        ["some", "keywords"],
    )

    latex.build(article)

    print(
        f"\n:tada: [green]Done! Feel free to edit the generated files at [cyan]'{path.abspath(name)}'."
    )


@app.command()
def run():
    typer.echo("Running project...")


def copy_skel(to: path, debug: bool = False):
    """Copy the skeleton project to the specified folder."""
    if path.exists(to):
        print(f"[red]Folder '{to}' already exists, exiting...")
        typer.Abort()

    internal_output_path = path.join(path.dirname(__file__), "outputs")
    internal_template_folder = path.join(path.dirname(__file__), "templates")

    if not path.exists(internal_output_path):
        print(
            f"[red]Template folder was not bundled with the package! Please reinstall the package."
        )
        typer.Abort()

    try:
        shutil.copytree(internal_output_path, to)
    except Exception as e:
        print(f"[red]Error copying output folder: {e}")
        typer.Abort()

    return LatexEngine(
        internal_template_folder, "main.tex", path.abspath(to), to + ".tex", debug
    )
