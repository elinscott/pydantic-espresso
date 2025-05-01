"""Pydantic model for the input of `projwfc.x` version `qe-4.1`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputppNamelist(Namelist):
    """Pydantic model for the `Inputpp` namelist."""

    prefix: str = Field("pwscf", description="Prefix of input file produced by pw.x (wavefunctions are needed).")
    outdir: Path = Field(./, description="directory containing the input file")
    ngauss: int = Field(0, description="Type of gaussian broadening: 0 ... Simple Gaussian (default) 1 ... Methfessel-Paxton of order 1 -1 ... Marzari-Vanderbilt 'cold smearing' -99 ... Fermi-Dirac function")
    degauss: float = Field(0.0, description="gaussian broadening, Ry (not eV!)")
    DeltaE: float | None = Field(None, description="energy grid step (eV)")
    lsym: bool = Field(True, description="if true the projections are symmetrized")
    filpdos: str | None = Field(None, description="prefix for output files containing PDOS(E)")
    filproj: str | None = Field(None, description="file containing the projections")


class PROJWFCEspressoInput(EspressoInput):
    """Pydantic model for the input of `projwfc.x.`"""

    inputpp: InputppNamelist = Field(default_factory=InputppNamelist)
