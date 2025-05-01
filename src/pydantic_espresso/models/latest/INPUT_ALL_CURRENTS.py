"""Pydantic model for the input of `all_currents.x` version `latest`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInputTemplate


class ALL_CURRENTSEspressoInput(EspressoInputTemplate):
    """Pydantic model for the input of `all_currents.x.`"""

    delta_t: float = Field( 1.D0
         , description="Small timestep used to do the numerical derivative needed in order to compute some parts of the current. Note that is in the pw.x units.")
    file_output: str = Field(" 'current_hz'
         ", description="The program will write the output in")
    trajdir: str = Field(" ''
         ", description="Prefix of the cp.x trajectory. The program will try to open the files")
    vel_input_units: Literal["'CP'", "'PW'"] = Field(" 'PW'
         ", description="This multiplies or not by a factor 2 the velocities given in the input.                       Available options are:")
    eta: float = Field( 1.D0
         , description="Convergence parameter for Ewald-like sums")
    n_max: int = Field( 5
         , description="Number of images in each direction used to converge some sums.")
    first_step: int = Field( 0
         , description="The program will start with step  istep >=")
    last_step: int = Field( 0
         , description="The program will end with step  istep <=")
    step_mul: int = Field( 1
         , description="The program will use the step only if MOD(step,")
    step_rem: int = Field( 0
         , description="The program will use the step only if MOD(step,")
    ethr_small_step: float = Field( 1.D-7
         , description="Diagonalization threshold after the small")
    ethr_big_step: float = Field( 1.D-3
         , description="Diagonalization threshold at the beginning of each step but the first, for wich the pw.x input value is used.")
    restart: bool = Field(False, description="If true try to read")
    subtract_cm_vel: bool = Field(False, description="If true subtract from the velocities of all atoms for every step the center of mass velocity for each atomic type. It help to decorrelate a little the mass flux from the energy flux")
    add_i_current_b: bool = Field(False, description="If true adds to the energy current a part that is correctly implemented only for cubic cells. This part is in the form of a sum over the atomic types of a constant time the center of mass velocity of the atomic type. It does not change the value of the thermal conductivity when the formula for the multicomponent case with the inverse of the Schur complement is used, and in the single component or solid case this is a non-diffusive contribution.")
    save_dvpsi: bool = Field(False, description="If true allocate the space needed for saving the solution of the linear system betweew every calculation. The iterative algorithm will always start from there. By default it starts always from scratch.")
    re_init_wfc_1: bool = Field(False, description="If true initializes, as specified in the ELECTRON namelist of the PW section, the wavefunctions before the first ground state calculation, then compute the charge density.  Otherwise use the last calculated wavefunctions.")
    re_init_wfc_2: bool = Field(False, description="If true initializes, as specified in the ELECTRON namelist of the PW section, the wavefunctions before the second ground state calculation, then compute the charge density. Otherwise use the last calculated wavefunctions. Note that if")
    re_init_wfc_3: bool = Field(False, description="If true initializes, as specified in the ELECTRON namelist of the PW section, the wavefunctions before the third ground state calculation, then compute the charge density. Otherwise use the last calculated wavefunctions.")
    three_point_derivative: bool = Field(True, description="If true calculates three ground stated: one at t -")
    n_repeat_every_step: int = Field( 1
         , description="Number of repetition of the full current calculation for each step. If > 1, the file")
    n_workers: int = Field( 0
         , description="The calculation over all the trajectory is splitted in")
    worker_id: int = Field( 0
         , description="See")
    continue_not_converged: bool = Field(False, description="If it is not possible to find a ground state for a given frame of the trajectory, go to the next one. You will not find this step in the output file(s).")
