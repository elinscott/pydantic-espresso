"""Pydantic model for the input of `cp.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from textwrap import dedent
from typing import Annotated, Literal

from pydantic import Field, field_validator

from pydantic_espresso.base import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class ControlNamelist(Namelist):
    """Pydantic model for the `CONTROL` namelist."""

    @field_validator("calculation", mode="before")
    @classmethod
    def map_calculation(cls, v: str) -> str:
        """Map equivalent values for `calculation` onto a canonical value."""
        mapping = {"md": "cp", "bands": "nscf", "vc-md": "vc-cp"}
        return mapping.get(v, v)

    @field_validator("verbosity", mode="before")
    @classmethod
    def map_verbosity(cls, v: str) -> str:
        """Map equivalent values for `verbosity` onto a canonical value."""
        mapping = {"default": "low"}
        return mapping.get(v, v)

    calculation: Literal[
        None,
        "cp",
        "scf",
        "nscf",
        "relax",
        "vc-relax",
        "vc-cp",
        "cp-wf",
        "vc-cp-wf",
        "cp-wf-nscf",
        "ensemble",
    ] = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "prog=='PW'", "value": "'scf'"},
                {"when": None, "value": "'cp'"},
            ],
        },
        description=dedent(
            """\
            A string describing the task to be performed. (vc = variable-cell; wf = Wannier
            functions). Options are:
            - 'cp': Car-Parrinello molecular dynamics (the CP equivalent of calculation='md').
            - 'scf': self-consistent field calculation.
            - 'nscf': non-self-consistent field calculation.
            - 'relax': ionic relaxation (damped electronic and ionic dynamics).
            - 'vc-relax': variable-cell ionic+cell relaxation.
            - 'vc-cp': variable-cell Car-Parrinello molecular dynamics.
            - 'cp-wf': Car-Parrinello molecular dynamics with Wannier functions (e.g. for hybrid
              functionals).
            - 'vc-cp-wf': variable-cell Car-Parrinello molecular dynamics with Wannier functions.
            - 'cp-wf-nscf': non-self-consistent Car-Parrinello calculation with Wannier functions.
            - 'ensemble': ensemble-DFT (eDFT) calculation; see also occupations."""
        ),
    )
    title: str | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "prog=='PW'", "value": "''"},
                {"when": None, "value": "'MD Simulation '"},
            ],
        },
        description="reprinted on output.",
    )
    verbosity: Literal["debug", "high", "medium", "low", "minimal"] = Field(
        "low",
        description=dedent(
            """\
            In order of decreasing verbose output:
            - 'debug': maximum verbosity.
            - 'high': high verbosity.
            - 'medium': medium verbosity.
            - 'low': default verbosity.
            - 'minimal': minimal verbosity."""
        ),
    )
    isave: int | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "prog=='PW'", "value": "0"},
                {"when": None, "value": "100"},
            ],
        },
        description=dedent(
            """\
            Number of steps between successive savings of information needed to restart the run."""
        ),
    )
    restart_mode: Literal[None, "from_scratch", "restart", "reset_counters", "auto"] = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "prog=='PW'", "value": "'from_scratch'"},
                {"when": None, "value": "'restart'"},
            ],
        },
        description=dedent(
            """\
            Available options are:
            - 'from_scratch': from scratch.
            - 'restart': from previous interrupted run.
            - 'reset_counters': continue a previous simulation, perform nstep new steps, resetting
              the counter and averages.
            - 'auto': autopilot: detect the presence of restart files and automatically choose
              between 'from_scratch' and 'restart'."""
        ),
    )
    nstep: int = Field(50, description="number of Car-Parrinello steps performed in this run")
    iprint: int | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "prog=='PW'", "value": "100000"},
                {"when": None, "value": "10"},
            ],
        },
        description=dedent(
            """\
            Number of steps between successive writings of relevant physical quantities to files
            named as 'prefix.???' depending on 'prefix' parameter. In the standard output relevant
            quantities are written every 10*iprint steps."""
        ),
    )
    tstress: bool = Field(
        False,
        description=dedent(
            """\
            Write stress tensor to standard output each 'iprint' steps. It is set to .TRUE.
            automatically if calculation='vc-relax"""
        ),
    )
    tprnfor: bool = Field(False, description="print forces. Set to .TRUE. when ions are moving.")
    dt: Annotated[
        float | None, Quantity(units="bohr electron_mass^1/2 Hartree^-1/2", dimensionality="time")
    ] = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "prog=='PW'", "value": "20.D0"},
                {"when": None, "value": "1.D0"},
            ],
        },
        description=dedent(
            """\
            time step for molecular dynamics, in Hartree atomic units (1 a.u.=2.4189 * 10^-17 s :
            beware, PW code use Rydberg atomic units, twice that much!!!)"""
        ),
    )
    outdir: Path | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "ESPRESSO_TMPDIR is set", "value": "from_environment"},
                {"when": None, "value": "'./'"},
            ],
        },
        description="input, temporary, trajectories and output files are found in this directory.",
    )
    saverho: bool = Field(
        True,
        description=dedent(
            """\
            This flag controls the saving of charge density in CP codes: If  .TRUE.        save
            charge density to restart dir, If .FALSE. do not save charge density."""
        ),
    )
    prefix: str | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "prog=='PW'", "value": "'pwscf'"},
                {"when": None, "value": "'cp'"},
            ],
        },
        description=dedent(
            """\
            prepended to input/output filenames and restart folders: prefix.pos : atomic positions
            prefix.vel : atomic velocities prefix.for : atomic forces prefix.cel : cell parameters
            prefix.str : stress tensors prefix.evp : energies prefix.hrs : Hirshfeld effective
            volumes (ts-vdw) prefix.eig : eigen values prefix.nos : Nose-Hoover variables
            prefix.spr : spread of Wannier orbitals prefix.wfc : center of Wannier orbitals
            prefix.ncg : number of Poisson CG steps (PBE0) prefix_ndw.save/ : write restart folder
            prefix_ndr.save/ : read restart folder where ndr and ndw are the integers number
            described below"""
        ),
    )
    ndr: int = Field(
        50,
        description=dedent(
            """\
            The restart files are read from the folder outdir/prefix_ndr.save/ where outdir, prefix
            and ndr are the input variables described in this document"""
        ),
    )
    ndw: int = Field(
        50,
        description=dedent(
            """\
            The restart files are written, if ndw > 0, in the folder outdir/prefix_ndw.save/ where
            outdir, prefix and ndw are the input variables described in this document"""
        ),
    )
    tabps: bool = Field(
        False,
        description=dedent(
            """\
            .true. to compute the volume and/or the surface of an isolated system for finite
            pressure/finite surface tension calculations (PRL 94, 145501 (2005)
            (https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.94.145501); JCP 124, 074103
            (2006))."""
        ),
    )
    max_seconds: Annotated[float, Quantity(units="s", dimensionality="time")] = Field(
        1.0e7,
        description=dedent(
            """\
            jobs stops after max_seconds CPU time. Used to prevent a hard kill from the queuing
            system."""
        ),
    )
    etot_conv_thr: Annotated[float, Quantity(units="Hartree", dimensionality="energy")] = Field(
        1.0e-4,
        description=dedent(
            """\
            convergence threshold on total energy for ionic minimization: the convergence criterion
            is satisfied when the total energy changes less than etot_conv_thr between two
            consecutive scf steps. See also forc_conv_thr - both criteria must be satisfied"""
        ),
    )
    forc_conv_thr: Annotated[
        float, Quantity(units="Hartree bohr^-1", dimensionality="energy length^-1")
    ] = Field(
        1.0e-3,
        description=dedent(
            """\
            convergence threshold on forces for ionic minimization: the convergence criterion is
            satisfied when all components of all forces are smaller than forc_conv_thr. See also
            etot_conv_thr - both criteria must be satisfied"""
        ),
    )
    ekin_conv_thr: Annotated[float, Quantity(units="Hartree", dimensionality="energy")] = Field(
        1.0e-6,
        description=dedent(
            """\
            convergence criterion for electron minimization: convergence is achieved when 'ekin <
            ekin_conv_thr'. See also etot_conv_thr - both criteria must be satisfied."""
        ),
    )
    disk_io: Literal["default", "high"] = Field(
        "default",
        description=dedent(
            """\
            Controls how much information CP writes to disk. Only 'high' triggers the writing of
            additional data needed for restarting with PW or for postprocessing tools; any other
            value produces a data file that is not readable by PW or PostProc.
            - 'default': standard CP output: data file written by CP is not intended to be read by
              PW or PostProc.
            - 'high': CP will write Kohn-Sham wavefunction files and additional information in the
              data file so that the run can be restarted with a PW calculation or used with
              postprocessing tools."""
        ),
    )
    memory: Literal["default", "small", "large"] = Field(
        "default",
        description=dedent(
            """\
            Controls the memory/disk usage strategy.
            - 'default': standard memory usage.
            - 'small': memory-saving tricks are enabled. Currently: - the G-vectors are sorted only
              locally, not globally - they are not collected and written to file For large systems,
              the memory and time gain is sizable but the resulting data files are not portable -
              use it only if you do not need to re-read the data file. Not compatible with
              wf_collect = .TRUE. in CP.
            - 'large': favour speed and convenience over memory usage."""
        ),
    )
    pseudo_dir: Path | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "ESPRESSO_PSEUDO is set", "value": "from_environment"},
                {"when": None, "value": "'$HOME/espresso/pseudo/'"},
            ],
        },
        description="directory containing pseudopotential files",
    )
    tefield: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE. a homogeneous finite electric field described through the modern theory of
            the polarization is applied."""
        ),
    )


class SystemNamelist(Namelist):
    """Pydantic model for the `SYSTEM` namelist."""

    @field_validator("occupations", mode="before")
    @classmethod
    def map_occupations(cls, v: str) -> str:
        """Map equivalent values for `occupations` onto a canonical value."""
        mapping = {"ensemble-dft": "ensemble", "edft": "ensemble"}
        return mapping.get(v, v)

    @field_validator("smearing", mode="before")
    @classmethod
    def map_smearing(cls, v: str) -> str:
        """Map equivalent values for `smearing` onto a canonical value."""
        mapping = {
            "g": "gaussian",
            "f-d": "fermi-dirac",
            "fd": "fermi-dirac",
            "h-d": "hermite-delta",
            "hd": "hermite-delta",
            "g-s": "gaussian-splines",
            "gs": "gaussian-splines",
            "c-s": "cold-smearing",
            "cs": "cold-smearing",
            "cs1": "cold-smearing",
            "m-v": "marzari-vanderbilt",
            "mv": "marzari-vanderbilt",
            "cs2": "marzari-vanderbilt",
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
            "TS": "tkatchenko-scheffler",
            "ts": "tkatchenko-scheffler",
            "ts-vdw": "tkatchenko-scheffler",
            "ts-vdW": "tkatchenko-scheffler",
            "xdm": "XDM",
        }
        return mapping.get(v, v)

    @field_validator("assume_isolated", mode="before")
    @classmethod
    def map_assume_isolated(cls, v: str) -> str:
        """Map equivalent values for `assume_isolated` onto a canonical value."""
        mapping = {"m-p": "makov-payne", "mp": "makov-payne"}
        return mapping.get(v, v)

    ibrav: Literal[0, 1, 2, 3, -3, 4, 5, -5, 6, 7, 8, 9, -9, 91, 10, 11, 12, -12, 13, -13, 14] = (
        Field(
            ...,
            description=dedent(
                """\
                Bravais-lattice index. If ibrav /= 0, specify EITHER [ celldm(1)-celldm(6) ] OR [
                A, B, C, cosAB, cosAC, cosBC ] but NOT both. The lattice parameter 'alat' is set to
                alat = celldm(1) (in a.u.) or alat = A (in Angstrom); see below for the other
                parameters. For ibrav=0 specify the lattice vectors in CELL_PARAMETERS, optionally
                the lattice parameter alat = celldm(1) (in a.u.) or = A (in Angstrom), or else it
                is taken from CELL_PARAMETERS.  The columns 'celldm(2)-celldm(6)' /
                'b,c,cosbc,cosac,cosab' below indicate which additional crystallographic constants
                must be set for each value of ibrav.
                - '0': free crystal axis provided in input via card CELL_PARAMETERS.
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
                  - 2*sqrt(2)*ty,  v = tz + sqrt(2)*ty and tx, ty, tz as for case ibrav=5. Note: if
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
                  celldm(4)=cos(gamma) v1 = (  a/2,         0,                -c/2), v2 =
                  (b*cos(gamma), b*sin(gamma),       0  ), v3 = (  a/2,         0,
                  c/2), where gamma=angle between axis a and b projected on xy plane.
                - '-13': Monoclinic base-centered (unique axis b) celldm(2)=b/a, celldm(3)=c/a,
                  celldm(5)=cos(beta) v1 = (  a/2,       b/2,             0), v2 = ( -a/2,
                  b/2,             0), v3 = (c*cos(beta),   0,   c*sin(beta)), where beta=angle
                  between axis a and c projected on xz plane. IMPORTANT NOTICE: until QE v.6.4.1,
                  axis for ibrav=-13 had a different definition: v1(old) = v2(now), v2(old) =
                  -v1(now).
                - '14': Triclinic                       celldm(2)= b/a, celldm(3)= c/a, celldm(4)=
                  cos(bc), celldm(5)= cos(ac), celldm(6)= cos(ab) v1 = (a, 0, 0), v2 =
                  (b*cos(gamma), b*sin(gamma), 0) v3 = (c*cos(beta),
                  c*(cos(alpha)-cos(beta)cos(gamma))/sin(gamma), c*sqrt( 1 +
                  2*cos(alpha)cos(beta)cos(gamma) - cos(alpha)^2-cos(beta)^2-cos(gamma)^2
                  )/sin(gamma) ) where alpha is the angle between axis b and c, beta is the angle
                  between axis a and c, gamma is the angle between axis a and b."""
            ),
        )
    )
    A: Annotated[
        float | None, Quantity(units="1-3:angstrom", dimensionality="1-3:length 4-6:dimensionless")
    ] = Field(
        None,
        description=dedent(
            """\
            Traditional crystallographic constants: a,b,c cosAB = cosine of the angle between axis
            a and b (gamma) cosAC = cosine of the angle between axis a and c (beta) cosBC = cosine
            of the angle between axis b and c (alpha) The axis are chosen according to the value of
            'ibrav'. Specify either these OR 'celldm' but NOT both. Only needed values (depending
            on 'ibrav') must be specified The lattice parameter alat = A If ibrav = 0, only A is
            used if present; cell vectors are read from card CELL_PARAMETERS"""
        ),
    )
    B: Annotated[
        float | None, Quantity(units="1-3:angstrom", dimensionality="1-3:length 4-6:dimensionless")
    ] = Field(
        None,
        description=dedent(
            """\
            Traditional crystallographic constants: a,b,c cosAB = cosine of the angle between axis
            a and b (gamma) cosAC = cosine of the angle between axis a and c (beta) cosBC = cosine
            of the angle between axis b and c (alpha) The axis are chosen according to the value of
            'ibrav'. Specify either these OR 'celldm' but NOT both. Only needed values (depending
            on 'ibrav') must be specified The lattice parameter alat = A If ibrav = 0, only A is
            used if present; cell vectors are read from card CELL_PARAMETERS"""
        ),
    )
    C: Annotated[
        float | None, Quantity(units="1-3:angstrom", dimensionality="1-3:length 4-6:dimensionless")
    ] = Field(
        None,
        description=dedent(
            """\
            Traditional crystallographic constants: a,b,c cosAB = cosine of the angle between axis
            a and b (gamma) cosAC = cosine of the angle between axis a and c (beta) cosBC = cosine
            of the angle between axis b and c (alpha) The axis are chosen according to the value of
            'ibrav'. Specify either these OR 'celldm' but NOT both. Only needed values (depending
            on 'ibrav') must be specified The lattice parameter alat = A If ibrav = 0, only A is
            used if present; cell vectors are read from card CELL_PARAMETERS"""
        ),
    )
    cosAB: Annotated[  # noqa: N815
        float | None, Quantity(units="1-3:angstrom", dimensionality="1-3:length 4-6:dimensionless")
    ] = Field(
        None,
        description=dedent(
            """\
            Traditional crystallographic constants: a,b,c cosAB = cosine of the angle between axis
            a and b (gamma) cosAC = cosine of the angle between axis a and c (beta) cosBC = cosine
            of the angle between axis b and c (alpha) The axis are chosen according to the value of
            'ibrav'. Specify either these OR 'celldm' but NOT both. Only needed values (depending
            on 'ibrav') must be specified The lattice parameter alat = A If ibrav = 0, only A is
            used if present; cell vectors are read from card CELL_PARAMETERS"""
        ),
    )
    cosAC: Annotated[  # noqa: N815
        float | None, Quantity(units="1-3:angstrom", dimensionality="1-3:length 4-6:dimensionless")
    ] = Field(
        None,
        description=dedent(
            """\
            Traditional crystallographic constants: a,b,c cosAB = cosine of the angle between axis
            a and b (gamma) cosAC = cosine of the angle between axis a and c (beta) cosBC = cosine
            of the angle between axis b and c (alpha) The axis are chosen according to the value of
            'ibrav'. Specify either these OR 'celldm' but NOT both. Only needed values (depending
            on 'ibrav') must be specified The lattice parameter alat = A If ibrav = 0, only A is
            used if present; cell vectors are read from card CELL_PARAMETERS"""
        ),
    )
    cosBC: Annotated[  # noqa: N815
        float | None, Quantity(units="1-3:angstrom", dimensionality="1-3:length 4-6:dimensionless")
    ] = Field(
        None,
        description=dedent(
            """\
            Traditional crystallographic constants: a,b,c cosAB = cosine of the angle between axis
            a and b (gamma) cosAC = cosine of the angle between axis a and c (beta) cosBC = cosine
            of the angle between axis b and c (alpha) The axis are chosen according to the value of
            'ibrav'. Specify either these OR 'celldm' but NOT both. Only needed values (depending
            on 'ibrav') must be specified The lattice parameter alat = A If ibrav = 0, only A is
            used if present; cell vectors are read from card CELL_PARAMETERS"""
        ),
    )
    nat: int = Field(..., description="number of atoms in the unit cell")
    ntyp: int = Field(..., description="number of types of atoms in the unit cell")
    nbnd: int | None = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            number of electronic states (bands) to be calculated. Note that in spin-polarized
            calculations the number of k-point, not the number of bands per k-point, is doubled  By
            default the number of bands is set internally: for an insulator, the number of valence
            bands (number of electrons / 2); for a metal, 20% more (at least 4 more)."""
        ),
    )
    tot_charge: Annotated[float, Quantity(units="e", dimensionality="charge")] = Field(
        0.0,
        description=dedent(
            """\
            total charge of the system. Useful for simulations with charged cells. By default the
            unit cell is assumed to be neutral (tot_charge=0). tot_charge=+1 means one electron
            missing from the system, tot_charge=-1 means one additional electron, and so on.  In a
            periodic calculation a compensating jellium background is inserted to remove
            divergences if the cell is not neutral."""
        ),
    )
    tot_magnetization: float = Field(
        -1,
        description=dedent(
            """\
            total majority spin charge - minority spin charge. Used to impose a specific total
            electronic magnetization. If unspecified, the tot_magnetization variable is ignored and
            the electronic magnetization is determined by the occupation numbers (see card
            OCCUPATIONS) read from input."""
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
            kinetic energy cutoff for charge density and potential For norm-conserving
            pseudopotential you should stick to the default value, you can reduce it by a little
            but it will introduce noise especially on forces and stress. If there are ultrasoft PP,
            a larger value than the default is often desirable (ecutrho = 8 to 12 times ecutwfc,
            typically). PAW datasets can often be used at 4*ecutwfc, but it depends on the shape of
            augmentation charge: testing is mandatory. The use of gradient-corrected functional,
            especially in cells with vacuum, or for pseudopotential without non-linear core
            correction, usually requires an higher values of ecutrho to be accurately converged."""
        ),
    )
    nr1: int | None = Field(
        None,
        description=dedent(
            """\
            three-dimensional FFT mesh (hard grid) for charge density (and scf potential). If not
            specified the grid is calculated based on the cutoff for charge density."""
        ),
    )
    nr2: int | None = Field(
        None,
        description=dedent(
            """\
            three-dimensional FFT mesh (hard grid) for charge density (and scf potential). If not
            specified the grid is calculated based on the cutoff for charge density."""
        ),
    )
    nr3: int | None = Field(
        None,
        description=dedent(
            """\
            three-dimensional FFT mesh (hard grid) for charge density (and scf potential). If not
            specified the grid is calculated based on the cutoff for charge density."""
        ),
    )
    nr1s: int | None = Field(
        None,
        description=dedent(
            """\
            three-dimensional mesh for wavefunction FFT and for the smooth part of charge density (
            smooth grid ). Coincides with nr1, nr2, nr3 if ecutrho = 4 * ecutwfc ( default )"""
        ),
    )
    nr2s: int | None = Field(
        None,
        description=dedent(
            """\
            three-dimensional mesh for wavefunction FFT and for the smooth part of charge density (
            smooth grid ). Coincides with nr1, nr2, nr3 if ecutrho = 4 * ecutwfc ( default )"""
        ),
    )
    nr3s: int | None = Field(
        None,
        description=dedent(
            """\
            three-dimensional mesh for wavefunction FFT and for the smooth part of charge density (
            smooth grid ). Coincides with nr1, nr2, nr3 if ecutrho = 4 * ecutwfc ( default )"""
        ),
    )
    nr1b: int | None = Field(
        None,
        description=dedent(
            """\
            dimensions of the 'box' grid for Ultrasoft pseudopotentials must be specified if
            Ultrasoft PP are present"""
        ),
    )
    nr2b: int | None = Field(
        None,
        description=dedent(
            """\
            dimensions of the 'box' grid for Ultrasoft pseudopotentials must be specified if
            Ultrasoft PP are present"""
        ),
    )
    nr3b: int | None = Field(
        None,
        description=dedent(
            """\
            dimensions of the 'box' grid for Ultrasoft pseudopotentials must be specified if
            Ultrasoft PP are present"""
        ),
    )
    occupations: Literal["fixed", "ensemble", "from_input"] = Field(
        "fixed",
        description=dedent(
            """\
            a string describing the occupation of the electronic states. In the case of conjugate
            gradient style of minimization of the electronic states, if occupations is set to
            'ensemble', this allows ensemble DFT calculations for metallic systems.
            - 'fixed': for insulators with a gap.
            - 'ensemble': ensemble DFT for metallic systems; see smearing and degauss.
            - 'from_input': occupations read from input (card 'OCCUPATIONS')."""
        ),
    )
    degauss: Annotated[float, Quantity(units="Hartree", dimensionality="energy")] = Field(
        0.0e0,
        description="parameter for the smearing function, only used for ensemble DFT calculations.",
    )
    smearing: Literal[
        "gaussian",
        "fermi-dirac",
        "hermite-delta",
        "gaussian-splines",
        "cold-smearing",
        "marzari-vanderbilt",
    ] = Field(
        "gaussian",
        description=dedent(
            """\
            a string describing the kind of occupations for electronic states in the case of
            ensemble DFT ( occupations == 'ensemble' ). Warning: only 'gaussian' is tested.
            - 'gaussian': ordinary Gaussian smearing.
            - 'fermi-dirac': Fermi-Dirac smearing.
            - 'hermite-delta': Hermite-delta smearing.
            - 'gaussian-splines': smearing based on Gaussian splines.
            - 'cold-smearing': Marzari-Vanderbilt cold smearing (variant cs1).
            - 'marzari-vanderbilt': Marzari-Vanderbilt cold smearing (variant cs2)."""
        ),
    )
    nspin: Literal[1, 2] = Field(
        1,
        description=dedent(
            """\
            Number of spin components.
            - '1': non-polarized calculation.
            - '2': spin-polarized calculation, LSDA (magnetization along z axis)."""
        ),
    )
    ecfixed: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.0, description=""
    )
    qcutz: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.0, description=""
    )
    q2sigma: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.1,
        description=dedent(
            """\
            ecfixed, qcutz, q2sigma:  parameters for modified functional to be used in
            variable-cell molecular dynamics (or in stress calculation). 'ecfixed' is the value of
            the constant-cutoff; 'qcutz' and 'q2sigma' are the height and the width of the energy
            step for reciprocal vectors whose square modulus is greater than 'ecfixed'. In the
            kinetic energy, G^2 is replaced by G^2 + qcutz * (1 + erf ( (G^2 - ecfixed)/q2sigma) )
            See: M. Bernasconi et al, J. Phys. Chem. Solids 56, 501 (1995)"""
        ),
    )
    input_dft: str | None = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            Exchange-correlation functional: eg 'PBE', 'BLYP' etc See Modules/funct.f90 for allowed
            values. Overrides the value read from pseudopotential files. Use with care and if you
            know what you are doing!  Use 'PBE0' to perform hybrid functional calculation using
            Wannier functions. Allowed calculation: 'cp-wf' and 'vc-cp-wf' See CP specific user
            manual for further guidance (or in CPV/Doc/user_guide.tex) and examples in
            CPV/examples/EXX-wf-example. Also see related keywords starting with exx_."""
        ),
    )
    exx_fraction: float | None = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            Fraction of EXX for hybrid functional calculations. In the case of input_dft='PBE0',
            the default value is 0.25. This entry overrides the default (as well as the restart
            file) value of a given functional."""
        ),
    )
    lda_plus_u: bool = Field(
        False,
        description=dedent(
            """\
            lda_plus_u = .TRUE. enables calculation with LDA+U ('rotationally invariant'). See also
            Hubbard_U. Anisimov, Zaanen, and Andersen, PRB 44, 943 (1991)
            (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.44.943); Anisimov et al., PRB
            48, 16929 (1993) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.48.16929);
            Liechtenstein, Anisimov, and Zaanen, PRB 52, R5467 (1994)
            (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.52.R5467); Cococcioni and de
            Gironcoli, PRB 71, 035105 (2005)
            (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.71.035105)."""
        ),
    )
    vdw_corr: Literal["none", "grimme-d2", "tkatchenko-scheffler", "XDM"] = Field(
        "none",
        description=dedent(
            """\
            Type of van der Waals correction. Allowed values:  Note that non-local functionals
            (e.g. vdw-DF) are NOT specified here but in input_dft.
            - 'none': no van der Waals correction.
            - 'grimme-d2': Semiempirical Grimme's DFT-D2. Optional variables: london_s6,
              london_rcut. S. Grimme, J. Comp. Chem. 27, 1787 (2006). V. Barone et al., J. Comp.
              Chem. 30, 934 (2009).
            - 'tkatchenko-scheffler': Tkatchenko-Scheffler dispersion corrections with
              first-principle derived C6 coefficients. Optional variables: ts_vdw_econv_thr,
              ts_vdw_isolated. A. Tkatchenko and M. Scheffler, PRL 102, 073005 (2009)
              (https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.102.073005). J. Hermann et
              al., J. Chem. Phys. 159, 174802 (2023), doi:10.1063/5.0170972
              (https://doi.org/10.1063/5.0170972).
            - 'XDM': Exchange-hole dipole-moment model (implemented in PW only). A. D. Becke and E.
              R. Johnson, J. Chem. Phys. 127, 154108 (2007). A. Otero de la Roza, E. R. Johnson, J.
              Chem. Phys. 136, 174109 (2012)."""
        ),
    )
    london_s6: float = Field(
        0.75, description="global scaling parameter for DFT-D. Default is good for PBE."
    )
    london_rcut: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        200, description="cutoff radius for dispersion interactions"
    )
    ts_vdw: bool = Field(False, description="OBSOLESCENT, same as vdw_corr='TS")
    ts_vdw_econv_thr: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        1.0e-6,
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
            Optional: set it to .TRUE. when computing the Tkatchenko-Scheffler vdW energy for an
            isolated (non-periodic) system."""
        ),
    )
    assume_isolated: Literal["none", "makov-payne"] = Field(
        "none",
        description=dedent(
            """\
            Used to perform calculation assuming the system to be isolated (a molecule or a cluster
            in a 3D supercell).  Currently available choices:
            - 'none': regular periodic calculation w/o any correction.
            - 'makov-payne': the Makov-Payne correction to the total energy is computed. Theory:
              G.Makov, and M.C.Payne, 'Periodic boundary conditions in ab initio calculations' ,
              Phys.Rev.B 51, 4014 (1995)."""
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
        tuple[float, float, float, float, float, float] | None,
        Quantity(units="1:bohr", dimensionality="dimensionless, 1:length"),
    ] = Field(
        None,
        description=dedent(
            """\
            Crystallographic constants - see the 'ibrav' variable. Specify either these OR
            A,B,C,cosAB,cosBC,cosAC NOT both. Only needed values (depending on 'ibrav') must be
            specified alat = celldm(1) is the lattice parameter 'a' If ibrav=0, only celldm(1) is
            used if present; cell vectors are read from card CELL_PARAMETERS"""
        ),
    )
    Hubbard_U: Annotated[list[float], Quantity(units="eV", dimensionality="energy")] = Field(
        default_factory=list,
        description=dedent(
            """\
            Hubbard_U(i): parameter U for LDA+U calculations. Currently only the simpler,
            one-parameter LDA+U is implemented (no 'alpha' or 'J' terms) (start = 1, end = ntyp)"""
        ),
    )


class ElectronsNamelist(Namelist):
    """Pydantic model for the `ELECTRONS` namelist."""

    @field_validator("electron_dynamics", mode="before")
    @classmethod
    def map_electron_dynamics(cls, v: str) -> str:
        """Map equivalent values for `electron_dynamics` onto a canonical value."""
        mapping = {"default": "sd"}
        return mapping.get(v, v)

    @field_validator("electron_temperature", mode="before")
    @classmethod
    def map_electron_temperature(cls, v: str) -> str:
        """Map equivalent values for `electron_temperature` onto a canonical value."""
        mapping = {"default": "not_controlled"}
        return mapping.get(v, v)

    @field_validator("startingwfc", mode="before")
    @classmethod
    def map_startingwfc(cls, v: str) -> str:
        """Map equivalent values for `startingwfc` onto a canonical value."""
        mapping = {"none": "default"}
        return mapping.get(v, v)

    electron_maxstep: int = Field(100, description="maximum number of iterations in a scf step")
    electron_dynamics: Literal["none", "sd", "damp", "verlet", "cg"] = Field(
        "none",
        description=dedent(
            """\
            set how electrons should be moved.
            - 'none': electronic degrees of freedom (d.o.f.) are kept fixed.
            - 'sd': steepest descent algorithm is used to minimize electronic d.o.f.
            - 'damp': damped dynamics is used to propagate electronic d.o.f.
            - 'verlet': standard Verlet algorithm is used to propagate electronic d.o.f.
            - 'cg': conjugate gradient is used to converge the wavefunction at each ionic step.
              'cg' can be used interchangeably with 'verlet' for a couple of ionic steps in order
              to 'cool down' the electrons and return them back to the Born-Oppenheimer surface.
              Then 'verlet' can be restarted again. This procedure is useful when electronic
              adiabaticity in CP is lost yet the ionic velocities need to be preserved."""
        ),
    )
    conv_thr: Annotated[float, Quantity(units="Hartree", dimensionality="energy")] = Field(
        1.0e-6,
        description="Convergence threshold for selfconsistency: estimated energy error < conv_thr",
    )
    niter_cg_restart: int = Field(
        20,
        description=dedent(
            """\
            frequency in iterations for which the conjugate-gradient algorithm for electronic
            relaxation is restarted"""
        ),
    )
    efield: Annotated[
        float, Quantity(units="Hartree e^-1 bohr^-1", dimensionality="energy charge^-1 length^-1")
    ] = Field(
        0.0e0,
        description=dedent(
            """\
            Amplitude of the finite electric field (in a.u.; 1 a.u. = 51.4220632*10^10 V/m). Used
            only if tefield=.TRUE."""
        ),
    )
    epol: int = Field(
        3,
        description=dedent(
            """\
            direction of the finite electric field (only if tefield == .TRUE.) In the case of a
            PARALLEL calculation only the case epol==3 is implemented"""
        ),
    )
    emass: Annotated[float, Quantity(units="electron_mass", dimensionality="mass")] = Field(
        400.0e0,
        description=dedent(
            """\
            effective electron mass in the CP Lagrangian, in atomic units ( 1 a.u. of mass =
            1/1822.9 a.m.u. = 9.10939 * 10^-31 kg )"""
        ),
    )
    emass_cutoff: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        2.5e0,
        description=dedent(
            """\
            mass cut-off for the Fourier acceleration effective mass is rescaled for 'G' vector
            components with kinetic energy above 'emass_cutoff"""
        ),
    )
    orthogonalization: Literal["ortho", "Gram-Schmidt"] = Field(
        "ortho",
        description=dedent(
            """\
            Selects the orthonormalization method for electronic wave functions.
            - 'ortho': use iterative algorithm - if it doesn't converge, reduce the timestep, or
              use options ortho_max and ortho_eps, or use Gram-Schmidt instead just to start the
              simulation.
            - 'Gram-Schmidt': use Gram-Schmidt algorithm - to be used ONLY in the first few steps.
              YIELDS INCORRECT ENERGIES AND EIGENVALUES."""
        ),
    )
    ortho_eps: float = Field(
        1.0e-8,
        description=dedent(
            """\
            tolerance for iterative orthonormalization meaningful only if orthogonalization =
            'ortho"""
        ),
    )
    ortho_max: int = Field(
        300,
        description=dedent(
            """\
            maximum number of iterations for orthonormalization meaningful only if
            orthogonalization = 'ortho"""
        ),
    )
    ortho_para: int = Field(0, description="")
    electron_damping: float = Field(
        0.1e0,
        description=dedent(
            """\
            damping frequency times delta t, optimal values could be calculated with the formula :
            SQRT( 0.5 * LOG( ( E1 - E2 ) / ( E2 - E3 ) ) ) where E1, E2, E3 are successive values
            of the DFT total energy in a steepest descent simulations. meaningful only if '
            electron_dynamics = 'damp"""
        ),
    )
    electron_velocities: Literal["default", "zero", "change_step"] = Field(
        "default",
        description=dedent(
            """\
            Specifies how to initialise electronic velocities at restart.
            - 'default': restart using electronic velocities of the previous run.
            - 'zero': restart setting electronic velocities to zero.
            - 'change_step': restart simulation using electronic velocities of the previous run,
              with rescaling due to the timestep change. Specify the old step via tolp as in tolp =
              'old_time_step_value' in au. Note that you may want to specify ion_velocities =
              'change_step'."""
        ),
    )
    electron_temperature: Literal["nose", "not_controlled"] = Field(
        "not_controlled",
        description=dedent(
            """\
            Specifies how the electronic temperature is controlled.
            - 'nose': control electronic temperature using Nose thermostat. See also fnosee and
              ekincw.
            - 'not_controlled': electronic temperature is not controlled."""
        ),
    )
    ekincw: Annotated[float, Quantity(units="Hartree", dimensionality="energy")] = Field(
        0.001e0,
        description=dedent(
            """\
            value of the average kinetic energy forced by the temperature control meaningful only
            with ' electron_temperature /= 'not_controlled"""
        ),
    )
    fnosee: Annotated[float, Quantity(units="THz", dimensionality="time^-1")] = Field(
        1.0e0,
        description=dedent(
            """\
            oscillation frequency of the nose thermostat meaningful only with '
            electron_temperature = 'nose"""
        ),
    )
    startingwfc: Literal["default", "random", "atomic"] = Field(
        "random",
        description=dedent(
            """\
            Specifies the initial guess for the electronic wavefunctions.
            - 'default': start from random wavefunctions, with no additional randomization (see
              ampre).
            - 'random': start from random wavefunctions, with an additional randomization step
              controlled by ampre.
            - 'atomic': start from random wavefunctions and superimpose as many atomic orbitals as
              possible."""
        ),
    )
    tcg: bool = Field(
        False,
        description=dedent(
            """\
            if .TRUE. perform a conjugate gradient minimization of the electronic states for every
            ionic step. It requires Gram-Schmidt orthogonalization of the electronic states."""
        ),
    )
    maxiter: int = Field(
        100,
        description=dedent(
            """\
            maximum number of conjugate gradient iterations for conjugate gradient minimizations of
            electronic states"""
        ),
    )
    passop: float = Field(
        0.3e0,
        description=dedent(
            """\
            small step used in the  conjugate gradient minimization of the electronic states."""
        ),
    )
    pre_state: bool = Field(
        False,
        description=dedent(
            """\
            if .TRUE. perform the precondition of the CG gradient using the kinetic energy of the
            state."""
        ),
    )
    n_inner: int = Field(
        2,
        description=dedent(
            """\
            number of internal cycles for every conjugate gradient iteration only for ensemble
            DFT"""
        ),
    )
    niter_cold_restart: int = Field(
        1,
        description=dedent(
            """\
            frequency in iterations at which a full inner cycle, only for cold smearing, is
            performed"""
        ),
    )
    lambda_cold: float = Field(
        0.03e0,
        description=dedent(
            """\
            step for inner cycle with cold smearing, used when a not full cycle is performed"""
        ),
    )
    grease: float = Field(
        1.0e0,
        description=dedent(
            """\
            a number <= 1, very close to 1: the damping in electronic damped dynamics is multiplied
            at each time step by 'grease' (avoids overdamping close to convergence: Obsolete ?)
            grease = 1 : normal damped dynamics"""
        ),
    )
    ampre: float = Field(
        0.0e0,
        description=dedent(
            """\
            amplitude of the randomization ( allowed values: 0.0 - 1.0 ) meaningful only if '
            startingwfc = 'random"""
        ),
    )


class IonsNamelist(Namelist):
    """Pydantic model for the `IONS` namelist."""

    @field_validator("ion_temperature", mode="before")
    @classmethod
    def map_ion_temperature(cls, v: str) -> str:
        """Map equivalent values for `ion_temperature` onto a canonical value."""
        mapping = {"default": "not_controlled"}
        return mapping.get(v, v)

    ion_dynamics: Literal["none", "sd", "damp", "verlet"] = Field(
        "none",
        description=dedent(
            """\
            Specify the type of ionic dynamics.  For constrained dynamics or constrained
            optimisations add the CONSTRAINTS card (when the card is present the SHAKE algorithm is
            automatically used).
            - 'none': ions are kept fixed.
            - 'sd': steepest descent algorithm is used to minimize ionic configuration.
            - 'damp': damped dynamics is used to propagate ions.
            - 'verlet': standard Verlet algorithm is used to propagate ions."""
        ),
    )
    ion_positions: Literal["default", "from_input"] = Field(
        "default",
        description=dedent(
            """\
            Selects the source of the initial atomic positions.
            - 'default': if restarting, use atomic positions read from the restart file; in all
              other cases, use atomic positions from standard input.
            - 'from_input': restart the simulation with atomic positions read from standard input,
              even if restarting."""
        ),
    )
    ion_velocities: Literal["default", "change_step", "random", "from_input", "zero"] = Field(
        "default",
        description=dedent(
            """\
            Initial ionic velocities.
            - 'default': restart the simulation with atomic velocities read from the restart file.
            - 'change_step': restart the simulation with atomic velocities read from the restart
              file, with rescaling due to the timestep change, specify the old step via tolp as in
              tolp = 'old_time_step_value' in au. Note that you may want to specify
              electron_velocities = 'change_step'.
            - 'random': start the simulation with random atomic velocities (see also variable
              tempw).
            - 'from_input': restart the simulation with atomic velocities read from standard input
              - see card 'ATOMIC_VELOCITIES'. BEWARE: tested only with electron_dynamics='cg'.
            - 'zero': restart the simulation with atomic velocities set to zero."""
        ),
    )
    ion_damping: float = Field(
        0.2e0,
        description=dedent(
            """\
            damping frequency times delta t, optimal values could be calculated with the formula :
            SQRT( 0.5 * LOG( ( E1 - E2 ) / ( E2 - E3 ) ) ) where E1, E2, E3 are successive values
            of the DFT total energy in a steepest descent simulations. meaningful only if '
            ion_dynamics = 'damp"""
        ),
    )
    iesr: int = Field(
        1,
        description=dedent(
            """\
            The real-space contribution to the Ewald summation is performed on iesr*iesr*iesr
            cells. Typically iesr=1 is sufficient to have converged results."""
        ),
    )
    ion_nstepe: int = Field(1, description="number of electronic steps per ionic step.")
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
    ion_temperature: Literal["nose", "rescaling", "not_controlled"] = Field(
        "not_controlled",
        description=dedent(
            """\
            Specifies how the ionic temperature is controlled.
            - 'nose': control ionic temperature using Nose-Hoover thermostat; see parameters
              fnosep, tempw, nhpcl, ndega, nhptyp.
            - 'rescaling': control ionic temperature via velocities rescaling; see parameter tolp.
            - 'not_controlled': ionic temperature is not controlled."""
        ),
    )
    tempw: Annotated[float, Quantity(units="K", dimensionality="temperature")] = Field(
        300.0e0,
        description=dedent(
            """\
            value of the ionic temperature forced by the temperature control. meaningful only
            with ' ion_temperature /= 'not_controlled' ' or when the initial velocities are set
            to 'random' 'ndega' controls number of degrees of freedom used in temperature
            calculation"""
        ),
    )
    fnosep: Annotated[float | None, Quantity(units="THz", dimensionality="time^-1")] = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "i==1", "value": "1.D0"},
                {"when": None, "value": "-1.D0"},
            ],
        },
        description=dedent(
            """\
            oscillation frequency of the nose thermostat [note that 3 terahertz = 100 cm^-1]
            meaningful only with ' ion_temperature = 'nose' ' for Nose-Hoover chain one can set
            frequencies of all thermostats ( fnosep = X Y Z etc. ) If only first is set, the
            defaults for the others will be same."""
        ),
    )
    tolp: Annotated[float, Quantity(units="K", dimensionality="temperature")] = Field(
        100.0e0,
        description=dedent(
            """\
            tolerance of the rescaling. When ionic temperature differs from 'tempw' more than
            'tolp' apply rescaling. meaningful only with ion_temperature = 'rescaling' or with
            ion_velocities='change_step', where it specifies the old timestep"""
        ),
    )
    nhpcl: int = Field(
        1,
        description="number of thermostats in the Nose-Hoover chain currently maximum allowed is 4",
    )
    nhptyp: Literal[0, 1, 2, 3] = Field(
        0,
        description=dedent(
            """\
            Type of the 'massive' Nose-Hoover chain thermostat. NOTE: if using more than 1
            thermostat per system there will be a common thermostat added on top of them all; to
            disable this common thermostat specify nhptyp=-X instead of nhptyp=X (i.e. use the
            negative of any of the values 1, 2, 3 below).
            - '0': A single Nose-Hoover chain for the whole system (default).
            - '1': One Nose-Hoover chain per each atomic type.
            - '2': One Nose-Hoover chain per atom; this one is useful for extremely rapid
              equipartitioning (equilibration is a different beast).
            - '3': Together with nhgrp allows fine grained thermostat control."""
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
    greasp: float = Field(1.0e0, description="same as 'grease', for ionic damped dynamics.")
    ion_radius: Annotated[list[float], Quantity(units="bohr", dimensionality="length")] = Field(
        default_factory=list,
        description=dedent(
            """\
            ion_radius(i): pseudo-atomic radius of the i-th atomic species used in Ewald summation.
            Typical values: between 0.5 and 2. Results should NOT depend upon such parameters if
            their values are properly chosen. See also 'iesr'. (start = 1, end = ntyp)"""
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
    tranp: list[bool] = Field(
        default_factory=list,
        description=dedent(
            """\
            If .TRUE. randomize ionic positions for the atomic type corresponding to the index.
            (start = 1, end = ntyp)"""
        ),
    )
    amprp: list[float] = Field(
        default_factory=list,
        description=dedent(
            """\
            amplitude of the randomization for the atomic type corresponding to the index i (
            allowed values: 0.0 - 1.0 ). meaningful only if ' tranp(i) = .TRUE.'. (start = 1, end =
            ntyp)"""
        ),
    )


class CellNamelist(Namelist):
    """Pydantic model for the `CELL` namelist."""

    @field_validator("cell_temperature", mode="before")
    @classmethod
    def map_cell_temperature(cls, v: str) -> str:
        """Map equivalent values for `cell_temperature` onto a canonical value."""
        mapping = {"default": "not_controlled"}
        return mapping.get(v, v)

    cell_parameters: Literal["default", "from_input"] = Field(
        "default",
        description=dedent(
            """\
            Specifies how cell parameters are initialised at restart.
            - 'default': restart the simulation with cell parameters read from the restart file or
              celldm if restart_mode = 'from_scratch'.
            - 'from_input': restart the simulation with cell parameters from standard input (see
              the card 'CELL_PARAMETERS')."""
        ),
    )
    cell_dynamics: Literal[None, "none", "sd", "damp-pr", "pr"] = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": (
                        "calculation=='vc-md' .or. calculation=='vc-cp' .or. "
                        "calculation=='vc-cp-wf'"
                    ),
                    "value": "'pr'",
                },
                {"when": "calculation=='vc-relax'", "value": "'damp-pr'"},
                {"when": None, "value": "'none'"},
            ],
        },
        description=dedent(
            """\
            set how cell should be moved.
            - 'none': cell is kept fixed.
            - 'sd': steepest descent algorithm is used to optimise the cell.
            - 'damp-pr': damped dynamics is used to optimise the cell (Parrinello-Rahman method).
            - 'pr': standard Verlet algorithm is used to propagate the cell (Parrinello-Rahman
              method)."""
        ),
    )
    cell_velocities: Literal["default", "zero"] = Field(
        "default",
        description=dedent(
            """\
            Selects the source of the initial cell velocities.
            - 'default': restart using cell velocities of the previous run.
            - 'zero': restart setting cell velocity to zero."""
        ),
    )
    cell_damping: float = Field(
        0.1e0,
        description=dedent(
            """\
            damping frequency times delta t, optimal values could be calculated with the formula :
            SQRT( 0.5 * LOG( ( E1 - E2 ) / ( E2 - E3 ) ) ) where E1, E2, E3 are successive values
            of the DFT total energy in a steepest descent simulations. meaningful only if '
            cell_dynamics = 'damp"""
        ),
    )
    press: Annotated[float, Quantity(units="kbar", dimensionality="energy length^-3")] = Field(
        0.0e0, description="Target pressure in a variable-cell md or relaxation run."
    )
    wmass: Annotated[float | None, Quantity(units="amu", dimensionality="mass")] = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            Fictitious cell mass for variable-cell simulations (both 'vc-md' and 'vc-relax')  By
            default it is set internally to 0.75*Tot_Mass/pi**2 for Parrinello-Rahman MD, or
            0.75*Tot_Mass/pi**2/Omega**(2/3) for Wentzcovitch MD."""
        ),
    )
    cell_factor: float = Field(
        1.2e0,
        description=dedent(
            """\
            Used in the construction of the pseudopotential tables. It should exceed the maximum
            linear contraction of the cell during a simulation."""
        ),
    )
    cell_temperature: Literal["nose", "not_controlled"] = Field(
        "not_controlled",
        description=dedent(
            """\
            Specifies how the cell temperature is controlled. Note: only 'nose' and
            'not_controlled' are currently implemented in the parser; 'rescaling' is documented in
            the literature but not handled.
            - 'nose': control cell temperature using Nose thermostat; see parameters fnoseh and
              temph.
            - 'not_controlled': cell temperature is not controlled."""
        ),
    )
    temph: Annotated[float, Quantity(units="K", dimensionality="temperature")] = Field(
        0.0e0,
        description=dedent(
            """\
            value of the cell temperature (in ???) forced by the temperature control. meaningful
            only with ' cell_temperature /= 'not_controlled"""
        ),
    )
    fnoseh: Annotated[float, Quantity(units="THz", dimensionality="time^-1")] = Field(
        1.0e0,
        description=dedent(
            """\
            oscillation frequency of the nose thermostat meaningful only with ' cell_temperature =
            'nose"""
        ),
    )
    greash: float = Field(1.0e0, description="same as 'grease', for cell damped dynamics")
    cell_dofree: str = Field(
        "all",
        description=dedent(
            """\
            Select which of the cell parameters should be moved:  all     = all axis and angles are
            moved x       = only the x component of axis 1 (v1_x) is moved y       = only the y
            component of axis 2 (v2_y) is moved z       = only the z component of axis 3 (v3_z) is
            moved xy      = only v1_x and v2_y are moved xz      = only v1_x and v3_z are moved yz
                = only v2_y and v3_z are moved xyz     = only v1_x, v2_y, v3_z are moved shape   =
            all axis and angles, keeping the volume fixed 2Dxy    = only x and y components are
            allowed to change 2Dshape = as above, keeping the area in xy plane fixed volume  =
            isotropic variations of v1_x, v2_y, v3_z, keeping the shape fixed. Should be used only
            with ibrav=1."""
        ),
    )


class PressAiNamelist(Namelist):
    """Pydantic model for the `PRESS_AI` namelist."""

    abivol: bool = Field(False, description=".true. for finite pressure calculations")
    abisur: bool = Field(False, description=".true. for finite surface tension calculations")
    P_ext: Annotated[float, Quantity(units="GPa", dimensionality="energy length^-3")] = Field(
        0.0e0, description="external pressure"
    )
    pvar: bool = Field(
        False,
        description=dedent(
            """\
            .true. for variable pressure calculations pressure changes linearly with time: Delta_P
            = (P_fin - P_in)/nstep"""
        ),
    )
    P_in: Annotated[float, Quantity(units="GPa", dimensionality="energy length^-3")] = Field(
        0.0e0, description="only if pvar = .true. initial value of the external pressure"
    )
    P_fin: Annotated[float, Quantity(units="GPa", dimensionality="energy length^-3")] = Field(
        0.0e0, description="only if pvar = .true. final value of the external pressure"
    )
    Surf_t: Annotated[
        float, Quantity(units="Hartree bohr^-2", dimensionality="energy length^-2")
    ] = Field(0.0e0, description="Surface tension (typical values 1.d-4 - 1.d-3)")
    rho_thr: Annotated[float, Quantity(units="e bohr^-3", dimensionality="charge length^-3")] = (
        Field(
            0.0e0,
            description=dedent(
                """\
                threshold parameter which defines the electronic charge density isosurface to
                compute the 'quantum' volume of the system (typical values: 1.d-4 - 1.d-3)
                (corresponds to alpha in PRL 94 145501 (2005)
                (https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.94.145501))"""
            ),
        )
    )
    dthr: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        0.0e0,
        description=dedent(
            """\
            thikness of the external skin of the electronic charge density used to compute the
            'quantum' surface (typical values: 1.d-4 - 1.d-3; 50% to 100% of rho_thr) (corresponds
            to Delta in PRL 94 145501 (2005)
            (https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.94.145501))"""
        ),
    )


class WannierNamelist(Namelist):
    """Pydantic model for the `WANNIER` namelist."""

    wf_efield: bool = Field(
        False, description="If dynamics will be done in the presence of a field"
    )
    wf_switch: bool = Field(
        False,
        description=dedent(
            """\
            Whether to turn on the field adiabatically (adiabatic switch) if true, then nbeg is set
            to 0."""
        ),
    )
    sw_len: int = Field(
        1,
        description=dedent(
            """\
            No. of iterations over which the field will be turned on to its final value. Starting
            value is 0.0 If sw_len < 0, then it is set to 1. If you want to just optimize
            structures on the presence of a field, then you may set this to 1 and run a regular
            geometry optimization."""
        ),
    )
    efx0: Annotated[
        float | None,
        Quantity(units="Hartree e^-1 bohr^-1", dimensionality="energy charge^-1 length^-1"),
    ] = Field(None, description="Initial values of the field along x, y, and z directions")
    efy0: Annotated[
        float | None,
        Quantity(units="Hartree e^-1 bohr^-1", dimensionality="energy charge^-1 length^-1"),
    ] = Field(None, description="Initial values of the field along x, y, and z directions")
    efz0: Annotated[
        float | None,
        Quantity(units="Hartree e^-1 bohr^-1", dimensionality="energy charge^-1 length^-1"),
    ] = Field(None, description="Initial values of the field along x, y, and z directions")
    efx1: Annotated[
        float | None,
        Quantity(units="Hartree e^-1 bohr^-1", dimensionality="energy charge^-1 length^-1"),
    ] = Field(None, description="Final values of the field along x, y, and z directions")
    efy1: Annotated[
        float | None,
        Quantity(units="Hartree e^-1 bohr^-1", dimensionality="energy charge^-1 length^-1"),
    ] = Field(None, description="Final values of the field along x, y, and z directions")
    efz1: Annotated[
        float | None,
        Quantity(units="Hartree e^-1 bohr^-1", dimensionality="energy charge^-1 length^-1"),
    ] = Field(None, description="Final values of the field along x, y, and z directions")
    wfsd: Literal[1, 2, 3] = Field(
        1,
        description=dedent(
            """\
            Localization algorithm for Wannier function calculation. This is consistent with all
            the calwf options as well as the tolw (see below). Not a good idea to do Wannier
            dynamics with this if you are using restart='from_scratch' option, since the spreads
            converge fast in the beginning and ortho goes bananas.
            - '1': Damped Dynamics.
            - '2': Steepest-Descent / Conjugate-Gradient.
            - '3': Jacobi Rotation."""
        ),
    )
    wfdt: float = Field(5.0e0, description="The minimum step size to take in the SD/CG direction")
    maxwfdt: float = Field(
        0.3e0,
        description=dedent(
            """\
            The maximum step size to take in the SD/CG direction The code calculates an optimum
            step size, but that may be either too small (takes forever to converge)  or too
            large (code goes crazy) . This option keeps the step size between wfdt and maxwfdt.
            In my experience 0.1 and 0.5 work quite well. (but don't blame me if it doesn't work
            for you)"""
        ),
    )
    nit: int = Field(10, description="Number of iterations to do for Wannier convergence.")
    nsd: int = Field(
        10,
        description=dedent(
            """\
            Out of a total of NIT iterations, NSD will be Steepest-Descent and ( nit - nsd ) will
            be Conjugate-Gradient."""
        ),
    )
    wf_q: float = Field(
        1500.0e0,
        description=dedent(
            """\
            Fictitious mass of the A matrix used for obtaining maximally localized Wannier
            functions. The unitary transformation matrix U is written as exp(A) where A is a
            anti-hermitian matrix. The Damped-Dynamics is performed in terms of the A matrix, and
            then U is computed from A. Usually a value between 1500 and 2500 works fine, but should
            be tested."""
        ),
    )
    wf_friction: float = Field(0.3e0, description="Damping coefficient for Damped-Dynamics.")
    nsteps: int = Field(
        20, description="Number of Damped-Dynamics steps to be performed per CP iteration."
    )
    tolw: float = Field(1.0e-8, description="Convergence criterion for localization.")
    adapt: bool = Field(True, description="Whether to adapt the damping parameter dynamically.")
    calwf: int = Field(
        3,
        description=dedent(
            """\
            Wannier Function Options, can be 1,2,3,4,5  1. Output the Wannier function density, nwf
            and wffort are used for this option. see below. 2. Output the Overlap matrix
            O_i,j=<w_i|exp{iGr}|w_j>. O is written to unit 38. For details on how O is constructed,
            see below. 3. Perform nsteps of Wannier dynamics per CP iteration, the orbitals are now
            Wannier Functions, not Kohn-Sham orbitals. This is a Unitary transformation of the
            occupied subspace and does not leave the CP Lagrangian invariant. Expectation values
            remain the same. So you will **NOT** have a constant of motion during the run. Don't
            freak out, its normal. 4. This option starts for the KS states and does 1 CP iteration
            and nsteps of Damped-Dynamics to generate  maximally localized wannier functions. Its
            useful when you have the converged KS groundstate and want to get to the converged
            Wannier function groundstate in 1 CP Iteration. 5. This option is similar to calwf 1,
            except that the output is the Wannier function/wavefunction, and not the orbital
            density. See nwf below."""
        ),
    )
    nwf: int = Field(
        0,
        description=dedent(
            """\
            This option is used with calwf 1 and calwf 5. with calwf=1, it tells the code how many
            Orbital densities are to be output. With calwf=5, set this to 1(i.e calwf=5 only writes
            one state during one run. so if you want 10 states, you have to run the code 10 times).
            With calwf=1, you can print many orbital densities in a single run. See also the
            PLOT_WANNIER card for specifying the states to be printed."""
        ),
    )
    wffort: int = Field(
        40,
        description=dedent(
            """\
            This tells the code where to dump the orbital densities. Used only with CALWF=1. for
            e.g. if you want to print 2 orbital densities, set calwf=1, nwf=2 and wffort to an
            appropriate number (e.g. 40) then the first orbital density will be output to fort.40,
            the second to fort.41 and so on. Note that in the current implementation, the following
            units are used 21,22,24,25,26,27,28,38,39,77,78 and whatever you define as ndr and ndw.
            so use number other than these."""
        ),
    )
    writev: bool = Field(
        False,
        description=dedent(
            """\
            Output the charge density (g-space) and the list of g-vectors This is useful if you
            want to reconstruct the electrostatic potential using the Poisson equation. If .TRUE.
            then the code will output the g-space charge density and the list if G-vectors, and
            STOP. Charge density is written to : CH_DEN_G_PARA.ispin (1 or 2 depending on the
            number of spin types) or CH_DEN_G_SERL.ispin depending on if the code is being run in
            parallel or serial G-vectors are written to G_PARA or G_SERL."""
        ),
    )
    exx_neigh: int = Field(
        60, description="An initial guess on the maximum number of neighboring (overlapping) MLWFs."
    )
    exx_dis_cutoff: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        8.0,
        description=dedent(
            """\
            Radial cutoff distance for including overlapping MLWF pairs in EXX calculations. See J.
            Chem. Theory Comput. 16, 3757â3785 (2020)."""
        ),
    )
    exx_poisson_eps: float = Field(
        1.0e-6,
        description="Poisson solver convergence criterion during computation of the EXX potential.",
    )
    exx_use_cube_domain: bool = Field(
        False,
        description=dedent(
            """\
            Use cubic instead of spherical subdomains as local supports during computation of the
            EXX potential. If set to .TRUE., the spherical domain radii (exx_ps_rcut_self,
            exx_ps_rcut_pair, exx_me_rcut_self, exx_me_rcut_pair) will be treated as half of the
            side length of the cubic subdomain."""
        ),
    )
    exx_ps_rcut_self: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        6.0,
        description=dedent(
            """\
            Radial cutoff distance to compute the self EXX energy. This distance determines the
            radius of the Poisson sphere centered at a given MLWF center, and should be large
            enough to cover the majority of the MLWF charge density. See J. Chem. Theory Comput.
            16, 3757â3785 (2020)."""
        ),
    )
    exx_ps_rcut_pair: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        5.0,
        description=dedent(
            """\
            Radial cutoff distance to compute the pair EXX energy. This distance determines the
            radius of the Poisson sphere centered at the midpoint of two overlapping MLWFs, and
            should be large enough to cover the majority of the MLWF product density. This
            parameter can generally be chosen as smaller than exx_ps_rcut_self. See J. Chem. Theory
            Comput. 16, 3757â3785 (2020)."""
        ),
    )
    exx_me_rcut_self: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        10.0,
        description=dedent(
            """\
            Radial cutoff distance for the multipole-expansion sphere centered at a given MLWF
            center. The far-field self EXX potential in this sphere is generated with a multipole
            expansion of the MLWF charge density. This parameter must be larger than
            exx_ps_rcut_self by at least 3 real-space grid point spacings. See J. Chem. Theory
            Comput. 16, 3757â3785 (2020)."""
        ),
    )
    exx_me_rcut_pair: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        7.0,
        description=dedent(
            """\
            Radial cutoff distance for the multipole-expansion sphere centered at the midpoint of
            two overlapping MLWFs. The far-field pair EXX potential in this sphere is generated
            with a multipole expansion of the MLWF product density. This parameter must be larger
            than exx_ps_rcut_pair by at least 3 real-space grid point spacings. Also, this
            parameter can generally be chosen as smaller than exx_me_rcut_self. See J. Chem. Theory
            Comput. 16, 3757â3785 (2020)."""
        ),
    )


class CPInput(EspressoInput):
    """Pydantic model for the input of `cp.x`."""

    control: ControlNamelist = Field(default_factory=lambda: ControlNamelist())
    system: SystemNamelist = Field(...)
    electrons: ElectronsNamelist = Field(default_factory=lambda: ElectronsNamelist())
    ions: IonsNamelist = Field(default_factory=lambda: IonsNamelist())
    cell: CellNamelist = Field(default_factory=lambda: CellNamelist())
    press_ai: PressAiNamelist = Field(default_factory=lambda: PressAiNamelist())
    wannier: WannierNamelist = Field(default_factory=lambda: WannierNamelist())
