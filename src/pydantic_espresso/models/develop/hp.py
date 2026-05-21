"""Pydantic model for the input of `hp.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class InputhpNamelist(Namelist):
    """Pydantic model for the `INPUTHP` namelist."""

    prefix: str = Field(
        "pwscf",
        description=(
            "Prepended to input/output filenames; must be the same used in the calculation of "
            "unperturbed system."
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
        description=(
            "Directory containing input, output, and scratch files; must be the same as specified "
            "in the calculation of the unperturbed system."
        ),
    )
    iverbosity: Literal[1, 2, 3, 4] = Field(1, description="")
    max_seconds: Annotated[float, Quantity(units="s", dimensionality="time")] = Field(
        1.0e7, description="Maximum allowed run time before the job stops smoothly."
    )
    skip_equivalence_q: bool = Field(
        False,
        description=(
            "If .true. then the HP code will skip the equivalence analysis of q points, and thus "
            "the full grid of q points will be used. Otherwise the symmetry is used to determine "
            "equivalent q points (star of q), and then perform calculations only for inequivalent "
            "q points."
        ),
    )
    determine_num_pert_only: bool = Field(
        False,
        description=(
            "If .true. determines the number of perturbations (i.e. which atoms will be perturbed) "
            "and exits smoothly without performing any calculation. For DFT+U+V, it also "
            "determines the indices of inter-site couples."
        ),
    )
    determine_q_mesh_only: bool = Field(
        False,
        description=(
            "If .true. determines the number of q points for a given perturbed atom and exits "
            "smoothly. This keyword can be used only if perturb_only_atom is set to .true."
        ),
    )
    find_atpert: Literal[1, 2, 3, 4] = Field(
        1, description="Method for searching of atoms which must be perturbed."
    )
    docc_thr: float = Field(
        5.0e-5,
        description=(
            "Threshold for a comparison of unperturbed occupations which is needed for the "
            "selection of atoms which must be perturbed. Can be used only when find_atpert = 1."
        ),
    )
    start_q: int = Field(
        1,
        description=(
            "Computes only the q points from start_q to last_q.  IMPORTANT: start_q must be "
            "smaller or equal to the total number of q points found."
        ),
    )
    last_q: int | None = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=(
            "Computes only the q points from start_q to last_q. By default it is set internally to "
            "the total number of q points.  IMPORTANT: last_q must be smaller or equal to the "
            "total number of q points found."
        ),
    )
    sum_pertq: bool = Field(
        False,
        description=(
            "If it is set to .true. then the HP code will collect pieces of the response "
            "occupation matrices for all q points. This variable should be used only when start_q, "
            "last_q and perturb_only_atom are used."
        ),
    )
    compute_hp: bool = Field(
        False,
        description=(
            "If it is set to .true. then the HP code will collect pieces of the chi0 and chi "
            "matrices (which must have been produced in previous runs) and then compute Hubbard "
            "parameters. The HP code will look for files tmp_dir/HP/prefix.chi.i.dat. Note that "
            "all files prefix.chi.i.dat (where i runs over all perturbed atoms) must be placed in "
            "one folder tmp_dir/HP/. compute_hp=.true. must be used only when the calculation was "
            "parallelized over perturbations."
        ),
    )
    conv_thr_chi: float = Field(
        1.0e-5,
        description=(
            "Convergence threshold for the response function chi, which is defined as a trace of "
            "the response occupation matrix."
        ),
    )
    thresh_init: float = Field(
        1.0e-14,
        description=(
            "Initial threshold for the solution of the linear system (first iteration). Needed to "
            "converge the bare (non-interacting) response function chi0. The specified value will "
            "be multiplied by the number of electrons in the system."
        ),
    )
    ethr_nscf: float = Field(
        1.0e-11,
        description=(
            "Threshold for the convergence of eigenvalues during the iterative diagonalization of "
            "the Hamiltonian in the non-self-consistent-field (NSCF) calculation at k and k+q "
            "points. Note, this quantity is NOT extensive."
        ),
    )
    niter_max: int = Field(
        100,
        description=(
            "Maximum number of iterations in the iterative solution of the linear-response "
            "Kohn-Sham equations."
        ),
    )
    alpha_mix: list[float] | None = Field(
        None,
        description=(
            "Mixing parameter (for the i-th iteration) for updating the response SCF potential "
            "using the modified Broyden method. See: D.D. Johnson, PRB 38, 12807 (1988) "
            "(https://journals.aps.org/prb/abstract/10.1103/PhysRevB.38.12807)."
        ),
    )
    nmix: int = Field(
        4,
        description=(
            "Number of iterations used in potential mixing using the modified Broyden method. See: "
            "D.D. Johnson, PRB 38, 12807 (1988) "
            "(https://journals.aps.org/prb/abstract/10.1103/PhysRevB.38.12807)."
        ),
    )
    num_neigh: int = Field(
        6,
        description=(
            "Number of nearest neighbors of every Hubbard atom which will be considered when "
            "writting Hubbard V parameters to the file parameters.out, which can be used in the "
            "subsequent DFT+U+V calculation. This keyword is used only for DFT+U+V "
            "(post-processing stage)."
        ),
    )
    lmin: Literal[0, 1, 2, 3] = Field(
        2,
        description=(
            "Minimum value of the orbital quantum number of the Hubbard atoms starting from which "
            "(and up to the maximum l in the system) Hubbard V will be written to the file "
            "parameters.out. lmin refers to the orbital quantum number of the atom corresponding "
            "to the first site-index in Hubbard_V(:,:,:). This keyword is used only for DFT+U+V "
            "and only in the post-processing stage."
        ),
    )
    rmax: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        100.0e0,
        description=(
            "Maximum distance between two atoms to search neighbors (used only at the "
            "postprocessing step for DFT+U+V). This keyword is useful when there are e.g. defects "
            "in the system."
        ),
    )
    dist_thr: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        6.0e-4,
        description=(
            "Threshold for comparing inter-atomic distances when reconstructing the missing "
            "elements of the response susceptibility in the post-processing step."
        ),
    )
    no_metq0: bool = Field(
        False,
        description=(
            "If .true. the metallic response term at q=0 is ignored (i.e. the last term in Eq. "
            "(22) in PRB 103, 045141 (2021) "
            "(https://journals.aps.org/prb/abstract/10.1103/PhysRevB.103.045141)). This is useful "
            "for magnetic insulators to avoid the divergence of the calculation."
        ),
    )
    skip_type: list[bool] = Field(
        default_factory=list,
        description=(
            "skip_type(i), where i runs over types of atoms. If skip_type(i)=.true. then no "
            "linear-response calculation will be performed for the i-th atomic type: in this case "
            "equiv_type(i) must be specified, otherwise the HP code will stop. This option is "
            "useful if the system has atoms of the same type but opposite spin pollarizations "
            "(anti-ferromagnetic case). This keyword cannot be used when find_atpert = 1. (start = "
            "1, end = ntyp)"
        ),
    )
    equiv_type: list[int] = Field(
        default_factory=list,
        description=(
            "equiv_type(i), where i runs over types of atoms. equiv_type(i)=j, will make type i "
            "equivalent to type j (useful when nspin=2). Such a merging of types is done only at "
            "the post-processing stage. This keyword cannot be used when find_atpert = 1. (start = "
            "1, end = ntyp)"
        ),
    )
    perturb_only_atom: list[bool] = Field(
        default_factory=list,
        description=(
            "If perturb_only_atom(i)=.true. then only the i-th atom will be perturbed and "
            "considered in the run. This variable is useful when one wants to split the whole "
            "calculation on parts.  Note: this variable has a higher priority than skip_type. "
            "(start = 1, end = ntyp)"
        ),
    )


class HPEspressoInput(EspressoInput):
    """Pydantic model for the input of `hp.x`."""

    inputhp: InputhpNamelist = Field(default_factory=lambda: InputhpNamelist())
