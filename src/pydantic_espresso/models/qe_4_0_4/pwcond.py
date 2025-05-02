"""Pydantic model for the input of `pwcond.x` version `qe-4.0.4`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputcondNamelist(Namelist):
    """Pydantic model for the `Inputcond` namelist."""


    outdir: Path | None = Field(None, description="temporary directory (as in PWscf)")
    prefixt: str | None = Field(None, description="prefix for the file (as in PWscf) containing all the regions (left lead + scatt. reg. + right lead)")
    prefixl: str | None = Field(None, description="prefix for the file containing only the        left lead")
    prefixs: str | None = Field(None, description="prefix for the file containing the scattering region")
    prefixr: str | None = Field(None, description="prefix for the file containing only the right lead")
    band_file: str | None = Field(None, description="file on which the complex bands are saved")
    tran_file: str | None = Field(None, description="file where the transmission is written")
    save_file: str | None = Field(None, description="file where the data necessary for PWCOND are written so that no prefix files of PW are longer needed")
    fil_loc: str | None = Field(None, description="file on/from which the 2D eigenvalue problem data are saved/read")
    lwrite_cond: bool | None = Field(None, description="if .t. save the data necessary for PWCOND in save_file")
    lread_cond: bool | None = Field(None, description="if .t. read the data necessary for PWCOND from save_file")
    lwrite_loc: bool | None = Field(None, description="if .t. save 2D eigenvalue problem result in fil_loc")
    lread_loc: bool | None = Field(None, description="if .t. read 2D eigenvalue problem result from fil_loc")
    ikind: int | None = Field(None, description="The kind of conductance calculation:  ikind=0  - just complex band structure (CBS) calculation  ikind=1  - conductance calculation with identical left and right leads  ikind=2  - conductance calculation with different left and right leads")
    iofspin: int | None = Field(None, description="spin index for which the calculations are performed")
    llocal: bool | None = Field(None, description="if .t. calculations are done with only local part of PP")
    bdl: float | None = Field(None, description="right boundary of the left lead (left one is supposed to be at 0)")
    bds: float | None = Field(None, description="right boundary of the scatt. reg. (left one is at 0 if prefixs is used and = bdl if prefixt is used)")
    bdr: float | None = Field(None, description="right boundary of the right lead (left one is at 0 if prefixr is used and = bds if prefixt is used)")
    nz1: int | None = Field(None, description="the number of subslabs in the slab (to calculate integrals)")
    energy0: float | None = Field(None, description="initial energy")
    denergy: float | None = Field(None, description="energy step (if denergy=0.0 the energy is read from the list)")
    nenergy: int | None = Field(None, description="number of energies  WARNING: the energy in input file is given in eV taken from Ef, and denergy should be negative")
    ecut2d: float | None = Field(None, description="2-D cutoff")
    ewind: float | None = Field(None, description="the energy window for reduction of 2D plane wave basis set (in XY)")
    epsproj: float | None = Field(None, description="accuracy of 2D basis set reduction")
    orbj_in: float | None = Field(None, description="the initial orbital for projecting the transmission")
    orbj_fin: float | None = Field(None, description="the final orbital for projecting the transmission")


class PWCONDEspressoInput(EspressoInput):
    """Pydantic model for the input of `pwcond.x.`"""

    inputcond: InputcondNamelist = Field(default_factory=lambda: InputcondNamelist())
