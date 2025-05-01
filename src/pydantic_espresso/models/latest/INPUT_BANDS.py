"""Pydantic model for the input of `bands.x` version `latest`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInputTemplate


class BANDSEspressoInput(EspressoInputTemplate):
    """Pydantic model for the input of `bands.x.`"""

    prefix: str = Field(" 'pwscf'
         ", description="prefix of files saved by program pw.x")
    outdir: str = Field("
value of the ESPRESSO_TMPDIR environment variable if set;
current directory ('./') otherwise
         ", description="directory containing the input data, i.e. the same as in pw.x")
    filband: str = Field(" 'bands.out'
         ", description="file name for band output (to be read by 'plotband.x')")
    spin_component: int = Field(..., description="In the lsda case select:     1 = spin-up    2 = spin-down")
    lp: bool = Field(False, description="If .true. matrix elements of the momentum operator p between conduction and valence bands are computed and written to file specified in")
    filp: str = Field(" 'p_avg.dat'
         ", description="If")
    lsym: bool = Field(True, description="If .true. the bands are classified according to the irreducible representations of the small group of k. A file 'filband'.rap with the same format of 'filband' is written, for usage by 'plotband.x'")
    no_overlap: bool = Field(True, description="If .false., and if")
    plot_2d: bool = Field(False, description="If .true. writes the eigenvalues in the output file in a 2D format readable by gnuplot. Band ordering is not changed. Each band is written in a different file called filband.# with the format:")
