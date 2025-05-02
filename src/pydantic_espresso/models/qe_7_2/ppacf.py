"""Pydantic model for the input of `ppacf.x` version `qe-7.2`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class PpacfNamelist(Namelist):
    """Pydantic model for the `Ppacf` namelist."""

    prefix: str | None = Field(
        None,
        description="prefix of files saved by program pw.x prepended to input/output filenames: prefix.ecnl, prefix.tcnl, etc.",
    )
    outdir: Path = Field(
        Path("value of the"),
        description="directory containing the output data from pw.x, i.e. the same as in pw.x",
    )
    n_lambda: int = Field(
        1,
        description="Number of fragments in coupling-constant scaling curve. In the default case, only $lambda=0$ and $lambda=1$ ends are calculated.",
    )
    lplot: bool = Field(
        False,
        description="If .True. print out the spatial distribution of energy density. prefix.tclda             the LDA component of kinetic-correlation energy density. prefix.tcnl(prefix.tcgc) the non-local (gradient corrected) component of kinetic-correlation energy density. prefix.exlda             the LDA component of exchange energy density. prefix.eclda             the LDA component of correlation energy density. prefix.exgc              the gradient-corrected component of exchange energy density. prefix.ecnl(prefix.ecgc) the non-local(gradient-corrected) component of correlation energy density. prefix.vcnl                  If vdW-DF: the non-local correlation-potential variation (at nspin=1). prefix.vcnl1,2                 If spin-vdW-DF: spin-reolved non-local correlation-potential variations.",
    )
    lfock: bool = Field(
        False,
        description="If .True. calculate the Fock exchange based on input Kohn-Sham orbitals.",
    )
    code_num: int = Field(
        1,
        description="Select from which code to read output files. 1 = Quantum ESPRESSO 2 = VASP The codes will read vasprun.xml and CHGCAR from VASP calculations. Please note that in VASP-based analysis: - Core charge is ignored. - The ppacf-from-VASP-read-in only works for VASP calculations done in PBE, revPBE, vdW-DF, vdW-DF2, or vdW-DF-cx - The ppacf-from-VASP-read-in only always uses the full Ecnl kernel for coupling-constant scaling analysis of vdW-DF versions. - Wavefunction based analysis (Fock exchange energy and Kohn-Sham kinetic energy) are not available from VASP - When lplot = .True., the code will also print out charge density in prefix.chg (prefix.chg1 and prefix.chg2 save the spin-up and spin-down components in case of spin-polarized calculations), which can be processed by pp.x.",
    )
    vdW_analysis: int | None = Field(
        None,
        description="Select type of vdw kernel table used in ppacf coupling-constant scaling analysis of nonlocal-correlations in vdW-DF versions: - vdW_analysis = 0: Full Ecnl kenel of vdW-DF method - vdW_analysis = 1: The cumulant- or susceptibility-Ecnl kernel component - vdW_analysis = 2: The pure-vdW-Ecnl kernel component See IOP JCPM (2020) for presentation of the latter two (non-default) options",
    )


class PPACFEspressoInput(EspressoInput):
    """Pydantic model for the input of `ppacf.x.`"""

    ppacf: PpacfNamelist = Field(default_factory=lambda: PpacfNamelist())
