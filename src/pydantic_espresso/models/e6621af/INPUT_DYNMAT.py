"""Pydantic model for the input of `dynmat.x` version `e6621af`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInputTemplate


class DYNMATEspressoInput(EspressoInputTemplate):
    """Pydantic model for the input of `dynmat.x.`"""

    fildyn: str = Field(" 'matdyn'
         ", description="input file containing the dynamical matrix")
    asr: Literal["'no'", "'simple'", "'crystal'", "'one-dim'", "'zero-dim'"] = Field(" 'no'
         ", description="Indicates the type of Acoustic Sum Rule imposed.  Allowed values:")
    remove_interaction_blocks: bool = Field(False, description="If .true. lines and rows corresponding to atoms that are not displaced are set to 0. This can be used for ph.x calculations with nat_todo set in ph.x, to remove the interaction between the diplaced and fixed parts of the system.")
    axis: int = Field( 3
         , description="indicates the rotation axis for a 1D system (1=Ox, 2=Oy, 3=Oz)")
    lperm: bool = Field(False, description="if .true. then calculate Gamma-point mode contributions to dielectric permittivity tensor")
    lplasma: bool = Field(False, description="if .true. then calculate Gamma-point mode effective plasma frequencies, automatically triggers")
    filout: str = Field(" 'dynmat.out'
         ", description="output file containing phonon frequencies and normalized phonon displacements (i.e. eigenvectors divided by the square root of the mass and then normalized; they are not orthogonal)")
    fileig: str = Field(" ' '
         ", description="output file containing phonon frequencies and eigenvectors of the dynamical matrix (they are orthogonal)")
    filmol: str = Field(" 'dynmat.mold'
         ", description="as above, in a format suitable for molden")
    filxsf: str = Field(" 'dynmat.axsf'
         ", description="as above, in axsf format suitable for xcrysden")
    loto_2d: bool = Field( '.false.'
         , description="set to .true. to activate two-dimensional treatment of LO-TO splitting.")
    el_ph_nsig: int = Field(..., description="The number of double-delta smearing values used in an electron-phonon coupling calculation.")
    el_ph_sigma: float = Field(..., description="The spacing of double-delta smearing values used in an electron-phonon coupling calculation.")
