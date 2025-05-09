"""Pydantic model for the input of `cp.x` version `qe-6.2.0`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class ControlNamelist(Namelist):
    """Pydantic model for the `CONTROL` namelist."""

    calculation: str = Field(
        "cp",
        description="a string describing the task to be performed: 'cp', 'scf', 'nscf', 'relax', 'vc-relax', 'vc-cp', 'cp-wf', 'vc-cp-wf'  (vc = variable-cell). (wf = Wannier functions).",
    )
    title: str | None = Field(None, description="reprinted on output.")
    verbosity: str = Field(
        "low",
        description="In order of decreasing verbose output: 'debug' | 'high' | 'medium' | 'low','default' | 'minimal",
    )
    isave: int = Field(
        100,
        description="Number of steps between successive savings of information needed to restart the run.",
    )
    restart_mode: str = Field(
        "restart",
        description="from_scratch'   : from scratch 'restart'        : from previous interrupted run 'reset_counters' : continue a previous simulation, performs  'nstep' new steps, resetting the counter and averages",
    )
    nstep: int = Field(50, description="number of Car-Parrinello steps performed in this run")
    iprint: int = Field(
        10,
        description="Number of steps between successive writings of relevant physical quantities to files named as 'prefix.???' depending on 'prefix' parameter. In the standard output relevant quantities are written every 10*iprint steps.",
    )
    tstress: bool = Field(
        False,
        description="Write stress tensor to standard output each 'iprint' steps. It is set to .TRUE. automatically if calculation='vc-relax",
    )
    tprnfor: bool = Field(False, description="print forces. Set to .TRUE. when ions are moving.")
    dt: float = Field(
        1.0e0,
        description="time step for molecular dynamics, in Hartree atomic units (1 a.u.=2.4189 * 10^-17 s : beware, PW code use Rydberg atomic units, twice that much!!!)",
    )
    outdir: Path = Field(
        default_factory=get_tmp_dir,
        description="input, temporary, trajectories and output files are found in this directory.",
    )
    saverho: bool | None = Field(
        None,
        description="This flag controls the saving of charge density in CP codes: If  .TRUE.        save charge density to restart dir, If .FALSE. do not save charge density.",
    )
    prefix: str = Field(
        "cp",
        description="prepended to input/output filenames: prefix.pos : atomic positions prefix.vel : atomic velocities prefix.for : atomic forces prefix.cel : cell parameters prefix.str : stress tensors prefix.evp : energies prefix.hrs : Hirshfeld effective volumes (ts-vdw) prefix.eig : eigen values prefix.nos : Nose-Hoover variables prefix.spr : spread of Wannier orbitals prefix.wfc : center of Wannier orbitals prefix.ncg : number of Poisson CG steps (PBE0)",
    )
    ndr: int = Field(50, description="Units for input and output restart file.")
    ndw: int = Field(50, description="Units for input and output restart file.")
    tabps: bool = Field(
        False,
        description=".true. to compute the volume and/or the surface of an isolated system for finite pressure/finite surface tension calculations (PRL 94, 145501 (2005) (https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.94.145501); JCP 124, 074103 (2006)).",
    )
    max_seconds: float | None = Field(
        None,
        description="jobs stops after max_seconds CPU time. Used to prevent a hard kill from the queuing system.",
    )
    etot_conv_thr: float = Field(
        1.0e-4,
        description="convergence threshold on total energy (a.u) for ionic minimization: the convergence criterion is satisfied when the total energy changes less than etot_conv_thr between two consecutive scf steps. See also forc_conv_thr - both criteria must be satisfied",
    )
    forc_conv_thr: float = Field(
        1.0e-3,
        description="convergence threshold on forces (a.u) for ionic minimization: the convergence criterion is satisfied when all components of all forces are smaller than forc_conv_thr. See also etot_conv_thr - both criteria must be satisfied",
    )
    ekin_conv_thr: float = Field(
        1.0e-6,
        description="convergence criterion for electron minimization: convergence is achieved when 'ekin < ekin_conv_thr'. See also etot_conv_thr - both criteria must be satisfied.",
    )
    disk_io: str = Field(
        "default",
        description="high': CP code will write Kohn-Sham wfc files and additional information in data-file.xml in order to restart with a PW calculation or to use postprocessing tools. If disk_io is not set to 'high', the data file written by CP will not be readable by PW or PostProc.",
    )
    memory: str = Field(
        "default",
        description="small': memory-saving tricks are implemented. Currently: - the G-vectors are sorted only locally, not globally - they are not collected and written to file For large systems, the memory and time gain is sizable but the resulting data files are not portable - use it only if you do not need to re-read the data file",
    )
    pseudo_dir: Path = Field(
        default_factory=get_pseudo_dir, description="directory containing pseudopotential files"
    )
    tefield: bool = Field(
        False,
        description="If .TRUE. a homogeneous finite electric field described through the modern theory of the polarization is applied.",
    )


class SystemNamelist(Namelist):
    """Pydantic model for the `SYSTEM` namelist."""

    ibrav: Literal[0, 1, 2, 3, -3, 4, 5, -5, 6, 7, 8, 9, -9, 91, 10, 11, 12, -12, 13, -13, 14] = (
        Field(
            0,
            description="Bravais-lattice index. If ibrav /= 0, specify EITHER [ celldm(1)-celldm(6) ] OR [ A,B,C,cosAB,cosAC,cosBC ] but NOT both. The lattice parameter 'alat' is set to alat = celldm(1) (in a.u.) or alat = A (in Angstrom); see below for the other parameters. For ibrav=0 specify the lattice vectors in CELL_PARAMETER, optionally the lattice parameter alat = celldm(1) (in a.u.) or = A (in Angstrom), or else it is taken from CELL_PARAMETERS  ibrav      structure                   celldm(2)-celldm(6) or: b,c,cosbc,cosac,cosab 0          free crystal axis provided in input: see card CELL_PARAMETERS  1          cubic P (sc) v1 = a(1,0,0),  v2 = a(0,1,0),  v3 = a(0,0,1)  2          cubic F (fcc) v1 = (a/2)(-1,0,1),  v2 = (a/2)(0,1,1), v3 = (a/2)(-1,1,0)  3          cubic I (bcc) v1 = (a/2)(1,1,1),  v2 = (a/2)(-1,1,1),  v3 = (a/2)(-1,-1,1) -3          cubic I (bcc), more symmetric axis: v1 = (a/2)(-1,1,1), v2 = (a/2)(1,-1,1),  v3 = (a/2)(1,1,-1)  4          Hexagonal and Trigonal P        celldm(3)=c/a v1 = a(1,0,0),  v2 = a(-1/2,sqrt(3)/2,0),  v3 = a(0,0,c/a)  5          Trigonal R, 3fold axis c        celldm(4)=cos(gamma) The crystallographic vectors form a three-fold star around the z-axis, the primitive cell is a simple rhombohedron: v1 = a(tx,-ty,tz),   v2 = a(0,2ty,tz),   v3 = a(-tx,-ty,tz) where c=cos(gamma) is the cosine of the angle gamma between any pair of crystallographic vectors, tx, ty, tz are: tx=sqrt((1-c)/2), ty=sqrt((1-c)/6), tz=sqrt((1+2c)/3) -5          Trigonal R, 3fold axis <111>    celldm(4)=cos(gamma) The crystallographic vectors form a three-fold star around <111>. Defining a' = a/sqrt(3) : v1 = a' (u,v,v),   v2 = a' (v,u,v),   v3 = a' (v,v,u) where u and v are defined as u = tz - 2*sqrt(2)*ty,  v = tz + sqrt(2)*ty and tx, ty, tz as for case ibrav=5 Note: if you prefer x,y,z as axis in the cubic limit, set  u = tz + 2*sqrt(2)*ty,  v = tz - sqrt(2)*ty See also the note in Modules/latgen.f90  6          Tetragonal P (st)               celldm(3)=c/a v1 = a(1,0,0),  v2 = a(0,1,0),  v3 = a(0,0,c/a)  7          Tetragonal I (bct)              celldm(3)=c/a v1=(a/2)(1,-1,c/a),  v2=(a/2)(1,1,c/a),  v3=(a/2)(-1,-1,c/a)  8          Orthorhombic P                  celldm(2)=b/a celldm(3)=c/a v1 = (a,0,0),  v2 = (0,b,0), v3 = (0,0,c)  9          Orthorhombic base-centered(bco) celldm(2)=b/a celldm(3)=c/a v1 = (a/2, b/2,0),  v2 = (-a/2,b/2,0),  v3 = (0,0,c) -9          as 9, alternate description v1 = (a/2,-b/2,0),  v2 = (a/2, b/2,0),  v3 = (0,0,c)  10          Orthorhombic face-centered      celldm(2)=b/a celldm(3)=c/a v1 = (a/2,0,c/2),  v2 = (a/2,b/2,0),  v3 = (0,b/2,c/2)  11          Orthorhombic body-centered      celldm(2)=b/a celldm(3)=c/a v1=(a/2,b/2,c/2),  v2=(-a/2,b/2,c/2),  v3=(-a/2,-b/2,c/2)  12          Monoclinic P, unique axis c     celldm(2)=b/a celldm(3)=c/a, celldm(4)=cos(ab) v1=(a,0,0), v2=(b*cos(gamma),b*sin(gamma),0),  v3 = (0,0,c) where gamma is the angle between axis a and b. -12          Monoclinic P, unique axis b     celldm(2)=b/a celldm(3)=c/a, celldm(5)=cos(ac) v1 = (a,0,0), v2 = (0,b,0), v3 = (c*cos(beta),0,c*sin(beta)) where beta is the angle between axis a and c  13          Monoclinic base-centered        celldm(2)=b/a celldm(3)=c/a, celldm(4)=cos(ab) v1 = (  a/2,         0,                -c/2), v2 = (b*cos(gamma), b*sin(gamma), 0), v3 = (  a/2,         0,                  c/2), where gamma is the angle between axis a and b  14          Triclinic                       celldm(2)= b/a, celldm(3)= c/a, celldm(4)= cos(bc), celldm(5)= cos(ac), celldm(6)= cos(ab) v1 = (a, 0, 0), v2 = (b*cos(gamma), b*sin(gamma), 0) v3 = (c*cos(beta),  c*(cos(alpha)-cos(beta)cos(gamma))/sin(gamma), c*sqrt( 1 + 2*cos(alpha)cos(beta)cos(gamma) - cos(alpha)^2-cos(beta)^2-cos(gamma)^2 )/sin(gamma) ) where alpha is the angle between axis b and c beta is the angle between axis a and c gamma is the angle between axis a and b",
        )
    )
    nat: int | None = Field(None, description="number of atoms in the unit cell")
    ntyp: int | None = Field(None, description="number of types of atoms in the unit cell")
    nbnd: int | None = Field(
        None,
        description="number of electronic states (bands) to be calculated. Note that in spin-polarized calculations the number of k-point, not the number of bands per k-point, is doubled",
    )
    tot_charge: float = Field(
        0.0,
        description="total charge of the system. Useful for simulations with charged cells. By default the unit cell is assumed to be neutral (tot_charge=0). tot_charge=+1 means one electron missing from the system, tot_charge=-1 means one additional electron, and so on.  In a periodic calculation a compensating jellium background is inserted to remove divergences if the cell is not neutral.",
    )
    tot_magnetization: float | None = Field(
        None,
        description="total majority spin charge - minority spin charge. Used to impose a specific total electronic magnetization. If unspecified, the tot_magnetization variable is ignored and the electronic magnetization is determined by the occupation numbers (see card OCCUPATIONS) read from input.",
    )
    ecutwfc: float | None = Field(None, description="kinetic energy cutoff (Ry) for wavefunctions")
    ecutrho: float | None = Field(
        None,
        description="kinetic energy cutoff (Ry) for charge density and potential For norm-conserving pseudopotential you should stick to the default value, you can reduce it by a little but it will introduce noise especially on forces and stress. If there are ultrasoft PP, a larger value than the default is often desirable (ecutrho = 8 to 12 times ecutwfc, typically). PAW datasets can often be used at 4*ecutwfc, but it depends on the shape of augmentation charge: testing is mandatory. The use of gradient-corrected functional, especially in cells with vacuum, or for pseudopotential without non-linear core correction, usually requires an higher values of ecutrho to be accurately converged.",
    )
    occupations: str | None = Field(
        None,
        description="a string describing the occupation of the electronic states. In the case of conjugate gradient style of minimization of the electronic states, if occupations is set to 'ensemble', this allows ensemble DFT calculations for metallic systems",
    )
    degauss: float | None = Field(
        None,
        description="parameter for the smearing function, only used for ensemble DFT calculations",
    )
    smearing: str | None = Field(
        None,
        description="a string describing the kind of occupations for electronic states in the case of ensemble DFT (occupations == 'ensemble' ); now only Fermi-Dirac ('fd') case is implemented",
    )
    nspin: int = Field(
        1,
        description="nspin = 1 :  non-polarized calculation (default)  nspin = 2 :  spin-polarized calculation, LSDA (magnetization along z axis)",
    )
    ecfixed: float = Field(0.0, description="")
    qcutz: float = Field(0.0, description="")
    q2sigma: float = Field(
        0.1,
        description="ecfixed, qcutz, q2sigma:  parameters for modified functional to be used in variable-cell molecular dynamics (or in stress calculation). 'ecfixed' is the value (in Rydberg) of the constant-cutoff; 'qcutz' and 'q2sigma' are the height and the width (in Rydberg) of the energy step for reciprocal vectors whose square modulus is greater than 'ecfixed'. In the kinetic energy, G^2 is replaced by G^2 + qcutz * (1 + erf ( (G^2 - ecfixed)/q2sigma) ) See: M. Bernasconi et al, J. Phys. Chem. Solids 56, 501 (1995)",
    )
    input_dft: str | None = Field(
        None,
        description="Exchange-correlation functional: eg 'PBE', 'BLYP' etc See Modules/funct.f90 for allowed values. Overrides the value read from pseudopotential files. Use with care and if you know what you are doing!  Use 'PBE0' to perform hybrid functional calculation using Wannier functions. Allowed calculation: 'cp-wf' and 'vc-cp-wf' See CP specific user manual for further guidance (or in CPV/Doc/user_guide.tex) and examples in CPV/examples/EXX-wf-example. Also see related keywords starting with exx_.",
    )
    exx_fraction: float | None = Field(
        None,
        description="Fraction of EXX for hybrid functional calculations. In the case of input_dft='PBE0', the default value is 0.25.",
    )
    lda_plus_u: bool = Field(
        False,
        description="lda_plus_u = .TRUE. enables calculation with LDA+U ('rotationally invariant'). See also Hubbard_U. Anisimov, Zaanen, and Andersen, PRB 44, 943 (1991) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.44.943); Anisimov et al., PRB 48, 16929 (1993) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.48.16929); Liechtenstein, Anisimov, and Zaanen, PRB 52, R5467 (1994) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.52.R5467); Cococcioni and de Gironcoli, PRB 71, 035105 (2005) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.71.035105).",
    )
    vdw_corr: str = Field(
        "none",
        description="Type of Van der Waals correction. Allowed values:  'grimme-d2', 'Grimme-D2', 'DFT-D', 'dft-d': semiempirical Grimme's DFT-D2. Optional variables: 'london_s6', 'london_rcut' S. Grimme, J. Comp. Chem. 27, 1787 (2006), V. Barone et al., J. Comp. Chem. 30, 934 (2009).  'TS', 'ts', 'ts-vdw', 'ts-vdW', 'tkatchenko-scheffler': Tkatchenko-Scheffler dispersion corrections with first-principle derived C6 coefficients Optional variables: 'ts_vdw_econv_thr', 'ts_vdw_isolated' See A. Tkatchenko and M. Scheffler, Phys. Rev. Lett. 102, 073005 (2009)  'XDM', 'xdm': Exchange-hole dipole-moment model. Optional variables: 'xdm_a1', 'xdm_a2' (implemented in PW only) A. D. Becke and E. R. Johnson, J. Chem. Phys. 127, 154108 (2007) A. Otero de la Roza, E. R. Johnson, J. Chem. Phys. 136, 174109 (2012)  Note that non-local functionals (eg vdw-DF) are NOT specified here but in 'input_dft",
    )
    london_s6: float = Field(
        0.75, description="global scaling parameter for DFT-D. Default is good for PBE."
    )
    london_rcut: float = Field(200, description="cutoff radius (a.u.) for dispersion interactions")
    ts_vdw: bool = Field(False, description="OBSOLESCENT, same as vdw_corr='TS")
    ts_vdw_econv_thr: float = Field(
        1.0e-6,
        description="Optional: controls the convergence of the vdW energy (and forces). The default value is a safe choice, likely too safe, but you do not gain much in increasing it",
    )
    ts_vdw_isolated: bool = Field(
        False,
        description="Optional: set it to .TRUE. when computing the Tkatchenko-Scheffler vdW energy for an isolated (non-periodic) system.",
    )
    assume_isolated: str = Field(
        "none",
        description="Used to perform calculation assuming the system to be isolated (a molecule of a clustr in a 3D supercell).  Currently available choices:  'none' (default): regular periodic calculation w/o any correction.  'makov-payne', 'm-p', 'mp' : the Makov-Payne correction to the total energy is computed. Theory: G.Makov, and M.C.Payne, 'Periodic boundary conditions in ab initio calculations' , Phys.Rev.B 51, 4014 (1995)",
    )


class ElectronsNamelist(Namelist):
    """Pydantic model for the `ELECTRONS` namelist."""

    electron_maxstep: int = Field(100, description="maximum number of iterations in a scf step")
    electron_dynamics: str = Field(
        "none",
        description="set how electrons should be moved 'none'    : electronic degrees of freedom (d.o.f.) are kept fixed 'sd'      : steepest descent algorithm is used to minimize electronic d.o.f. 'damp'    : damped dynamics is used to propagate electronic d.o.f. 'verlet'  : standard Verlet algorithm is used to propagate electronic d.o.f. 'cg'      : conjugate gradient is used to converge the wavefunction at each ionic step. 'cg' can be used interchangeably with 'verlet' for a couple of ionic steps in order to 'cool down' the electrons and return them back to the Born-Oppenheimer surface. Then 'verlet' can be restarted again. This procedure is useful when electronic adiabaticity in CP is lost yet the ionic velocities need to be preserved.",
    )
    conv_thr: float = Field(
        1.0e-6,
        description="Convergence threshold for selfconsistency: estimated energy error < conv_thr",
    )
    niter_cg_restart: int = Field(
        20,
        description="frequency in iterations for which the conjugate-gradient algorithm for electronic relaxation is restarted",
    )
    efield: float = Field(
        0.0e0,
        description="Amplitude of the finite electric field (in a.u.; 1 a.u. = 51.4220632*10^10 V/m). Used only if tefield=.TRUE.",
    )
    epol: int = Field(
        3,
        description="direction of the finite electric field (only if tefield == .TRUE.) In the case of a PARALLEL calculation only the case epol==3 is implemented",
    )
    emass: float = Field(
        400.0e0,
        description="effective electron mass in the CP Lagrangian, in atomic units ( 1 a.u. of mass = 1/1822.9 a.m.u. = 9.10939 * 10^-31 kg )",
    )
    emass_cutoff: float = Field(
        2.5e0,
        description="mass cut-off (in Rydberg) for the Fourier acceleration effective mass is rescaled for 'G' vector components with kinetic energy above 'emass_cutoff",
    )
    orthogonalization: str = Field(
        "ortho",
        description="selects the orthonormalization method for electronic wave functions 'ortho'        : use iterative algorithm - if it doesn't converge, reduce the timestep, or use options ortho_max and ortho_eps, or use Gram-Schmidt instead just to start the simulation 'Gram-Schmidt' : use Gram-Schmidt algorithm - to be used ONLY in the first few steps. YIELDS INCORRECT ENERGIES AND EIGENVALUES.",
    )
    ortho_eps: float = Field(
        1.0e-8,
        description="tolerance for iterative orthonormalization meaningful only if orthogonalization = 'ortho",
    )
    ortho_max: int = Field(
        20,
        description="maximum number of iterations for orthonormalization meaningful only if orthogonalization = 'ortho",
    )
    ortho_para: int = Field(0, description="")
    electron_damping: float = Field(
        0.1e0,
        description="damping frequency times delta t, optimal values could be calculated with the formula : SQRT( 0.5 * LOG( ( E1 - E2 ) / ( E2 - E3 ) ) ) where E1, E2, E3 are successive values of the DFT total energy in a steepest descent simulations. meaningful only if ' electron_dynamics = 'damp",
    )
    electron_velocities: str | None = Field(
        None,
        description="zero'      : restart setting electronic velocities to zero 'default'   : restart using electronic velocities of the previous run",
    )
    electron_temperature: str = Field(
        "not_controlled",
        description="nose'            : control electronic temperature using Nose thermostat. See also 'fnosee' and 'ekincw'. 'rescaling'       : control electronic temperature via velocities rescaling. 'not_controlled'  : electronic temperature is not controlled.",
    )
    ekincw: float = Field(
        0.001e0,
        description="value of the average kinetic energy (in atomic units) forced by the temperature control meaningful only with ' electron_temperature /= 'not_controlled",
    )
    fnosee: float = Field(
        1.0e0,
        description="oscillation frequency of the nose thermostat (in terahertz) meaningful only with ' electron_temperature = 'nose",
    )
    startingwfc: str = Field(
        "random",
        description="atomic': start from superposition of atomic orbitals (not yet implemented)   'random': start from random wfcs. See 'ampre'.",
    )
    tcg: bool = Field(
        False,
        description="if .TRUE. perform a conjugate gradient minimization of the electronic states for every ionic step. It requires Gram-Schmidt orthogonalization of the electronic states.",
    )
    maxiter: int = Field(
        100,
        description="maximum number of conjugate gradient iterations for conjugate gradient minimizations of electronic states",
    )
    passop: float = Field(
        0.3e0,
        description="small step used in the  conjugate gradient minimization of the electronic states.",
    )
    n_inner: int = Field(
        2,
        description="number of internal cycles for every conjugate gradient iteration only for ensemble DFT",
    )
    ninter_cold_restart: int = Field(
        1,
        description="frequency in iterations at which a full inner cycle, only for cold smearing, is performed",
    )
    lambda_cold: float = Field(
        0.03e0,
        description="step for inner cycle with cold smearing, used when a not full cycle is performed",
    )
    grease: float = Field(
        1.0e0,
        description="a number <= 1, very close to 1: the damping in electronic damped dynamics is multiplied at each time step by 'grease' (avoids overdamping close to convergence: Obsolete ?) grease = 1 : normal damped dynamics",
    )
    ampre: float = Field(
        0.0e0,
        description="amplitude of the randomization ( allowed values: 0.0 - 1.0 ) meaningful only if ' startingwfc = 'random",
    )


class IonsNamelist(Namelist):
    """Pydantic model for the `IONS` namelist."""

    ion_dynamics: str | None = Field(
        None,
        description="Specify the type of ionic dynamics.  For constrained dynamics or constrained optimisations add the CONSTRAINTS card (when the card is present the SHAKE algorithm is automatically used). 'none'    : ions are kept fixed 'sd'      : steepest descent algorithm is used to minimize ionic configuration 'cg'      : conjugate gradient algorithm is used to minimize ionic configuration 'damp'    : damped dynamics is used to propagate ions 'verlet'  : standard Verlet algorithm is used to propagate ions",
    )
    ion_positions: str = Field(
        "default",
        description="default '  : if restarting, use atomic positions read from the restart file; in all other cases, use atomic positions from standard input.  'from_input' : restart the simulation with atomic positions read from standard input, even if restarting.",
    )
    ion_velocities: str = Field(
        "default",
        description="initial ionic velocities 'default'     : restart the simulation with atomic velocities read from the restart file 'change_step' : restart the simulation with atomic velocities read from the restart file, with rescaling due to the timestep change, specify the old step via tolp as in tolp = 'old_time_step_value' in au 'random'      : start the simulation with random atomic velocities 'from_input'  : restart the simulation with atomic velocities read from standard input - see card 'ATOMIC_VELOCITIES' BEWARE: works only if restart_mode='from_scratch', tested only with electrons_dynamics='cg' 'zero'        : restart the simulation with atomic velocities set to zero",
    )
    ion_damping: float = Field(
        0.2e0,
        description="damping frequency times delta t, optimal values could be calculated with the formula : SQRT( 0.5 * LOG( ( E1 - E2 ) / ( E2 - E3 ) ) ) where E1, E2, E3 are successive values of the DFT total energy in a steepest descent simulations. meaningful only if ' ion_dynamics = 'damp",
    )
    iesr: int = Field(
        1,
        description="The real-space contribution to the Ewald summation is performed on iesr*iesr*iesr cells. Typically iesr=1 is sufficient to have converged results.",
    )
    ion_nstepe: int = Field(1, description="number of electronic steps per ionic step.")
    remove_rigid_rot: bool = Field(
        False,
        description="This keyword is useful when simulating the dynamics and/or the thermodynamics of an isolated system. If set to true the total torque of the internal forces is set to zero by adding new forces that compensate the spurious interaction with the periodic images. This allows for the use of smaller supercells.  BEWARE: since the potential energy is no longer consistent with the forces (it still contains the spurious interaction with the repeated images), the total energy is not conserved anymore. However the dynamical and thermodynamical properties should be in closer agreement with those of an isolated system. Also the final energy of a structural relaxation will be higher, but the relaxation itself should be faster.",
    )
    ion_temperature: str = Field(
        "not_controlled",
        description="nose'           : control ionic temperature using Nose-Hoover thermostat  see parameters 'fnosep', 'tempw', 'nhpcl', 'ndega', 'nhptyp' 'rescaling'      : control ionic temperature via velocities rescaling. see parameter 'tolp' 'not_controlled' : ionic temperature is not controlled",
    )
    tempw: float = Field(
        300.0e0,
        description="value of the ionic temperature (in Kelvin) forced by the temperature control. meaningful only with ' ion_temperature /= 'not_controlled' ' or when the initial velocities are set to 'random' 'ndega' controls number of degrees of freedom used in temperature calculation",
    )
    fnosep: float = Field(
        1.0e0,
        description="oscillation frequency of the nose thermostat (in terahertz) [note that 3 terahertz = 100 cm^-1] meaningful only with ' ion_temperature = 'nose' ' for Nose-Hoover chain one can set frequencies of all thermostats ( fnosep = X Y Z etc. ) If only first is set, the defaults for the others will be same.",
    )
    tolp: float = Field(
        100.0e0,
        description="tolerance (in Kelvin) of the rescaling. When ionic temperature differs from 'tempw' more than 'tolp' apply rescaling. meaningful only with ' ion_temperature = 'rescaling' ' and with ion_velocities='change_step', where it specifies the old timestep",
    )
    nhpcl: int = Field(
        1,
        description="number of thermostats in the Nose-Hoover chain currently maximum allowed is 4",
    )
    nhptyp: int = Field(
        0,
        description="type of the 'massive' Nose-Hoover chain thermostat nhptyp=1 uses a NH chain per each atomic type nhptyp=2 uses a NH chain per atom, this one is useful for extremely rapid equipartitioning (equilibration is a different beast) nhptyp=3 together with nhgrp allows fine grained thermostat control NOTE: if using more than 1 thermostat per system there will be a common thermostat added on top of them all, to disable this common thermostat specify nhptyp=-X instead of nhptyp=X",
    )
    ndega: int = Field(
        0,
        description="number of degrees of freedom used for temperature calculation ndega <= 0 sets the number of degrees of freedom to [3*nat-abs(ndega)], ndega > 0 is used as the target number",
    )
    greasp: float = Field(1.0e0, description="same as 'grease', for ionic damped dynamics.")


class CellNamelist(Namelist):
    """Pydantic model for the `CELL` namelist."""

    cell_parameters: str | None = Field(
        None,
        description="default'      : restart the simulation with cell parameters read from the restart file or 'celldm' if 'restart = 'from_scratch'' 'from_input'   : restart the simulation with cell parameters from standard input. ( see the card 'CELL_PARAMETERS' )",
    )
    cell_dynamics: str = Field(
        "none",
        description="set how cell should be moved 'none'      : cell is kept fixed 'sd'        : steepest descent algorithm is used to optimise the cell 'damp-pr'   : damped dynamics is used to optimise the cell ( Parrinello-Rahman method ). 'pr'        : standard Verlet algorithm is used to propagate the cell ( Parrinello-Rahman method ).",
    )
    cell_velocities: str | None = Field(
        None,
        description="zero'      : restart setting cell velocity to zero 'default'   : restart using cell velocity of the previous run",
    )
    cell_damping: float = Field(
        0.1e0,
        description="damping frequency times delta t, optimal values could be calculated with the formula : SQRT( 0.5 * LOG( ( E1 - E2 ) / ( E2 - E3 ) ) ) where E1, E2, E3 are successive values of the DFT total energy in a steepest descent simulations. meaningful only if ' cell_dynamics = 'damp",
    )
    press: float = Field(
        0.0e0, description="Target pressure [KBar] in a variable-cell md or relaxation run."
    )
    wmass: float | None = Field(
        None,
        description="Fictitious cell mass [amu] for variable-cell simulations (both 'vc-md' and 'vc-relax')",
    )
    cell_factor: float = Field(
        1.2e0,
        description="Used in the construction of the pseudopotential tables. It should exceed the maximum linear contraction of the cell during a simulation.",
    )
    cell_temperature: str = Field(
        "not_controlled",
        description="nose'            : control cell temperature using Nose thermostat see parameters 'fnoseh' and 'temph'. 'rescaling'       : control cell temperature via velocities rescaling. 'not_controlled'  : cell temperature is not controlled.",
    )
    temph: float = Field(
        0.0e0,
        description="value of the cell temperature (in ???) forced by the temperature control. meaningful only with ' cell_temperature /= 'not_controlled",
    )
    fnoseh: float = Field(
        1.0e0,
        description="oscillation frequency of the nose thermostat (in terahertz) meaningful only with ' cell_temperature = 'nose",
    )
    greash: float = Field(1.0e0, description="same as 'grease', for cell damped dynamics")
    cell_dofree: str = Field(
        "all",
        description="Select which of the cell parameters should be moved:  all     = all axis and angles are moved x       = only the x component of axis 1 (v1_x) is moved y       = only the y component of axis 2 (v2_y) is moved z       = only the z component of axis 3 (v3_z) is moved xy      = only v1_x and v2_y are moved xz      = only v1_x and v3_z are moved yz      = only v2_y and v3_z are moved xyz     = only v1_x, v2_y, v3_z are moved shape   = all axis and angles, keeping the volume fixed 2Dxy    = only x and y components are allowed to change 2Dshape = as above, keeping the area in xy plane fixed volume  = isotropic variations of v1_x, v2_y, v3_z, keeping the shape fixed. Should be used only with ibrav=1.",
    )


class PressAiNamelist(Namelist):
    """Pydantic model for the `PRESS_AI` namelist."""

    abivol: bool = Field(False, description=".true. for finite pressure calculations")
    P_ext: float = Field(0.0e0, description="external pressure in GPa")
    pvar: bool = Field(
        False,
        description=".true. for variable pressure calculations pressure changes linearly with time: Delta_P = (P_fin - P_in)/nstep",
    )
    P_in: float = Field(
        0.0e0, description="only if pvar = .true. initial value of the external pressure (GPa)"
    )
    P_fin: float = Field(
        0.0e0, description="only if pvar = .true. final value of the external pressure (GPa)"
    )
    Surf_t: float = Field(
        0.0e0, description="Surface tension (in a.u.; typical values 1.d-4 - 1.d-3)"
    )
    rho_thr: float = Field(
        0.0e0,
        description="threshold parameter which defines the electronic charge density isosurface to compute the 'quantum' volume of the system (typical values: 1.d-4 - 1.d-3) (corresponds to alpha in PRL 94 145501 (2005) (https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.94.145501))",
    )
    dthr: float = Field(
        0.0e0,
        description="thikness of the external skin of the electronic charge density used to compute the 'quantum' surface (typical values: 1.d-4 - 1.d-3; 50% to 100% of rho_thr) (corresponds to Delta in PRL 94 145501 (2005) (https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.94.145501))",
    )


class WannierNamelist(Namelist):
    """Pydantic model for the `WANNIER` namelist."""

    wf_efield: bool = Field(
        False, description="If dynamics will be done in the presence of a field"
    )
    wf_switch: bool = Field(
        False,
        description="Whether to turn on the field adiabatically (adiabatic switch) if true, then nbeg is set to 0.",
    )
    sw_len: int = Field(
        1,
        description="No. of iterations over which the field will be turned on to its final value. Starting value is 0.0 If sw_len < 0, then it is set to 1. If you want to just optimize structures on the presence of a field, then you may set this to 1 and run a regular geometry optimization.",
    )
    wfsd: int = Field(
        1,
        description="Localization algorithm for Wannier function calculation: wfsd=1  Damped Dynamics wfsd=2  Steepest-Descent / Conjugate-Gradient wfsd=3  Jocobi Rotation Remember, this is consistent with all the calwf options as well as the tolw (see below). Not a good idea to Wannier dynamics with this if you are using restart='from_scratch' option, since the spreads converge fast in the beginning and ortho goes bananas.",
    )
    wfdt: float = Field(5.0e0, description="The minimum step size to take in the SD/CG direction")
    maxwfdt: float = Field(
        0.3e0,
        description="The maximum step size to take in the SD/CG direction The code calculates an optimum step size, but that may be either too small (takes forever to converge)  or too large (code goes crazy) . This option keeps the step size between wfdt and maxwfdt. In my experience 0.1 and 0.5 work quite well. (but don't blame me if it doesn't work for you)",
    )
    nit: int = Field(10, description="Number of iterations to do for Wannier convergence.")
    nsd: int = Field(
        10,
        description="Out of a total of NIT iterations, NSD will be Steepest-Descent and ( nit - nsd ) will be Conjugate-Gradient.",
    )
    wf_q: float = Field(
        1500.0e0,
        description="Fictitious mass of the A matrix used for obtaining maximally localized Wannier functions. The unitary transformation matrix U is written as exp(A) where A is a anti-hermitian matrix. The Damped-Dynamics is performed in terms of the A matrix, and then U is computed from A. Usually a value between 1500 and 2500 works fine, but should be tested.",
    )
    wf_friction: float = Field(0.3e0, description="Damping coefficient for Damped-Dynamics.")
    nsteps: int = Field(
        20, description="Number of Damped-Dynamics steps to be performed per CP iteration."
    )
    tolw: float = Field(1.0e-8, description="Convergence criterion for localization.")
    adapt: bool = Field(True, description="Whether to adapt the damping parameter dynamically.")
    calwf: int = Field(
        3,
        description="Wannier Function Options, can be 1,2,3,4,5  1. Output the Wannier function density, nwf and wffort are used for this option. see below. 2. Output the Overlap matrix O_i,j=<w_i|exp{iGr}|w_j>. O is written to unit 38. For details on how O is constructed, see below. 3. Perform nsteps of Wannier dynamics per CP iteration, the orbitals are now Wannier Functions, not Kohn-Sham orbitals. This is a Unitary transformation of the occupied subspace and does not leave the CP Lagrangian invariant. Expectation values remain the same. So you will **NOT** have a constant of motion during the run. Don't freak out, its normal. 4. This option starts for the KS states and does 1 CP iteration and nsteps of Damped-Dynamics to generate  maximally localized wannier functions. Its useful when you have the converged KS groundstate and want to get to the converged Wannier function groundstate in 1 CP Iteration. 5. This option is similar to calwf 1, except that the output is the Wannier function/wavefunction, and not the orbital density. See nwf below.",
    )
    nwf: int = Field(
        0,
        description="This option is used with calwf 1 and calwf 5. with calwf=1, it tells the code how many Orbital densities are to be output. With calwf=5, set this to 1(i.e calwf=5 only writes one state during one run. so if you want 10 states, you have to run the code 10 times). With calwf=1, you can print many orbital densities in a single run. See also the PLOT_WANNIER card for specifying the states to be printed.",
    )
    wffort: int = Field(
        40,
        description="This tells the code where to dump the orbital densities. Used only with CALWF=1. for e.g. if you want to print 2 orbital densities, set calwf=1, nwf=2 and wffort to an appropriate number (e.g. 40) then the first orbital density will be output to fort.40, the second to fort.41 and so on. Note that in the current implementation, the following units are used 21,22,24,25,26,27,28,38,39,77,78 and whatever you define as ndr and ndw. so use number other than these.",
    )
    writev: bool = Field(
        False,
        description="Output the charge density (g-space) and the list of g-vectors This is useful if you want to reconstruct the electrostatic potential using the Poisson equation. If .TRUE. then the code will output the g-space charge density and the list if G-vectors, and STOP. Charge density is written to : CH_DEN_G_PARA.ispin (1 or 2 depending on the number of spin types) or CH_DEN_G_SERL.ispin depending on if the code is being run in parallel or serial G-vectors are written to G_PARA or G_SERL.",
    )
    exx_neigh: int = Field(
        60,
        description="An initial guess on the maximum number of neighboring (overlapping) Wannier functions.",
    )
    exx_dis_cutoff: float = Field(
        8.0,
        description="Radial cutoff distance (in bohr) for including overlapping Wannier function pairs in EXX calculations.",
    )
    exx_poisson_eps: float = Field(
        1.0e-6,
        description="Poisson solver convergence criterion during computation of the EXX potential.",
    )
    exx_ps_rcut_self: float = Field(
        6.0,
        description="Radial cutoff distance (in bohr) to compute the self EXX energy. This distance determines the radius of the Poisson sphere centered at a given Wannier function center, and should be large enough to cover the majority of the orbital charge density.",
    )
    exx_ps_rcut_pair: float = Field(
        5.0,
        description="Radial cutoff distance (in bohr) to compute the pair EXX energy. This distance determines the radius of the Poisson sphere centered at the midpoint of two overlapping Wannier functions, and should be large enough to cover the majority of the orbital overlap charge density. This parameter can generally be chosen as smaller than exx_ps_rcut_self.",
    )
    exx_me_rcut_self: float = Field(
        10.0,
        description="Radial cutoff distance (in bohr) for the multipole-expansion sphere centered at a given Wannier function center. The far-field self EXX potential in this sphere is generated with multipole expansion of the orbital charge density.",
    )
    exx_me_rcut_pair: float = Field(
        7.0,
        description="Radial cutoff distance (in bohr) for the multipole-expansion sphere centered at the midpoint of two overlapping Wannier functions. The far-field pair EXX potential in this sphere is generated with a multipole expansion of the orbital overlap charge density. This parameter can generally be chosen as smaller than exx_me_rcut_self.",
    )


class CPEspressoInput(EspressoInput):
    """Pydantic model for the input of `cp.x`"""

    control: ControlNamelist = Field(default_factory=lambda: ControlNamelist())
    system: SystemNamelist = Field(default_factory=lambda: SystemNamelist())
    electrons: ElectronsNamelist = Field(default_factory=lambda: ElectronsNamelist())
    ions: IonsNamelist = Field(default_factory=lambda: IonsNamelist())
    cell: CellNamelist = Field(default_factory=lambda: CellNamelist())
    press_ai: PressAiNamelist = Field(default_factory=lambda: PressAiNamelist())
    wannier: WannierNamelist = Field(default_factory=lambda: WannierNamelist())
