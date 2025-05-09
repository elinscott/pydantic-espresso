"""Pydantic model for the input of `ph.x` version `qe-5.1.2`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputphNamelist(Namelist):
    """Pydantic model for the `INPUTPH` namelist."""

    outdir: Path = Field(
        default_factory=get_tmp_dir,
        description="Directory containing input, output, and scratch files; must be the same as specified in the calculation of the unperturbed system.",
    )
    prefix: str = Field(
        "pwscf",
        description="Prepended to input/output filenames; must be the same used in the calculation of unperturbed system.",
    )
    niter_ph: int | None = Field(
        None,
        description="Maximum number of iterations in a scf step. If you want more than 100, edit variable 'maxter' in PH/phcom.f90",
    )
    tr2_ph: float = Field(1e-12, description="Threshold for self-consistency.")
    alpha_mix: list[float] | None = Field(
        None,
        description="Mixing factor (for each iteration) for updating the scf potential:  vnew(in) = alpha_mix*vold(out) + (1-alpha_mix)*vold(in)",
    )
    nmix_ph: int = Field(4, description="Number of iterations used in potential mixing.")
    verbosity: str = Field(
        "low",
        description="debug', 'high', 'medium'   = verbose output 'low', 'default', 'minimal' = short output",
    )
    reduce_io: bool = Field(False, description="Reduce I/O to the strict minimum.")
    max_seconds: float = Field(
        1.0e7, description="Maximum allowed run time before the job stops smoothly."
    )
    fildyn: str = Field("matdyn", description="File where the dynamical matrix is written.")
    fildrho: str | None = Field(
        None, description="File where the charge density responses are written."
    )
    fildvscf: str | None = Field(
        None,
        description="File where the the potential variation is written (for later use in electron-phonon calculation).",
    )
    epsil: bool = Field(
        False,
        description="If .true. in a q=0 calculation for a non metal the macroscopic dielectric constant of the system is computed. Do not set epsil to .true. if you have a metallic system or q/=0: the code will complain and stop.",
    )
    lrpa: bool = Field(
        False,
        description="If .true. the dielectric constant is calculated at the RPA level with DV_xc=0.",
    )
    lnoloc: bool = Field(
        False,
        description="If .true. the dielectric constant is calculated without local fields, i.e. by setting DV_H=0 and DV_xc=0.",
    )
    trans: bool = Field(
        True,
        description="If .true. the phonons are computed. If trans .and. epsil are .true. effective charges are calculated.",
    )
    lraman: bool = Field(
        False,
        description="If .true. calculate non-resonant Raman coefficients using second-order response as in: M. Lazzeri and F. Mauri, Phys. Rev. Lett. 90, 036401 (2003).",
    )
    recover: bool = Field(False, description="If .true. restart from an interrupted run.")
    low_directory_check: bool = Field(
        False,
        description="If .true. search in the phsave directory only the quantities requested in input.",
    )
    only_init: bool = Field(
        False,
        description="If .true. only the bands and other initialization quantities are calculated. (used for GRID parallelization)",
    )
    qplot: bool = Field(False, description="If .true. a list of q points is read from input.")
    q2d: bool = Field(
        False,
        description="If .true. three q points and relative weights are read from input. The three q points define the rectangle q(:,1) + l (q(:,2)-q(:,1)) + m (q(:,3)-q(:,1)) where 0< l,m < 1. The weights are integer and those of points two and three are the number of points in the two directions.",
    )
    q_in_band_form: bool = Field(
        False,
        description="This flag is used only when qplot is .true. and q2d is .false.. When .true. each couple of q points q(:,i+1) and q(:,i) define the line from q(:,i) to q(:,i+1) and nq points are generated along that line. nq is the weigth of q(:,i). When .false. only the list of q points given as input is calculated. The weights are not used.",
    )
    electron_phonon: str | None = Field(
        None,
        description="If equal to 'simple' electron-phonon lambda coefficients are computed for a given q and a grid of k-points specified by the variables nk1, nk2, nk3, k1, k2, k3.  If equal to 'interpolated' electron-phonon is calculated by interpolation over the Brillouin Zone as in M. Wierzbowska, et al. arXiv:cond-mat/0504077 (https://arxiv.org/abs/cond-mat/0504077)  For metals only, requires gaussian smearing.  If trans=.true., the lambdas are calculated in the same run, using the same k-point grid for phonons and lambdas. If trans=.false., the lambdas are calculated using previously saved DeltaVscf in fildvscf, previously saved dynamical matrix, and the present punch file. This allows the use of a different (larger) k-point grid.",
    )
    zeu: bool | None = Field(
        None,
        description="If .true. in a q=0 calculation for a non metal the effective charges are computed from the dielectric response. This is the default algorithm. If epsil=.true. and zeu=.false. only the dielectric tensor is calculated.",
    )
    zue: bool = Field(
        False,
        description="If .true. in a q=0 calculation for a non metal the effective charges are computed from the phonon density responses. This is an alternative algorithm, different from the default one (if trans .and. epsil ) The results should be the same within numerical noise.",
    )
    elop: bool = Field(False, description="If .true. calculate electro-optic tensor.")
    fpol: bool = Field(
        False,
        description="If .true. calculate dynamic polarizabilities Requires epsil=.true. ( experimental stage: see example09 for calculation of methane ).",
    )
    ldisp: bool = Field(
        False,
        description="If .true. the run calculates phonons for a grid of q-points specified by nq1, nq2, nq3 - for direct calculation of the entire phonon dispersion.",
    )
    nogg: bool = Field(
        False,
        description="If .true. disable the 'gamma_gamma' trick used to speed up calculations at q=0 (phonon wavevector) if the sum over the Brillouin Zone includes k=0 only. The gamma_gamma trick exploits symmetry and acoustic sum rule to reduce the number of linear response calculations to the strict minimum, as it is done in code phcg.x. This option MUST BE USED if a run with ph.x is to be followed by a run with d3.x for third-order terms calculation.",
    )
    ldiag: bool = Field(
        False,
        description="If .true. forces the diagonalization of the dynamical matrix also when only a part of the dynamical matrix has been calculated. It is used together with start_irr and last_irr. If all modes corresponding to a given irreducible representation have been calculated, the phonon frequencies of that representation are correct. The others are zero or wrong. Use with care.",
    )
    lqdir: bool = Field(
        False,
        description="If .true. ph.x creates inside outdir a separate subdirectory for each q vector. The flag is set to .true. when ldisp= .true. and fildvscf /= ' ' or when an electron-phonon calculation is performed. The induced potential is saved separately for each q inside the subdirectories.",
    )
    search_sym: bool = Field(
        True, description="Set it to .false. if you want to disable the mode symmetry analysis."
    )


class PHEspressoInput(EspressoInput):
    """Pydantic model for the input of `ph.x`"""

    inputph: InputphNamelist = Field(default_factory=lambda: InputphNamelist())
