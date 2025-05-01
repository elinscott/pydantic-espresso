"""Pydantic model for the input of `bands.x` version `latest`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import BaseModel


class BandsNamelist(BaseModel):
   """Pydantic model for the `Bands` namelist."""

    prefix: str = Field("pwscf", description="prefix of files saved by program pw.x")
    outdir: str = Field("value of the ESPRESSO_TMPDIR environment variable if set;
current directory ('./') otherwise", description="directory containing the input data, i.e. the same as in pw.x")
    filband: str = Field("bands.out", description="file name for band output (to be read by 'plotband.x')")
    spin_component: int | None = Field(None, description="In the lsda case select:  1 = spin-up 2 = spin-down")
    lp: bool = Field(False, description="If .true. matrix elements of the momentum operator p between conduction and valence bands are computed and written to file specified in filp. The matrix elements include the contribution from the nonlocal potential, i*m*[V_nl, x]. In other words, the calculated matrix elements are those of the velocity operator i*m*[H, x] times mass, not those of the true momentum operator.")
    filp: str = Field("p_avg.dat", description="If lp is set to .true., file name for matrix elements of p")
    lsym: bool = Field(True, description="If .true. the bands are classified according to the irreducible representations of the small group of k. A file 'filband'.rap with the same format of 'filband' is written, for usage by 'plotband.x'")
    no_overlap: bool = Field(True, description="If .false., and if lsym is .false., writes the eigenvalues in the order that maximises overlap with the neighbor k-points")
    plot_2d: bool = Field(False, description="If .true. writes the eigenvalues in the output file in a 2D format readable by gnuplot. Band ordering is not changed. Each band is written in a different file called filband.# with the format:")


class BANDSEspressoInput(BaseModel):
    """Pydantic model for the input of `bands.x.`"""

    Bands: BandsNamelist
