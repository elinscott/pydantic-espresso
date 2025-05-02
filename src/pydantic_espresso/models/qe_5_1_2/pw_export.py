"""Pydantic model for the input of `pw_export.x` version `qe-5.1.2`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputppNamelist(Namelist):
    """Pydantic model for the `Inputpp` namelist."""


    prefix: str | None = Field(None, description="the first part of the name of all the file written by the code should be equal to the value given in the main calculations.")
    outdir: Path = Field(Path("./"), description="the scratch directory where the massive data-files are written")
    pseudo_dir: Path = Field(Path("./"), description="directory containing pseudopotential (PP) files")
    single_file: bool = Field(False, description="if .TRUE. one-file output is produced")
    ascii: bool = Field(False, description="if .TRUE. output files are textual, otherwise they are partly binary.")
    pp_file: str = Field("prefix.export/", description="Output file.  If it is omitted, a directory 'prefix.export/' is created in outdir and some output files are put there. Anyway all the data are accessible through the 'prefix.export/index.xml' file which contains implicit pointers to all the other files in the export directory. If reading is done by the IOTK library all data appear to be in index.xml even if physically it is not.")
    uspp_spsi: bool = Field(False, description="when using USPP,  if set .TRUE. the code writes S | psi > and | psi > vectors separately in the output file.")


class PW_EXPORTEspressoInput(EspressoInput):
    """Pydantic model for the input of `pw_export.x.`"""

    inputpp: InputppNamelist = Field(default_factory=lambda: InputppNamelist())
