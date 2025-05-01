"""Pydantic model for the input of `molecularpdos.x` version `e6621af`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInputTemplate


class MOLECULARPDOSEspressoInput(EspressoInputTemplate):
    """Pydantic model for the input of `molecularpdos.x.`"""

    i_atmwfc_beg_full: int = Field( 1
         , description="first atomic wavefunction of the full system considered for the projection")
    i_atmwfc_end_full: int = Field( 0, i.e., all atomic wavefunctions
         , description="last atomic wavefunction of the full system considered for the projection")
    i_atmwfc_beg_part: int = Field( 1
         , description="first atomic wavefunction of the molecular part considered for the projection")
    i_atmwfc_end_part: int = Field( 0, i.e., all atomic wavefunctions
         , description="last atomic wavefunction of the molecular part considered for the projection")
    i_bnd_beg_full: int = Field( 1
         , description="first eigenstate of the full system to be taken into account for the projection")
    i_bnd_end_full: int = Field( 0, i.e., all eigenstates
         , description="last eigenstate of the full system to be taken into account for the projection")
    i_bnd_beg_part: int = Field( 1
         , description="first eigenstate of the molecular part to be taken into account for the projection")
    i_bnd_end_part: int = Field( 0, i.e., all eigenstates
         , description="last eigenstate of the molecular part to be taken into account for the projection")
    fileout: str = Field(" 'molecularpdos'
         ", description="prefix for output files containing molecular PDOS(E)")
    ngauss: int = Field( 0
         , description="Type of gaussian broadening:     0 ... Simple Gaussian (default)     1 ... Methfessel-Paxton of order 1    -1 ... 'cold smearing' (Marzari-Vanderbilt-DeVita-Payne)   -99 ... Fermi-Dirac function")
    degauss: float = Field( 0.0
         , description="gaussian broadening, Ry (not eV!)")
    DeltaE: float = Field( 0.01
         , description="energy grid step (eV)")
    kresolveddos: bool = Field(False, description="if .true. the k-resolved DOS is computed: not summed over all k-points but written as a function of the k-point index. In this case all k-point weights are set to unity")
