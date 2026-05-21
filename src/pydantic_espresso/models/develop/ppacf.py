"""Pydantic model for the input of `ppacf.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from textwrap import dedent
from typing import Literal

from pydantic import Field

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist


class PpacfNamelist(Namelist):
    """Pydantic model for the `PPACF` namelist."""

    prefix: str = Field(
        "ppacf",
        description=dedent(
            """\
            prefix of files saved by program pw.x prepended to input/output filenames: prefix.ecnl,
            prefix.tcnl, etc."""
        ),
    )
    outdir: Path = Field(
        Path("'./'"),
        description="directory containing the output data from pw.x, i.e. the same as in pw.x.",
    )
    n_lambda: int = Field(
        1,
        description=dedent(
            """\
            Number of fragments in coupling-constant scaling curve. In the default case, only
            $lambda=0$ and $lambda=1$ ends are calculated."""
        ),
    )
    lplot: bool = Field(
        False,
        description=dedent(
            """\
            If .True. print out the spatial distribution of energy density. prefix.tclda
             the LDA component of kinetic-correlation energy density. prefix.tcnl(prefix.tcgc) the
            non-local (gradient corrected) component of kinetic-correlation energy density.
            prefix.exlda             the LDA component of exchange energy density. prefix.eclda
                    the LDA component of correlation energy density. prefix.exgc              the
            gradient-corrected component of exchange energy density. prefix.ecnl(prefix.ecgc) the
            non-local(gradient-corrected) component of correlation energy density. prefix.vcnl
                        If vdW-DF: the non-local correlation-potential variation (at nspin=1).
            prefix.vcnl1,2                 If spin-vdW-DF: spin-reolved non-local
            correlation-potential variations."""
        ),
    )
    ltks: bool = Field(
        False,
        description=dedent(
            """\
            If .True. also print out prefix.tks               the Kohn-Sham kinetic energy density.
            In case of spin-polarized calculations, prefix.tks1 and prefix.tks2 save the spin-up
            and spin-down components."""
        ),
    )
    lfock: bool = Field(
        False,
        description="If .True. calculate the Fock exchange based on input Kohn-Sham orbitals.",
    )
    use_ace: bool = Field(
        True,
        description=dedent(
            """\
            If .True. use Lin Lin's ACE (J. Chem. Theory Comput. 12(5), 2242-2249 (2016), doi:
            10.1021/acs.jctc.6b00092 (https://doi.org/10.1021/acs.jctc.6b00092))."""
        ),
    )
    code_num: Literal[1, 2] = Field(
        1,
        description=dedent(
            """\
            Select from which code to read output files.
            - '1': Quantum ESPRESSO.
            - '2': VASP. The codes will read vasprun.xml and CHGCAR from VASP calculations. Please
              note that in VASP-based analysis: - Core charge is ignored. - The
              ppacf-from-VASP-read-in only works for VASP calculations done in PBE, revPBE, vdW-DF,
              vdW-DF2, or vdW-DF-cx - The ppacf-from-VASP-read-in only always uses the full Ecnl
              kernel for coupling-constant scaling analysis of vdW-DF versions. - Wavefunction
              based analysis (Fock exchange energy and Kohn-Sham kinetic energy) are not available
              from VASP - When lplot = .True., the code will also print out charge density in
              prefix.chg (prefix.chg1 and prefix.chg2 save the spin-up and spin-down components in
              case of spin-polarized calculations), which can be processed by pp.x."""
        ),
    )
    vdW_analysis: Literal[0, 1, 2] = Field(  # noqa: N815
        0,
        description=dedent(
            """\
            Select type of vdw kernel table used in ppacf coupling-constant scaling analysis of
            nonlocal-correlations in vdW-DF versions. See IOP JCPM (2020) for presentation of the
            two non-default options.
            - '0': Full Ecnl kernel of vdW-DF method.
            - '1': The cumulant- or susceptibility-Ecnl kernel component.
            - '2': The pure-vdW-Ecnl kernel component."""
        ),
    )


class PPACFEspressoInput(EspressoInput):
    """Pydantic model for the input of `ppacf.x`."""

    ppacf: PpacfNamelist = Field(default_factory=lambda: PpacfNamelist())
