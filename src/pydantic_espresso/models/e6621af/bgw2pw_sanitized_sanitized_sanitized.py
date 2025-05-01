"""Pydantic model for the input of `bgw2pw.x` version `e6621af`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import BaseModel


class Input_bgw2pwNamelist(BaseModel):
   """Pydantic model for the `Input_bgw2pw` namelist."""

    prefix: str | None = Field(None, description="prefix of files saved by program pw.x")
    outdir: str = Field("./", description="the scratch directory where the massive data-files are written")
    real_or_complex: int = Field(2, description="1 | 2 1 for real flavor of BerkeleyGW (for systems with inversion symmetry and time-reversal symmetry) or 2 for complex flavor of BerkeleyGW (for systems without inversion symmetry and time-reversal symmetry)")
    wfng_flag: bool = Field(False, description="read wavefunctions in G-space from BerkeleyGW WFN file")
    wfng_file: str = Field("WFN", description="name of BerkeleyGW WFN input file. Not used if wfng_flag = .FALSE.")
    wfng_nband: int = Field(0, description="number of bands to write (0 = all). Not used if wfng_flag = .FALSE.")
    rhog_flag: bool = Field(False, description="read charge density in G-space from BerkeleyGW RHO file")
    rhog_file: str = Field("RHO", description="name of BerkeleyGW RHO input file. Not used if rhog_flag = .FALSE.")


class BGW2PWEspressoInput(BaseModel):
    """Pydantic model for the input of `bgw2pw.x.`"""

    Input_bgw2pw: Input_bgw2pwNamelist
