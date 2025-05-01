"""Pydantic model for the input of `q2r.x` version `e6621af`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInputTemplate


class Q2REspressoInput(EspressoInputTemplate):
    """Pydantic model for the input of `q2r.x.`"""

    fildyn: str = Field(..., description="Input file name (must be specified).")
    flfrc: str = Field(..., description="Output file containing the IFC in real space (must be specified)")
    zasr: Literal["'no'", "'simple'", "'crystal'", "'one-dim'", "'zero-dim'"] = Field(" 'no'
         ", description="Indicates the type of Acoustic Sum Rules used for the Born effective charges.  Allowed values:")
    loto_2d: bool = Field(..., description="set to")
    write_lr: bool = Field( , description="set to")
