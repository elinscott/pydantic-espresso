"""Pydantic model for the input of `oscdft_pp.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class Oscdft_pp_namelistNamelist(Namelist):
    """Pydantic model for the `Oscdft_pp_namelist` namelist."""


    prefix: str | None = Field(None, description="prefix of the pw.x calculation.")
    outdir: Path | None = Field(None, description="directory containing the input data, i.e. the same as in pw.x")


class OSCDFT_PPEspressoInput(EspressoInput):
    """Pydantic model for the input of `oscdft_pp.x.`"""

    oscdft_pp_namelist: Oscdft_pp_namelistNamelist = Field(default_factory=lambda: Oscdft_pp_namelistNamelist())
