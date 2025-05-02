"""Pydantic model for the input of `all_currents.x` version `qe-7.1rc`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class Energy_currentNamelist(Namelist):
    """Pydantic model for the `Energy_current` namelist."""

    delta_t: float = Field(
        1.0e0,
        description="Small timestep used to do the numerical derivative needed in order to compute some parts of the current. Note that is in the pw.x units.",
    )
    file_output: str = Field(
        "current_hz",
        description="The program will write the output in file_output and file_output  + '.dat'. In the latter file the format of the output is:  NSTEP t_ps J_x J_y J_z Jele_x Jele_y Jele_z v_cm(1)_x v_cm(1)_y v_cm(1)_z ...  where J_x, J_y, J_z are the three components of the DFT energy current, and can be easily post-processed by other external programs. Jele_* are the components of the electronic density current that may be used for decorrelation and better data analysis or for calculating the electric current. v_cm(1) ... v_cm(nsp) are the center of mass velocities for each atomic species.  If n_repeat_every_step > 1, an additional file file_output + '.stat' is written with the following format:  NSTEP t_ps mean(J_x) mean(J_y) mean(J_z) std(J_x) std(J_y) std(J_z)  only one line per step is printed in this case (in the other output files you will find every calculation, also repeated ones). std is the standard deviation.",
    )
    trajdir: str | None = Field(
        None,
        description="Prefix of the cp.x trajectory. The program will try to open the files trajdir .pos and trajdir .vel The files, for n atoms, are formatted like this:  NSTEP1 t_ps1 x(1) y(1) z(2) .    .    . .    .    . .    .    . x(n) y(n) z(n) NSTEP2 t_ps2 x(1) y(1) z(2) .    .    . .    .    . .    .    . x(n) y(n) z(n) ...  the order of the atomic types must be the same of the one provided in the input file. If the files are not found, only the positions and the velocities from the input file will be used. Note that the units are specified by the input file. The units of the velocities are the same of the positions with time in atomic units. If a cp.x trajectory is provided (see vel_input_units ) a factor 2 can be used for the velocities.",
    )
    vel_input_units: Literal["CP", "PW"] = Field(
        "PW",
        description="This multiplies or not by a factor 2 the velocities given in the input. Available options are:",
    )
    eta: float = Field(1.0e0, description="Convergence parameter for Ewald-like sums")
    n_max: int = Field(
        5, description="Number of images in each direction used to converge some sums."
    )
    first_step: int = Field(
        0,
        description="The program will start with step  istep >= first_step. If greater than zero the input file's positions and velocities will be ignored. Note that this is not a sequential index but refers to the indexes reported in the input trajectory file. The index of 0 is assigned to the snapshot described in the input namelist file.",
    )
    last_step: int = Field(
        0,
        description="The program will end with step  istep <= last_step. If 0, it will stop at the end of the trajectory file Note that this is not a sequential index but refers to the indexes reported in the input trajectory file.",
    )
    step_mul: int = Field(
        1, description="The program will use the step only if MOD(step, step_mul) == step_rem."
    )
    step_rem: int = Field(
        0, description="The program will use the step only if MOD(step, step_mul) == step_rem."
    )
    ethr_small_step: float = Field(
        1.0e-7,
        description="Diagonalization threshold after the small delta_t numerical derivative step. (the system changed a very little)",
    )
    ethr_big_step: float = Field(
        1.0e-3,
        description="Diagonalization threshold at the beginning of each step but the first, for wich the pw.x input value is used.",
    )
    restart: bool = Field(
        False,
        description="If true try to read file_output .dat and try to set first_step to the last step in the file + 1",
    )
    subtract_cm_vel: bool = Field(
        False,
        description="If true subtract from the velocities of all atoms for every step the center of mass velocity for each atomic type. It help to decorrelate a little the mass flux from the energy flux",
    )
    add_i_current_b: bool = Field(
        False,
        description="If true adds to the energy current a part that is correctly implemented only for cubic cells. This part is in the form of a sum over the atomic types of a constant time the center of mass velocity of the atomic type. It does not change the value of the thermal conductivity when the formula for the multicomponent case with the inverse of the Schur complement is used, and in the single component or solid case this is a non-diffusive contribution.",
    )
    save_dvpsi: bool = Field(
        False,
        description="If true allocate the space needed for saving the solution of the linear system betweew every calculation. The iterative algorithm will always start from there. By default it starts always from scratch.",
    )
    re_init_wfc_1: bool = Field(
        False,
        description="If true initializes, as specified in the ELECTRON namelist of the PW section, the wavefunctions before the first ground state calculation, then compute the charge density. Otherwise use the last calculated wavefunctions.",
    )
    re_init_wfc_2: bool = Field(
        False,
        description="If true initializes, as specified in the ELECTRON namelist of the PW section, the wavefunctions before the second ground state calculation, then compute the charge density. Otherwise use the last calculated wavefunctions. Note that if three_point_derivative is false, this has no effect.",
    )
    re_init_wfc_3: bool = Field(
        False,
        description="If true initializes, as specified in the ELECTRON namelist of the PW section, the wavefunctions before the third ground state calculation, then compute the charge density. Otherwise use the last calculated wavefunctions.",
    )
    three_point_derivative: bool = Field(
        True,
        description="If true calculates three ground stated: one at t - delta_t /2, one at t and one at t + delta_t/2. Obviously it needs more computer time, but the derivative should be better.",
    )
    n_repeat_every_step: int = Field(
        1,
        description="Number of repetition of the full current calculation for each step. If > 1, the file file_output + '.stat' is written with some statistics. Note that if you don't specify at least re_init_wfc_1 ,this may be useless. You may want to specify startingwfc = 'random' in the ELECTRONS namelist.",
    )
    n_workers: int = Field(
        0,
        description="The calculation over all the trajectory is splitted in n_workers chunks. Then to run the code over all the trajectory you must run n_workers input files each one with a different worker_id, from 0 to n_workers - 1 . Those inputs can run at the same time in the same folder. The worker_id will be appended to the outdir folder and to the file_output input variables, so you can safely run all the inputs in the same directory at the same time.",
    )
    worker_id: int = Field(0, description="See n_workers variable")
    continue_not_converged: bool = Field(
        False,
        description="If it is not possible to find a ground state for a given frame of the trajectory, go to the next one. You will not find this step in the output file(s).",
    )


class ALL_CURRENTSEspressoInput(EspressoInput):
    """Pydantic model for the input of `all_currents.x.`"""

    energy_current: Energy_currentNamelist = Field(default_factory=lambda: Energy_currentNamelist())
