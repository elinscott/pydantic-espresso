"""Pydantic model for the input of `ld1.x` version `qe-4.0.4`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputNamelist(Namelist):
    """Pydantic model for the `INPUT` namelist."""

    title: str | None = Field(None, description="A string describing the job.")
    beta: float = Field(0.2, description="parameter for potential mixing")
    tr2: float = Field(1e-14, description="convergence threshold for scf")
    iswitch: int = Field(
        1, description="1    all-electron calculation 2    PP test calculation 3    PP generation"
    )
    rel: int | None = Field(
        None,
        description="0 ... non relativistic calculation 1 ... scalar relativistic calculation 2 ... full relativistic calculation with spin-orbit",
    )
    lsmall: bool = Field(False, description="if .true. writes on files the small component")
    lsd: int = Field(
        0,
        description="0 ... non spin polarized calculation 1 ... spin-polarized calculation  BEWARE: not allowed if iswitch=3 (PP generation) or with full relativistic calculation",
    )
    dft: str | None = Field(
        None,
        description="Exchange-correlation functional.  Examples: 'PZ'    Perdew and Zunger formula for LDA 'PW91'  Perdew and Wang GGA 'BP'    Becke and Perdew GGA 'PBE'   Perdew, Becke and Ernzerhof GGA 'BLYP'  ...  For the complete list, see module 'functionals' in ../flib/ The default is 'PZ' for all-electron calculations, it is read from the PP file in a PP calculation.",
    )
    latt: int = Field(0, description="0 ... no Latter correction 1 ... apply Latter correction")
    isic: int = Field(
        0,
        description="0 ... no Self-interaction correction 1 ... apply Self-interaction correction",
    )
    rytoev_fact: float | None = Field(None, description="Factor used to convert Ry into eV.")
    cau_fact: float | None = Field(
        None,
        description="Speed of light in a.u..  (Be careful the default value is always used in the relativistic exchange.)",
    )
    vdw: bool = Field(
        False,
        description="If .true., the frequency dependent polarizability and van der Waals coefficient C6 will be computed in Thomas-Fermi and von Weizsaecker approximation(only for closed-shell ions).",
    )
    prefix: str = Field(
        "ld1",
        description="Prefix for file names - only for output file names containing the orbitals, logarithmic derivatives, tests See below for file names and the content of the file.",
    )
    verbosity: str = Field(
        "low",
        description="low' or 'high'  if 'high' with iswitch=2,3 prints separately core and valence contributions to the energies. Print the frozen-core energy.",
    )
    config: str | None = Field(
        None,
        description="A string with the electronic configuration.  Example: '[Ar] 3d10 4s2 4p2.5'  * If lsd=1, spin-up and spin-down state may appear twice with the respective occupancy: 3p4 3p2 = 4 up, 2 down. Otherwise, the Hund's rule is assumed.  * If rel=2, states with jj=l-1/2 are filled first. If a state appears twice, the first one has jj=l-1/2, the second one jj=l+1/2 (except S states) (Use rel_dist if you want to average the electrons over all available states.)  Negative occupancies are used to flag unbound states; they are not actually used.",
    )
    rel_dist: str = Field(
        "energy",
        description="energy' or 'average'  * if 'energy' the relativistic l-1/2 states are filled first.  * if 'average' the electrons are uniformly distributed among all the states with the given l.",
    )
    write_coulomb: bool = Field(
        False,
        description="If .true., a fake pseuopotential file with name X.UPF, where X is the atomic symbol, is written. It contains the radial grid and the wavefunctions as specified in input, plus the info needed to build the Coulomb potential for an all-electron calculation - for testing only.",
    )


class InputpNamelist(Namelist):
    """Pydantic model for the `INPUTP` namelist."""

    zval: float | None = Field(
        None,
        description="Valence charge.  zval is automatically calculated from available data. If the value of zval is provided in input, it will be checked versus the calculated value. The only case in which you need to explicitly provide the value of zval is for noninteger zval (i.e. half core-hole pseudopotentials).",
    )
    pseudotype: int | None = Field(
        None,
        description="1 ... norm-conserving, single-projector PP (old format) IMPORTANT: if pseudotype=1 all calculations are done using the SEMILOCAL form, not the separable nonlocal form  2 ... norm-conserving, multiple-projector PP in separable form  3 ... ultrasoft PP",
    )
    upf_v1_format: bool = Field(
        False,
        description=".true. generates pseudopotential file in UPF version 1 format, compatible with QE version 3",
    )
    file_pseudopw: str | None = Field(
        None,
        description="File where the generated PP is written.  * if the file name ends with 'upf' or 'UPF', or in any case for spin-orbit PP (rel=2), the file is written in UPF format;  * if the file name ends with 'psp' it is written in native CPMD format (this is currently an experimental feature); otherwise it is written in the old 'NC' format if pseudotype=1, or in the old RRKJ format if pseudotype=2 or 3 (no default, must be specified).",
    )
    file_recon: str | None = Field(
        None,
        description="File containing data needed for PAW reconstruction of all-electron wavefunctions from PP results. If you want to use additional states to perform the reconstruction, add them at the end of the list of all-electron states.",
    )
    lloc: int = Field(
        -1,
        description="Angular momentum of the local channel.  * lloc=-1 pseudizes the all-electron potential * lloc>-1 uses the corresponding channel as local PP  NB: if lloc>-1, the corresponding channel must be the last in the list of wavefunctions appearing after the namelist &inputp In the relativistic case, if lloc > 0 both the j=lloc-1/2 and the j=lloc+1/2 wavefunctions must be at the end of the list.",
    )
    rcloc: float | None = Field(
        None, description="Matching radius (a.u.) for local pseudo-potential (no default)."
    )
    nlcc: bool = Field(
        False,
        description="If .true. produce a PP with the nonlinear core correction of Froyen, Cohen, and Louie.",
    )
    new_core_ps: bool = Field(
        False, description="If .true. pseudizes the core charge with bessel functions."
    )
    rcore: float | None = Field(
        None,
        description="Matching radius (a.u.) for the smoothing of the core charge. If not specified, the matching radius is determined by the condition:  rho_core(rcore) = 2*rho_valence(rcore)",
    )
    tm: bool = Field(
        False,
        description="* .true. for Troullier-Martins pseudization [PRB 43, 1993 (1991) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.43.1993)]  * .false. for Rabe-Rappe-Kaxiras-Joannopoulos pseudization [PRB 41, 1227 (1990) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.41.1227), erratum PRB 44, 13175 (1991) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.44.13175)]",
    )
    rho0: float = Field(
        0.0,
        description="Charge at the origin: when the Rabe-Rappe-Kaxiras-Joannopoulos method with 3 Bessel functions fails, specifying rho0 > 0 may allow to override the problem (using 4 Bessel functions). Typical values are in the order of 0.01-0.02",
    )
    lpaw: bool = Field(
        False,
        description="If .true. produce a PAW dataset, experimental feature only for pseudotype=3",
    )
    lsave_wfc: bool | None = Field(
        None,
        description="Set it to .true. to save all-electron and pseudo wavefunctions used in the pseudopotential generation in the UPF file. Only works for UPFv2 format.",
    )
    author: str = Field("anonymous", description="Name of the author.")
    file_chi: str | None = Field(None, description="file containing output PP chi functions")
    file_beta: str | None = Field(None, description="file containing output PP beta functions")
    file_qvan: str | None = Field(None, description="file containing output PP qvan functions")
    file_screen: str | None = Field(None, description="file containing output screening potential")
    file_core: str | None = Field(None, description="file containing output total and core charge")
    file_wfcaegen: str | None = Field(
        None, description="file with the all-electron wfc for generation"
    )
    file_wfcncgen: str | None = Field(
        None, description="file with the norm-conserving wfc for generation"
    )
    file_wfcusgen: str | None = Field(
        None, description="file with the ultra-soft wfc for generation"
    )


class TestNamelist(Namelist):
    """Pydantic model for the `TEST` namelist."""

    nconf: int = Field(1, description="the number of configurations to be tested")
    file_pseudo: str | None = Field(
        None,
        description="File containing the PP.  * If the file name contains  '.upf' or '.UPF', the file is assumed to be in UPF format;  * else if the file name contains '.rrkj3' or '.RRKJ3', the old RRKJ format is first tried;  * otherwise, the old NC format is read.  IMPORTANT: in the latter case, all calculations are done using the SEMILOCAL form, not the separable nonlocal form. Use the UPF format if you want to test the separable form!",
    )
    rm: float | None = Field(
        None, description="Radius of the box used with spherical Bessel functions."
    )
    frozen_core: bool = Field(
        False,
        description="If .true. only the core wavefunctions of the first configuration are calculated. The eigenvalues, orbitals and energies of the other configurations are calculated with the core of the first configuration. The first configuration must be spin-unpolarized.",
    )


class LD1EspressoInput(EspressoInput):
    """Pydantic model for the input of `ld1.x`"""

    input: InputNamelist = Field(default_factory=lambda: InputNamelist())
    inputp: InputpNamelist = Field(default_factory=lambda: InputpNamelist())
    test: TestNamelist = Field(default_factory=lambda: TestNamelist())
