"""Pydantic model for the input of `oscdft_pp.x` version `e6621af`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInputTemplate


class OSCDFT_PPEspressoInput(EspressoInputTemplate):
    """Pydantic model for the input of `oscdft_pp.x.`"""

    prefix: str = Field(..., description="prefix of the pw.x calculation.")
    outdir: str = Field(..., description="directory containing the input data, i.e. the same as in pw.x")
