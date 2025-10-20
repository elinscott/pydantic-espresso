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

from pydantic_espresso.models import get_module, versions

__all__ = [
    "main",
]


@click.group()
def main() -> None:
    """CLI for pydantic_espresso."""
    pass


@main.command()
def download_defs() -> None:
    """Download the latest XML files."""
    from pydantic_espresso.fetch import fetch_all_defs

    fetch_all_defs()


@main.command()
def def2xml() -> None:
    """Convert the .def files to .xml files."""
    from pydantic_espresso.def2xml import defs_to_xmls

    defs_to_xmls()


@main.command()
def xml2pydantic() -> None:
    """Generate the pydantic models from the XML files."""
    from pydantic_espresso.xml2pydantic import convert_all_xml_files_to_models

    convert_all_xml_files_to_models()


@main.command()
@click.pass_context
def update(ctx: click.Context) -> None:
    """Update all the pydantic models."""
    ctx.invoke(download_defs)
    ctx.invoke(def2xml)
    ctx.invoke(xml2pydantic)


@main.command()
@click.argument(
    "executable",
    required=True,
)
@click.option(
    "--version",
    default="develop",
    type=click.Choice(
        ["develop" if v.is_devrelease else str(v) for v in versions], case_sensitive=False
    ),
)
def schema(executable: str, version: str) -> None:
    """Print the JSON schema of the specified executable model."""
    try:
        # Try to find the module from which to import the model
        module = get_module(version=version, executable=executable)
    except ImportError:
        click.echo(f"Models for {executable} not found for version {version}.")
        return

    try:
        # Try to import the model class
        model_class = getattr(module, f"{executable.upper()}EspressoInput")
    except AttributeError:
        click.echo(
            f"Model class {executable.upper()}EspressoInput not found for version {version}."
        )
        return

    click.echo(json.dumps(model_class.model_json_schema(), indent=2))


if __name__ == "__main__":
    main()
