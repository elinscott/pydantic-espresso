"""Pydantic model for the input of `oscdft_pp.x` version `latest`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import BaseModel


class Oscdft_pp_namelistNamelist(BaseModel):
   """Pydantic model for the `Oscdft_pp_namelist` namelist."""

    prefix: str | None = Field(None, description="prefix of the pw.x calculation.")
    outdir: str | None = Field(None, description="directory containing the input data, i.e. the same as in pw.x")


class OSCDFT_PPEspressoInput(BaseModel):
    """Pydantic model for the input of `oscdft_pp.x.`"""

    Oscdft_pp_namelist: Oscdft_pp_namelistNamelist
