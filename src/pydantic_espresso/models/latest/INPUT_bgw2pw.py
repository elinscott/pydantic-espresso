"""Pydantic model for the input of `bgw2pw.x` version `latest`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInputTemplate


class BGW2PWEspressoInput(EspressoInputTemplate):
    """Pydantic model for the input of `bgw2pw.x.`"""

    prefix: str = Field(..., description="prefix of files saved by program pw.x")
    outdir: str = Field(" './'
         ", description="the scratch directory where the massive data-files are written")
    real_or_complex: int = Field( 2
         , description="1 | 2")
    wfng_flag: bool = Field(False, description="read wavefunctions in G-space from BerkeleyGW WFN file")
    wfng_file: str = Field(" 'WFN'
         ", description="name of BerkeleyGW WFN input file. Not used if")
    wfng_nband: int = Field( 0
         , description="number of bands to write (0 = all). Not used if")
    rhog_flag: bool = Field(False, description="read charge density in G-space from BerkeleyGW RHO file")
    rhog_file: str = Field(" 'RHO'
         ", description="name of BerkeleyGW RHO input file. Not used if")
