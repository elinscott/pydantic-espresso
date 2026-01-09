"""Pydantic model for the input of `d3.x` version `qe-4.1`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputphNamelist(Namelist):
    """Pydantic model for the `INPUTPH` namelist."""

    prefix: str = Field("pwscf", description="prefix for file names")
    outdir: Path = Field(Path("./"), description="scratch directory")
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
    q0mode_todo: list[int] = Field(
        default_factory=list,
        description="This array contains the list of the q=0 modes that will be computed. If q0mode_todo(1).eq.0 the program will compute every q=0 mode. (start = 1, end = 3*nat)",
    )


class D3EspressoInput(EspressoInput):
    """Pydantic model for the input of `d3.x`"""

    inputph: InputphNamelist = Field(default_factory=lambda: InputphNamelist())
