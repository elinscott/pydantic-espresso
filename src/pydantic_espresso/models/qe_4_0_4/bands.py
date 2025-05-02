"""Pydantic model for the input of `bands.x` version `qe-4.0.4`.

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

    prefix: str | None = Field(None, description="prefix of files saved by program pw.x")
    outdir: Path | None = Field(None, description="temporary directory where pw.x files resides")
    filband: str | None = Field(None, description="file 'filband' contains the bands")
    spin_component: int | None = Field(
        None, description="In the lsda case select:  1 = spin-up 2 = spin-down"
    )
    lsym: bool | None = Field(
        None,
        description="If .true. the bands are classified according to the irreducible representations of the small group of k. A file 'filband'.rap with the same format of 'filband' is written.",
    )
    no_overlap: bool = Field(
        False,
        description="If .true. writes the eigenvalues in the output file without changing their order.",
    )


class BANDSEspressoInput(EspressoInput):
    """Pydantic model for the input of `bands.x.`"""

    inputpp: InputppNamelist = Field(default_factory=lambda: InputppNamelist())
