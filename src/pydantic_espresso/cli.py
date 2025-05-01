"""Command line interface for :mod:`pydantic_espresso`.

Why does this file exist, and why not put this in ``__main__``?
You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m pydantic_espresso`` python will
  execute``__main__.py`` as a script. That means there won't be any
  ``pydantic_espresso.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``pydantic_espresso.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/8.1.x/setuptools/#setuptools-integration
"""

import json

import click

__all__ = [
    "main",
]


@click.group()
def main() -> None:
    """CLI for pydantic_espresso."""
    pass


@main.command()
def fetch_def() -> None:
    """Download the latest XML files."""
    from pydantic_espresso.fetch import fetch_def

    fetch_def()


@main.command()
def xml2pydantic() -> None:
    """Generate the pydantic models from the XML files."""
    from pydantic_espresso.xml2pydantic import convert_all_xml_files_to_models

    convert_all_xml_files_to_models()


@main.command()
def update() -> None:
    """Download the latest XML files and update the pydantic models accordingly."""
    from pydantic_espresso.fetch import fetch_xml
    from pydantic_espresso.generate import generate_models

    fetch_xml()
    generate_models()


@main.command
def schema() -> None:
    """Print the JSON schema of the latest Wannier90Input model."""
    from pydantic_espresso.models.latest import Wannier90Input

    print(json.dumps(Wannier90Input.model_json_schema(), indent=2))  # noqa: T201


if __name__ == "__main__":
    main()
