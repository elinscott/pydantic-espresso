"""Pydantic model for the input of `hp.x` version `qe-6.4.1`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputhpNamelist(Namelist):
    """Pydantic model for the `Inputhp` namelist."""

    prefix: str = Field(
        "pwscf",
        description="Prepended to input/output filenames; must be the same used in the calculation of unperturbed system.",
    )
    outdir: Path = Field(
        Path("value of the"),
        description="Directory containing input, output, and scratch files; must be the same as specified in the calculation of the unperturbed system.",
    )
    iverbosity: int = Field(
        1,
        description="= 1 : minimal output = 2 : as above + symmetry matrices, final response matrices chi0 and chi1 and their inverse matrices, full U matrix = 3 : as above + various detailed info about the NSCF calculation at k and k+q = 4 : as above + response occupation matrices at every iteration and for every q point in the star",
    )
    max_seconds: float = Field(
        1.0e7, description="Maximum allowed run time before the job stops smoothly."
    )
    skip_equivalence_q: bool = Field(
        False,
        description="If .true. then the HP code will skip the equivalence analysis of q points, and thus the full grid of q points will be used. Otherwise the symmetry is used to determine equivalent q points (star of q), and then perform calculations only for inequivalent q points.",
    )
    determine_num_pert_only: bool = Field(
        False,
        description="If .true. determines the number of perturbations (i.e. which atoms will be perturbed) and exits smoothly without performing any calculation.",
    )
    find_atpert: int = Field(
        1,
        description="Method for searching of atoms which must be perturbed. 1 = Find how many inequivalent Hubbard atoms there are by analyzing unperturbed occupations. 2 = Find how many Hubbard atoms to perturb based on how many different Hubbard atomic types there are. Warning: atoms which have the same type but which are inequivalent by symmetry or which have different occupations will not be distinguished in this case (use option 1 or 3 instead). 3 = Find how many inequivalent Hubbard atoms there are using symmetry. Atoms which have the same type but are not equivalent by symmetry will be distinguished in this case.",
    )
    docc_thr: float = Field(
        5.0e-5,
        description="Threshold for a comparison of unperturbed occupations which is needed for the selection of atoms which must be perturbed. Can be used only when find_atpert = 1.",
    )
    skip_type: bool = Field(
        False,
        description="skip_type(i), where i runs over types of atoms. If skip_type(i)=.true. then no linear-response calculation will be performed for the i-th atomic type: in this case equiv_type(i) must be specified, otherwise the HP code will stop. This option is useful if the system has atoms of the same type but opposite spin pollarizations (anti-ferromagnetic case). This keyword cannot be used when find_atpert = 1.",
    )
    equiv_type: int = Field(
        0,
        description="equiv_type(i), where i runs over types of atoms. equiv_type(i)=j, will make type i equivalent to type j (useful when nspin=2). Such a merging of types is done only at the post-processing stage. This keyword cannot be used when find_atpert = 1.",
    )
    perturb_only_atom: bool = Field(
        False,
        description="If perturb_only_atom(i)=.true. then only the i-th atom will be perturbed and considered in the run. This variable is useful when one wants to split the whole calculation on parts. Note: this variable has a higher priority than skip_type.",
    )
    start_q: int = Field(
        1,
        description="Computes only the q points from start_q to last_q. IMPORTANT: start_q must be smaller or equal to the total number of q points found.",
    )
    last_q: int | None = Field(
        None,
        description="Computes only the q points from start_q to last_q. IMPORTANT: last_q must be smaller or equal to the total number of q points found.",
    )
    sum_pertq: bool = Field(
        False,
        description="If it is set to .true. then the HP code will collect pieces of the response occupation matrices for all q points. This variable should be used only when start_q, last_q and perturb_only_atom are used.",
    )
    compute_hp: bool = Field(
        False,
        description="If it is set to .true. then the HP code will collect pieces of the chi0 and chi matrices (which must have been produced in previous runs) and then compute Hubbard parameters. The HP code will look for files tmp_dir/HP/prefix.chi.i.dat. Note that all files prefix.chi.i.dat (where i runs over all perturbed atoms) must be placed in one folder tmp_dir/HP/. compute_hp=.true. must be used only when the calculation was parallelized over perturbations.",
    )
    conv_thr_chi: float = Field(
        1.0e-5,
        description="Convergence threshold for the response function chi, which is defined as a trace of the response occupation matrix.",
    )
    thresh_init: float = Field(
        1.0e-14,
        description="Initial threshold for the solution of the linear system (first iteration). Needed to converge the bare (non-interacting) response function chi0. The specified value will be multiplied by the number of electrons in the system.",
    )
    ethr_nscf: float = Field(
        1.0e-11,
        description="Threshold for the convergence of eigenvalues during the iterative diagonalization of the Hamiltonian in the non-self-consistent-field (NSCF) calculation at k and k+q points. Note, this quantity is NOT extensive.",
    )
    niter_max: int = Field(
        100,
        description="Maximum number of iterations in the iterative solution of the linear-response Kohn-Sham equations.",
    )
    alpha_mix: list[float] | None = Field(
        None,
        description="Mixing parameter (for the i-th iteration) for updating the response SCF potential using the modified Broyden method: D.D. Johnson, PRB 38, 12807 (1988) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.38.12807).",
    )
    nmix: int = Field(
        4,
        description="Number of iterations used in potential mixing using the modified Broyden method D.D. Johnson, PRB 38, 12807 (1988) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.38.12807).",
    )


class HPEspressoInput(EspressoInput):
    """Pydantic model for the input of `hp.x.`"""

    inputhp: InputhpNamelist = Field(default_factory=lambda: InputhpNamelist())
