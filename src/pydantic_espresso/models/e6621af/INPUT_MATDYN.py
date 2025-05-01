"""Pydantic model for the input of `matdyn.x` version `e6621af`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInputTemplate


class MATDYNEspressoInput(EspressoInputTemplate):
    """Pydantic model for the input of `matdyn.x.`"""

    flfrc: str = Field(..., description="File produced by")
    asr: Literal["'no'", "'simple'", "'crystal'", "'all'", "'one-dim'", "'zero-dim'"] = Field(" 'no'
         ", description="Indicates the type of Acoustic Sum Rule imposed.  Allowed values:")
    huang: bool = Field( , description="if")
    dos: bool = Field(..., description="if")
    deltaE: float = Field(..., description="energy step, in cm")
    ndos: int = Field(..., description="number of energy steps for DOS calculations (default: calculated from deltaE if not specified)")
    degauss: float = Field(..., description="DOS broadening in cm")
    fldos: str = Field(..., description="output file for dos (default:")
    flfrq: str = Field(..., description="output file for frequencies (default:")
    flvec: str = Field(..., description="output file for normalized phonon displacements (default:")
    fleig: str = Field(..., description="output file for phonon eigenvectors (default:")
    fldyn: str = Field(..., description="output file for dynamical matrix (default: ' ' i.e. not written)")
    ntyp: int = Field(..., description="number of atom types in the supercell (default:")
    readtau: bool = Field(..., description="read  atomic positions of the supercell from input (used to specify different masses) (default:")
    fltau: str = Field(..., description="write atomic positions of the supercell to file")
    la2F: bool = Field(..., description="if")
    q_in_band_form: bool = Field(..., description="if")
    q_in_cryst_coord: bool = Field(..., description="if")
    eigen_similarity: bool = Field(..., description="use similarity of the displacements to order frequencies  (default:")
    fd: bool = Field(..., description="if")
    na_ifc: bool = Field(..., description="add non analitic contributions to the interatomic force constants if finite displacement method is used (as in Wang et al.")
    nosym: bool = Field(..., description="if")
    loto_2d: bool = Field(..., description="set to")
    loto_disable: bool = Field(..., description="if")
    read_lr: bool = Field( , description="if")
    write_frc: bool = Field( , description="if")
