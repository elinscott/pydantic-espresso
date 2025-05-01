"""Pydantic model for the input of `dos.x` version `e6621af`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import BaseModel


class DosNamelist(BaseModel):
   """Pydantic model for the `Dos` namelist."""

    prefix: str = Field("pwscf", description="prefix of input file produced by pw.x (wavefunctions are not needed)")
    outdir: str = Field("value of the", description="directory containing the input data, i.e. the same as in pw.x")
    bz_sum: Literal["smearing", "tetrahedra", "tetrahedra_lin", "tetrahedra_opt"] = Field("smearing' if degauss is given in input;
                        options read from the xml data file otherwise.", description="Keyword selecting  the method for BZ summation. Available options are:")
    ngauss: int = Field(0, description="Type of gaussian broadening:  =  0  Simple Gaussian (default)  =  1  Methfessel-Paxton of order 1  = -1  'cold smearing' (Marzari-Vanderbilt-DeVita-Payne)  =-99  Fermi-Dirac function")
    degauss: float | None = Field(None, description="gaussian broadening, Ry (not eV!) (see below)")
    DeltaE: float | None = Field(None, description="energy grid step (eV)")
    fildos: str = Field("prefix.dos", description="output file containing DOS(E)")


class DOSEspressoInput(BaseModel):
    """Pydantic model for the input of `dos.x.`"""

    Dos: DosNamelist
