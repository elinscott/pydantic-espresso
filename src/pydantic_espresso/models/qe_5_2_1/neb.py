"""Pydantic model for the input of `neb.x` version `qe-5.2.1`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class PathNamelist(Namelist):
    """Pydantic model for the `Path` namelist."""


    string_method: str = Field("neb", description="a string describing the task to be performed: 'neb', 'smd")
    restart_mode: str = Field("from_scratch", description="from_scratch'  : from scratch  'restart'       : from previous interrupted run")
    nstep_path: int = Field(1, description="number of ionic + electronic steps")
    num_of_images: int = Field(0, description="Number of points used to discretize the path (it must be larger than 3).")
    opt_scheme: str = Field("quick-min", description="Specify the type of optimization scheme:  'sd'         : steepest descent  'broyden'    : quasi-Newton Broyden's second method (suggested)  'broyden2'   : another variant of the quasi-Newton Broyden's second method to be tested and compared with the previous one.  'quick-min'  : an optimisation algorithm based on the projected velocity Verlet scheme  'langevin'   : finite temperature langevin dynamics of the string (smd only). It is used to compute the average path and the free-energy profile.")
    CI_scheme: str = Field("no-CI", description="Specify the type of Climbing Image scheme:  'no-CI'      : climbing image is not used  'auto'       : original CI scheme. The image highest in energy does not feel the effect of springs and is allowed to climb along the path  'manual'     : images that have to climb are manually selected. See also CLIMBING_IMAGES card")
    first_last_opt: bool = Field(False, description="Also the first and the last configurations are optimized 'on the fly' (these images do not feel the effect of the springs).")
    minimum_image: bool = Field(False, description="Assume a 'minimum image criterion' to build the path. If an atom moves by more than half the length of a crystal axis between one image and the next in the input (before interpolation), an appropriate periodic replica of that atom is chosen. Useful to avoid jumps in the initial reaction path.")
    temp_req: float | None = Field(None, description="Temperature used for the langevin dynamics of the string.")
    ds: float = Field(1.e0, description="Optimisation step length ( Hartree atomic units ). If opt_scheme='broyden', ds is used as a guess for the diagonal part of the Jacobian matrix.")
    path_thr: float | None = Field(None, description="The simulation stops when the error ( the norm of the force orthogonal to the path in eV/A ) is less than path_thr.")
    use_masses: bool = Field(False, description="If. TRUE. the optimisation of the path is performed using mass-weighted coordinates. Useful together with quick-min optimization scheme, if some bonds are much stiffer than others. By assigning a larger (fictitious) mass to atoms with stiff bonds, one may use a longer time step 'ds")
    use_freezing: bool = Field(False, description="If. TRUE. the images are optimised according to their error: only those images with an error larger than half of the largest are optimised. The other images are kept frozen.")
    lfcpopt: bool = Field(False, description="If .TRUE. perform a constant bias potential (constant-mu) calculation with ESM method (assume_isolated = 'esm' and esm_bc = 'bc2' or 'bc3' must be set in SYSTEM namelist). 'fcp_mu' gives the target Fermi energy. See the header of PW/src/fcp.f90 for documentation")
    fcp_mu: float = Field(0.e0, description="If lfcpopt = .TRUE., gives the target Fermi energy [Ry]. One can specify the total charge of the system for the first and last image by giving 'fcp_tot_charge_first' and 'fcp_tot_charge_last' so that the Fermi energy of these systems will be the target value, otherwise 'first_last_opt' should be .TRUE.")
    fcp_tot_charge_first: float = Field(0.e0, description="Total charge of the system ('tot_charge') for the first image. Initial 'tot_charge' for intermediate images will be given by linear interpolation of 'fcp_tot_charge_first' and 'fcp_tot_charge_last")
    fcp_tot_charge_last: float = Field(0.e0, description="Total charge of the system ('tot_charge') for the last image. Initial 'tot_charge' for intermediate images will be given by linear interpolation of 'fcp_tot_charge_first' and 'fcp_tot_charge_last")


class NEBEspressoInput(EspressoInput):
    """Pydantic model for the input of `neb.x.`"""

    path: PathNamelist = Field(default_factory=lambda: PathNamelist())
