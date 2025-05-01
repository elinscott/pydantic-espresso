"""Pydantic model for the input of `bands.x` version `qe-5.1.0`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class BandsNamelist(Namelist):
    """Pydantic model for the `Bands` namelist."""

    prefix: str | None = Field(None, description="prefix of files saved by program pw.x")
    outdir: Path = Field(default_factory=get_tmp_dir, description="directory containing the input data, i.e. the same as in pw.x")
    filband: str | None = Field(None, description="file 'filband' contains the bands")
    spin_component: int | None = Field(None, description="In the lsda case select:  1 = spin-up 2 = spin-down")
    lsym: bool | None = Field(None, description="If .true. the bands are classified according to the irreducible representations of the small group of k. A file 'filband'.rap with the same format of 'filband' is written.")
    no_overlap: bool = Field(False, description="If .true. writes the eigenvalues in the output file without changing their order.")
    plot_2d: bool = Field(False, description="If .true. writes the eigenvalues in the output file in a 2D format readable by gnuplot. Band ordering is not changed. Each band is written in a different file called filband.# with the format: xk, yk, energy xk, yk, energy ..  ..  .. energies are written in eV and xk in units 2\pi/a.")


class BANDSEspressoInput(EspressoInput):
    """Pydantic model for the input of `bands.x.`"""

    bands: BandsNamelist = Field(default_factory=BandsNamelist)
