"""Pydantic model for the input of `projwfc.x` version `latest`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInputTemplate


class PROJWFCEspressoInput(EspressoInputTemplate):
    """Pydantic model for the input of `projwfc.x.`"""

    prefix: str = Field(" 'pwscf'
         ", description="prefix of input file produced by")
    outdir: str = Field("
value of the ESPRESSO_TMPDIR environment variable if set;
current directory ('./') otherwise
         ", description="directory containing the input data, i.e. the same as in")
    ngauss: int = Field( 0
         , description="Type of gaussian broadening:     0 ... Simple Gaussian (default)     1 ... Methfessel-Paxton of order 1    -1 ... 'cold smearing' (Marzari-Vanderbilt-DeVita-Payne)   -99 ... Fermi-Dirac function")
    degauss: float = Field( 0.0
         , description="gaussian broadening, Ry (not eV!)")
    DeltaE: float = Field(..., description="energy grid step (eV)")
    lsym: bool = Field(True, description="if")
    diag_basis: bool = Field(False, description="if")
    pawproj: bool = Field(False, description="if")
    filpdos: str = Field(" (value of ", description="prefix for output files containing PDOS(E)")
    filproj: str = Field(" (standard output)
         ", description="file containing the projections")
    lwrite_overlaps: bool = Field(False, description="if")
    lbinary_data: bool = Field(False, description="CURRENTLY DISABLED. if")
    kresolveddos: bool = Field(False, description="if")
    tdosinboxes: bool = Field(False, description="if")
    n_proj_boxes: int = Field( 1
         , description="number of boxes where the local DOS is computed")
    plotboxes: bool = Field(False, description="if")
