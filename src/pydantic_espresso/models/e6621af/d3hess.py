"""Pydantic model for the input of `d3hess.x` version `e6621af`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputNamelist(Namelist):
    """Pydantic model for the `Input` namelist."""

    prefix: str = Field(
        "pwscf", description="prefix of input file produced by pw.x (wavefunctions are not needed)"
    )
    outdir: Path = Field(
        Path("value of the"),
        description="directory containing the input data, i.e. the same as in pw.x",
    )
    filhess: str = Field(
        "prefix.hess",
        description="output file where the D3 hessian matrix is written (should match dftd3_hess keyword in phonon calculation)",
    )
    step: float = Field(1.0e-3, description="step for numerical differentiation in a.u.")


class D3HESSEspressoInput(EspressoInput):
    """Pydantic model for the input of `d3hess.x.`"""

    input: InputNamelist = Field(default_factory=lambda: InputNamelist())
