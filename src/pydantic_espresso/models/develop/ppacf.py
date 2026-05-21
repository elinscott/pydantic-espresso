"""Pydantic model for the input of `ppacf.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from typing import Literal

from pydantic import Field

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist


class PpacfNamelist(Namelist):
    """Pydantic model for the `PPACF` namelist."""

    prefix: str = Field(
        "ppacf",
        description=(
            "prefix of files saved by program pw.x prepended to input/output filenames: "
            "prefix.ecnl, prefix.tcnl, etc."
        ),
    )
    outdir: Path = Field(
        Path("'./'"),
        description="directory containing the output data from pw.x, i.e. the same as in pw.x.",
    )
    n_lambda: int = Field(
        1,
        description=(
            "Number of fragments in coupling-constant scaling curve. In the default case, only "
            "$lambda=0$ and $lambda=1$ ends are calculated."
        ),
    )
    lplot: bool = Field(
        False,
        description=(
            "If .True. print out the spatial distribution of energy density. prefix.tclda          "
            "   the LDA component of kinetic-correlation energy density. prefix.tcnl(prefix.tcgc) "
            "the non-local (gradient corrected) component of kinetic-correlation energy density. "
            "prefix.exlda             the LDA component of exchange energy density. prefix.eclda   "
            "          the LDA component of correlation energy density. prefix.exgc              "
            "the gradient-corrected component of exchange energy density. prefix.ecnl(prefix.ecgc) "
            "the non-local(gradient-corrected) component of correlation energy density. "
            "prefix.vcnl                  If vdW-DF: the non-local correlation-potential variation "
            "(at nspin=1). prefix.vcnl1,2                 If spin-vdW-DF: spin-reolved non-local "
            "correlation-potential variations."
        ),
    )
    lfock: bool = Field(
        False,
        description="If .True. calculate the Fock exchange based on input Kohn-Sham orbitals.",
    )
    code_num: Literal[1, 2] = Field(1, description="Select from which code to read output files.")
    vdW_analysis: Literal[0, 1, 2] = Field(  # noqa: N815
        0,
        description=(
            "Select type of vdw kernel table used in ppacf coupling-constant scaling analysis of "
            "nonlocal-correlations in vdW-DF versions. See IOP JCPM (2020) for presentation of the "
            "two non-default options."
        ),
    )


class PPACFEspressoInput(EspressoInput):
    """Pydantic model for the input of `ppacf.x`."""

    ppacf: PpacfNamelist = Field(default_factory=lambda: PpacfNamelist())
