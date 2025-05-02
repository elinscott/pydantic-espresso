"""Pydantic model for the input of `molecularpdos.x` version `qe-5.1.2`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputmopdosNamelist(Namelist):
    """Pydantic model for the `Inputmopdos` namelist."""


    i_atmwfc_beg_full: int = Field(1, description="first atomic wavefunction of the full system considered for the projection")
    i_atmwfc_end_full: int | None = Field(None, description="last atomic wavefunction of the full system considered for the projection")
    i_atmwfc_beg_part: int = Field(1, description="first atomic wavefunction of the molecular part considered for the projection")
    i_atmwfc_end_part: int | None = Field(None, description="first atomic wavefunction of the molecular part considered for the projection")
    i_bnd_beg_full: int = Field(1, description="first eigenstate of the full system to be taken into account for the projection")
    i_bnd_end_full: int | None = Field(None, description="last eigenstate of the full system to be taken into account for the projection")
    i_bnd_beg_part: int = Field(1, description="first eigenstate of the molecular part to be taken into account for the projection")
    i_bnd_end_part: int | None = Field(None, description="last eigenstate of the molecular part to be taken into account for the projection")
    fileout: str = Field("molecularpdos", description="prefix for output files containing molecular PDOS(E)")
    ngauss: int = Field(0, description="Type of gaussian broadening: 0 ... Simple Gaussian (default) 1 ... Methfessel-Paxton of order 1 -1 ... Marzari-Vanderbilt 'cold smearing' -99 ... Fermi-Dirac function")
    degauss: float = Field(0.0, description="gaussian broadening, Ry (not eV!)")
    DeltaE: float = Field(0.01, description="energy grid step (eV)")


class MOLECULARPDOSEspressoInput(EspressoInput):
    """Pydantic model for the input of `molecularpdos.x.`"""

    inputmopdos: InputmopdosNamelist = Field(default_factory=lambda: InputmopdosNamelist())
