"""Pydantic model for the input of `pw.x with os-cdft` version `latest`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import BaseModel


class OscdftNamelist(BaseModel):
   """Pydantic model for the `Oscdft` namelist."""

    oscdft_type: int = Field(1, description="1 : C. Ku, P. H. L. Sit, J. Chem. Theory Comput. 15, 4781 (2019). 2 : L. Ponet, E. Di Lucente, N. Marzari, npj Comput. Mater. 10, 151 (2024).  Note: For oscdft_type=2, only the keyword 'occupation' and the keywords constraint_* can be used (see below).")
    n_oscdft: int | None = Field(None, description="Number of entries of the TARGET_OCCUPATION_NUMBERS card.")
    get_ground_state_first: bool = Field(False, description="If .TRUE., perform an scf calculation to convergence before applying constraint.")
    warm_up_niter: int = Field(0, description="Runs warm_up_niter scf iterations first before applying constraint. If get_ground_state_first is .TRUE. then scf convergence is achieved first before running warm_up_niter scf iterations without applying the constraints.")
    convergence_type: Literal["multipliers", "gradient", "energy", "always_false", "always_true"] = Field("gradient", description="The variable that is checked for convergence with the convergence threshold.")
    iteration_type: Literal[0, 1] = Field(None, description="Order of charge density and OS-CDFT multipliers optimizations.")
    optimization_method: Literal["gradient descent", "gradient descent2"] = Field("gradient descent", description="Method to update the OS-CDFT multipliers.")
    array_convergence_func: Literal["maxval", "norm", "rms"] = Field("maxval", description="Specify the method of multiple values to scalar for convergence test when convergence_type is either 'gradient' or 'multipliers'.")
    max_conv_thr: float | None = Field(None, description="If iteration_type is 0, this is the starting convergence threshold. If iteration_type is 1, this is the convergence threshold. See iteration_type for more explanations.")
    min_conv_thr: float | None = Field(None, description="If iteration_type is 0, this is the minimum convergence threshold. If iteration_type is 1, this is ignored. See iteration_type for more explanations.")
    final_conv_thr: float | None = Field(None, description="If iteration_type is 0 and final_conv_thr > 0.D0, the charge density convergence is prevented when the OS-CDFT convergence test is larger than final_conv_thr. Otherwise, this is ignored.")
    conv_thr_multiplier: float | None = Field(None, description="If iteration_type is 0, see iteration_type for explanations. Otherwise, this is ignored.")
    print_occupation_matrix: bool = Field(False, description="If .TRUE., prints the occupation matrices.")
    print_occupation_eigenvectors: bool = Field(False, description="If .TRUE., prints the occupation eigenvectors.")
    min_gamma_n: float | None = Field(None, description="Learning rate of optimizations. See optimization_method.")
    has_min_multiplier: bool = Field(False, description="If .TRUE., sets the minimum value of the OS-CDFT multipliers to min_multiplier.")
    min_multiplier: float | None = Field(None, description="Minimum value of the OS-CDFT multipliers. Enabled using has_min_multiplier")
    has_max_multiplier: bool = Field(False, description="If .TRUE., sets the maximum value of the OS-CDFT multipliers to max_multiplier.")
    max_multiplier: float | None = Field(None, description="Maximum value of the OS-CDFT multipliers. Enabled using has_max_multiplier")
    miniter: int = Field(0, description="Minimum OS-CDFT iterations.")
    maxiter: int = Field(0, description="Maximum OS-CDFT iterations.")
    swapping_technique: Literal["none", "permute"] = Field("none", description="See https://doi.org/10.1021/acs.jctc.9b00281")
    debug_print: bool = Field(False, description="If .TRUE., prints additional debug informations.")
    orthogonalize_swfc: bool = Field(False, description="If .TRUE., uses Lowdin orthogonalized atomic orbitals.")
    normalize_swfc: bool = Field(False, description="If .TRUE., uses Lowdin normalized atomic orbitals. Atomic orbitals are not orthogonalized in this case.")
    constraint_strength: float | None = Field(None, description="Multiplicative factor in front of the constraint term in the potential (and energy).")
    constraint_conv_thr: float | None = Field(None, description="Convergence threshold for the mean absolute error (MAE) computed by averaging the absolute difference between the current and target occupation matrices. When this threshold is reached, the constarined is released.")
    constraint_maxstep: int = Field(200, description="When the number of SCF iterations is larger than this number, the constraint is not updated.")
    constraint_mixing_beta: float | None = Field(None, description="The multiplicative factor in front of the constraint term.")
    constraint_diag: bool = Field(False, description="If .TRUE., TARGET_OCCUPATION_NUMBERS must contain the eigenvalues of the occupation matrix instead of the full (generally) nondiagonal target occupation matrix. The code will read these eigenvalues and reconstruct the nondiagonal target occupation matrix that will be used for constrained calculations. This should behave similarly to the starting_ns_eigenvalue keyword, but better since the constraint is applied until the constraint_conv_thr is reached (contrary to a simple reinitialization of starting occupations that is done using starting_ns_eigenvalue).")


class PW WITH OS-CDFTEspressoInput(BaseModel):
    """Pydantic model for the input of `pw.x with OS-CDFT.`"""

    Oscdft: OscdftNamelist
