"""Pydantic model for the input of `importexport_binary.x` version `qe-5.2.1`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputppNamelist(Namelist):
    """Pydantic model for the `INPUTPP` namelist."""

    prefix: str = Field(
        "pwscf", description="prefix of input file produced by pw.x (wavefunctions are not needed)"
    )
    outdir: Path = Field(
        default_factory=get_tmp_dir,
        description="directory containing the input data, i.e. the same as in pw.x",
    )
    direction: str = Field(
        "export",
        description="selects the direction:  'export': for converting the charge density from the native binary format to text XML format  'import': for converting a previously exported folder from text XML format to binary format",
    )
    newoutdir: str | None = Field(
        None,
        description="directory into which the export data is going to be generated; after the 'import' phase, it can be then used as the outdir to restart for instance a pw.x NSCF calculation",
    )


class IMPORTEXPORTBINARYEspressoInput(EspressoInput):
    """Pydantic model for the input of `importexport_binary.x`"""

    inputpp: InputppNamelist = Field(default_factory=lambda: InputppNamelist())
