"""Implement the following bash script in Python."""

import os
import subprocess
import warnings
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from pydantic_espresso.def_files import directory as def_directory
from pydantic_espresso.xml_files import directory as xml_directory


def defs_to_xmls() -> None:
    """Convert all .def files to .xml files."""
    # First copy over the .xsl files
    for xsl_file in def_directory.rglob("*.xsl"):
        xsl_file_in_xml_directory = (
            xml_directory / xsl_file.parent.relative_to(def_directory) / xsl_file.name
        )
        if not xsl_file_in_xml_directory.parent.exists():
            xsl_file_in_xml_directory.parent.mkdir(parents=True, exist_ok=True)
        xsl_file_in_xml_directory.write_text(xsl_file.read_text())

    # Then convert the .def files to .xml files
    for def_file in def_directory.rglob("*.def"):
        def_to_xml(def_file)


@contextmanager
def chdir(new_dir: str | Path) -> Generator[None, None]:
    """Change to a new directory temporarily."""
    prev_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(prev_dir)


def def_to_xml(def_file: Path) -> None:
    """Convert a single .def file to .xml file."""
    # Copy the .def file to the xml directory
    xml_subdirectory = xml_directory / def_file.parent.relative_to(def_directory)
    def_file_in_xml_directory = xml_subdirectory / def_file.name.lower()
    if not def_file_in_xml_directory.parent.exists():
        def_file_in_xml_directory.parent.mkdir(parents=True, exist_ok=True)
    def_file_in_xml_directory.write_text(def_file.read_text())

    # Run helpdoc in the xml_subdirectory
    helpdoc = Path(__file__).parents[2] / "q-e/dev-tools/helpdoc"
    if not os.access(helpdoc, os.X_OK):
        raise PermissionError(f"Helpdoc script at {helpdoc} is not executable")
    with chdir(xml_subdirectory):
        copied_def_file = Path(def_file_in_xml_directory.name)
        if not copied_def_file.exists():
            raise FileNotFoundError(f"DEF file {copied_def_file} not found")
        try:
            subprocess.run(
                [str(helpdoc), str(copied_def_file)], check=True, stdout=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            warnings.warn(
                f"Error running helpdoc for {def_file.relative_to(def_directory)}", stacklevel=2
            )

    # Remove the extra files
    for ext in [".def", ".html", ".txt", ".xsl"]:
        file_to_remove = def_file_in_xml_directory.with_suffix(ext)
        if file_to_remove.exists():
            file_to_remove.unlink()
