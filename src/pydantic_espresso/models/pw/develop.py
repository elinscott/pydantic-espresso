"""Pydantic model for the input of `pw.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from textwrap import dedent
from typing import Annotated, Literal

from pydantic import Field, field_validator

from pydantic_espresso.base import EspressoInput
from pydantic_espresso.models.pw.cards.atomic_forces import AtomicForce
from pydantic_espresso.models.pw.cards.atomic_positions import AtomicPositionsCard
from pydantic_espresso.models.pw.cards.atomic_species import AtomicSpecies
from pydantic_espresso.models.pw.cards.atomic_velocities import AtomicVelocity
from pydantic_espresso.models.pw.cards.cell_parameters import CellParametersCard
from pydantic_espresso.models.pw.cards.constraints import Constraint
from pydantic_espresso.models.pw.cards.hubbard import HubbardCard
from pydantic_espresso.models.pw.cards.k_points import KPointsCard
from pydantic_espresso.models.pw.cards.occupations import PositiveFloat0to1, PositiveFloat0to2
from pydantic_espresso.models.pw.cards.solvents import SolventsCard, SolventsLRCard
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class ControlNamelist(Namelist):
    """Pydantic model for the `CONTROL` namelist."""

    @field_validator("verbosity", mode="before")
    @classmethod
    def map_verbosity(cls, v: str) -> str:
        """Map equivalent values for `verbosity` onto a canonical value."""
        mapping = {"medium": "high", "debug": "high", "default": "low", "minimal": "low"}
        return mapping.get(v, v)

    calculation: Literal["scf", "nscf", "bands", "relax", "md", "vc-relax", "vc-md"] = Field(
        "scf",
        description=dedent(
            """\
            A string describing the task to be performed. Options are:  (vc = variable-cell)."""
        ),
    )
    title: str | None = Field(None, description="reprinted on output.")
    verbosity: Literal["high", "low"] = Field(
        "low", description="Currently two verbosity levels are implemented:"
    )
    restart_mode: Literal["from_scratch", "restart"] = Field(
        "from_scratch",
        description=dedent(
            """\
            Available options are:
            - 'from_scratch': From scratch. This is the normal way to perform a PWscf calculation.
            - 'restart': From previous interrupted run. Use this switch only if you want to
              continue, using the same number of processors and parallelization, an interrupted
              calculation. Do not use to start a new one, or to perform a non-scf calculations.
              Works only if the calculation was cleanly stopped using variable max_seconds, or by
              user request with an 'exit file' (i.e.: create a file 'prefix'.EXIT, in directory
              'outdir'; see variables prefix, outdir). The default for startingwfc and startingpot
              is set to 'file'."""
        ),
    )
    nstep: int | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "calculation=='scf' || calculation=='nscf' || calculation=='bands'",
                    "value": "1",
                },
                {"when": None, "value": "50"},
            ],
        },
        description=dedent(
            """\
            number of molecular-dynamics or structural optimization steps performed in this run. If
            set to 0, the code performs a quick 'dry run', stopping just after initialization. This
            is useful to check for input correctness and to have the summary printed. NOTE: in MD
            calculations, the code will perform 'nstep' steps even if restarting from a previously
            interrupted calculation."""
        ),
    )
    iprint: int = Field(
        100000,
        description=dedent(
            """\
            When calculation == 'md' (molecular dynamics) trajectory is written every iprint md
            steps. With the default value, output is written only at convergence."""
        ),
    )
    tstress: bool = Field(
        False,
        description=dedent(
            """\
            calculate stress. It is set to .TRUE. automatically if calculation == 'vc-md' or
            'vc-relax"""
        ),
    )
    tprnfor: bool = Field(
        False,
        description=dedent(
            """\
            calculate forces. It is set to .TRUE. automatically if calculation ==
            'relax','md','vc-md"""
        ),
    )
    dt: Annotated[
        float, Quantity(units="bohr electron_mass^1/2 Ry^-1/2", dimensionality="time")
    ] = Field(
        20.0,
        description=dedent(
            """\
            time step for molecular dynamics, in Rydberg atomic units (1 a.u.=4.8378 * 10^-17 s :
            beware, the CP code uses Hartree atomic units, half that much!!!)"""
        ),
    )
    outdir: Path | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "ESPRESSO_TMPDIR is set", "value": "from_environment"},
                {"when": None, "value": "./"},
            ],
        },
        description="input, temporary, output files are found in this directory, see also wfcdir",
    )
    wfcdir: Path | None = Field(
        None,
        json_schema_extra={"default_ref": "outdir"},
        description=dedent(
            """\
            This directory specifies where to store files generated by each processor (*.wfc{N},
            *.igk{N}, etc.). Useful for machines without a parallel file system: set wfcdir to a
            local file system, while outdir should be a parallel or network file system, visible to
            all processors. Beware: in order to restart from interrupted runs, or to perform
            further calculations using the produced data files, you may need to copy files to
            outdir. Works only for pw.x."""
        ),
    )
    prefix: str = Field(
        "pwscf", description="prepended to input/output filenames: prefix.wfc, prefix.rho, etc."
    )
    max_seconds: Annotated[float, Quantity(units="s", dimensionality="time")] = Field(
        10000000.0,
        description=dedent(
            """\
            Jobs stops after max_seconds CPU time. Use this option in conjunction with option
            restart_mode if you need to split a job too long to complete into shorter jobs that fit
            into your batch queues. The default value (10000000 s, about 150 days) effectively
            means that no time limit is imposed."""
        ),
    )
    etot_conv_thr: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.0001,
        description=dedent(
            """\
            Convergence threshold on total energy (a.u) for ionic minimization: the convergence
            criterion is satisfied when the total energy changes less than etot_conv_thr between
            two consecutive scf steps. Note that etot_conv_thr is extensive, like the total energy.
            See also forc_conv_thr - both criteria must be satisfied"""
        ),
    )
    forc_conv_thr: Annotated[
        float, Quantity(units="Ry bohr^-1", dimensionality="energy length^-1")
    ] = Field(
        0.001,
        description=dedent(
            """\
            Convergence threshold on forces for ionic minimization: the convergence criterion is
            satisfied when all components of all forces are smaller than forc_conv_thr. See also
            etot_conv_thr - both criteria must be satisfied"""
        ),
    )
    disk_io: Literal["default", "high", "medium", "low", "nowf", "minimal", "none"] = Field(
        "default",
        description=dedent(
            """\
            Specifies the amount of disk I/O activity: (only for binary files and xml data file in
            data directory; other files printed at each molecular dynamics / structural
            optimization step are not controlled by this option )  Default is 'low' for the scf
            case, 'medium' otherwise. Note that the needed RAM increases as disk I/O decreases
            - 'default': the amount of disk I/O is chosen automatically depending on the kind of
              calculation.
            - 'high': save charge to disk at each SCF step, keep wavefunctions on disk (in
              'distributed' format), save mixing data as well. Do not use this option unless you
              have a good reason! It is no longer needed to specify 'high' in order to be able to
              restart from an interrupted calculation (see restart_mode).
            - 'medium': save charge to disk at each SCF step, keep wavefunctions on disk only if
              more than one k-point, per process is present, otherwise keep them in memory; save
              them to disk only at the end (in 'portable' format).
            - 'low': save charge to disk at each SCF step, keep wavefunctions in memory (for all
              k-points), save them to disk only at the end (in 'portable' format). Reduces I/O but
              increases memory wrt the previous cases.
            - 'nowf': save to disk only the xml data file and the charge density at convergence,
              never save wavefunctions. Restarting from an interrupted calculation is not possible
              with this option.
            - 'minimal': save to disk only the xml data file at convergence.
            - 'none': do not save anything to disk."""
        ),
    )
    pseudo_dir: Path | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "ESPRESSO_PSEUDO is set", "value": "from_environment"},
                {"when": None, "value": "$HOME/espresso/pseudo/"},
            ],
        },
        description="directory containing pseudopotential files",
    )
    tefield: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE. a saw-like potential simulating an electric field is added to the bare ionic
            potential. See variables edir, eamp, emaxpos, eopreg for the form and size of the added
            potential."""
        ),
    )
    dipfield: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE. and tefield==.TRUE. a dipole correction is also added to the bare ionic
            potential - implements the recipe of L. Bengtsson, PRB 59, 12301 (1999)
            (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.59.12301). See variables edir,
            emaxpos, eopreg for the form of the correction. Must be used ONLY in a slab geometry,
            for surface calculations, with the discontinuity FALLING IN THE EMPTY SPACE."""
        ),
    )
    lelfield: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE. a homogeneous finite electric field described through the modern theory of
            the polarization is applied. This is different from tefield == .true. !"""
        ),
    )
    nberrycyc: int = Field(
        1,
        description=dedent(
            """\
            In the case of a finite electric field  ( lelfield == .TRUE. ) it defines the number of
            iterations for converging the wavefunctions in the electric field Hamiltonian, for each
            external iteration on the charge density"""
        ),
    )
    lorbm: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE. perform orbital magnetization calculation. If finite electric field is
            applied (lelfield==.true.) only Kubo terms are computed [for details see New J. Phys.
            12, 053032 (2010), doi:10.1088/1367-2630/12/5/053032
            (https://doi.org/10.1088/1367-2630/12/5/053032)].  The type of calculation is 'nscf'
            and should be performed on an automatically generated uniform grid of k points.  Works
            ONLY with norm-conserving pseudopotentials."""
        ),
    )
    lberry: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE. perform a Berry phase calculation. See the header of PW/src/bp_c_phase.f90
            for documentation."""
        ),
    )
    gdir: Literal[0, 1, 2, 3] = Field(
        0,
        description=dedent(
            """\
            For Berry phase calculation: direction of the k-point strings in reciprocal space. For
            calculations with finite electric fields (lelfield == .true.) this is the direction of
            the field. A value of 1, 2 or 3 is required when lberry == .true. or lelfield ==
            .true.; PW/src/setup.f90 raises an error otherwise.
            - '0': No Berry-phase or finite-field calculation requested (the value is unused).
            - '1': first reciprocal lattice vector.
            - '2': second reciprocal lattice vector.
            - '3': third reciprocal lattice vector."""
        ),
    )
    nppstr: int = Field(
        0,
        description=dedent(
            """\
            For Berry phase calculation: number of k-points to be calculated along each
            symmetry-reduced string. The same for calculation with finite electric fields
            (lelfield==.true.)."""
        ),
    )
    gate: bool = Field(
        False,
        description=dedent(
            """\
            In the case of charged cells (tot_charge .ne. 0) setting gate = .TRUE. represents the
            counter charge (i.e. -tot_charge) not by a homogeneous background charge but with a
            charged plate, which is placed at zgate (see below). Details of the gate potential can
            be found in T. Brumme, M. Calandra, F. Mauri; PRB 89, 245406 (2014)
            (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.89.245406). Note, that in
            systems which are not symmetric with respect to the plate, one needs to enable the
            dipole correction! (dipfield=.true.). Currently, symmetry can be used with gate=.true.
            but carefully check that no symmetry is included which maps z to -z even if in
            principle one could still use them for symmetric systems (i.e. no dipole correction).
            For nosym=.false. verbosity is set to 'high'. Note: this option was called 'monopole'
            in v6.0 and 6.1 of pw.x"""
        ),
    )
    twochem: bool = Field(
        False,
        description=dedent(
            """\
            IF .TRUE. , a two chemical potential calculation for the simulation of photoexcited
            systems is performed, constraining a fraction of the electrons in the conduction
            manifold. See G. Marini, M. Calandra; PRB 104, 144103 (2021)
            (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.104.144103). Note: requires
            occupations to be set to 'smearing'."""
        ),
    )
    lfcp: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE. perform a constant bias potential (constant-mu) calculation for a system with
            ESM method. See the header of PW/src/fcp_module.f90 for documentation. To perform the
            calculation, you must set a namelist FCP.  NB: - The total energy displayed in output
            includes the potentiostat contribution (-mu*N). - calculation must be 'relax' or 'md'.
            - assume_isolated = 'esm' and esm_bc = 'bc2' or 'bc3' must be set in SYSTEM namelist. -
            ESM-RISM is also supported (assume_isolated = 'esm' and esm_bc = 'bc1' and trism =
            .TRUE.). - ignore_wolfe is always .TRUE., for BFGS."""
        ),
    )
    trism: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE. perform a 3D-RISM-SCF calculation [for details see H.Sato et al., JCP 112,
            9463 (2000), doi:10.1063/1.481564 (https://doi.org/10.1063/1.481564)]. The solvent's
            distributions are calculated by 3D-RISM, though solute is treated as SCF. The charge
            density and the atomic positions are optimized, simultaneously with the solvents. To
            perform the calculation, you must set a namelist RISM and a card SOLVENTS.  If
            assume_isolated = 'esm' and esm_bc = 'bc1', Laue-RISM is calculated instead of 3D-RISM
            and coupled with ESM method (i.e. ESM-RISM). [for details see S.Nishihara and M.Otani,
            PRB 96, 115429 (2017)
            (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.96.115429)].  The default of
            mixing_beta is 0.2 for both 3D-RISM and Laue-RISM.  For structural relaxation with
            BFGS, ignore_wolfe is always .TRUE. ."""
        ),
    )


class SystemNamelist(Namelist):
    """Pydantic model for the `SYSTEM` namelist."""

    @field_validator("smearing", mode="before")
    @classmethod
    def map_smearing(cls, v: str) -> str:
        """Map equivalent values for `smearing` onto a canonical value."""
        mapping = {
            "gauss": "gaussian",
            "m-p": "methfessel-paxton",
            "mp": "methfessel-paxton",
            "cold": "marzari-vanderbilt",
            "m-v": "marzari-vanderbilt",
            "mv": "marzari-vanderbilt",
            "f-d": "fermi-dirac",
            "fd": "fermi-dirac",
        }
        return mapping.get(v, v)

    @field_validator("assume_isolated", mode="before")
    @classmethod
    def map_assume_isolated(cls, v: str) -> str:
        """Map equivalent values for `assume_isolated` onto a canonical value."""
        mapping = {
            "m-p": "makov-payne",
            "mp": "makov-payne",
            "m-t": "martyna-tuckerman",
            "mt": "martyna-tuckerman",
        }
        return mapping.get(v, v)

    @field_validator("vdw_corr", mode="before")
    @classmethod
    def map_vdw_corr(cls, v: str) -> str:
        """Map equivalent values for `vdw_corr` onto a canonical value."""
        mapping = {
            "Grimme-D2": "grimme-d2",
            "DFT-D": "grimme-d2",
            "dft-d": "grimme-d2",
            "Grimme-D3": "grimme-d3",
            "DFT-D3": "grimme-d3",
            "dft-d3": "grimme-d3",
            "TS": "tkatchenko-scheffler",
            "ts": "tkatchenko-scheffler",
            "ts-vdw": "tkatchenko-scheffler",
            "ts-vdW": "tkatchenko-scheffler",
            "MBD": "many-body-dispersion",
            "mbd": "many-body-dispersion",
            "mbd_vdw": "many-body-dispersion",
            "xdm": "XDM",
        }
        return mapping.get(v, v)

    ibrav: Literal[0, 1, 2, 3, -3, 4, 5, -5, 6, 7, 8, 9, -9, 91, 10, 11, 12, -12, 13, -13, 14] = (
        Field(
            ...,
            description=dedent(
                """\
                Bravais-lattice index. Optional only if space_group is set. If ibrav /= 0, specify
                EITHER [ celldm(1)-celldm(6) ] OR [ A, B, C, cosAB, cosAC, cosBC ] but NOT both.
                The lattice parameter 'alat' is set to alat = celldm(1) (in a.u.) or alat = A (in
                Angstrom); see below for the other parameters. For ibrav=0 specify the lattice
                vectors in CELL_PARAMETERS, optionally the lattice parameter alat = celldm(1) (in
                a.u.) or = A (in Angstrom). If not specified, the lattice parameter is taken from
                CELL_PARAMETERS IMPORTANT NOTICE 1: with ibrav=0 lattice vectors must be given with
                a sufficiently large number of digits and with the correct symmetry, or else
                symmetry detection may fail and strange problems may arise in symmetrization.
                IMPORTANT NOTICE 2: do not use celldm(1) or A as a.u. to Ang conversion factor, use
                the true lattice parameters or nothing, specify units in CELL_PARAMETERS and
                ATOMIC_POSITIONS  The accepted values of ibrav and the corresponding lattices (with
                the required celldm(2)-celldm(6), or equivalently b,c,cosbc,cosac,cosab) are listed
                below.
                - '0': free crystal axis provided in input: see card CELL_PARAMETERS.
                - '1': cubic P (sc) v1 = a(1,0,0),  v2 = a(0,1,0),  v3 = a(0,0,1).
                - '2': cubic F (fcc) v1 = (a/2)(-1,0,1),  v2 = (a/2)(0,1,1), v3 = (a/2)(-1,1,0).
                - '3': cubic I (bcc) v1 = (a/2)(1,1,1),  v2 = (a/2)(-1,1,1),  v3 = (a/2)(-1,-1,1).
                - '-3': cubic I (bcc), more symmetric axis: v1 = (a/2)(-1,1,1), v2 = (a/2)(1,-1,1),
                   v3 = (a/2)(1,1,-1).
                - '4': Hexagonal and Trigonal P        celldm(3)=c/a v1 = a(1,0,0),  v2 =
                  a(-1/2,sqrt(3)/2,0),  v3 = a(0,0,c/a).
                - '5': Trigonal R, 3fold axis c        celldm(4)=cos(gamma) The crystallographic
                  vectors form a three-fold star around the z-axis, the primitive cell is a simple
                  rhombohedron: v1 = a(tx,-ty,tz),   v2 = a(0,2ty,tz),   v3 = a(-tx,-ty,tz) where
                  c=cos(gamma) is the cosine of the angle gamma between any pair of
                  crystallographic vectors, tx, ty, tz are: tx=sqrt((1-c)/2), ty=sqrt((1-c)/6),
                  tz=sqrt((1+2c)/3).
                - '-5': Trigonal R, 3fold axis <111>    celldm(4)=cos(gamma) The crystallographic
                  vectors form a three-fold star around <111>. Defining a' = a/sqrt(3) : v1 = a'
                  (u,v,v),   v2 = a' (v,u,v),   v3 = a' (v,v,u) where u and v are defined as u = tz
                  - 2*sqrt(2)*ty,  v = tz + sqrt(2)*ty and tx, ty, tz as for case ibrav=5 Note: if
                  you prefer x,y,z as axis in the cubic limit, set  u = tz + 2*sqrt(2)*ty,  v = tz
                  - sqrt(2)*ty See also the note in Modules/latgen.f90.
                - '6': Tetragonal P (st)               celldm(3)=c/a v1 = a(1,0,0),  v2 = a(0,1,0),
                   v3 = a(0,0,c/a).
                - '7': Tetragonal I (bct)              celldm(3)=c/a v1=(a/2)(1,-1,c/a),
                  v2=(a/2)(1,1,c/a),  v3=(a/2)(-1,-1,c/a).
                - '8': Orthorhombic P                  celldm(2)=b/a, celldm(3)=c/a v1 = (a,0,0),
                  v2 = (0,b,0), v3 = (0,0,c).
                - '9': Orthorhombic base-centered(bco) celldm(2)=b/a, celldm(3)=c/a v1 = (a/2,
                  b/2,0),  v2 = (-a/2,b/2,0),  v3 = (0,0,c).
                - '-9': as 9, alternate description v1 = (a/2,-b/2,0),  v2 = (a/2, b/2,0),  v3 =
                  (0,0,c).
                - '91': Orthorhombic one-face base-centered A-type, celldm(2)=b/a, celldm(3)=c/a v1
                  = (a, 0, 0),  v2 = (0,b/2,-c/2),  v3 = (0,b/2,c/2).
                - '10': Orthorhombic face-centered      celldm(2)=b/a, celldm(3)=c/a v1 =
                  (a/2,0,c/2),  v2 = (a/2,b/2,0),  v3 = (0,b/2,c/2).
                - '11': Orthorhombic body-centered      celldm(2)=b/a, celldm(3)=c/a
                  v1=(a/2,b/2,c/2),  v2=(-a/2,b/2,c/2),  v3=(-a/2,-b/2,c/2).
                - '12': Monoclinic P, unique axis c     celldm(2)=b/a, celldm(3)=c/a,
                  celldm(4)=cos(ab) v1=(a,0,0), v2=(b*cos(gamma),b*sin(gamma),0),  v3 = (0,0,c)
                  where gamma is the angle between axis a and b.
                - '-12': Monoclinic P, unique axis b     celldm(2)=b/a, celldm(3)=c/a,
                  celldm(5)=cos(ac) v1 = (a,0,0), v2 = (0,b,0), v3 = (c*cos(beta),0,c*sin(beta))
                  where beta is the angle between axis a and c.
                - '13': Monoclinic base-centered (unique axis c) celldm(2)=b/a, celldm(3)=c/a,
                  celldm(4)=cos(gamma) v1 = (  a/2,         0,          -c/2), v2 = (b*cos(gamma),
                  b*sin(gamma), 0  ), v3 = (  a/2,         0,           c/2), where gamma=angle
                  between axis a and b projected on xy plane.
                - '-13': Monoclinic base-centered (unique axis b) celldm(2)=b/a, celldm(3)=c/a,
                  celldm(5)=cos(beta) v1 = (  a/2,       b/2,             0), v2 = ( -a/2,
                  b/2,             0), v3 = (c*cos(beta),   0,   c*sin(beta)), where beta=angle
                  between axis a and c projected on xz plane IMPORTANT NOTICE: until QE v.6.4.1,
                  axis for ibrav=-13 had a different definition: v1(old) =-v2(now), v2(old) =
                  v1(now).
                - '14': Triclinic                       celldm(2)= b/a, celldm(3)= c/a, celldm(4)=
                  cos(bc), celldm(5)= cos(ac), celldm(6)= cos(ab) v1 = (a, 0, 0), v2 =
                  (b*cos(gamma), b*sin(gamma), 0) v3 = (c*cos(beta),
                  c*(cos(alpha)-cos(beta)cos(gamma))/sin(gamma), c*sqrt( 1 +
                  2*cos(alpha)cos(beta)cos(gamma) - cos(alpha)^2-cos(beta)^2-cos(gamma)^2
                  )/sin(gamma) ) where alpha is the angle between axis b and c beta is the angle
                  between axis a and c gamma is the angle between axis a and b."""
            ),
        )
    )
    A: Annotated[float, Quantity(units="angstrom", dimensionality="length")] = Field(
        0.0,
        description=dedent(
            """\
            Traditional crystallographic constants:  a,b,c in ANGSTROM cosAB = cosine of the angle
            between axis a and b (gamma) cosAC = cosine of the angle between axis a and c (beta)
            cosBC = cosine of the angle between axis b and c (alpha)  The axis are chosen according
            to the value of ibrav. Specify either these OR celldm but NOT both. Only needed values
            (depending on ibrav) must be specified.  The lattice parameter alat = A (in ANGSTROM ).
             If ibrav == 0, only A is used if present, and cell vectors are read from card
            CELL_PARAMETERS."""
        ),
    )
    B: Annotated[float, Quantity(units="angstrom", dimensionality="length")] = Field(
        0.0,
        description=dedent(
            """\
            Traditional crystallographic constants:  a,b,c in ANGSTROM cosAB = cosine of the angle
            between axis a and b (gamma) cosAC = cosine of the angle between axis a and c (beta)
            cosBC = cosine of the angle between axis b and c (alpha)  The axis are chosen according
            to the value of ibrav. Specify either these OR celldm but NOT both. Only needed values
            (depending on ibrav) must be specified.  The lattice parameter alat = A (in ANGSTROM ).
             If ibrav == 0, only A is used if present, and cell vectors are read from card
            CELL_PARAMETERS."""
        ),
    )
    C: Annotated[float, Quantity(units="angstrom", dimensionality="length")] = Field(
        0.0,
        description=dedent(
            """\
            Traditional crystallographic constants:  a,b,c in ANGSTROM cosAB = cosine of the angle
            between axis a and b (gamma) cosAC = cosine of the angle between axis a and c (beta)
            cosBC = cosine of the angle between axis b and c (alpha)  The axis are chosen according
            to the value of ibrav. Specify either these OR celldm but NOT both. Only needed values
            (depending on ibrav) must be specified.  The lattice parameter alat = A (in ANGSTROM ).
             If ibrav == 0, only A is used if present, and cell vectors are read from card
            CELL_PARAMETERS."""
        ),
    )
    cosAB: float = Field(  # noqa: N815
        0.0,
        description=dedent(
            """\
            Traditional crystallographic constants:  a,b,c in ANGSTROM cosAB = cosine of the angle
            between axis a and b (gamma) cosAC = cosine of the angle between axis a and c (beta)
            cosBC = cosine of the angle between axis b and c (alpha)  The axis are chosen according
            to the value of ibrav. Specify either these OR celldm but NOT both. Only needed values
            (depending on ibrav) must be specified.  The lattice parameter alat = A (in ANGSTROM ).
             If ibrav == 0, only A is used if present, and cell vectors are read from card
            CELL_PARAMETERS."""
        ),
    )
    cosAC: float = Field(  # noqa: N815
        0.0,
        description=dedent(
            """\
            Traditional crystallographic constants:  a,b,c in ANGSTROM cosAB = cosine of the angle
            between axis a and b (gamma) cosAC = cosine of the angle between axis a and c (beta)
            cosBC = cosine of the angle between axis b and c (alpha)  The axis are chosen according
            to the value of ibrav. Specify either these OR celldm but NOT both. Only needed values
            (depending on ibrav) must be specified.  The lattice parameter alat = A (in ANGSTROM ).
             If ibrav == 0, only A is used if present, and cell vectors are read from card
            CELL_PARAMETERS."""
        ),
    )
    cosBC: float = Field(  # noqa: N815
        0.0,
        description=dedent(
            """\
            Traditional crystallographic constants:  a,b,c in ANGSTROM cosAB = cosine of the angle
            between axis a and b (gamma) cosAC = cosine of the angle between axis a and c (beta)
            cosBC = cosine of the angle between axis b and c (alpha)  The axis are chosen according
            to the value of ibrav. Specify either these OR celldm but NOT both. Only needed values
            (depending on ibrav) must be specified.  The lattice parameter alat = A (in ANGSTROM ).
             If ibrav == 0, only A is used if present, and cell vectors are read from card
            CELL_PARAMETERS."""
        ),
    )
    nat: int = Field(
        ...,
        description=dedent(
            """\
            number of atoms in the unit cell (ALL atoms, except if space_group is set, in which
            case, INEQUIVALENT atoms)"""
        ),
    )
    ntyp: int = Field(..., description="number of types of atoms in the unit cell")
    nbnd: int | None = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            Number of electronic states (bands) to be calculated. Note that in spin-polarized
            calculations the number of k-point, not the number of bands per k-point, is doubled  By
            default, for an insulator nbnd is set to the number of valence bands (nbnd = number of
            electrons / 2); for a metal, 20% more (with a minimum of 4 more) states are added."""
        ),
    )
    nbnd_cond: int | None = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            Number of electronic states in the conduction manifold for a two chemical-potential
            calculation (twochem=.true.).  By default it is set to nbnd - (number of electrons / 2)
            in the collinear case, and to nbnd - (number of electrons) in the noncollinear case."""
        ),
    )
    tot_charge: Annotated[float, Quantity(units="e", dimensionality="charge")] = Field(
        0.0,
        description=dedent(
            """\
            Total charge of the system. Useful for simulations with charged cells. By default the
            unit cell is assumed to be neutral (tot_charge=0). tot_charge=+1 means one electron
            missing from the system, tot_charge=-1 means one additional electron, and so on.  In a
            periodic calculation a compensating jellium background is inserted to remove
            divergences if the cell is not neutral."""
        ),
    )
    tot_magnetization: float = Field(
        -10000,
        description=dedent(
            """\
            Total majority spin charge - minority spin charge. Used to impose a specific total
            electronic magnetization. The default value -10000 is a sentinel meaning 'unspecified':
            if left unspecified the tot_magnetization variable is ignored and the amount of
            electronic magnetization is determined during the self-consistent cycle."""
        ),
    )
    ecutwfc: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        ..., description="kinetic energy cutoff for wavefunctions"
    )
    ecutrho: Annotated[float | None, Quantity(units="Ry", dimensionality="energy")] = Field(
        None,
        json_schema_extra={"default_expr": "4 * ecutwfc"},
        description=dedent(
            """\
            Kinetic energy cutoff for charge density and potential For norm-conserving
            pseudopotential you should stick to the default value, you can reduce it by a little
            but it will introduce noise especially on forces and stress. If there are ultrasoft PP,
            a larger value than the default is often desirable (ecutrho = 8 to 12 times ecutwfc,
            typically). PAW datasets can often be used at 4*ecutwfc, but it depends on the shape of
            augmentation charge: testing is mandatory. The use of gradient-corrected functional,
            especially in cells with vacuum, or for pseudopotential without non-linear core
            correction, usually requires an higher values of ecutrho to be accurately converged."""
        ),
    )
    ecutfock: Annotated[float | None, Quantity(units="Ry", dimensionality="energy")] = Field(
        None,
        json_schema_extra={"default_ref": "ecutrho"},
        description=dedent(
            """\
            Kinetic energy cutoff for the exact exchange operator in EXX type calculations. By
            default this is the same as ecutrho but in some EXX calculations, a significant
            speed-up can be obtained by reducing ecutfock, at the expense of some loss in accuracy.
            Must be .gt. ecutwfc. Not implemented for stress calculation and for US-PP and PAW
            pseudopotentials. Use with care, especially in metals where it may give raise to
            instabilities."""
        ),
    )
    nr1: int = Field(
        0,
        description=dedent(
            """\
            Three-dimensional FFT mesh (hard grid) for charge density (and scf potential). If not
            specified the grid is calculated based on the cutoff for charge density (see also
            ecutrho) Note: you must specify all three dimensions for this setting to be used."""
        ),
    )
    nr2: int = Field(
        0,
        description=dedent(
            """\
            Three-dimensional FFT mesh (hard grid) for charge density (and scf potential). If not
            specified the grid is calculated based on the cutoff for charge density (see also
            ecutrho) Note: you must specify all three dimensions for this setting to be used."""
        ),
    )
    nr3: int = Field(
        0,
        description=dedent(
            """\
            Three-dimensional FFT mesh (hard grid) for charge density (and scf potential). If not
            specified the grid is calculated based on the cutoff for charge density (see also
            ecutrho) Note: you must specify all three dimensions for this setting to be used."""
        ),
    )
    nr1s: int = Field(
        0,
        description=dedent(
            """\
            Three-dimensional mesh for wavefunction FFT and for the smooth part of charge density (
            smooth grid ). Coincides with nr1, nr2, nr3 if ecutrho = 4 * ecutwfc ( default ) Note:
            you must specify all three dimensions for this setting to be used."""
        ),
    )
    nr2s: int = Field(
        0,
        description=dedent(
            """\
            Three-dimensional mesh for wavefunction FFT and for the smooth part of charge density (
            smooth grid ). Coincides with nr1, nr2, nr3 if ecutrho = 4 * ecutwfc ( default ) Note:
            you must specify all three dimensions for this setting to be used."""
        ),
    )
    nr3s: int = Field(
        0,
        description=dedent(
            """\
            Three-dimensional mesh for wavefunction FFT and for the smooth part of charge density (
            smooth grid ). Coincides with nr1, nr2, nr3 if ecutrho = 4 * ecutwfc ( default ) Note:
            you must specify all three dimensions for this setting to be used."""
        ),
    )
    nosym: bool = Field(
        False,
        description=dedent(
            """\
            if (.TRUE.) symmetry is not used. Consequences:  - if a list of k points is provided in
            input, it is used 'as is': symmetry-inequivalent k-points are not generated, and the
            charge density is not symmetrized;  - if a uniform (Monkhorst-Pack) k-point grid is
            provided in input, it is expanded to cover the entire Brillouin Zone, irrespective of
            the crystal symmetry. Time reversal symmetry is assumed so k and -k are considered as
            equivalent unless noinv=.true. is specified.  Do not use this option unless you know
            exactly what you want and what you get. May be useful in the following cases: - in
            low-symmetry large cells, if you cannot afford a k-point grid with the correct symmetry
            - in MD simulations - in calculations for isolated atoms"""
        ),
    )
    nosym_evc: bool = Field(
        False,
        description=dedent(
            """\
            if (.TRUE.) symmetry is not used, and k points are forced to have the symmetry of the
            Bravais lattice; an automatically generated Monkhorst-Pack grid will contain all points
            of the grid over the entire Brillouin Zone, plus the points rotated by the symmetries
            of the Bravais lattice which were not in the original grid. The same applies if a
            k-point list is provided in input instead of a Monkhorst-Pack grid. Time reversal
            symmetry is assumed so k and -k are equivalent unless noinv=.true. is specified. This
            option differs from nosym because it forces k-points in all cases to have the full
            symmetry of the Bravais lattice (not all uniform grids have such property!)"""
        ),
    )
    noinv: bool = Field(
        False,
        description=dedent(
            """\
            if (.TRUE.) disable the usage of k => -k symmetry (time reversal) in k-point
            generation"""
        ),
    )
    no_t_rev: bool = Field(
        False,
        description=dedent(
            """\
            if (.TRUE.) disable the usage of magnetic symmetry operations that consist in a
            rotation + time reversal."""
        ),
    )
    force_symmorphic: bool = Field(
        False,
        description=dedent(
            """\
            if (.TRUE.) force the symmetry group to be symmorphic by disabling symmetry operations
            having an associated fractionary translation"""
        ),
    )
    use_all_frac: bool = Field(
        False,
        description=dedent(
            """\
            if (.FALSE.) force real-space FFT grids to be commensurate with fractionary
            translations of non-symmorphic symmetry operations, if present (e.g.: if a fractional
            translation (0,0,c/4) exists, the FFT dimension along the c axis must be multiple of
            4). if (.TRUE.) do not impose any constraints to FFT grids, even in the presence of
            non-symmorphic symmetry operations. BEWARE: use_all_frac=.TRUE. may lead to wrong
            results for hybrid functionals and phonon calculations. Both cases use symmetrization
            in real space that works for non-symmorphic operations only if the real-space FFT grids
            are commensurate."""
        ),
    )
    occupations: Literal[
        "smearing", "tetrahedra", "tetrahedra_lin", "tetrahedra_opt", "fixed", "from_input"
    ] = Field(
        "fixed",
        description=dedent(
            """\
            Available options are:
            - 'smearing': gaussian smearing for metals; see variables smearing and degauss.
            - 'tetrahedra': Tetrahedron method, Bloechl's version: P.E. Bloechl, PRB 49, 16223
              (1994) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.49.16223) Requires
              uniform grid of k-points, to be automatically generated (see card K_POINTS). Well
              suited for calculation of DOS, less so (because not variational) for
              force/optimization/dynamics calculations.
            - 'tetrahedra_lin': Original linear tetrahedron method. To be used only as a reference;
              the optimized tetrahedron method is more efficient.
            - 'tetrahedra_opt': Optimized tetrahedron method: see M. Kawamura, PRB 89, 094515
              (2014) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.89.094515). Can be
              used for phonon calculations as well.
            - 'fixed': for insulators with a gap.
            - 'from_input': The occupation are read from input file, card OCCUPATIONS. Option valid
              only for a single k-point, requires nbnd to be set in input. Occupations should be
              consistent with the value of tot_charge."""
        ),
    )
    one_atom_occupations: bool = Field(
        False,
        description=dedent(
            """\
            This flag is used for isolated atoms (nat=1) together with occupations='from_input'. If
            it is .TRUE., the wavefunctions are ordered as the atomic starting wavefunctions,
            independently from their eigenvalue. The occupations indicate which atomic states are
            filled.  The order of the states is written inside the UPF pseudopotential file. In the
            scalar relativistic case: S -> l=0, m=0 P -> l=1, z, x, y D -> l=2, r^2-3z^2, xz, yz,
            xy, x^2-y^2  In the noncollinear magnetic case (with or without spin-orbit), each group
            of states is doubled. For instance: P -> l=1, z, x, y for spin up, l=1, z, x, y for
            spin down. Up and down is relative to the direction of the starting magnetization.  In
            the case with spin-orbit and time-reversal (starting_magnetization=0.0) the atomic
            wavefunctions are radial functions multiplied by spin-angle functions. For instance: P
            -> l=1, j=1/2, m_j=-1/2,1/2. l=1, j=3/2, m_j=-3/2, -1/2, 1/2, 3/2.  In the magnetic
            case with spin-orbit the atomic wavefunctions can be forced to be spin-angle functions
            by setting starting_spin_angle to .TRUE.."""
        ),
    )
    starting_spin_angle: bool = Field(
        False,
        description=dedent(
            """\
            In the spin-orbit case when domag=.TRUE., by default, the starting wavefunctions are
            initialized as in scalar relativistic noncollinear case without spin-orbit.  By setting
            starting_spin_angle=.TRUE. this behaviour can be changed and the initial wavefunctions
            are radial functions multiplied by spin-angle functions.  When domag=.FALSE. the
            initial wavefunctions are always radial functions multiplied by spin-angle functions
            independently from this flag.  When lspinorb is .FALSE. this flag is not used."""
        ),
    )
    degauss_cond: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.0,
        description=dedent(
            """\
            value of the gaussian spreading for brillouin-zone integration in the conduction
            manifold in a two-chemical potential calculation (twochem=.true.)."""
        ),
    )
    nelec_cond: float = Field(
        0.0,
        description=dedent(
            """\
            Number of electrons placed in the conduction manifold in a two-chemical potential
            calculation (twochem=.true.). Of the total # of electrons nelec, nelec-nelec_cond will
            occupy the valence manifold and nelec_cond will be constrained in the conduction
            manifold."""
        ),
    )
    degauss: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.0, description="value of the gaussian spreading for brillouin-zone integration in metals."
    )
    smearing: Literal["gaussian", "methfessel-paxton", "marzari-vanderbilt", "fermi-dirac"] = Field(
        "gaussian",
        description=dedent(
            """\
            Available options are:
            - 'gaussian': ordinary Gaussian spreading.
            - 'methfessel-paxton': Methfessel-Paxton first-order spreading (see PRB 40, 3616 (1989)
              (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.40.3616)).
            - 'marzari-vanderbilt': Marzari-Vanderbilt-DeVita-Payne cold smearing (see PRL 82, 3296
              (1999) (https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.82.3296)).
            - 'fermi-dirac': smearing with Fermi-Dirac function."""
        ),
    )
    nspin: Literal[1, 2, 4] = Field(
        1,
        description=dedent(
            """\
            Spin polarization mode of the calculation.
            - '1': non-polarized calculation.
            - '2': spin-polarized calculation, LSDA (magnetization along z axis).
            - '4': spin-polarized calculation, noncollinear (magnetization in generic direction) DO
              NOT specify nspin in this case; specify noncolin=.TRUE. instead."""
        ),
    )
    sic_gamma: float = Field(0.0, description="Strength of the gammaDFT potential.")
    pol_type: Literal["none", "e", "h"] = Field(
        "none",
        description=dedent(
            """\
            Type of polaron in gammaDFT.
            - 'none': no polaron.
            - 'e': electron polaron.
            - 'h': hole polaron."""
        ),
    )
    sic_energy: bool = Field(
        False,
        description=dedent(
            """\
            Enable the calculation of the total energy in gammaDFT. When .true., a preliminary
            calculation is performed to calculate the electron density in the absence of the
            polaron. When .false., the total energy printed in output should not be considered. For
            structural relaxations, it is recommended to use .false. to avoid doubling the
            computational cost."""
        ),
    )
    sci_vb: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(
        0.0,
        description=dedent(
            """\
            Valence band shift through self-consistent scissor operator. When performing gammaDFT
            calculations of polarons, the polaron level is not shifted."""
        ),
    )
    sci_cb: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(
        0.0,
        description=dedent(
            """\
            Conduction band band shift through self-consistent scissor operator. When performing
            gammaDFT calculations of polarons, the polaron level is not shifted."""
        ),
    )
    noncolin: bool = Field(
        False, description="if .true. the program will perform a noncollinear calculation."
    )
    ecfixed: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.0, description=""
    )
    qcutz: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.0, description=""
    )
    q2sigma: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.01,
        description=dedent(
            """\
            ecfixed, qcutz, q2sigma:  parameters for modified functional to be used in
            variable-cell molecular dynamics (or in stress calculation). 'ecfixed' is the value of
            the constant-cutoff; 'qcutz' and 'q2sigma' are the height and the width of the energy
            step for reciprocal vectors whose square modulus is greater than 'ecfixed'. In the
            kinetic energy, G^2 is replaced by G^2 + qcutz * (1 + erf ( (G^2 - ecfixed)/q2sigma) )
            See: M. Bernasconi et al, J. Phys. Chem. Solids 56, 501 (1995),
            doi:10.1016/0022-3697(94)00228-2 (https://doi.org/10.1016/0022-3697(94)00228-2)"""
        ),
    )
    input_dft: str | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [{"when": None, "value": "from_pseudopotential"}],
        },
        description=dedent(
            """\
            Exchange-correlation functional: eg 'PBE', 'BLYP' etc See Modules/funct.f90 for allowed
            values. Overrides the value read from pseudopotential files. Use with care and if you
            know what you are doing!"""
        ),
    )
    ace: bool = Field(
        True,
        description=dedent(
            """\
            Use Adaptively Compressed Exchange operator as in Lin Lin, J. Chem. Theory Comput.
            2016, 12, 2242--2249, doi:10.1021/acs.jctc.6b00092
            (https://doi.org/10.1021/acs.jctc.6b00092)  Set to false to use standard Exchange (much
            slower)"""
        ),
    )
    exx_fraction: float | None = Field(
        None,
        json_schema_extra={"conditional_default": [{"when": None, "value": "internal"}]},
        description=dedent(
            """\
            Fraction of EXX for hybrid functional calculations. In the case of input_dft='PBE0',
            the default value is 0.25, while for input_dft='B3LYP' the exx_fraction default value
            is 0.20."""
        ),
    )
    screening_parameter: Annotated[float, Quantity(units="bohr^-1", dimensionality="length^-1")] = (
        Field(
            0.106,
            description=dedent(
                """\
                screening_parameter for HSE like hybrid functionals. For more information, see: J.
                Chem. Phys. 118, 8207 (2003), doi:10.1063/1.1564060
                (https://doi.org/10.1063/1.1564060) J. Chem. Phys. 124, 219906 (2006),
                doi:10.1063/1.2204597 (https://doi.org/10.1063/1.2204597)"""
            ),
        )
    )
    exxdiv_treatment: Literal["gygi-baldereschi", "vcut_spherical", "vcut_ws", "none"] = Field(
        "gygi-baldereschi",
        description=dedent(
            """\
            Specific for EXX. It selects the kind of approach to be used for treating the Coulomb
            potential divergencies at small q vectors.
            - 'gygi-baldereschi': appropriate for cubic and quasi-cubic supercells.
            - 'vcut_spherical': appropriate for cubic and quasi-cubic supercells (untested for
              non-orthogonal crystal axis).
            - 'vcut_ws': appropriate for strongly anisotropic supercells, see also ecutvcut
              (untested for non-orthogonal crystal axis).
            - 'none': sets Coulomb potential at G,q=0 to 0.0 (required for GAU-PBE)."""
        ),
    )
    exx_type: Literal["bands", "band_pairs"] = Field(
        "band_pairs",
        description=dedent(
            """\
            Specific for EXX. This keyword defines the band distribution scheme to use when band
            groups are enabled. When band groups are not used (-nb=1 or not specified), the two
            schemes are equivalent, but their internal implementations differ.
            - 'bands': distribute bands among band groups (GPU execution not yet implemented).
            - 'band_pairs': distribute band pairs among band groups (see Barnes et al., Computer
              Physics Communications, Volume 214, 2017, Pages 52-58)."""
        ),
    )
    x_gamma_extrapolation: bool = Field(
        True,
        description=dedent(
            """\
            Specific for EXX. If .true., extrapolate the G=0 term of the potential (see README in
            examples/EXX_example for more) Set this to .false. for GAU-PBE."""
        ),
    )
    ecutvcut: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.0,
        description=dedent(
            """\
            Reciprocal space cutoff for correcting Coulomb potential divergencies at small q
            vectors."""
        ),
    )
    nqx1: int | None = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            Three-dimensional mesh for q (k1-k2) sampling of the Fock operator (EXX). Can be
            smaller than the number of k-points.  Currently this defaults to the size of the
            k-point mesh used. In QE =< 5.0.2 it defaulted to nqx1=nqx2=nqx3=1."""
        ),
    )
    nqx2: int | None = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            Three-dimensional mesh for q (k1-k2) sampling of the Fock operator (EXX). Can be
            smaller than the number of k-points.  Currently this defaults to the size of the
            k-point mesh used. In QE =< 5.0.2 it defaulted to nqx1=nqx2=nqx3=1."""
        ),
    )
    nqx3: int | None = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            Three-dimensional mesh for q (k1-k2) sampling of the Fock operator (EXX). Can be
            smaller than the number of k-points.  Currently this defaults to the size of the
            k-point mesh used. In QE =< 5.0.2 it defaulted to nqx1=nqx2=nqx3=1."""
        ),
    )
    localization_thr: float = Field(
        0.0,
        description=dedent(
            """\
            Overlap threshold over which the exchange integral over a pair of localized orbitals is
            included in the evaluation of EXX operator. Any value greater than 0.0 triggers the
            SCDM localization and the evaluation on EXX using the localized orbitals. Very small
            value of the threshold should yield the same result as the default EXX evaluation"""
        ),
    )
    dmft: bool = Field(
        False,
        description=dedent(
            """\
            If true, nscf calculation will exit in restart mode, scf calculation will restart from
            there if DMFT updates are provided as hdf5 archive. Scf calculation should be used only
            with electron_maxstep = 1. K_POINTS have to be identical and given explicitly with
            nosym."""
        ),
    )
    dmft_prefix: str | None = Field(
        None,
        json_schema_extra={"default_ref": "prefix"},
        description=dedent(
            """\
            prepended to hdf5 archive: dmft_prefix.h5  DMFT update should be provided in
            group/dataset as: - dft_misc_input/band_window with dimension [1, number of k-points, 2
            (real + complex)] - dft_update/delta_N with dimension [number of k-points, number of
            correlated orbitals, number of correlated orbitals, 2 (real + complex)]"""
        ),
    )
    ensemble_energies: bool = Field(
        False,
        description=dedent(
            """\
            If ensemble_energies = .true., an ensemble of xc energies is calculated
            non-selfconsistently for perturbed exchange-enhancement factors and LDA vs. PBE
            correlation ratios after each converged electronic ground state calculation.  Ensemble
            energies can be analyzed with the 'bee' utility included with libbeef.  Requires
            linking against libbeef. input_dft must be set to a BEEF-type functional (e.g.
            input_dft = 'BEEF-vdW')"""
        ),
    )
    edir: int = Field(
        1,
        description=dedent(
            """\
            The direction of the electric field or dipole correction is parallel to the bg(:,edir)
            reciprocal lattice vector, so the potential is constant in planes defined by FFT grid
            points; edir = 1, 2 or 3. Used only if tefield is .TRUE."""
        ),
    )
    emaxpos: float = Field(
        0.5,
        description=dedent(
            """\
            Position of the maximum of the saw-like potential along crystal axis edir, within the
            unit cell (see below), 0 < emaxpos < 1 Used only if tefield is .TRUE."""
        ),
    )
    eopreg: float = Field(
        0.1,
        description=dedent(
            """\
            Zone in the unit cell where the saw-like potential decreases. ( see below, 0 < eopreg <
            1 ). Used only if tefield is .TRUE."""
        ),
    )
    eamp: Annotated[
        float, Quantity(units="Ry e^-1 bohr^-1", dimensionality="energy charge^-1 length^-1")
    ] = Field(
        0.0,
        description=dedent(
            """\
            Amplitude of the electric field, in ***Hartree*** a.u.; 1 a.u. = 51.4220632*10^10 V/m.
            Used only if tefield==.TRUE. The saw-like potential increases with slope eamp in the
            region from (emaxpos+eopreg-1) to (emaxpos), then decreases to 0 until
            (emaxpos+eopreg), in units of the crystal vector edir. Important: the change of slope
            of this potential must be located in the empty region, or else unphysical forces will
            result."""
        ),
    )
    lforcet: bool = Field(
        False,
        description=dedent(
            """\
            When starting a non collinear calculation using an existing density file from a
            collinear lsda calculation assumes previous density points in z direction and rotates
            it in the direction described by angle1 and angle2 variables for atomic type 1"""
        ),
    )
    constrained_magnetization: Literal[
        "none", "total", "atomic", "total direction", "atomic direction"
    ] = Field(
        "none",
        description=dedent(
            """\
            Used to perform constrained calculations in magnetic systems. Currently available
            choices:  N.B.: symmetrization may prevent to reach the desired orientation of the
            magnetization. Try not to start with very highly symmetric configurations or use the
            nosym flag (only as a last remedy)
            - 'none': no constraint.
            - 'total': total magnetization is constrained by adding a penalty functional to the
              total energy:  LAMBDA * SUM_{i} ( magnetization(i) - fixed_magnetization(i) )**2
              where the sum over i runs over the three components of the magnetization. Lambda is a
              real number (see below). Noncolinear case only. Use tot_magnetization for LSDA.
            - 'atomic': atomic magnetization are constrained to the defined starting magnetization
              adding a penalty:  LAMBDA * SUM_{i,itype} ( magnetic_moment(i,itype) - mcons(i,itype)
              )**2  where i runs over the cartesian components (or just z in the collinear case)
              and itype over the types (1-ntype). mcons(:,:) array is defined from
              starting_magnetization, (also from angle1, angle2 in the noncollinear case). lambda
              is a real number.
            - 'total direction': the angle theta of the total magnetization with the z axis (theta
              = fixed_magnetization(3)) is constrained:  LAMBDA * (
              arccos(magnetization(3)/mag_tot) - theta )**2  where mag_tot is the modulus of the
              total magnetization.
            - 'atomic direction': not all the components of the atomic magnetic moment are
              constrained but only the cosine of angle1, and the penalty functional is:  LAMBDA *
              SUM_{itype} ( mag_mom(3,itype)/mag_mom_tot - cos(angle1(ityp)) )**2."""
        ),
    )
    Lambda: float = Field(
        1.0,
        description=dedent(
            """\
            parameter used for constrained_magnetization calculations N.B.: if the scf calculation
            does not converge, try to reduce lambda to obtain convergence, then restart the run
            with a larger lambda"""
        ),
    )
    report: int = Field(
        -1,
        description=dedent(
            """\
            determines when atomic magnetic moments are printed on output: report = 0  never report
            =-1  at the beginning of the scf and at convergence report = N  as -1, plus every N scf
            iterations"""
        ),
    )
    lspinorb: bool = Field(
        False,
        description="if .TRUE. the noncollinear code can use a pseudopotential with spin-orbit.",
    )
    assume_isolated: Literal["none", "makov-payne", "martyna-tuckerman", "esm", "2D"] = Field(
        "none",
        description=dedent(
            """\
            Used to perform calculation assuming the system to be isolated (a molecule or a cluster
            in a 3D supercell).  Currently available choices:
            - 'none': regular periodic calculation w/o any correction.
            - 'makov-payne': the Makov-Payne correction to the total energy is computed. An
              estimate of the vacuum level is also calculated so that eigenvalues can be properly
              aligned. ONLY FOR CUBIC SYSTEMS (ibrav=1,2,3). Theory: G.Makov, and M.C.Payne,
              'Periodic boundary conditions in ab initio calculations' , PRB 51, 4014 (1995)
              (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.51.4014).
            - 'martyna-tuckerman': Martyna-Tuckerman correction to both total energy and scf
              potential. Adapted from: G.J. Martyna, and M.E. Tuckerman, 'A reciprocal space based
              method for treating long range interactions in ab-initio and force-field-based
              calculation in clusters', J. Chem. Phys. 110, 2810 (1999), doi:10.1063/1.477923
              (https://doi.org/10.1063/1.477923).
            - 'esm': Effective Screening Medium Method. For polarized or charged slab calculation,
              embeds the simulation cell within an effective semi- infinite medium in the
              perpendicular direction (along z). Embedding regions can be vacuum or semi-infinite
              metal electrodes (use esm_bc to choose boundary conditions). If between two
              electrodes, an optional electric field (esm_efield) may be applied. Method described
              in M. Otani and O. Sugino, 'First-principles calculations of charged surfaces and
              interfaces: A plane-wave nonrepeated slab approach', PRB 73, 115407 (2006)
              (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.73.115407).  NB: - Two
              dimensional (xy plane) average charge density and electrostatic potentials are
              printed out to 'prefix.esm1'.  - Requires cell with a_3 lattice vector along z,
              normal to the xy plane, with the slab centered around z=0.  - For bc2 with an
              electric field and bc3 boundary conditions, the inversion symmetry along z-direction
              is automatically eliminated.  - In case of calculation='vc-relax', use
              cell_dofree='2Dxy' or other parameters so that c-vector along z-axis should not be
              moved.  See esm_bc, esm_efield, esm_w, esm_nfit.
            - '2D': Truncation of the Coulomb interaction in the z direction for structures
              periodic in the x-y plane. Total energy, forces and stresses are computed in a
              two-dimensional framework. Linear-response calculations () done on top of a
              self-consistent calculation with this flag will automatically be performed in the
              2D framework as well. Please refer to: Sohier, T., Calandra, M., & Mauri, F.
              (2017), 'Density functional perturbation theory for gated two-dimensional
              heterostructures: Theoretical developments and application to flexural phonons in
              graphene', PRB, 96, 075448 (2017)
              (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.96.075448).  NB: - The
              length of the unit-cell along the z direction should be larger than twice the
              thickness of the 2D material (including electrons). A reasonable estimate for a
              layer's thickness could be the interlayer distance in the corresponding layered
              bulk material. Otherwise, the atomic thickness + 10 bohr should be a safe
              estimate. There is also a lower limit of 20 bohr imposed by the cutoff radius used
              to read pseudopotentials (see read_pseudo.f90 in Modules).  - As for ESM above,
              only in-plane stresses make sense and one should use cell_dofree= '2Dxy' in a
              vc-relax calculation."""
        ),
    )
    esm_bc: Literal["pbc", "bc1", "bc2", "bc3"] = Field(
        "pbc",
        description=dedent(
            """\
            If assume_isolated = 'esm', determines the boundary conditions used for either side of
            the slab.  Currently available choices:
            - 'pbc': regular periodic calculation (no ESM).
            - 'bc1': Vacuum-slab-vacuum (open boundary conditions).
            - 'bc2': Metal-slab-metal (dual electrode configuration). See also esm_efield.
            - 'bc3': Vacuum-slab-metal."""
        ),
    )
    esm_w: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        0.0,
        description=dedent(
            """\
            If assume_isolated = 'esm', determines the position offset of the start of the
            effective screening region, measured relative to the cell edge. (ESM region begins at z
            = +/- [L_z/2 + esm_w] )."""
        ),
    )
    esm_efield: Annotated[
        float, Quantity(units="Ry e^-1 bohr^-1", dimensionality="energy charge^-1 length^-1")
    ] = Field(
        0.0,
        description=dedent(
            """\
            If assume_isolated = 'esm' and esm_bc = 'bc2', gives the magnitude of the electric
            field to be applied between semi-infinite ESM electrodes."""
        ),
    )
    esm_nfit: int = Field(
        4,
        description=dedent(
            """\
            If assume_isolated = 'esm', gives the number of z-grid points for the polynomial fit
            along the cell edge."""
        ),
    )
    lgcscf: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE. perform a constant bias potential (constant-mu) calculation with
            Grand-Canonical SCF. (JCP 146, 114104 (2017), R.Sundararaman, et al.)  NB: - The total
            energy displayed in output includes the potentiostat contribution (-mu*N). -
            assume_isolated = 'esm' and esm_bc = 'bc2' or 'bc3' must be set in SYSTEM namelist. -
            ESM-RISM is also supported (assume_isolated = 'esm' and esm_bc = 'bc1' and trism =
            .TRUE.). - mixing_mode has to be 'TF' or 'local-TF', also its default is 'TF.' - The
            default of mixing_beta is 0.1 with ESM-RISM, 0.2 without ESM-RISM. - The default of
            diago_thr_init is 1.D-5. - diago_full_acc is always .TRUE. . - diago_rmm_conv is always
            .TRUE. ."""
        ),
    )
    gcscf_mu: Annotated[float | None, Quantity(units="eV", dimensionality="energy")] = Field(
        None,
        description=dedent(
            """\
            The target Fermi energy of GC-SCF. One can start with appropriate total charge of the
            system by giving tot_charge ."""
        ),
    )
    gcscf_conv_thr: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(
        0.01, description="Convergence threshold of Fermi energy for GC-SCF."
    )
    gcscf_beta: float = Field(
        0.05,
        description=dedent(
            """\
            Mixing factor for GC-SCF. Larger values are recommended, if systems with small DOS on
            Fermi surface as graphite."""
        ),
    )
    vdw_corr: Literal[
        "none", "grimme-d2", "grimme-d3", "tkatchenko-scheffler", "many-body-dispersion", "XDM"
    ] = Field(
        "none",
        description=dedent(
            """\
            Type of the van der Waals correction. Allowed values: Note that non-local functionals
            (eg vdw-DF) are NOT specified here but in input_dft
            - 'none': no van der Waals correction.
            - 'grimme-d2': Semiempirical Grimme's DFT-D2. Optional variables: london_s6,
              london_rcut, london_c6, london_rvdw S. Grimme, J. Comp. Chem. 27, 1787 (2006),
              doi:10.1002/jcc.20495 (https://doi.org/10.1002/jcc.20495) V. Barone et al., J. Comp.
              Chem. 30, 934 (2009), doi:10.1002/jcc.21112 (https://doi.org/10.1002/jcc.21112).
            - 'grimme-d3': Semiempirical Grimme's DFT-D3. Optional variables: dftd3_version,
              dftd3_threebody S. Grimme et al, J. Chem. Phys 132, 154104 (2010),
              doi:10.1063/1.3382344 (https://doi.org/10.1063/1.3382344).
            - 'tkatchenko-scheffler': Tkatchenko-Scheffler dispersion corrections with
              first-principle derived C6 coefficients. Optional variables: ts_vdw_econv_thr,
              ts_vdw_isolated See A. Tkatchenko and M. Scheffler, PRL 102, 073005 (2009)
              (https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.102.073005). J. Hermann et
              al., J. Chem. Phys. 159, 174802 (2023), doi:10.1063/5.0170972
              (https://doi.org/10.1063/5.0170972).
            - 'many-body-dispersion': Many-body dipersion (MBD) correction to long-range
              interactions. Optional variables: ts_vdw_isolated A. Ambrosetti et al., J. Chem.
              Phys. 140, 18A508 (2014), doi:10.1063/1.4865104 (https://doi.org/10.1063/1.4865104)
              J. Hermann et al., J. Chem. Phys. 159, 174802 (2023), doi:10.1063/5.0170972
              (https://doi.org/10.1063/5.0170972).
            - 'XDM': Exchange-hole dipole-moment model. Optional variables: xdm_a1, xdm_a2 A. D.
              Becke et al., J. Chem. Phys. 127, 154108 (2007), doi:10.1063/1.2795701
              (https://doi.org/10.1063/1.2795701) A. Otero de la Roza et al., J. Chem. Phys. 136,
              174109 (2012), doi:10.1063/1.4705760 (https://doi.org/10.1063/1.4705760)."""
        ),
    )
    london: bool = Field(False, description="")
    london_s6: float = Field(
        0.75, description="global scaling parameter for DFT-D. Default is good for PBE."
    )
    london_rcut: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        200.0, description="cutoff radius for dispersion interactions"
    )
    dftd3_version: Literal[2, 3, 4, 5, 6] = Field(
        3,
        description=dedent(
            """\
            Version of Grimme implementation of Grimme-D3:  NOTE: not all functionals are
            parametrized.
            - '2': Original Grimme-D2 parametrization.
            - '3': Grimme-D3 (zero damping).
            - '4': Grimme-D3 (BJ damping).
            - '5': Grimme-D3M (zero damping).
            - '6': Grimme-D3M (BJ damping)."""
        ),
    )
    dftd3_threebody: bool = Field(
        True,
        description=dedent(
            """\
            Turn three-body terms in Grimme-D3 on. If .false. two-body contributions only are
            computed, using two-body parameters of Grimme-D3. If dftd3_version=2, three-body
            contribution is always disabled."""
        ),
    )
    ts_vdw_econv_thr: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        1e-06,
        description=dedent(
            """\
            Optional: controls the convergence of the vdW energy (and forces). The default value is
            a safe choice, likely too safe, but you do not gain much in increasing it"""
        ),
    )
    ts_vdw_isolated: bool = Field(
        False,
        description=dedent(
            """\
            Optional: set it to .TRUE. when computing the Tkatchenko-Scheffler vdW energy or the
            Many-Body dispersion (MBD) energy for an isolated (non-periodic) system."""
        ),
    )
    xdm: bool = Field(False, description="")
    xdm_a1: float | None = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            Damping function parameter a1 (adimensional). It is NOT necessary to give a value if
            the functional is one of B86bPBE, PW86PBE, PBE, BLYP. For functionals in this list, the
            coefficients are given in:
            https://github.com/aoterodelaroza/postg/blob/master/xdm.param or
            https://erin-r-johnson.github.io/software/ A. Otero de la Roza, E. R. Johnson, J. Chem.
            Phys. 138, 204109 (2013), doi:10.1063/1.4705760 (https://doi.org/10.1063/1.4705760)"""
        ),
    )
    xdm_a2: Annotated[float | None, Quantity(units="angstrom", dimensionality="length")] = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            Damping function parameter a2. It is NOT necessary to give a value if the functional is
            one of B86bPBE, PW86PBE, PBE, BLYP. For functionals in this list, the coefficients are
            given in: https://github.com/aoterodelaroza/postg/blob/master/xdm.param or
            https://erin-r-johnson.github.io/software/ A. Otero de la Roza, E. R. Johnson, J. Chem.
            Phys. 138, 204109 (2013), doi:10.1063/1.4705760 (https://doi.org/10.1063/1.4705760)"""
        ),
    )
    space_group: int = Field(
        0,
        description=dedent(
            """\
            The number of the space group of the crystal, as given in the International Tables of
            Crystallography A (ITA). This allows to give in input only the inequivalent atomic
            positions. The positions of all the symmetry equivalent atoms are calculated by the
            code. Used only when the atomic positions are of type crystal_sg. See also uniqueb,
            origin_choice, rhombohedral"""
        ),
    )
    uniqueb: bool = Field(
        False,
        description=dedent(
            """\
            Used only for monoclinic lattices. If .TRUE. the b unique ibrav (-12 or -13) are used,
            and symmetry equivalent positions are chosen assuming that the twofold axis or the
            mirror normal is parallel to the b axis. If .FALSE. it is parallel to the c axis."""
        ),
    )
    origin_choice: Literal[1, 2] = Field(
        1,
        description=dedent(
            """\
            Used only for space groups that in the ITA allow the use of two different origins.
            - '1': the first origin.
            - '2': the second origin."""
        ),
    )
    rhombohedral: bool = Field(
        True,
        description=dedent(
            """\
            Used only for rhombohedral space groups. When .TRUE. the coordinates of the
            inequivalent atoms are given with respect to the rhombohedral axes, when .FALSE. the
            coordinates of the inequivalent atoms are given with respect to the hexagonal axes.
            They are converted internally to the rhombohedral axes and ibrav=5 is used in both
            cases."""
        ),
    )
    zgate: float = Field(
        0.5,
        description=dedent(
            """\
            used only if gate = .TRUE. Specifies the position of the charged plate which represents
            the counter charge in doped systems (tot_charge .ne. 0). In units of the unit cell
            length in z direction, zgate in ]0,1[ Details of the gate potential can be found in T.
            Brumme, M. Calandra, F. Mauri; PRB 89, 245406 (2014)
            (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.89.245406)."""
        ),
    )
    relaxz: bool = Field(
        False,
        description=dedent(
            """\
            used only if gate = .TRUE. Allows the relaxation of the system towards the charged
            plate. Use carefully and utilize either a layer of fixed atoms or a potential barrier
            (block=.TRUE.) to avoid the atoms moving to the position of the plate or the dipole of
            the dipole correction (dipfield=.TRUE.)."""
        ),
    )
    block: bool = Field(
        False,
        description=dedent(
            """\
            used only if gate = .TRUE. Adds a potential barrier to the total potential seen by the
            electrons to mimic a dielectric in field effect configuration and/or to avoid electrons
            spilling into the vacuum region for electron doping. Potential barrier is from block_1
            to block_2 and has a height of block_height. If dipfield = .TRUE. then eopreg is used
            for a smooth increase and decrease of the potential barrier."""
        ),
    )
    block_1: float = Field(
        0.45,
        description=dedent(
            """\
            used only if gate = .TRUE. and block = .TRUE. lower beginning of the potential barrier,
            in units of the unit cell size along z, block_1 in ]0,1["""
        ),
    )
    block_2: float = Field(
        0.55,
        description=dedent(
            """\
            used only if gate = .TRUE. and block = .TRUE. upper beginning of the potential barrier,
            in units of the unit cell size along z, block_2 in ]0,1["""
        ),
    )
    block_height: float = Field(
        0.0,
        description=dedent(
            """\
            used only if gate = .TRUE. and block = .TRUE. Height of the potential barrier in
            Rydberg."""
        ),
    )
    nextffield: int = Field(
        0,
        description=dedent(
            """\
            Number of activated external ionic force fields. See Doc/ExternalForceFields.tex for
            further explanation and parameterizations"""
        ),
    )
    celldm: Annotated[
        tuple[float, float, float, float, float, float],
        Quantity(units="1:bohr", dimensionality="dimensionless, 1:length"),
    ] = Field(
        (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        description=dedent(
            """\
            Crystallographic constants - see the ibrav variable. Specify either these OR
            A,B,C,cosAB,cosBC,cosAC NOT both. Only needed values (depending on 'ibrav') must be
            specified alat = celldm(1) is the lattice parameter 'a' If ibrav==0, only celldm(1) is
            used if present; cell vectors are read from card CELL_PARAMETERS"""
        ),
    )
    starting_charge: Annotated[list[float], Quantity(units="e", dimensionality="charge")] = Field(
        default_factory=list,
        description=dedent(
            """\
            starting charge on atomic type 'i', to create starting potential with startingpot =
            'atomic'. (start = 1, end = ntyp)"""
        ),
    )
    starting_magnetization: list[float] = Field(
        default_factory=list,
        description=dedent(
            """\
            Starting spin polarization on atomic type 'i' in a spin-polarized (LSDA or
            non-collinear/spin-orbit) calculation. The input values can have an absolute value
            greater than or equal to 1, which will be interpreted as the site's magnetic moment.
            Alternatively, the values can range between -1 and 1, which will be interpreted as the
            site magnetization per valence electron. For QE-v7.2 and older versions, only the
            second option is allowed.  If you expect a nonzero magnetization in your ground state,
            you MUST either specify a nonzero value for at least one atomic type, or constrain the
            magnetization using variable tot_magnetization for LSDA, constrained_magnetization for
            noncollinear/spin-orbit calculations. If you don't, you will get a nonmagnetic (zero
            magnetization) state. In order to perform LSDA calculations for an antiferromagnetic
            state, define two different atomic species corresponding to sublattices of the same
            atomic type.  NOTE 1: starting_magnetization is ignored in most BUT NOT ALL cases in
            non-scf calculations: it is safe to keep the same values for the scf and subsequent
            non-scf calculation.  NOTE 2: If you fix the magnetization with tot_magnetization, do
            not specify starting_magnetization.  NOTE 3: In the noncollinear/spin-orbit case,
            starting with zero starting_magnetization on all atoms imposes time reversal symmetry.
            The magnetization is never calculated and is set to zero (the internal variable domag
            is set to .FALSE.). (start = 1, end = ntyp)"""
        ),
    )
    Hubbard_beta: Annotated[list[float], Quantity(units="eV", dimensionality="energy")] = Field(
        default_factory=list,
        description=dedent(
            """\
            Hubbard_beta(i) is the perturbation (on atom i) used to compute J0 with the
            linear-response method of Cococcioni and de Gironcoli, PRB 71, 035105 (2005)
            (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.71.035105) (only for DFT+U or
            DFT+U+V). See also PRB 84, 115108 (2011)
            (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.84.115108). (start = 1, end =
            ntyp)"""
        ),
    )
    angle1: list[float] = Field(
        default_factory=list,
        description=dedent(
            """\
            The angle expressed in degrees between the initial magnetization and the z-axis. For
            noncollinear calculations only; index i runs over the atom types. (start = 1, end =
            ntyp)"""
        ),
    )
    angle2: list[float] = Field(
        default_factory=list,
        description=dedent(
            """\
            The angle expressed in degrees between the projection of the initial magnetization on
            x-y plane and the x-axis. For noncollinear calculations only. (start = 1, end = ntyp)"""
        ),
    )
    fixed_magnetization: tuple[float, float, float] = Field(
        (0.0, 0.0, 0.0),
        description=dedent(
            """\
            total magnetization vector (x,y,z components) to be kept fixed when
            constrained_magnetization=='total"""
        ),
    )
    london_c6: Annotated[
        list[float] | None, Quantity(units="Ry bohr^6", dimensionality="energy length^6")
    ] = Field(
        None,
        json_schema_extra={"conditional_default": [{"when": None, "value": "internal"}]},
        description=dedent(
            """\
            atomic C6 coefficient of each atom type  ( if not specified default values from S.
            Grimme, J. Comp. Chem. 27, 1787 (2006), doi:10.1002/jcc.20495
            (https://doi.org/10.1002/jcc.20495) are used; see file Modules/mm_dispersion.f90 )
            (start = 1, end = ntyp)"""
        ),
    )
    london_rvdw: Annotated[list[float] | None, Quantity(units="bohr", dimensionality="length")] = (
        Field(
            None,
            json_schema_extra={"conditional_default": [{"when": None, "value": "internal"}]},
            description=dedent(
                """\
                atomic vdw radii of each atom type  ( if not specified default values from S.
                Grimme, J. Comp. Chem. 27, 1787 (2006), doi:10.1002/jcc.20495
                (https://doi.org/10.1002/jcc.20495) are used; see file Modules/mm_dispersion.f90 )
                (start = 1, end = ntyp)"""
            ),
        )
    )


class ElectronsNamelist(Namelist):
    """Pydantic model for the `ELECTRONS` namelist."""

    @field_validator("diagonalization", mode="before")
    @classmethod
    def map_diagonalization(cls, v: str) -> str:
        """Map equivalent values for `diagonalization` onto a canonical value."""
        mapping = {"ParO": "paro", "rmm": "rmm-davidson", "rmm-diis": "rmm-davidson"}
        return mapping.get(v, v)

    electron_maxstep: int = Field(
        100,
        description=dedent(
            """\
            In a scf calculation: maximum number of scf iterations. If exact exchange is active:
            maximum number of iterations in the inner loop. If restarting from a previously
            interrupted calculation: maximum number of scf iterations performed in the current run,
            irrespective of how many have already been performed in previous runs."""
        ),
    )
    exx_maxstep: int = Field(
        100,
        description="maximum number of outer iterations in a scf calculation with exact exchange.",
    )
    scf_must_converge: bool = Field(
        True,
        description=dedent(
            """\
            If .false. do not stop molecular dynamics or ionic relaxation when electron_maxstep is
            reached. Use with care."""
        ),
    )
    conv_thr: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        1e-06,
        description=dedent(
            """\
            Convergence threshold for selfconsistency: estimated energy error < conv_thr (note that
            conv_thr is extensive, like the total energy).  For non-self-consistent calculations,
            conv_thr is used to set the default value of the threshold (ethr) for iterative
            diagonalization: see diago_thr_init"""
        ),
    )
    adaptive_thr: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE. this turns on the use of an adaptive conv_thr for the inner scf loops when
            using EXX."""
        ),
    )
    conv_thr_init: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.001,
        description=dedent(
            """\
            When adaptive_thr = .TRUE. this is the convergence threshold used for the first scf
            cycle."""
        ),
    )
    conv_thr_multi: float = Field(
        0.1,
        description=dedent(
            """\
            When adaptive_thr = .TRUE. the convergence threshold for each scf cycle is given by:
            max( conv_thr, conv_thr_multi * dexx )"""
        ),
    )
    mixing_mode: Literal["plain", "TF", "local-TF"] = Field(
        "plain",
        description=dedent(
            """\
            Available options are:
            - 'plain': charge density Broyden mixing.
            - 'TF': as above, with simple Thomas-Fermi screening (for highly homogeneous systems).
            - 'local-TF': as above, with local-density-dependent TF screening (for highly
              inhomogeneous systems)."""
        ),
    )
    mixing_beta: float = Field(0.7, description="mixing factor for self-consistency")
    mixing_ndim: int = Field(
        8,
        description=dedent(
            """\
            number of iterations used in mixing scheme. If you are tight with memory, you may
            reduce it to 4 or so."""
        ),
    )
    mixing_fixed_ns: int = Field(
        0,
        description=dedent(
            """\
            For DFT+U : number of iterations with fixed ns ( ns is the atomic density appearing in
            the Hubbard term )."""
        ),
    )
    diagonalization: Literal[
        "david", "cg", "ppcg", "paro", "rmm-davidson", "rmm-paro", "direct"
    ] = Field(
        "david",
        description=dedent(
            """\
            Available options are:
            - 'david': Davidson iterative diagonalization with overlap matrix. Fast, may in some
              rare cases fail.
            - 'cg': Conjugate-gradient-like band-by-band diagonalization. MUCH slower than 'david'
              but uses less memory and is (a little bit) more robust.
            - 'ppcg': PPCG iterative diagonalization (end support on Dec 2024).
            - 'paro': ParO iterative diagonalization.
            - 'rmm-davidson': RMM-DIIS iterative diagonalization. To stabilize the SCF loop
              RMM-DIIS is alternated with calls to Davidson or ParO  solvers depending on the
              string used. Other variables that can be used to tune the behavior of RMM-DIIS are:
              diago_rmm_ndim and diago_rmm_conv.
            - 'rmm-paro': RMM-DIIS iterative diagonalization. To stabilize the SCF loop RMM-DIIS is
              alternated with calls to Davidson or ParO  solvers depending on the string used.
              Other variables that can be used to tune the behavior of RMM-DIIS are:
              diago_rmm_ndim and diago_rmm_conv.
            - 'direct': Direct diagonalization of the dense Hamiltonian in the plane-wave basis.
              Use ONLY when a large number of unoccupied states are needed."""
        ),
    )
    diago_thr_init: float = Field(
        0.0,
        description=dedent(
            """\
            Convergence threshold (ethr) for iterative diagonalization (the check is on eigenvalue
            convergence).  For scf calculations: default is 1.D-2 if starting from a superposition
            of atomic orbitals; 1.D-5 if starting from a charge density. During self consistency
            the threshold is automatically reduced (but never below 1.D-13) when approaching
            convergence.  For non-scf calculations: default is (conv_thr/N elec)/10."""
        ),
    )
    diago_cg_maxiter: int = Field(
        20, description="For conjugate gradient diagonalization:  max number of iterations"
    )
    diago_david_ndim: int = Field(
        2,
        description=dedent(
            """\
            For Davidson diagonalization: dimension of workspace (number of wavefunction
            packets, at least 2 needed). A larger value may yield a smaller number of iterations
            in the algorithm but uses more memory and more CPU time in subspace diagonalization
            (cdiaghg/rdiaghg). You may try diago_david_ndim=4 if you are not tight on memory and
            if the time spent in subspace diagonalization is small compared to the time spent in
            h_psi"""
        ),
    )
    diago_rmm_ndim: int = Field(
        4,
        description=dedent(
            """\
            For RMM-DIIS diagonalization: dimension of workspace (number of wavefunction packets,
            at least 2 needed)."""
        ),
    )
    diago_rmm_conv: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE., RMM-DIIS is performed up to converge. If .FALSE., RMM-DIIS is performed only
            once."""
        ),
    )
    diago_gs_nblock: int = Field(
        16,
        description="For RMM-DIIS diagonalization: blocking size of Gram-Schmidt orthogonalization",
    )
    diago_full_acc: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE. all the empty states are diagonalized at the same level of accuracy of the
            occupied ones. Otherwise the empty states are diagonalized using a larger threshold
            (this should not affect total energy, forces, and other ground-state properties)."""
        ),
    )
    efield: Annotated[
        float, Quantity(units="Ry e^-1 bohr^-1", dimensionality="energy charge^-1 length^-1")
    ] = Field(
        0.0,
        description=dedent(
            """\
            Amplitude of the finite electric field (1 a.u. = 36.3609*10^10 V/m). Used only if
            lelfield==.TRUE. and if k-points (K_POINTS card) are not automatic."""
        ),
    )
    efield_phase: Literal["read", "write", "none"] = Field(
        "none",
        description=dedent(
            """\
            Available options are:
            - 'read': set the zero of the electronic polarization (with lelfield==.true..) to the
              result of a previous calculation.
            - 'write': write on disk data on electronic polarization to be read in another
              calculation.
            - 'none': none of the above points."""
        ),
    )
    startingpot: Literal["atomic", "file"] = Field(
        "atomic",
        description=dedent(
            """\
            Available options are:
            - 'atomic': starting potential from atomic charge superposition (default for scf,
              *relax, *md).
            - 'file': start from existing 'charge-density.xml' file in the directory specified by
              variables prefix and outdir For nscf and bands calculation this is the default and
              the only sensible possibility."""
        ),
    )
    startingwfc: Literal["atomic", "atomic+random", "random", "file"] = Field(
        "atomic+random",
        description=dedent(
            """\
            Available options are:
            - 'atomic': Start from superposition of atomic orbitals. If not enough atomic orbitals
              are available, fill with random numbers the remaining wfcs The scf typically starts
              better with this option, but in some high-symmetry cases one can 'loose' valence
              states, ending up in the wrong ground state.
            - 'atomic+random': As above, plus a superimposed 'randomization' of atomic orbitals.
              Prevents the 'loss' of states mentioned above.
            - 'random': Start from random wfcs. Slower start of scf but safe. It may also reduce
              memory usage in conjunction with diagonalization='cg'.
            - 'file': Start from an existing wavefunction file in the directory specified by
              variables prefix and outdir."""
        ),
    )
    tqr: bool = Field(
        False,
        description=dedent(
            """\
            If .true., use a real-space algorithm for augmentation charges of ultrasoft
            pseudopotentials and PAWsets. Faster but numerically less accurate than the default
            G-space algorithm. Use with care and after testing!"""
        ),
    )
    real_space: bool = Field(
        False,
        description=dedent(
            """\
            If .true., exploit real-space localization to compute matrix elements for nonlocal
            projectors. Faster and in principle better scaling than the default G-space algorithm,
            but numerically less accurate, may lead to some loss of translational invariance. Use
            with care and after testing!"""
        ),
    )
    efield_cart: Annotated[
        tuple[float, float, float],
        Quantity(units="Ry e^-1 bohr^-1", dimensionality="energy charge^-1 length^-1"),
    ] = Field(
        (0.0, 0.0, 0.0),
        description=dedent(
            """\
            Finite electric field (1 a.u. = 36.3609*10^10 V/m) in cartesian axis. Used only if
            lelfield==.TRUE. and if k-points (K_POINTS card) are automatic."""
        ),
    )


class IonsNamelist(Namelist):
    """Pydantic model for the `IONS` namelist."""

    ion_positions: Literal["default", "from_input"] = Field(
        "default",
        description=dedent(
            """\
            Available options are:
            - 'default': if restarting, use atomic positions read from the restart file; in all
              other cases, use atomic positions from standard input.
            - 'from_input': read atomic positions from standard input, even if restarting."""
        ),
    )
    ion_velocities: Literal["default", "from_input"] = Field(
        "default",
        description=dedent(
            """\
            Initial ionic velocities. Available options are:
            - 'default': start a new simulation from random thermalized distribution of velocities
              if tempw is set, with zero velocities otherwise; restart from atomic velocities read
              from the restart file.
            - 'from_input': start or continue the simulation with atomic velocities read from
              standard input - see card ATOMIC_VELOCITIES."""
        ),
    )
    ion_dynamics: Literal[
        "none",
        "bfgs",
        "damp",
        "fire",
        "verlet",
        "velocity-verlet",
        "langevin",
        "langevin-smc",
        "bfgs",
        "damp",
        "beeman",
    ] = Field(
        "none",
        description=dedent(
            """\
            Specify the type of ionic dynamics.  For different type of calculation different
            possibilities are allowed and different default values apply:  CASE ( calculation ==
            'relax' )  CASE ( calculation == 'md' )  CASE ( calculation == 'vc-relax' )  CASE (
            calculation == 'vc-md' )
            - 'none': no ionic dynamics (this is the default for calculation = 'scf', 'nscf',
              'bands').
            - 'bfgs': (default)  use BFGS quasi-newton algorithm, based on the trust radius
              procedure, for structural relaxation.
            - 'damp': use damped (quick-min Verlet) dynamics for structural relaxation Can be used
              for constrained optimisation: see CONSTRAINTS card.
            - 'fire': use the FIRE minimization algorithm employing the semi-implicit Euler
              integration scheme see: Bitzek et al.,PRL, 97, 170201, (2006)
              (https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.97.170201), doi:
              10.1103/PhysRevLett.97.170201 (https://doi.org/10.1103/PhysRevLett.97.170201) Guenole
              et al.,CMS, 175, 109584, (2020), doi: 10.1016/j.commatsci.2020.109584
              (https://doi.org/10.1016/j.commatsci.2020.109584)  Can be used for constrained
              optimisation: see CONSTRAINTS card.
            - 'verlet': (default)  use Verlet algorithm to integrate Newton's equation. For
              constrained dynamics, see CONSTRAINTS card.
            - 'velocity-verlet': use velocity-Verlet algorithm to integrate Newton's equation. For
              constrained dynamics, see CONSTRAINTS card.
            - 'langevin': ion dynamics is over-damped Langevin.
            - 'langevin-smc': over-damped Langevin with Smart Monte Carlo: see R.J. Rossky, JCP,
              69, 4628 (1978), doi:10.1063/1.436415 (https://doi.org/10.1063/1.436415).
            - 'bfgs': (default)  use BFGS quasi-newton algorithm; cell_dynamics must be 'bfgs' too.
            - 'damp': use damped (Beeman) dynamics for structural relaxation.
            - 'beeman': (default)  use Beeman algorithm to integrate Newton's equation."""
        ),
    )
    pot_extrapolation: Literal["none", "atomic", "first_order", "second_order"] = Field(
        "atomic",
        description=dedent(
            """\
            Used to extrapolate the potential from preceding ionic steps.  Note: 'first_order' and
            'second-order' extrapolation make sense only for molecular dynamics calculations
            - 'none': no extrapolation.
            - 'atomic': extrapolate the potential as if it was a sum of atomic-like orbitals.
            - 'first_order': extrapolate the potential with first-order formula.
            - 'second_order': as above, with second order formula."""
        ),
    )
    wfc_extrapolation: Literal["none", "first_order", "second_order"] = Field(
        "none",
        description=dedent(
            """\
            Used to extrapolate the wavefunctions from preceding ionic steps.  Note: 'first_order'
            and 'second-order' extrapolation make sense only for molecular dynamics calculations
            - 'none': no extrapolation.
            - 'first_order': extrapolate the wave-functions with first-order formula.
            - 'second_order': as above, with second order formula."""
        ),
    )
    remove_rigid_rot: bool = Field(
        False,
        description=dedent(
            """\
            This keyword is useful when simulating the dynamics and/or the thermodynamics of an
            isolated system. If set to true the total torque of the internal forces is set to zero
            by adding new forces that compensate the spurious interaction with the periodic images.
            This allows for the use of smaller supercells.  BEWARE: since the potential energy is
            no longer consistent with the forces (it still contains the spurious interaction with
            the repeated images), the total energy is not conserved anymore. However the dynamical
            and thermodynamical properties should be in closer agreement with those of an isolated
            system. Also the final energy of a structural relaxation will be higher, but the
            relaxation itself should be faster."""
        ),
    )
    ion_temperature: Literal[
        "rescaling",
        "rescale-v",
        "rescale-T",
        "reduce-T",
        "nose",
        "berendsen",
        "andersen",
        "svr",
        "initial",
        "not_controlled",
    ] = Field(
        "not_controlled",
        description=dedent(
            """\
            Available options are:
            - 'rescaling': control ionic temperature via velocity rescaling (first method) see
              parameters tempw, tolp, and nraise (for VC-MD only).
            - 'rescale-v': control ionic temperature via velocity rescaling (second method) see
              parameters tempw and nraise.
            - 'rescale-T': scale temperature of the thermostat every nraise steps by delta_t,
              starting from tempw. The temperature is controlled via velocitiy rescaling.
            - 'reduce-T': reduce temperature of the thermostat every nraise steps by the (negative)
              value delta_t, starting from tempw. If  delta_t is positive, the target temperature
              is augmented. The temperature is controlled via velocitiy rescaling.
            - 'nose': control ionic temperature using Nose-Hoover thermostat. See also parameters
              fnosep , tempw , nhpcl, ndega , nhptyp.
            - 'berendsen': control ionic temperature using 'soft' velocity rescaling - see
              parameters tempw and nraise.
            - 'andersen': control ionic temperature using Andersen thermostat see parameters tempw
              and nraise.
            - 'svr': control ionic temperature using stochastic-velocity rescaling (Donadio, Bussi,
              Parrinello, J. Chem. Phys. 126, 014101, 2007), with parameters tempw and nraise.
            - 'initial': initialize ion velocities to temperature tempw and leave uncontrolled
              further on.
            - 'not_controlled': ionic temperature is not controlled."""
        ),
    )
    tempw: Annotated[float, Quantity(units="K", dimensionality="temperature")] = Field(
        300.0,
        description="Starting temperature in MD runs target temperature for most thermostats.",
    )
    fnosep: Annotated[float, Quantity(units="THz", dimensionality="time^-1")] = Field(
        1.0,
        description=dedent(
            """\
            oscillation frequency of the Nose thermorstat [note that 3 THz = 100 cm^-1], meaningful
            only with 'ion_temperature = 'nose'' for Nose-Hoover chain one can ser frequncies for
            all nhpcl thermostats ( fnosep = X Y Z etc.) If only first is set, the defaults for the
            others will be the same."""
        ),
    )
    nhpcl: int = Field(
        0,
        description=dedent(
            """\
            number of thermostats in the Nose-Hoover chain; currently maximum allowed is 4"""
        ),
    )
    nhptyp: Literal[0, 1, 2, 3] = Field(
        0,
        description=dedent(
            """\
            type of the 'massive' Nose-Hoover chain thermostat.
            - '0': uses one NH chain for all atoms.
            - '1': uses a NH chain per each atomic type.
            - '2': use a NH chaing per atom, this one is usefulf for extremely rapid equipartioning.
            - '3': together with nhgrp allows fine grained thermostat control."""
        ),
    )
    ndega: int = Field(
        0,
        description=dedent(
            """\
            number of degrees of freedom used for temperature calculation ndega <= 0 sets the
            number of degrees of freedom to [3*nat-abs(ndega)], ndega > 0 is used as the target
            number"""
        ),
    )
    tolp: Annotated[float, Quantity(units="K", dimensionality="temperature")] = Field(
        100.0,
        description=dedent(
            """\
            Tolerance for velocity rescaling. Velocities are rescaled if the run-averaged and
            target temperature differ more than tolp."""
        ),
    )
    delta_t: float = Field(
        1.0,
        description=dedent(
            """\
            if ion_temperature == 'rescale-T' : at each step the instantaneous temperature is
            multiplied by delta_t; this is done rescaling all the velocities.  if ion_temperature
            == 'reduce-T' : every 'nraise' steps the instantaneous temperature is reduced by
            -delta_t (i.e. delta_t < 0 is added to T)  The instantaneous temperature is calculated
            at the end of every ionic move and BEFORE rescaling. This is the temperature reported
            in the main output.  For delta_t < 0, the actual average rate of heating or cooling
            should be roughly C*delta_t/(nraise*dt) (C=1 for an ideal gas, C=0.5 for a harmonic
            solid, theorem of energy equipartition between all quadratic degrees of freedom)."""
        ),
    )
    nraise: int = Field(
        1,
        description=dedent(
            """\
            if ion_temperature == 'reduce-T' : every nraise steps the instantaneous temperature is
            reduced by -delta_t (i.e. delta_t is added to the temperature)  if ion_temperature ==
            'rescale-v' : every nraise steps the average temperature, computed from the last nraise
            steps, is rescaled to tempw  if ion_temperature == 'rescaling' and calculation ==
            'vc-md' : every nraise steps the instantaneous temperature is rescaled to tempw  if
            ion_temperature == 'berendsen' : the 'rise time' parameter is given in units of the
            time step: tau = nraise*dt, so dt/tau = 1/nraise  if ion_temperature == 'andersen' :
            the 'collision frequency' parameter is given as nu=1/tau defined above, so nu*dt =
            1/nraise  if ion_temperature == 'svr' : the 'characteristic time' of the thermostat is
            set to tau = nraise*dt"""
        ),
    )
    refold_pos: bool = Field(
        False,
        description=dedent(
            """\
            This keyword applies only in the case of molecular dynamics or damped dynamics. If true
            the ions are refolded at each step into the supercell."""
        ),
    )
    upscale: float = Field(
        100.0,
        description=dedent(
            """\
            Max reduction factor for conv_thr during structural optimization conv_thr is
            automatically reduced when the relaxation approaches convergence so that forces are
            still accurate, but conv_thr will not be reduced to less that conv_thr / upscale."""
        ),
    )
    bfgs_ndim: int = Field(
        1,
        description=dedent(
            """\
            Number of old forces and displacements vectors used in the PULAY (GDIIS) mixing of the
            residual vectors obtained on the basis of the inverse hessian matrix given by the BFGS
            algorithm. The variable  tgdiis_step in this case sets whether to use to full GDIIS
            step or the BFGS trust_radius. When bfgs_ndim = 1, the standard quasi-Newton BFGS
            method is used. (bfgs only)"""
        ),
    )
    tgdiis_step: bool = Field(
        True,
        description=dedent(
            """\
            When G-DIIS (bfgs_ndim > 1) is used for the structural relaxation this variable selects
            whether to use to full gdiis step or the BFGS trus radius. (bfgs only)"""
        ),
    )
    trust_radius_max: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        0.8, description="Maximum ionic displacement in the structural relaxation. (bfgs only)"
    )
    trust_radius_min: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        0.0001,
        description=dedent(
            """\
            Minimum ionic displacement in the structural relaxation BFGS is reset when trust_radius
            < trust_radius_min. (bfgs only)"""
        ),
    )
    trust_radius_ini: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        0.5, description="Initial ionic displacement in the structural relaxation. (bfgs only)"
    )
    w_1: float = Field(0.01, description="")
    w_2: float = Field(
        0.5, description="Parameters used in line search based on the Wolfe conditions. (bfgs only)"
    )
    fire_alpha_init: float = Field(
        0.2,
        description=dedent(
            """\
            Initial value of the alpha mixing factor in the FIRE minimization scheme; recommended
            values are between 0.1 and 0.3"""
        ),
    )
    fire_falpha: float = Field(
        0.99, description="Scaling of the alpha mixing parameter for steps with P > 0;"
    )
    fire_nmin: int = Field(
        5, description="Minimum number of steps with P > 0 before increase of dt"
    )
    fire_f_inc: float = Field(1.1, description="Factor for increasing dt")
    fire_f_dec: float = Field(0.5, description="Factor for decreasing dt")
    fire_dtmax: float = Field(
        10.0,
        description=dedent(
            """\
            Determines the maximum value of dt in the FIRE minimization; dtmax = fire_dtmax*dt"""
        ),
    )
    nhgrp: list[int] = Field(
        default_factory=list,
        description=dedent(
            """\
            specifies which thermostat group to use for given atomic type when >0 assigns all the
            atoms in this type to thermostat labeled nhgrp(i), when =0 each atom in the type gets
            its own thermostat. Finally, when <0, then this atomic type will have temperature 'not
            controlled'. Example: HCOOLi, with types H (1), C(2), O(3), Li(4); setting nhgrp={2 2 0
            -1} will add a common thermostat for both H & C, one thermostat per each O (2 in
            total), and a non-updated thermostat for Li which will effectively make temperature for
            Li 'not controlled (start = 1, end = ntyp)"""
        ),
    )
    fnhscl: list[float] | None = Field(
        None,
        json_schema_extra={"default_expr": "(Nat-1)/Nat"},
        description=dedent(
            """\
            these are the scaling factors to be used together with nhptyp=3 and nhgrp(i) in order
            to take care of possible reduction in the degrees of freedom due to constraints.
            Suppose that with the previous example HCOOLi, C-H bond is constrained. Then, these 2
            atoms will have 5 degrees of freedom in total instead of 6, and one can set fnhscl={5/6
            5/6 1. 1.}. This way the target kinetic energy for H&C will become 6(kT/2)*5/6 =
            5(kT/2). This option is to be used for simulations with many constraints, such as rigid
            water with something else in there (start = 1, end = ntyp)"""
        ),
    )


class CellNamelist(Namelist):
    """Pydantic model for the `CELL` namelist."""

    cell_dynamics: Literal["none", "sd", "damp-pr", "damp-w", "bfgs", "none", "pr", "w"] = Field(
        "none",
        description=dedent(
            """\
            Specify the type of dynamics for the cell. For different type of calculation different
            possibilities are allowed and different default values apply:  CASE ( calculation ==
            'vc-relax' )  CASE ( calculation == 'vc-md' )
            - 'none': no dynamics.
            - 'sd': steepest descent ( not implemented ).
            - 'damp-pr': damped (Beeman) dynamics of the Parrinello-Rahman extended lagrangian.
            - 'damp-w': damped (Beeman) dynamics of the new Wentzcovitch extended lagrangian.
            - 'bfgs': BFGS quasi-newton algorithm (default) ion_dynamics must be 'bfgs' too.
            - 'none': no dynamics.
            - 'pr': (Beeman) molecular dynamics of the Parrinello-Rahman extended lagrangian.
            - 'w': (Beeman) molecular dynamics of the new Wentzcovitch extended lagrangian."""
        ),
    )
    press: Annotated[float, Quantity(units="kbar", dimensionality="energy length^-3")] = Field(
        0.0, description="Target pressure in a variable-cell md or relaxation run."
    )
    wmass: Annotated[float | None, Quantity(units="amu", dimensionality="mass")] = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            Fictitious cell mass for variable-cell simulations (both 'vc-md' and 'vc-relax')  If
            not specified, it is computed from the total mass of the system as
            0.75*Tot_Mass/pi**2 for Parrinello-Rahman MD, and as
            0.75*Tot_Mass/pi**2/Omega**(2/3) for Wentzcovitch MD."""
        ),
    )
    cell_factor: float | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "variable-cell calculation", "value": "2.0"},
                {"when": None, "value": "1.0"},
            ],
        },
        description=dedent(
            """\
            Used in the construction of the pseudopotential tables. It should exceed the maximum
            linear contraction of the cell during a simulation."""
        ),
    )
    press_conv_thr: Annotated[float, Quantity(units="kbar", dimensionality="energy length^-3")] = (
        Field(
            0.5,
            description=dedent(
                """\
                Convergence threshold on the pressure for variable cell relaxation ('vc-relax' :
                note that the other convergence thresholds for ionic relaxation apply as well)."""
            ),
        )
    )
    cell_dofree: Literal[
        "all",
        "ibrav",
        "a",
        "b",
        "c",
        "fixa",
        "fixb",
        "fixc",
        "x",
        "y",
        "z",
        "xy",
        "xz",
        "yz",
        "xyz",
        "shape",
        "volume",
        "2Dxy",
        "2Dshape",
        "epitaxial_ab",
        "epitaxial_ac",
        "epitaxial_bc",
    ] = Field(
        "all",
        description=dedent(
            """\
            Select which of the cell parameters should be moved:  BEWARE: if axis are not
            orthogonal, some of these options do not work (symmetry is broken). If you are not
            happy with them, edit subroutine init_dofree in file Modules/cell_base.f90
            - 'all': all axis and angles are moved.
            - 'ibrav': all axis and angles are moved, but the lattice remains consistent with the
              initial ibrav choice. You can use this option in combination with any other one by
              specifying 'ibrav+option'. Please note that some combinations do not make sense for
              some crystals and will guarantee that the relax will never converge. E.g.
              'ibrav+2Dxy' is not a problem for hexagonal cells, but will never converge for cubic
              ones.
            - 'a': the x component of axis 1 (v1_x) is fixed.
            - 'b': the y component of axis 2 (v2_y) is fixed.
            - 'c': the z component of axis 3 (v3_z) is fixed.
            - 'fixa': axis 1 (v1_x,v1_y,v1_z) is fixed.
            - 'fixb': axis 2 (v2_x,v2_y,v2_z) is fixed.
            - 'fixc': axis 3 (v3_x,v3_y,v3_z) is fixed.
            - 'x': only the x component of axis 1 (v1_x) is moved.
            - 'y': only the y component of axis 2 (v2_y) is moved.
            - 'z': only the z component of axis 3 (v3_z) is moved.
            - 'xy': only v1_x and v2_y are moved.
            - 'xz': only v1_x and v3_z are moved.
            - 'yz': only v2_y and v3_z are moved.
            - 'xyz': only v1_x, v2_y, v3_z are moved.
            - 'shape': all axis and angles, keeping the volume fixed.
            - 'volume': the volume changes, keeping all angles fixed (i.e. only celldm(1) changes).
            - '2Dxy': only x and y components are allowed to change.
            - '2Dshape': as above, keeping the area in xy plane fixed.
            - 'epitaxial_ab': fix axis 1 and 2 while allowing axis 3 to move.
            - 'epitaxial_ac': fix axis 1 and 3 while allowing axis 2 to move.
            - 'epitaxial_bc': fix axis 2 and 3 while allowing axis 1 to move."""
        ),
    )


class FcpNamelist(Namelist):
    """Pydantic model for the `FCP` namelist."""

    fcp_mu: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(
        ...,
        description=dedent(
            """\
            The target Fermi energy. One can start with appropriate total charge of the system by
            giving tot_charge ."""
        ),
    )
    fcp_dynamics: Literal["none", "bfgs", "newton", "damp", "lm", "velocity-verlet", "verlet"] = (
        Field(
            "none",
            description=dedent(
                """\
                Specify the type of dynamics for the Fictitious Charge Particle (FCP).  For
                different type of calculation different possibilities are allowed and different
                default values apply:  CASE ( calculation == 'relax' )  CASE ( calculation == 'md' )
                - 'none': no FCP dynamics.
                - 'bfgs': (default) BFGS quasi-newton algorithm, coupling with ions relaxation
                  ion_dynamics must be 'bfgs' too.
                - 'newton': Newton-Raphson algorithm with DIIS ion_dynamics must be 'damp' too.
                - 'damp': damped (quick-min Verlet) dynamics for FCP relaxation ion_dynamics must
                  be 'damp' too.
                - 'lm': Line-Minimization algorithm for FCP relaxation ion_dynamics must be 'damp'
                  too.
                - 'velocity-verlet': (default) Velocity-Verlet algorithm to integrate Newton's
                  equation. ion_dynamics must be 'verlet' too.
                - 'verlet': Verlet algorithm to integrate Newton's equation. ion_dynamics must be
                  'verlet' too."""
            ),
        )
    )
    fcp_conv_thr: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(
        0.01, description="Convergence threshold on force for FCP relaxation."
    )
    fcp_ndiis: int = Field(
        4, description="Size of DIIS for FCP relaxation, used only if fcp_dynamics = 'newton'."
    )
    fcp_mass: float | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "esm_bc=='bc2' || esm_bc=='bc3'", "value": "5.D+6 / xy_area"},
                {"when": None, "value": "5.D+4 / xy_area"},
            ],
        },
        description="Mass of the FCP.",
    )
    fcp_velocity: float | None = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            Initial velocity of the FCP. If not specified, it is determined by fcp_temperature."""
        ),
    )
    fcp_temperature: Literal[
        None,
        "rescaling",
        "rescale-v",
        "rescale-T",
        "reduce-T",
        "berendsen",
        "andersen",
        "initial",
        "not_controlled",
    ] = Field(
        None,
        json_schema_extra={"default_ref": "ion_temperature"},
        description=dedent(
            """\
            Available options are:
            - 'rescaling': control FCP's temperature via velocity rescaling (first method) see
              parameters fpc_tempw and fcp_tolp.
            - 'rescale-v': control FCP's temperature via velocity rescaling (second method) see
              parameters fcp_tempw and fcp_nraise.
            - 'rescale-T': control FCP's temperature via velocity rescaling (third method) see
              parameter fcp_delta_t.
            - 'reduce-T': reduce FCP's temperature every fcp_nraise steps by the (negative) value
              fcp_delta_t.
            - 'berendsen': control FCP's temperature using 'soft' velocity rescaling - see
              parameters fcp_tempw and fcp_nraise.
            - 'andersen': control FCP's temperature using Andersen thermostat see parameters
              fcp_tempw and fcp_nraise.
            - 'initial': initialize FCP's velocities to temperature fcp_tempw and leave
              uncontrolled further on.
            - 'not_controlled': FCP's temperature is not controlled."""
        ),
    )
    fcp_tempw: Annotated[float | None, Quantity(units="K", dimensionality="temperature")] = Field(
        None,
        json_schema_extra={"default_ref": "tempw"},
        description=dedent(
            """\
            Starting temperature in FCP dynamics runs target temperature for most thermostats."""
        ),
    )
    fcp_tolp: Annotated[float | None, Quantity(units="K", dimensionality="temperature")] = Field(
        None,
        json_schema_extra={"default_ref": "tolp"},
        description=dedent(
            """\
            Tolerance for velocity rescaling. Velocities are rescaled if the run-averaged and
            target temperature differ more than tolp."""
        ),
    )
    fcp_delta_t: float | None = Field(
        None,
        json_schema_extra={"default_ref": "delta_t"},
        description=dedent(
            """\
            if fcp_temperature == 'rescale-T' : at each step the instantaneous temperature is
            multiplied by fcp_delta_t; this is done rescaling all the velocities.  if
            fcp_temperature == 'reduce-T' : every fcp_nraise steps the instantaneous temperature is
            reduced by -fcp_delta_t (i.e. fcp_delta_t < 0 is added to T)  The instantaneous
            temperature is calculated at the end of FCP's move and BEFORE rescaling. This is the
            temperature reported in the main output.  For fcp_delta_t < 0, the actual average rate
            of heating or cooling should be roughly C*fcp_delta_t/(fcp_nraise*dt) (C=1 for an ideal
            gas, C=0.5 for a harmonic solid, theorem of energy equipartition between all quadratic
            degrees of freedom)."""
        ),
    )
    fcp_nraise: int | None = Field(
        None,
        json_schema_extra={"default_ref": "nraise"},
        description=dedent(
            """\
            if fcp_temperature == 'reduce-T' : every fcp_nraise steps the instantaneous temperature
            is reduced by -fcp_delta_t (i.e. fcp_delta_t is added to the temperature)  if
            fcp_temperature == 'rescale-v' : every fcp_nraise steps the average temperature,
            computed from the last fcp_nraise steps, is rescaled to fcp_tempw  if fcp_temperature
            == 'berendsen' : the 'rise time' parameter is given in units of the time step: tau =
            fcp_nraise*dt, so dt/tau = 1/fcp_nraise  if fcp_temperature == 'andersen' : the
            'collision frequency' parameter is given as nu=1/tau defined above, so nu*dt =
            1/fcp_nraise"""
        ),
    )
    freeze_all_atoms: bool = Field(
        False,
        description="If .TRUE., freeze all atoms to perform relaxation or dynamics only with FCP.",
    )


class RismNamelist(Namelist):
    """Pydantic model for the `RISM` namelist."""

    nsolv: int = Field(
        ..., description="The number of solvents (i.e. molecular species) in the unit cell"
    )
    closure: Literal["kh", "hnc"] = Field(
        "kh",
        description=dedent(
            """\
            Specify the type of closure equation:
            - 'kh': The Kovalenko and Hirata's model. [A.Kovalenko, F.Hirata, JCP 110, 10095
              (1999), doi:10.1063/1.478883 (https://doi.org/10.1063/1.478883)].
            - 'hnc': The HyperNetted-Chain model, which is suitable only for solvents without
              charge. [J.P.Hansen et al., Theory of simple liquids. Academic Press, London,
              1990]."""
        ),
    )
    tempv: Annotated[float, Quantity(units="K", dimensionality="temperature")] = Field(
        300.0, description="Temperature of solvents."
    )
    ecutsolv: Annotated[float | None, Quantity(units="Ry", dimensionality="energy")] = Field(
        None,
        json_schema_extra={"default_expr": "4 * ecutwfc"},
        description=dedent(
            """\
            Kinetic energy cutoff for solvent's correlation functions. If a solute is an isolated
            system or slab, you may allowed to use default value. For a frameworked or porous
            solute (e.g. Zeolite, MOF), it is desirable to apply a larger value. Solvents confined
            in a framework often have a high frequency."""
        ),
    )
    starting1d: Literal["zero", "file", "fix"] = Field(
        "zero",
        description=dedent(
            """\
            - 'zero': Starting correlation functions of 1D-RISM from zero. ( default for scf,
              *relax, *md ).
            - 'file': Start from existing '1d-rism_csvv_r.xml' file in the directory specified by
              variables 'prefix' and 'outdir'.
            - 'fix': Read from existing '1d-rism_csvv_r.xml' file in the directory specified by
              variables 'prefix' and 'outdir', and never calculate 1D-RISM. For nscf and bands
              calculation this is the default."""
        ),
    )
    starting3d: Literal["zero", "file"] = Field(
        "zero",
        description=dedent(
            """\
            - 'zero': Starting correlation functions of 3D-RISM from zero. ( default for scf,
              *relax, *md ).
            - 'file': Start from existing '3d-rism_csuv_r.dat' file in the directory specified
              by variables 'prefix' and 'outdir'. For nscf and bands calculation this is the
              default."""
        ),
    )
    smear1d: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        2.0, description="Coulomb smearing radius for 1D-RISM."
    )
    smear3d: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        2.0, description="Coulomb smearing radius for 3D-RISM."
    )
    rism1d_maxstep: int = Field(
        50000, description="Maximum number of iterations in a 1D-RISM step."
    )
    rism3d_maxstep: int = Field(5000, description="Maximum number of iterations in a 3D-RISM step.")
    rism1d_conv_thr: float = Field(1e-08, description="Convergence threshold for 1D-RISM.")
    rism3d_conv_thr: float | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "lgcscf==.FALSE.", "value": "1e-05"},
                {"when": None, "value": "5e-06"},
            ],
        },
        description="Convergence threshold for 3D-RISM.",
    )
    mdiis1d_size: int = Field(20, description="Size of Modified DIIS (MDIIS) for 1D-RISM.")
    mdiis3d_size: int = Field(10, description="Size of Modified DIIS (MDIIS) for 3D-RISM.")
    mdiis1d_step: float = Field(0.5, description="Step of Modified DIIS (MDIIS) for 1D-RISM.")
    mdiis3d_step: float = Field(0.8, description="Step of Modified DIIS (MDIIS) for 3D-RISM.")
    rism1d_bond_width: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        0.0,
        description=dedent(
            """\
            Gaussian width of bonds to smear intra-molecular correlation for 1D-RISM. If 3D-RISM
            calculation, default is 0. If Laue-RISM calculation, default is 2 / SQRT(ecutwfc)."""
        ),
    )
    rism1d_dielectric: float = Field(
        -1.0,
        description=dedent(
            """\
            Dielectric constant for 1D-RISM. If rism1d_dielectric > 0, dielectrically consistent
            RISM (DRISM) is performed.  For details of DRISM, see: J.S.Perkyns and B.M.Pettitt, CPL
            1992, 190, 626, doi:10.1016/0009-2614(92)85201-K
            (https://doi.org/10.1016/0009-2614(92)85201-K)"""
        ),
    )
    rism1d_molesize: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        2.0,
        description=dedent(
            """\
            Size of solvent molecules for 1D-RISM. This is used only if rism1d_dielectric > 0. If
            you have large molecules, you have to set ~ 20 a.u. ."""
        ),
    )
    rism1d_nproc: int = Field(128, description="Number of processes to calculate 1D-RISM.")
    rism3d_conv_level: float | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "laue_both_hands==.TRUE.", "value": "0.5"},
                {"when": "lgcscf==.TRUE.", "value": "0.3"},
                {"when": None, "value": "0.1"},
            ],
        },
        description="",
    )
    rism3d_planar_average: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE., planar averages of solvent densities and potentials are calculated and
            written to 'prefix.rism1'. For 3D-RISM, default is .FALSE. For Laue-RISM, default is
            .TRUE."""
        ),
    )
    laue_nfit: int = Field(
        4,
        description=dedent(
            """\
            The number of z-grid points for the polynomial fit along the cell edge. This is only
            for Laue-RISM."""
        ),
    )
    laue_expand_right: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        -1.0,
        description=dedent(
            """\
            If positive value, set the ending position offset [in a.u.] of the solvent region on
            right-hand side of the unit cell, measured relative to the unit cell edge. (the solvent
            region ends at z = + [L_z/2 + laue_expand_right].) This is only for Laue-RISM."""
        ),
    )
    laue_expand_left: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        -1.0,
        description=dedent(
            """\
            If positive value, set the ending position offset [in a.u.] of the solvent region on
            left-hand side of the unit cell, measured relative to the unit cell edge. (the solvent
            region ends at z = - [L_z/2 + laue_expand_left].) This is only for Laue-RISM."""
        ),
    )
    laue_starting_right: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        0.0,
        description=dedent(
            """\
            Set the starting position [in a.u.] of the solvent region on right-hand side of the
            unit cell. Then the solvent region is defined as [ laue_starting_right , L_z/2 +
            laue_expand_right ], where distribution functions are finite. This is only for
            Laue-RISM."""
        ),
    )
    laue_starting_left: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        0.0,
        description=dedent(
            """\
            Set the starting position [in a.u.] of the solvent region on left-hand side of the unit
            cell. Then the solvent region is defined as [ -L_z/2 - laue_expand_left ,
            laue_starting_left ], where distribution functions are finite. This is only for
            Laue-RISM."""
        ),
    )
    laue_buffer_right: Annotated[float | None, Quantity(units="bohr", dimensionality="length")] = (
        Field(
            None,
            json_schema_extra={
                "conditional_default": [
                    {"when": "laue_expand_right > 0.0", "value": "8.0"},
                    {"when": None, "value": "-1.0"},
                ],
            },
            description=dedent(
                """\
                If positive value, set the buffering length [in a.u.] of the solvent region on
                right-hand side of the unit cell. Then correlation functions are defined inside of
                [ laue_starting_right - laue_buffer_right , L_z/2 + laue_expand_right ]. This is
                only for Laue-RISM."""
            ),
        )
    )
    laue_buffer_left: Annotated[float | None, Quantity(units="bohr", dimensionality="length")] = (
        Field(
            None,
            json_schema_extra={
                "conditional_default": [
                    {"when": "laue_expand_left > 0.0", "value": "8.0"},
                    {"when": None, "value": "-1.0"},
                ],
            },
            description=dedent(
                """\
                If positive value, set the buffering length [in a.u.] of the solvent region on
                left-hand side of the unit cell. Then correlation functions are defined inside of [
                -L_z/2 - laue_expand_left , laue_starting_left + laue_buffer_left ]. This is only
                for Laue-RISM."""
            ),
        )
    )
    laue_both_hands: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE., you can set different densities to the solvent regions of right-hand side
            and left-hand side. See SOLVENTS card."""
        ),
    )
    laue_wall: Literal["none", "auto", "manual"] = Field(
        "auto",
        description=dedent(
            """\
            Set the repulsive wall with (1/r)^12 term of Lennard-Jones potential. This is only for
            Laue-RISM.
            - 'none': The repulsive wall is not defined.
            - 'auto': The repulsive wall is defined, whose edge position is set automatically. One
              does not have to set laue_wall_z (the edge position).
            - 'manual': The repulsive wall is defined, whose edge position is set manually. One
              have to set laue_wall_z (the edge position)."""
        ),
    )
    laue_wall_z: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        0.0,
        description=dedent(
            """\
            Set the edge position [in a.u.] of the repulsive wall. If laue_expand_right > 0.0, the
            repulsive wall is defined on [ -inf , laue_wall_z ]. If laue_expand_left > 0.0, the
            repulsive wall is defined on [ laue_wall_z , inf ]. This is only for Laue-RISM and
            laue_wall == 'manual' ."""
        ),
    )
    laue_wall_rho: Annotated[float, Quantity(units="bohr^-3", dimensionality="length^-3")] = Field(
        0.01,
        description=dedent(
            """\
            The density (1/bohr^3) of the repulsive wall. This is only for Laue-RISM and laue_wall
            /= 'none' ."""
        ),
    )
    laue_wall_epsilon: Annotated[float, Quantity(units="kcal mol^-1", dimensionality="energy")] = (
        Field(
            0.1,
            description=dedent(
                """\
                The Lennard-Jones potential of the repulsive wall. Here, you can set the parameter
                'epsilon'. This is only for Laue-RISM and laue_wall /= 'none' ."""
            ),
        )
    )
    laue_wall_sigma: Annotated[float, Quantity(units="angstrom", dimensionality="length")] = Field(
        4.0,
        description=dedent(
            """\
            The Lennard-Jones potential of the repulsive wall. Here, you can set the parameter
            'sigma'. This is only for Laue-RISM and laue_wall /= 'none' ."""
        ),
    )
    laue_wall_lj6: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE., the attractive term -(1/r)^6 of Lennard-Jones potential is added. This is
            only for Laue-RISM and laue_wall /= 'none' ."""
        ),
    )
    solute_lj: list[str] = Field(default_factory=list, description="(start = 1, end = ntyp)")
    solute_epsilon: Annotated[
        list[float] | None, Quantity(units="kcal mol^-1", dimensionality="energy")
    ] = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            The Lennard-Jones potential of solute on atomic type 'i'. Here, you can set the
            parameter 'epsilon'. (start = 1, end = ntyp)"""
        ),
    )
    solute_sigma: Annotated[
        list[float] | None, Quantity(units="angstrom", dimensionality="length")
    ] = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            The Lennard-Jones potential of solute on atomic type 'i'. Here, you can set the
            parameter 'sigma'. (start = 1, end = ntyp)"""
        ),
    )


class PWInput(EspressoInput):
    """Pydantic model for the input of `pw.x`."""

    control: ControlNamelist = Field(default_factory=lambda: ControlNamelist())
    system: SystemNamelist | None = Field(None)
    electrons: ElectronsNamelist = Field(default_factory=lambda: ElectronsNamelist())
    ions: IonsNamelist = Field(default_factory=lambda: IonsNamelist())
    cell: CellNamelist = Field(default_factory=lambda: CellNamelist())
    fcp: FcpNamelist | None = Field(None)
    rism: RismNamelist | None = Field(None)
    atomic_species: list[AtomicSpecies] = Field(default_factory=list)
    atomic_positions: AtomicPositionsCard = Field(..., discriminator="unit")
    k_points: KPointsCard = Field(discriminator="kind")
    additional_k_points: KPointsCard | None = Field(None, discriminator="kind")
    cell_parameters: CellParametersCard = Field(..., discriminator="unit")
    constraints: list[Constraint] = Field(default_factory=list)
    occupations: (
        tuple[list[PositiveFloat0to2]]
        | tuple[list[PositiveFloat0to1], list[PositiveFloat0to1]]
        | None
    ) = Field(None)
    atomic_velocities: list[AtomicVelocity] = Field(default_factory=list)
    atomic_forces: list[AtomicForce] = Field(default_factory=list)
    solvents: SolventsCard | SolventsLRCard | None = Field(None)
    hubbard: HubbardCard | None = Field(None)
