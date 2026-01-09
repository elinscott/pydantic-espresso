"""Pydantic model for the input of `bands.x` version `qe-7.1rc`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class BandsNamelist(Namelist):
    """Pydantic model for the `BANDS` namelist."""

    prefix: str = Field("pwscf", description="prefix of files saved by program pw.x")
    outdir: Path = Field(
        default_factory=get_tmp_dir,
        description="directory containing the input data, i.e. the same as in pw.x",
    )
    filband: str = Field(
        "bands.out", description="file name for band output (to be read by 'plotband.x')"
    )
    spin_component: int | None = Field(
        None, description="In the lsda case select:  1 = spin-up 2 = spin-down"
    )
    lp: bool = Field(
        False,
        description="If .true. matrix elements of the momentum operator p between conduction and valence bands are computed and written to file specified in filp. The matrix elements include the contribution from the nonlocal potential, i*m*[V_nl, x]. In other words, the calculated matrix elements are those of the velocity operator i*m*[H, x] times mass, not those of the true momentum operator.",
    )
    filp: str = Field(
        "p_avg.dat", description="If lp is set to .true., file name for matrix elements of p"
    )
    lsym: bool = Field(
        True,
        description="If .true. the bands are classified according to the irreducible representations of the small group of k. A file 'filband'.rap with the same format of 'filband' is written, for usage by 'plotband.x",
    )
    no_overlap: bool = Field(
        True,
        description="If .false., and if lsym is .false., writes the eigenvalues in the order that maximises overlap with the neighbor k-points",
    )
    plot_2d: bool = Field(
        False,
        description="If .true. writes the eigenvalues in the output file in a 2D format readable by gnuplot. Band ordering is not changed. Each band is written in a different file called filband.# with the format:",
    )
    lsigma: tuple[bool, bool, bool] | None = Field(
        None,
        description="If true computes expectation values of the spin operator on the spinor wave-functions (only in the noncollinear case), writes them to a file 'filband'.i, i=1,2,3",
    )


class BANDSEspressoInput(EspressoInput):
    """Pydantic model for the input of `bands.x`"""

    bands: BandsNamelist = Field(default_factory=lambda: BandsNamelist())
