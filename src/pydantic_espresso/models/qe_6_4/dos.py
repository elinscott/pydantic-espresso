"""Pydantic model for the input of `dos.x` version `qe-6.4`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class DosNamelist(Namelist):
    """Pydantic model for the `DOS` namelist."""

    prefix: str = Field(
        "pwscf", description="prefix of input file produced by pw.x (wavefunctions are not needed)"
    )
    outdir: Path = Field(
        Path("value of the"),
        description="directory containing the input data, i.e. the same as in pw.x",
    )
    bz_sum: Literal[None, "smearing", "tetrahedra", "tetrahedra_lin", "tetrahedra_opt"] = Field(
        None, description="Keyword selecting  the method for BZ summation. Available options are:"
    )
    ngauss: int = Field(
        0,
        description="Type of gaussian broadening:  =  0  Simple Gaussian (default)  =  1  Methfessel-Paxton of order 1  = -1  Marzari-Vanderbilt 'cold smearing'  =-99  Fermi-Dirac function",
    )
    degauss: float | None = Field(None, description="gaussian broadening, Ry (not eV!) (see below)")
    DeltaE: float | None = Field(None, description="energy grid step (eV)")
    fildos: str = Field("prefix.dos", description="output file containing DOS(E)")


class DOSEspressoInput(EspressoInput):
    """Pydantic model for the input of `dos.x`"""

    dos: DosNamelist = Field(default_factory=lambda: DosNamelist())
