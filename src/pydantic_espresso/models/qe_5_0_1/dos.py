"""Pydantic model for the input of `dos.x` version `qe-5.0.1`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class DosNamelist(Namelist):
    """Pydantic model for the `Dos` namelist."""

    prefix: str = Field(
        "pwscf", description="prefix of input file produced by pw.x (wavefunctions are not needed)"
    )
    outdir: Path = Field(Path("./"), description="directory containing the input file")
    ngauss: int = Field(
        0,
        description="Type of gaussian broadening:  =  0  Simple Gaussian (default)  =  1  Methfessel-Paxton of order 1  = -1  Marzari-Vanderbilt 'cold smearing'  =-99  Fermi-Dirac function",
    )
    degauss: float | None = Field(
        None, description="gaussian broadening, Ry (not eV!)          see below"
    )
    DeltaE: float | None = Field(None, description="energy grid step (eV)")
    fildos: str | None = Field(None, description="output file containing DOS(E)")


class DOSEspressoInput(EspressoInput):
    """Pydantic model for the input of `dos.x.`"""

    dos: DosNamelist = Field(default_factory=lambda: DosNamelist())
