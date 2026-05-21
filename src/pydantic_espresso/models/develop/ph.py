"""Pydantic model for the input of `ph.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, field_validator

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class InputphNamelist(Namelist):
    """Pydantic model for the `INPUTPH` namelist."""

    @field_validator("verbosity", mode="before")
    @classmethod
    def map_verbosity(cls, v: str) -> str:
        """Map equivalent values for `verbosity` onto a canonical value."""
        mapping = {"debug": "high", "medium": "high", "default": "low", "minimal": "low"}
        return mapping.get(v, v)

    outdir: Path | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "ESPRESSO_TMPDIR is set", "value": "from_environment"},
                {"when": None, "value": "'./'"},
            ],
        },
        description=(
            "Directory containing input, output, and scratch files; must be the same as specified "
            "in the calculation of the unperturbed system."
        ),
    )
    prefix: str = Field(
        "pwscf",
        description=(
            "Prepended to input/output filenames; must be the same used in the calculation of "
            "unperturbed system."
        ),
    )
    niter_ph: int | None = Field(
        None,
        json_schema_extra={"default_ref": ""},
        description=(
            "Maximum number of iterations in a scf step. If you want more than 100, edit variable "
            "'maxter' in PH/phcom.f90"
        ),
    )
    tr2_ph: float = Field(1e-12, description="Threshold for self-consistency.")
    alpha_mix: list[float] | None = Field(
        None,
        description=(
            "Mixing factor (for each iteration) for updating the scf potential:  vnew(in) = "
            "alpha_mix*vold(out) + (1-alpha_mix)*vold(in)"
        ),
    )
    nmix_ph: int = Field(
        4,
        description=(
            "Number of iterations used in potential mixing. Using a larger value (8~20) can "
            "significantly speed up convergence, at the cost of using more memory."
        ),
    )
    verbosity: Literal["high", "low"] = Field("low", description="Options are:")
    reduce_io: bool = Field(
        False,
        description=(
            "Reduce I/O to the strict minimum.  BEWARE: If the input flag reduce_io=.true. was "
            "used, it is not allowed to restart from an interrupted run."
        ),
    )
    max_seconds: Annotated[float, Quantity(units="s", dimensionality="time")] = Field(
        1.0e7, description="Maximum allowed run time before the job stops smoothly."
    )
    dftd3_hess: str | None = Field(
        None,
        json_schema_extra={"default_expr": "prefix // '.hess'"},
        description=(
            "File where the D3 dispersion hessian matrix is read. Set to 'automatic.hess' to "
            "enable automatic mode (experimental). In this mode, D3 Hessian is computed if "
            "'automatic.hess' file is missing."
        ),
    )
    fildyn: str = Field("matdyn", description="File where the dynamical matrix is written.")
    fildrho: str | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "lraman .or. elop .or. drho_star%open .or. lmultipole", "value": "'drho'"},
                {"when": None, "value": "' '"},
            ],
        },
        description=(
            "File where the charge density responses are written. Note that the file will actually "
            "be saved as ${outdir}/_ph0/${prefix}.${fildrho}1 where  ${outdir}, ${prefix} and "
            "${fildrho} are the values of the corresponding input variables"
        ),
    )
    fildvscf: str | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "elph_mat .or. dvscf_star%open .or. lmultipole", "value": "'dvscf'"},
                {"when": None, "value": "' '"},
            ],
        },
        description=(
            "File where the the potential variation is written (for later use in electron-phonon "
            "calculation, see also fildrho)."
        ),
    )
    epsil: bool = Field(
        False,
        description=(
            "If .true. in a q=0 calculation for a non metal the macroscopic dielectric constant of "
            "the system is computed. Do not set epsil to .true. if you have a metallic system or "
            "q/=0: the code will complain and stop.  Note: the input value of epsil will be "
            "ignored if ldisp=.true. (the code will automatically set epsil to .false. for metals, "
            "to .true. for insulators: see routine PHonon/PH/prepare_q.f90)."
        ),
    )
    lrpa: bool = Field(
        False,
        description=(
            "If .true. the dielectric constant is calculated at the RPA level with DV_xc=0."
        ),
    )
    lnoloc: bool = Field(
        False,
        description=(
            "If .true. the dielectric constant is calculated without local fields, i.e. by setting "
            "DV_H=0 and DV_xc=0."
        ),
    )
    trans: bool = Field(
        True,
        description=(
            "If .false. the phonons are not computed. If trans .and. epsil are both .true., the "
            "effective charges are calculated. If ldisp is .true., trans=.false. is overridden "
            "(except for the case of electron-phonon calculations)"
        ),
    )
    lraman: bool = Field(
        False,
        description=(
            "If .true. calculate non-resonant Raman coefficients using second-order response as "
            "in: M. Lazzeri and F. Mauri, PRL 90, 036401 (2003) "
            "(https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.90.036401)."
        ),
    )
    lmultipole: bool = Field(
        False,
        description=(
            "If .true. prints the induced density and potentials in fildrho and fildvscf. To "
            "extract multipoles and the finite-q dielectric function, multiple finite-q "
            "calculations need to be performed (see test-suite/ph_multipole, where multipole.py "
            "manages the flow of the calculations as described in test-suite/run-ph.sh). N.B.:  "
            "works only for 3d systems."
        ),
    )
    eth_rps: float = Field(1.0e-9, description="Threshold for calculation of  Pc R |psi>.")
    eth_ns: float = Field(1.0e-12, description="Threshold for non-scf wavefunction calculation.")
    dek: float = Field(1.0e-3, description="Delta_xk used for wavefunction derivation wrt k.")
    recover: bool = Field(False, description="If .true. restart from an interrupted run.")
    low_directory_check: bool = Field(
        False,
        description=(
            "If .true. search in the phsave directory only the quantities requested in input."
        ),
    )
    only_init: bool = Field(
        False,
        description=(
            "If .true. only the bands and other initialization quantities are calculated. (used "
            "for GRID parallelization)"
        ),
    )
    qplot: bool = Field(False, description="If .true. a list of q points is read from input.")
    q2d: bool = Field(
        False,
        description=(
            "If .true. three q points and relative weights are read from input. The three q points "
            "define the rectangle q(:,1) + l (q(:,2)-q(:,1)) + m (q(:,3)-q(:,1)) where 0< l,m < 1. "
            "The weights are integer and those of points two and three are the number of points in "
            "the two directions."
        ),
    )
    q_in_band_form: bool = Field(
        False,
        description=(
            "This flag is used only when qplot is .true. and q2d is .false.. When .true. each "
            "couple of q points q(:,i+1) and q(:,i) define the line from q(:,i) to q(:,i+1) and nq "
            "points are generated along that line. nq is the weigth of q(:,i). When .false. only "
            "the list of q points given as input is calculated. The weights are not used."
        ),
    )
    electron_phonon: Literal[
        None, "simple", "interpolated", "lambda_tetra", "gamma_tetra", "epa", "ahc"
    ] = Field(
        None,
        description=(
            "Options are:  For metals only, requires gaussian smearing (except for 'ahc').  If "
            "trans=.true., the lambdas are calculated in the same run, using the same k-point grid "
            "for phonons and lambdas. If trans=.false., the lambdas are calculated using "
            "previously saved DeltaVscf in fildvscf, previously saved dynamical matrix, and the "
            "present punch file. This allows the use of a different (larger) k-point grid."
        ),
    )
    el_ph_nsigma: int = Field(
        10,
        description=(
            "The number of double-delta smearing values used in an electron-phonon coupling "
            "calculation."
        ),
    )
    el_ph_sigma: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.02,
        description=(
            "The spacing between double-delta smearing values used in an electron-phonon coupling "
            "calculation."
        ),
    )
    ahc_dir: str | None = Field(
        None,
        json_schema_extra={"default_expr": "outdir // 'ahc_dir/'"},
        description="Directory where the output binary files are written.",
    )
    ahc_nbnd: int | None = Field(
        None, description="Number of bands for which the electron self-energy is to be computed."
    )
    ahc_nbndskip: int = Field(
        0,
        description=(
            "Number of bands to exclude when computing the self-energy. Self-energy is computed "
            "for bands with indices from ahc_nbndskip+1 to ahc_nbndskip+ahc_nbnd. "
            "ahc_nbndskip+ahc_nbnd cannot exceed nbnd of the preceding SCF or NSCF calculation."
        ),
    )
    skip_upper: bool = Field(
        False,
        description=(
            "If .true., skip calculation of the upper Fan self-energy, which involves solving the "
            "Sternheimer equation."
        ),
    )
    lshift_q: bool = Field(
        False,
        description=(
            "Use a wave-vector grid displaced by half a grid step in each direction - meaningful "
            "only when ldisp is .true. When this option is set, the q2r.x code cannot be used."
        ),
    )
    zeu: bool | None = Field(
        None,
        json_schema_extra={"default_ref": ""},
        description=(
            "If .true. in a q=0 calculation for a non metal the effective charges are computed "
            "from the dielectric response. This is the default algorithm. If epsil=.true. and "
            "zeu=.false. only the dielectric tensor is calculated."
        ),
    )
    zue: bool = Field(
        False,
        description=(
            "If .true. in a q=0 calculation for a non metal the effective charges are computed "
            "from the phonon density responses. This is an alternative algorithm, different from "
            "the default one (if trans .and. epsil ) The results should be the same within "
            "numerical noise."
        ),
    )
    elop: bool = Field(False, description="If .true. calculate electro-optic tensor.")
    fpol: bool = Field(
        False,
        description=(
            "If .true. calculate dynamic polarizabilities Requires epsil=.true. ( experimental "
            "stage: see example09 for calculation of methane )."
        ),
    )
    ldisp: bool = Field(
        False,
        description=(
            "If .true. the run calculates phonons for a grid of q-points specified by nq1, nq2, "
            "nq3 - for direct calculation of the entire phonon dispersion."
        ),
    )
    nogg: bool = Field(
        False,
        description=(
            "If .true. disable the 'gamma_gamma' trick used to speed up calculations at q=0 "
            "(phonon wavevector) if the sum over the Brillouin Zone includes k=0 only. The "
            "gamma_gamma trick exploits symmetry and acoustic sum rule to reduce the number of "
            "linear response calculations to the strict minimum, as it is done in code phcg.x."
        ),
    )
    asr: bool = Field(
        False,
        description=(
            "Apply Acoustic Sum Rule to dynamical matrix, effective charges Works only in "
            "conjunction with 'gamma_gamma' tricks (see above)"
        ),
    )
    ldiag: bool = Field(
        False,
        description=(
            "If .true. forces the diagonalization of the dynamical matrix also when only a part of "
            "the dynamical matrix has been calculated. It is used together with start_irr and "
            "last_irr. If all modes corresponding to a given irreducible representation have been "
            "calculated, the phonon frequencies of that representation are correct. The others are "
            "zero or wrong. Use with care."
        ),
    )
    lqdir: bool = Field(
        False,
        description=(
            "If .true. ph.x creates inside outdir a separate subdirectory for each q vector. The "
            "flag is set to .true. when ldisp=.true. and fildvscf /= ' ' or when an "
            "electron-phonon calculation is performed. The induced potential is saved separately "
            "for each q inside the subdirectories."
        ),
    )
    search_sym: bool = Field(
        True, description="Set it to .false. if you want to disable the mode symmetry analysis."
    )
    nq1: int | None = Field(None, description="")
    nq2: int | None = Field(None, description="")
    nq3: int | None = Field(None, description="")
    nk1: int | None = Field(None, description="")
    nk2: int | None = Field(None, description="")
    nk3: int | None = Field(None, description="")
    k1: int | None = Field(None, description="")
    k2: int | None = Field(None, description="")
    k3: int | None = Field(None, description="")
    diagonalization: Literal["david", "cg", "direct"] = Field(
        "david", description="Diagonalization method for the non-SCF calculations."
    )
    read_dns_bare: bool = Field(
        False,
        description=(
            "If .true. the PH code tries to read three files in the DFPT+U calculation: dns_orth, "
            "dns_bare, d2ns_bare. dns_orth and dns_bare are the first-order variations of the "
            "occupation matrix, while d2ns_bare is the second-order variation of the occupation "
            "matrix. These matrices are computed only once during the DFPT+U calculation. However, "
            "their calculation (especially of d2ns_bare) is computationally expensive, this is why "
            "they are written to file and then can be read (e.g. for restart) in order to save "
            "time."
        ),
    )
    ldvscf_interpolate: bool = Field(
        False,
        description=(
            "If .true., use Fourier interpolation of phonon potential to compute the induced part "
            "of phonon potential at each q point. Results of a dvscf_q2r.x run is needed. Requires "
            "trans = .false.."
        ),
    )
    wpot_dir: str | None = Field(
        None,
        json_schema_extra={"default_expr": "outdir // 'w_pot/'"},
        description=(
            "Directory where the w_pot binary files are written. Must be the same with wpot_dir "
            "used in dvscf_q2r.x. The real space potential files are stored in wpot_dir with names "
            "${prefix}.wpot.irc${irc}//'1'."
        ),
    )
    do_long_range: bool = Field(
        False,
        description=(
            "If .true., add the long-range part of the potential to the Fourier interpolated "
            "potential as in: S. Ponce et al, J. Chem. Phys. 143, 102813 (2015). Reads dielectric "
            "matrix and Born effective charges from the ${wpot_dir}/tensors.dat file, written in "
            "dvscf_q2r.x. Currently, only the dipole (Frohlich) part is implemented. The "
            "quadrupole part is not implemented."
        ),
    )
    do_charge_neutral: bool = Field(
        False,
        description=(
            "If .true., impose charge neutrality on the Born effective charges. Used only if "
            "do_long_range = .true.."
        ),
    )
    start_irr: int = Field(
        1,
        description=(
            "Perform calculations only from start_irr to last_irr irreducible representations.  "
            "IMPORTANT: * start_irr must be <= 3*nat * do not specify nat_todo together with "
            "start_irr, last_irr"
        ),
    )
    last_irr: int | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "not specified", "value": "3*nat"},
                {"when": None, "value": "-1000"},
            ],
        },
        description=(
            "Perform calculations only from start_irr to last_irr irreducible representations.  "
            "IMPORTANT: * start_irr must be <= 3*nat * do not specify nat_todo together with "
            "start_irr, last_irr"
        ),
    )
    nat_todo: int = Field(
        0,
        description=(
            "The default value 0 means that all atoms are displaced. Choose the subset of atoms to "
            "be used in the linear response calculation: nat_todo atoms, specified in input (see "
            "below) are displaced. Can be used to estimate modes for a molecule adsorbed over a "
            "surface without performing a full fledged calculation. Use with care, at your own "
            "risk, and be aware that this is an approximation and may not work. IMPORTANT: * "
            "nat_todo <= nat * if linear-response is calculated for a given atom, it should also "
            "be done for all symmetry-equivalent atoms, or else you will get incorrect results"
        ),
    )
    modenum: int = Field(
        0,
        description=(
            "For single-mode phonon calculation : modenum is the index of the irreducible "
            "representation (irrep) into which the reducible representation formed by the 3*nat "
            "atomic displacements are decomposed in order to perform the phonon calculation. Note "
            "that a single-mode calculation will not give you the frequency of a single phonon "
            "mode: in general, the selected 'modenum' is not an eigenvector. What you get on "
            "output is a column of the dynamical matrix."
        ),
    )
    start_q: int = Field(
        1,
        description=(
            "Used only when ldisp=.true.. Computes only the q points from start_q to last_q.  "
            "IMPORTANT: * start_q must be <= nqs (number of q points found) * do not specify "
            "nat_todo together with start_q, last_q"
        ),
    )
    last_q: int | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "not specified", "value": "number of q points (nqs)"},
                {"when": None, "value": "-1000"},
            ],
        },
        description=(
            "Used only when ldisp=.true.. Computes only the q points from start_q to last_q.  "
            "IMPORTANT * last_q must be <= nqs (number of q points) * do not specify nat_todo "
            "together with start_q, last_q"
        ),
    )
    amass: Annotated[list[float] | None, Quantity(units="amu", dimensionality="mass")] = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=(
            "Atomic mass of each atomic type. If not specified, masses are read from data file. "
            "(start = 1, end = ntyp)"
        ),
    )


class PHEspressoInput(EspressoInput):
    """Pydantic model for the input of `ph.x`."""

    inputph: InputphNamelist = Field(default_factory=lambda: InputphNamelist())
