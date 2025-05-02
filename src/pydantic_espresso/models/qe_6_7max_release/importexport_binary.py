"""Pydantic model for the input of `importexport_binary.x` version `qe-6.7MaX-Release`.

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

    prefix: str = Field(
        "pwscf", description="prefix of input file produced by pw.x (wavefunctions are not needed)"
    )
    outdir: Path = Field(
        Path("value of the"),
        description="directory containing the input data, i.e. the same as in pw.x",
    )
    direction: Literal["export", "import"] = Field("export", description="Selects the direction:")
    newoutdir: str | None = Field(
        None,
        description="directory into which the export data is going to be generated; after the 'import' phase, it can be then used as the outdir to restart for instance a pw.x NSCF calculation",
    )


class IMPORTEXPORT_BINARYEspressoInput(EspressoInput):
    """Pydantic model for the input of `importexport_binary.x.`"""

    inputpp: InputppNamelist = Field(default_factory=lambda: InputppNamelist())
