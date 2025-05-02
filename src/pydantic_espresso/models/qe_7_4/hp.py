"""Pydantic model for the input of `hp.x` version `qe-7.4`.

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


    prefix: str = Field("pwscf", description="Prepended to input/output filenames; must be the same used in the calculation of unperturbed system.")
    outdir: Path = Field(Path("value of the"), description="Directory containing input, output, and scratch files; must be the same as specified in the calculation of the unperturbed system.")
    iverbosity: int = Field(1, description="= 1 : minimal output = 2 : as above + symmetry matrices, final response matrices chi0 and chi1 and their inverse matrices, full U matrix = 3 : as above + various detailed info about the NSCF calculation at k and k+q = 4 : as above + response occupation matrices at every iteration and for every q point in the star")
    max_seconds: float = Field(1.e7, description="Maximum allowed run time before the job stops smoothly.")
    skip_equivalence_q: bool = Field(False, description="If .true. then the HP code will skip the equivalence analysis of q points, and thus the full grid of q points will be used. Otherwise the symmetry is used to determine equivalent q points (star of q), and then perform calculations only for inequivalent q points.")
    determine_num_pert_only: bool = Field(False, description="If .true. determines the number of perturbations (i.e. which atoms will be perturbed) and exits smoothly without performing any calculation. For DFT+U+V, it also determines the indices of inter-site couples.")
    determine_q_mesh_only: bool = Field(False, description="If .true. determines the number of q points for a given perturbed atom and exits smoothly. This keyword can be used only if perturb_only_atom is set to .true.")
    find_atpert: int = Field(1, description="Method for searching of atoms which must be perturbed. 1 = Find how many inequivalent Hubbard atoms there are by analyzing unperturbed occupations. 2 = Find how many Hubbard atoms to perturb based on how many different Hubbard atomic types there are. Warning: atoms which have the same type but which are inequivalent by symmetry or which have different occupations will not be distinguished in this case (use option 1 or 3 instead). 3 = Find how many inequivalent Hubbard atoms there are using symmetry. Atoms which have the same type but are not equivalent by symmetry will be distinguished in this case. 4 = Perturb all Hubbard atoms (the most expensive option)")
    docc_thr: float = Field(5.e-5, description="Threshold for a comparison of unperturbed occupations which is needed for the selection of atoms which must be perturbed. Can be used only when find_atpert = 1.")
    start_q: int = Field(1, description="Computes only the q points from start_q to last_q.  IMPORTANT: start_q must be smaller or equal to the total number of q points found.")
    last_q: int | None = Field(None, description="Computes only the q points from start_q to last_q.  IMPORTANT: last_q must be smaller or equal to the total number of q points found.")
    sum_pertq: bool = Field(False, description="If it is set to .true. then the HP code will collect pieces of the response occupation matrices for all q points. This variable should be used only when start_q, last_q and perturb_only_atom are used.")
    compute_hp: bool = Field(False, description="If it is set to .true. then the HP code will collect pieces of the chi0 and chi matrices (which must have been produced in previous runs) and then compute Hubbard parameters. The HP code will look for files tmp_dir/HP/prefix.chi.i.dat. Note that all files prefix.chi.i.dat (where i runs over all perturbed atoms) must be placed in one folder tmp_dir/HP/. compute_hp=.true. must be used only when the calculation was parallelized over perturbations.")
    conv_thr_chi: float = Field(1.e-5, description="Convergence threshold for the response function chi, which is defined as a trace of the response occupation matrix.")
    thresh_init: float = Field(1.e-14, description="Initial threshold for the solution of the linear system (first iteration). Needed to converge the bare (non-interacting) response function chi0. The specified value will be multiplied by the number of electrons in the system.")
    ethr_nscf: float = Field(1.e-11, description="Threshold for the convergence of eigenvalues during the iterative diagonalization of the Hamiltonian in the non-self-consistent-field (NSCF) calculation at k and k+q points. Note, this quantity is NOT extensive.")
    niter_max: int = Field(100, description="Maximum number of iterations in the iterative solution of the linear-response Kohn-Sham equations.")
    alpha_mix: list[float] | None = Field(None, description="Mixing parameter (for the i-th iteration) for updating the response SCF potential using the modified Broyden method. See: D.D. Johnson, PRB 38, 12807 (1988) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.38.12807).")
    nmix: int = Field(4, description="Number of iterations used in potential mixing using the modified Broyden method. See: D.D. Johnson, PRB 38, 12807 (1988) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.38.12807).")
    num_neigh: int = Field(6, description="Number of nearest neighbors of every Hubbard atom which will be considered when writting Hubbard V parameters to the file parameters.out, which can be used in the subsequent DFT+U+V calculation. This keyword is used only for DFT+U+V (post-processing stage).")
    lmin: int = Field(2, description="Minimum value of the orbital quantum number of the Hubbard atoms starting from which (and up to the maximum l in the system) Hubbard V will be written to the file parameters.out. lmin refers to the orbital quantum number of the atom corresponding to the first site-index in Hubbard_V(:,:,:). This keyword is used only for DFT+U+V and only in the post-processing stage. Example: lmin=1 corresponds to writing to file V between e.g. oxygen (with p states) and its neighbors, and including V between transition metals (with d states) and their neighbors. Instead, when lmin=2 only the latter will be written to parameters.out.")
    rmax: float = Field(100.e0, description="Maximum distance (in Bohr) between two atoms to search neighbors (used only at the postprocessing step for DFT+U+V). This keyword is useful when there are e.g. defects in the system.")
    dist_thr: float = Field(6.e-4, description="Threshold (in Bohr) for comparing inter-atomic distances when reconstructing the missing elements of the response susceptibility in the post-processing step.")


class HPEspressoInput(EspressoInput):
    """Pydantic model for the input of `hp.x.`"""

    inputhp: InputhpNamelist = Field(default_factory=lambda: InputhpNamelist())
