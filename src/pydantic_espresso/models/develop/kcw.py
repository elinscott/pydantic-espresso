"""Pydantic model for the input of `kcw.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from textwrap import dedent
from typing import Annotated, Literal

from pydantic import Field, field_validator

from pydantic_espresso.card.pw.k_points import KPointsCard
from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class ControlNamelist(Namelist):
    """Pydantic model for the `CONTROL` namelist."""

    @field_validator("assume_isolated", mode="before")
    @classmethod
    def map_assume_isolated(cls, v: str) -> str:
        """Map equivalent values for `assume_isolated` onto a canonical value."""
        mapping = {"m-t": "martyna-tuckerman", "mt": "martyna-tuckerman"}
        return mapping.get(v, v)

    prefix: str = Field(
        "pwscf",
        description=dedent(
            """\
            Prepended to input/output filenames; must be the same used in the previous PW
            calculations."""
        ),
    )
    outdir: Path | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "ESPRESSO_TMPDIR environment variable is set",
                    "value": "value of the ESPRESSO_TMPDIR environment variable",
                },
                {"when": None, "value": "'./'"},
            ],
        },
        description=dedent(
            """\
            Directory containing input, output, and scratch files; must be the same as specified in
            the calculation of previous PW calculation."""
        ),
    )
    calculation: Literal[None, "wann2kcw", "screen", "ham", "cc"] = Field(
        None,
        description=dedent(
            """\
            Specify the KCW calculation to be done Possible choices:
            - 'wann2kcw': Pre-processing to prepare KCW calculation. Read previous PWSCF and
              possibly W90 outputs and prepare the KCW calculation.
            - 'screen': Perform the calculation of KCW screening coefficient using a LR approach as
              described here https://doi.org/10.1021/acs.jctc.7b01116 and arXiv:2202.08155
              (https://arxiv.org/abs/2202.08155).
            - 'ham': Perform the calculation interpolation and diagonalization of the KI
              hamiltonian.
            - 'cc': Computes the (estimated) q+G=0 contribution to the bare and screened KC
              corrections. A report on this quantities is printed on output and can be used to
              correct a posteriori a 'screen' calculation performed without any corrective scheme
              (l_vcut=.false.) avoiding the need of re-doing a 'screen' calculation."""
        ),
    )
    kcw_iverbosity: Literal[0, 1, 2] = Field(
        1,
        description=dedent(
            """\
            Verbosity level of the KCW output.
            - '0': Minimal output.
            - '1': As above + performs additional checks.
            - '2': As above + additional infos on all the steps (any value > 1 selects this
              verbosity tier)."""
        ),
    )
    kcw_at_ks: bool = Field(
        True,
        description=dedent(
            """\
            If true the KS canonical orbitals are used instead of Wannier functions. It makes sense
            for isolated system only."""
        ),
    )
    read_unitary_matrix: bool = Field(
        False,
        description=dedent(
            """\
            If true read the Unitary matrix written by Wannier90. Implicitely means a previous
            wannier90 calculation was performed and a KCW calculation will be performed starting
            from MLWF. Requires 'write_hr = .true.' in wannier90."""
        ),
    )
    spread_thr: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.001,
        description=dedent(
            """\
            HARD-CODED FOR NOW. Two or more Wannier functions are considered identical if their
            spread (self-hartree) differ by less than spread_thr. Requires check_spread = .true."""
        ),
    )
    homo_only: bool = Field(
        False,
        description=dedent(
            """\
            If kcw_at_ks = .TRUE. only the screening paramenter for the HOMO is calculated. Mainly
            for a perturbative calculation of the first Ionization Potential in isolated systems."""
        ),
    )
    l_vcut: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE. the Gygi-Baldereschi scheme is used to deal with the q->0 divergence of the
            Coulomb integral (bare and screened). Improves the convergence wrt k/q-point sampling.
            Requires to correctly set eps_inf for the calculation of the screened interaction.  Use
            it only for periodic system. For isoleted system use assume_isolated, instead."""
        ),
    )
    assume_isolated: Literal["none", "martyna-tuckerman"] = Field(
        "none",
        description=dedent(
            """\
            Used to perform calculation assuming the system to be isolated (a molecule or a cluster
            in a 3D supercell).  Currently available choices:
            - 'none': regular periodic calculation w/o any correction.
            - 'martyna-tuckerman': Martyna-Tuckerman correction to both total energy and scf
              potential. Adapted from: G.J. Martyna, and M.E. Tuckerman, 'A reciprocal space based
              method for treating long range interactions in ab-initio and force-field-based
              calculation in clusters', J. Chem. Phys. 110, 2810 (1999), doi:10.1063/1.477923
              (https://doi.org/10.1063/1.477923)."""
        ),
    )
    spin_component: Literal[1, 2] = Field(
        1,
        description=dedent(
            """\
            Which spin channel to calculate (only collinear calculation). It has to be consistent
            with the previous Wannier90 calculation (see 'spin' keyword in Wannier90 documentation).
            - '1': spin up channel.
            - '2': spin down channel."""
        ),
    )
    mp1: int = Field(
        -1,
        description=dedent(
            """\
            Parameters of the Monkhorst-Pack grid (no offset). Same meaning as for nk1, nk2, nk3 in
            the input of pw.x. It has to coincide with the regular mesh used for the wannier90
            calculation."""
        ),
    )
    mp2: int = Field(
        -1,
        description=dedent(
            """\
            Parameters of the Monkhorst-Pack grid (no offset). Same meaning as for nk1, nk2, nk3 in
            the input of pw.x. It has to coincide with the regular mesh used for the wannier90
            calculation."""
        ),
    )
    mp3: int = Field(
        -1,
        description=dedent(
            """\
            Parameters of the Monkhorst-Pack grid (no offset). Same meaning as for nk1, nk2, nk3 in
            the input of pw.x. It has to coincide with the regular mesh used for the wannier90
            calculation."""
        ),
    )
    lrpa: bool = Field(
        False,
        description=dedent(
            """\
            If .true. the response function is computed neglecting xc effects both in the kernel
            and in the response function (RPA)."""
        ),
    )
    io_sp: bool = Field(
        False, description="If .true. write wannier orbital densities in single-precision."
    )
    io_real_space: bool = Field(
        False,
        description=dedent(
            """\
            If .true. write Wannier orbital densities and Wannier functions in real space."""
        ),
    )
    irr_bz: bool = Field(
        False,
        description=dedent(
            """\
            If .true. compute and use the symmetries of the Wannier orbital densities to reduce the
            number of k and q points for the BZ sampling."""
        ),
    )
    use_wct: bool = Field(
        False,
        description=dedent(
            """\
            If .true. allow to use symmetries that send the Wannier orbital density into the
            Wannier translated by a lattice vector (wcf= wannier center translation) to further
            reduce the number of q points"""
        ),
    )


class WannierNamelist(Namelist):
    """Pydantic model for the `WANNIER` namelist."""

    seedname: str | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "kcw_at_ks is .TRUE.", "value": "value of prefix"},
                {"when": None, "value": "wann"},
            ],
        },
        description=dedent(
            """\
            The seedname of the previous Wannier90 calculation for occupied states. NOTA BENE: the
            code implicitely assumed that the seedname for empty state is the same as that for
            occupied state with '_emp' appended. Keep this in mind when set up the wannier90
            inputs.  For example: wann.win         is the wannier90 input file for the occupied
            states. wann_emp.win     is the wannier90 input file for the empty states."""
        ),
    )
    num_wann_occ: int = Field(
        0,
        description=dedent(
            """\
            The number of wannier function for the occupied manifold. It has to coincide with the
            number of occupied KS orbitals. The whole KS manifold has to be wannierised (no
            'exclude_band' option for occupied state, at the moment)."""
        ),
    )
    num_wann_emp: int = Field(
        0,
        description=dedent(
            """\
            The number of wannier function for the empty manifold. It has to coincide with the
            number of empty wannier function from the previous wannier90 calculation"""
        ),
    )
    have_empty: bool = Field(
        False,
        description=dedent(
            """\
            If true empty state are computed. Require a previous wannier90 calculation for the
            empty manifold. The code search for the unitary matrices in the wannier90 file
            seedname_emp_u.mat"""
        ),
    )
    has_disentangle: bool = Field(
        False,
        description=dedent(
            """\
            Specify if a disentangle unitary matrix needs to be read. Requires a consisten
            calcuation from the previous wannier90 run."""
        ),
    )
    check_ks: bool = Field(
        False,
        description=dedent(
            """\
            Specify if a diagonalization of the KS matrix build using the wannier function in input
            has to be performed. This is mainly for debugging purpose."""
        ),
    )
    alpha_mix: list[float] | None = Field(
        None,
        description=dedent(
            """\
            Mixing factor (for each iteration) for updating the scf potential:  vnew(in) =
            alpha_mix*vold(out) + (1-alpha_mix)*vold(in)"""
        ),
    )


class ScreenNamelist(Namelist):
    """Pydantic model for the `SCREEN` namelist."""

    niter: int | None = Field(
        None,
        json_schema_extra={"default_ref": ""},
        description=dedent(
            """\
            Maximum number of iterations in a scf step. If you want more than 100, edit variable
            'maxter' in PH/phcom.f90"""
        ),
    )
    nmix: int = Field(4, description="Number of iterations used in potential mixing.")
    tr2: float = Field(1e-14, description="Threshold for self-consistency.")
    i_orb: int = Field(
        -1,
        description=dedent(
            """\
            Perform the screening calculation for a particular orbital. If i_orb = -1 all the
            orbitals are computed. Assumes values between 1 and the total number of wannier
            functions."""
        ),
    )
    eps_inf: float = Field(
        1.0e0,
        description=dedent(
            """\
            The macroscopic dielectric constant. Needed for the Gygi-Baldereschi scheme if l_vcut =
            .TRUE. Typically from exp or from a ph.x calculation.  NOTA BENE: This would be
            equivalent to a Makov-Payne correction. It works well for cubic systems. Less well for
            anisotropic systems.  ANISOTROPIC SYSTEMS: In this case a generalization of the GB
            scheme is implemented based on Nano Lett.,9, 975 (2009). It requires the full
            dielectric tensor to be provided. The code searches (in the working dir) for a file
            named 'eps.dat' containing the macrospocic dielectric tensor. If it does not find it,
            the value eps_inf provided in input will be used (isotropic approximation). If not even
            eps_inf is provided in input no correction is applied to the screened KC correction."""
        ),
    )
    check_spread: bool = Field(
        False,
        description=dedent(
            """\
            If .TRUE. the spread (self-hartree) of the Wannier functions is checked and used to
            decide whether two or more Wannier functions can be considered 'identical' or not. Two
            Wannier functions are considered identical if their spread (self-hartree) differ by
            less than 1e-4 Ry (Hard coded for now, see spread_thr)."""
        ),
    )


class HamNamelist(Namelist):
    """Pydantic model for the `HAM` namelist."""

    do_bands: bool = Field(
        False,
        description=dedent(
            """\
            If .true. the interpolated band structure is computed along a path specified with the
            K_POINTS card ( see PW documentation
            https://www.quantum-espresso.org/Doc/INPUT_PW.html#K_POINTS )"""
        ),
    )
    use_ws_distance: bool = Field(
        True,
        description=dedent(
            """\
            If .true. the position of the Wannier function inside the cell is used to set the
            proper distance and to have a smoother interpolation. Requires seedname_centres.xyz to
            be printed by the previous Wannier90 run. If the file is not found it is automatically
            switched to .FALSE. and only the distance between the cells is used (see also Wannier90
            documentation)"""
        ),
    )
    write_hr: bool = Field(
        True,
        description=dedent(
            """\
            If .true. the KCW hamiltonain in the Wannier basis and in real spase H(R)_m_n is
            printed to file. Usefull for furhter post-processing."""
        ),
    )
    on_site_only: bool = Field(
        False,
        description=dedent(
            """\
            If .true. only the on-site and diagonal elements of the KCW hamiltonain are computed
            (R=0 and n=m)."""
        ),
    )


class KCWEspressoInput(EspressoInput):
    """Pydantic model for the input of `kcw.x`."""

    control: ControlNamelist = Field(default_factory=lambda: ControlNamelist())
    wannier: WannierNamelist = Field(default_factory=lambda: WannierNamelist())
    screen: ScreenNamelist = Field(default_factory=lambda: ScreenNamelist())
    ham: HamNamelist = Field(default_factory=lambda: HamNamelist())
    k_points: KPointsCard = Field(discriminator="kind")
