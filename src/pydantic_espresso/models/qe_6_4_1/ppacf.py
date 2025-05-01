"""Pydantic model for the input of `ppacf.x` version `qe-6.4.1`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class PpacfNamelist(Namelist):
    """Pydantic model for the `Ppacf` namelist."""

    prefix: str | None = Field(None, description="prefix of files saved by program pw.x prepended to input/output filenames: prefix.ecnl, prefix.tcnl, etc.")
    outdir: Path = Field(value of the, description="directory containing the output data from pw.x, i.e. the same as in pw.x")
    n_lambda: int = Field(1, description="Number of fragments in coupling-constant scaling curve. In the default case, only $\lambda=0$ and $\lambda=1$ ends are calculated.")
    lplot: bool = Field(False, description="If .True. print out the spatial distribution of energy density. prefix.tclda             the LDA component of kinetic-correlation energy density. prefix.tcnl(prefix.tcgc) the non-local (gradient corrected) component of kinetic-correlation energy density. prefix.exlda             the LDA component of exchange energy density. prefix.eclda             the LDA component of correlation energy density. prefix.exgc              the gradient-corrected component of exchange energy density. prefix.ecnl(prefix.ecgc) the non-local(gradient-corrected) component of correlation energy density.")
    lfock: bool = Field(False, description="If .True. calculate the Fock exchange based on input Kohn-Sham orbitals.")
    code_num: int = Field(1, description="Select from which code to read output files. 1 = Quantum ESPRESSO 2 = VASP The codes will read vasprun.xml and CHGCAR from VASP calculations. Please note that in VASP-based analysis: - Core charge is ignored. - Wavefunction based analysis (Fock exchange energy and Kohn-Sham kinetic energy) are not available. - When lplot = .True., the code will also print out charge density in prefix.chg (prefix.chg1 and prefix.chg2 save the spin-up and spin-down components in case of spin-polarized calculations), which can be processed by pp.x.")
    pseudo_dir: Path = Field(default_factory=get_pseudo_dir, description="Directory containing pseudopotential files (and vdw kernel table).")
    vdw_table_name: str = Field("vdW_kernel_table", description="The vdw kernel table (in Quantum ESPRESSO format).")


class PPACFEspressoInput(EspressoInput):
    """Pydantic model for the input of `ppacf.x.`"""

    ppacf: PpacfNamelist = Field(default_factory=PpacfNamelist)
