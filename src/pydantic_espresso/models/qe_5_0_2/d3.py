"""Pydantic model for the input of `d3.x` version `qe-5.0.2`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputphNamelist(Namelist):
    """Pydantic model for the `Inputph` namelist."""

    prefix: str = Field("pwscf", description="prefix for file names")
    outdir: Path = Field(
        default_factory=get_tmp_dir,
        description="Directory containing input, output, and scratch files; must be the same as specified in the calculation of the unperturbed system and for phonon calculation.",
    )
    fildyn: str = Field(
        "d3dyn", description="The file where the derivative of the dynamical matrix will be written"
    )
    ethr_ph: float = Field(
        1.0e-5,
        description="Threshold for iterative diagonalization (accuracy in ryd of the calculated eigenvalues).",
    )
    wraux: bool = Field(
        False,
        description="If .true. the program will write different terms of the matrix on different files.",
    )
    recv: bool = Field(False, description="Specify .true. for a recover run.")
    istop: int = Field(
        0,
        description="If this number is set different from zero the program will stop after the specified routine and will write the partial result in the recover file.",
    )
    iverbosity: int = Field(0, description="type of printing ( 0 few, 1 all )")


class D3EspressoInput(EspressoInput):
    """Pydantic model for the input of `d3.x.`"""

    inputph: InputphNamelist = Field(default_factory=lambda: InputphNamelist())
