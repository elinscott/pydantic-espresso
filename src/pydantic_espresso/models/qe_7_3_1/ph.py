"""Pydantic model for the input of `ph.x` version `qe-7.3.1`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputphNamelist(Namelist):
    """Pydantic model for the `Inputph` namelist."""

    @field_validator("verbosity", mode="before")
    def map_verbosity(cls, v: str) -> str:
        """Map equivalent values for verbosity to the same string so that comparisons work as expected."""
        mapping = {
            "debug": "debug",
            "high": "debug",
            "medium": "debug",
            "low": "low",
            "default": "low",
            "minimal": "low",
        }
        return mapping.get(v, v)

    outdir: Path = Field(
        Path("value of the"),
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
    nmix_ph: int = Field(
        4,
        description="Number of iterations used in potential mixing. Using a larger value (8~20) can significantly speed up convergence, at the cost of using more memory.",
    )
    verbosity: Literal["debug", "low"] = Field("low", description="Options are:")
    reduce_io: bool = Field(
        False,
        description="Reduce I/O to the strict minimum.  BEWARE: If the input flag reduce_io=.true. was used, it is not allowed to restart from an interrupted run.",
    )
    max_seconds: float = Field(
        1.0e7, description="Maximum allowed run time before the job stops smoothly."
    )
    dftd3_hess: str = Field(
        "prefix.hess",
        description="File where the D3 dispersion hessian matrix is read. Set to 'automatic.hess' to enable automatic mode (experimental). In this mode, D3 Hessian is computed if 'automatic.hess' file is missing.",
    )
    fildyn: str = Field("matdyn", description="File where the dynamical matrix is written.")
    fildrho: str | None = Field(
        None,
        description="File where the charge density responses are written. Note that the file will actually be saved as ${outdir}/_ph0/${prefix}.${fildrho}1 where  ${outdir}, ${prefix} and ${fildrho} are the values of the corresponding input variables",
    )
    fildvscf: str | None = Field(
        None,
        description="File where the the potential variation is written (for later use in electron-phonon calculation, see also fildrho).",
    )
    epsil: bool = Field(
        False,
        description="If .true. in a q=0 calculation for a non metal the macroscopic dielectric constant of the system is computed. Do not set epsil to .true. if you have a metallic system or q/=0: the code will complain and stop.  Note: the input value of epsil will be ignored if ldisp=.true. (the code will automatically set epsil to .false. for metals, to .true. for insulators: see routine PHonon/PH/prepare_q.f90).",
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
        description="If .false. the phonons are not computed. If trans .and. epsil are both .true., the effective charges are calculated. If ldisp is .true., trans=.false. is overridden (except for the case of electron-phonon calculations)",
    )
    lraman: bool = Field(
        False,
        description="If .true. calculate non-resonant Raman coefficients using second-order response as in: M. Lazzeri and F. Mauri, PRL 90, 036401 (2003) (https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.90.036401).",
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
    electron_phonon: Literal[
        None, "simple", "interpolated", "lambda_tetra", "gamma_tetra", "epa", "ahc"
    ] = Field(
        None,
        description="Options are:  For metals only, requires gaussian smearing (except for 'ahc').  If trans=.true., the lambdas are calculated in the same run, using the same k-point grid for phonons and lambdas. If trans=.false., the lambdas are calculated using previously saved DeltaVscf in fildvscf, previously saved dynamical matrix, and the present punch file. This allows the use of a different (larger) k-point grid.",
    )
    el_ph_nsigma: int = Field(
        10,
        description="The number of double-delta smearing values used in an electron-phonon coupling calculation.",
    )
    el_ph_sigma: float = Field(
        0.02,
        description="The spacing between double-delta smearing values used in an electron-phonon coupling calculation.",
    )
    lshift_q: bool = Field(
        False,
        description="Use a wave-vector grid displaced by half a grid step in each direction - meaningful only when ldisp is .true. When this option is set, the q2r.x code cannot be used.",
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
        description="If .true. disable the 'gamma_gamma' trick used to speed up calculations at q=0 (phonon wavevector) if the sum over the Brillouin Zone includes k=0 only. The gamma_gamma trick exploits symmetry and acoustic sum rule to reduce the number of linear response calculations to the strict minimum, as it is done in code phcg.x.",
    )
    asr: bool = Field(
        False,
        description="Apply Acoustic Sum Rule to dynamical matrix, effective charges Works only in conjunction with 'gamma_gamma' tricks (see above)",
    )
    ldiag: bool = Field(
        False,
        description="If .true. forces the diagonalization of the dynamical matrix also when only a part of the dynamical matrix has been calculated. It is used together with start_irr and last_irr. If all modes corresponding to a given irreducible representation have been calculated, the phonon frequencies of that representation are correct. The others are zero or wrong. Use with care.",
    )
    lqdir: bool = Field(
        False,
        description="If .true. ph.x creates inside outdir a separate subdirectory for each q vector. The flag is set to .true. when ldisp=.true. and fildvscf /= ' ' or when an electron-phonon calculation is performed. The induced potential is saved separately for each q inside the subdirectories.",
    )
    search_sym: bool = Field(
        True, description="Set it to .false. if you want to disable the mode symmetry analysis."
    )
    diagonalization: Literal["david", "cg"] = Field(
        "david", description="Diagonalization method for the non-SCF calculations."
    )
    read_dns_bare: bool = Field(
        False,
        description="If .true. the PH code tries to read three files in the DFPT+U calculation: dns_orth, dns_bare, d2ns_bare. dns_orth and dns_bare are the first-order variations of the occupation matrix, while d2ns_bare is the second-order variation of the occupation matrix. These matrices are computed only once during the DFPT+U calculation. However, their calculation (especially of d2ns_bare) is computationally expensive, this is why they are written to file and then can be read (e.g. for restart) in order to save time.",
    )
    ldvscf_interpolate: bool = Field(
        False,
        description="If .true., use Fourier interpolation of phonon potential to compute the induced part of phonon potential at each q point. Results of a dvscf_q2r.x run is needed. Requires trans = .false..",
    )


class PHEspressoInput(EspressoInput):
    """Pydantic model for the input of `ph.x.`"""

    inputph: InputphNamelist = Field(default_factory=lambda: InputphNamelist())
