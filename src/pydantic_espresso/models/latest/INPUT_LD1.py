"""Pydantic model for the input of `ld1.x` version `latest`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInputTemplate


class LD1EspressoInput(EspressoInputTemplate):
    """Pydantic model for the input of `ld1.x.`"""

    title: str = Field(..., description="A string describing the job.")
    beta: float = Field( 0.2
         , description="parameter for potential mixing")
    tr2: float = Field( 1e-14
         , description="convergence threshold for scf")
    iswitch: int = Field( 1
         , description="1    all-electron calculation 2    PP test calculation 3    PP generation 4    LDA-1/2 correction, needs a previously generated PP file")
    rel: int = Field(
0 for Z <= 18;
1 for Z >  18
         , description="0 ... non relativistic calculation 1 ... scalar relativistic calculation 2 ... full relativistic calculation with spin-orbit")
    lsmall: bool = Field(False, description="if .true. writes on files the small component")
    max_out_wfc: int = Field( 7
         , description="Maximum number of atomic wavefunctions written in the output file.")
    noscf: bool = Field(False, description="if .true. the charge is not computed. The occupations are not used and the eigenvalues and eigenfunctions are those of a hydrogen-like atom.")
    lsd: int = Field( 0
         , description="0 ... non spin polarized calculation 1 ... spin-polarized calculation")
    dft: str = Field(..., description="Exchange-correlation functional.  Examples:")
    latt: int = Field( 0
         , description="0 ... no Latter correction 1 ... apply Latter correction")
    isic: int = Field( 0
         , description="0 ... no Self-interaction correction 1 ... apply Self-interaction correction")
    rytoev_fact: float = Field( as specified in file Modules/constants.f90
         , description="Factor used to convert Ry into eV.")
    cau_fact: float = Field( as specified in file Modules/constants.f90
         , description="Speed of light in a.u..  (Be careful the default value is always used in the  relativistic exchange.)")
    vdw: bool = Field(False, description="If .true., the frequency dependent polarizability and van der Waals coefficient C6 will be computed in Thomas-Fermi and von Weizsaecker approximation(only for closed-shell ions).")
    prefix: str = Field(" 'ld1'
         ", description="Prefix for file names - only for output file names containing the orbitals, logarithmic derivatives, tests See below for file names and the content of the file.")
    verbosity: str = Field(" 'low'
         ", description="")
    file_charge: str = Field(" ' '
         ", description="Name of the file where the code writes the all-electron total charge. No charge is written if file_charge=' '.")
    config: str = Field(" ' '
         ", description="A string with the electronic configuration.  Example:   '[Ar] 3d10 4s2 4p2.5'  * If")
    relpert: bool = Field(False, description="If .true. the relativistic corrections to the non-relativistic Kohn-Sham energy levels (")
    rel_dist: str = Field(" 'energy'
         ", description="")
    write_coulomb: bool = Field(False, description="If .true., a fake pseudo-potential file with name X.UPF, where X is the atomic symbol, is written. It contains the radial grid and the wavefunctions as specified in input, plus the info needed to build the Coulomb potential for an all-electron calculation - for testing only.")
    zval: float = Field( (calculated)
         , description="Valence charge.  zval is automatically calculated from available data. If the value of zval is provided in input, it will be checked versus the calculated value. The only case in which you need to explicitly provide the value of zval for noninteger zval (i.e. half core-hole pseudo-potentials).")
    pseudotype: int = Field(..., description="1 ... norm-conserving, single-projector PP")
    file_pseudopw: str = Field(..., description="File where the generated PP is written.  * if the file name ends with 'upf' or 'UPF', or in any case for spin-orbit PP (rel=2), the file is written in UPF format;  * if the file name ends with 'psp' it is written in native CPMD format (this is currently an experimental feature); otherwise it is written in the old 'NC' format if pseudotype=1, or in the old RRKJ format if pseudotype=2 or 3 (no default, must be specified).")
    file_recon: str = Field(" ' '
         ", description="File containing data needed for GIPAW reconstruction of all-electron wavefunctions from PP results. If you want to use additional states to perform the reconstruction, add them at the end of the list of all-electron states.")
    lloc: int = Field( -1
         , description="Angular momentum of the local channel.  * lloc=-1 or lloc=-2 pseudizes the all-electron potential   if lloc=-2 the original recipe of Troullier-Martins   is used (zero first and second derivatives at r=0) * lloc>-1 uses the corresponding channel as local PP  NB: if lloc>-1, the corresponding channel must be the last in the list of wavefunctions appearing after the namelist &inputp In the relativistic case, if lloc > 0 both the j=lloc-1/2 and the j=lloc+1/2 wavefunctions must be at the end of the list.")
    rcloc: float = Field(..., description="Matching radius (a.u.) for local pseudo-potential (no default).")
    nlcc: bool = Field(False, description="If .true. produce a PP with the nonlinear core correction of Louie, Froyen, and Cohen [")
    new_core_ps: bool = Field(False, description="If .true. pseudizes the core charge with bessel functions.")
    rcore: float = Field(..., description="Matching radius (a.u.) for the smoothing of the core charge. If not specified, the matching radius is determined by the condition:  rho_core(rcore) = 2*rho_valence(rcore)")
    tm: bool = Field(False, description="* .true. for Troullier-Martins pseudization [")
    rho0: float = Field( 0.0
         , description="Charge at the origin: when the Rappe-Rabe-Kaxiras-Joannopoulos method with 3 Bessel functions fails, specifying rho0 > 0 may allow to override the problem (using 4 Bessel functions). Typical values are in the order of 0.01-0.02")
    lpaw: bool = Field(False, description="If .true. produce a PAW dataset, experimental feature only for")
    lsave_wfc: bool = Field( .false. if .not. lpaw, otherwise .true.
         , description="Set it to .true. to save all-electron and pseudo wavefunctions used in the pseudo-potential generation in the UPF file. Only works for UPFv2 format.")
    lgipaw_reconstruction: bool = Field(False, description="Set it to .true. to generate pseudo-potentials containing the additional info required for reconstruction of all-electron orbitals, used by GIPAW. You will typically need to specify additional projectors beyond those used in the generation of pseudo-potentials. You should also specify")
    use_paw_as_gipaw: bool = Field(False, description="When generating a PAW dataset, setting this option to .true. will save the core all-electron wavefunctions to the UPF file. The GIPAW reconstruction to be performed using the PAW data and projectors for the valence wavefunctions.  In the default case, the GIPAW valence wavefunction and projectors are independent from the PAW ones and must be then specified as explained above in lgipaw_reconstruction.  Setting this to .true. always implies")
    author: str = Field(" 'anonymous'
         ", description="Name of the author.")
    file_chi: str = Field(" ' '
         ", description="file containing output PP chi functions")
    file_beta: str = Field(" ' '
         ", description="file containing output PP beta functions")
    file_qvan: str = Field(" ' '
         ", description="file containing output PP qvan functions")
    file_screen: str = Field(" ' '
         ", description="file containing output screening potential")
    file_core: str = Field(" ' '
         ", description="file containing output total and core charge")
    file_wfcaegen: str = Field(" ' '
         ", description="file with the all-electron wfc for generation")
    file_wfcncgen: str = Field(" ' '
         ", description="file with the norm-conserving wfc for generation")
    file_wfcusgen: str = Field(" ' '
         ", description="file with the ultra-soft wfc for generation")
    nconf: int = Field( 1
         , description="the number of configurations to be tested. For")
    file_pseudo: str = Field(" ' '
         ", description="File containing the PP.  * If the file name contains  '.upf' or '.UPF', the file is assumed to be in UPF format;  * else if the file name contains '.rrkj3' or '.RRKJ3', the old RRKJ format is first tried;  * otherwise, the old NC format is read.")
    rm: float = Field( 30 a.u.
         , description="Radius of the box used with spherical Bessel functions.")
    frozen_core: bool = Field(False, description="If .true. only the core wavefunctions of the first configuration are calculated. The eigenvalues, orbitals and energies of the other configurations are calculated with the core of the first configuration. The first configuration must be spin-unpolarized.")
    rcutv: float = Field( -1.0
         , description="Cutoff distance (CUT) for the inclusion of LDA-1/2 potential. Needed (mandatory) only if")
