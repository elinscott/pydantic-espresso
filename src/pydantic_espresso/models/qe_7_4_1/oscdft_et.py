"""Pydantic model for the input of `oscdft_et.x` version `qe-7.4.1`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class Oscdft_et_namelistNamelist(Namelist):
    """Pydantic model for the `Oscdft_et_namelist` namelist."""

    initial_prefix: str | None = Field(None, description="prefix of the initial pw.x calculation.")
    final_prefix: str | None = Field(None, description="prefix of the final pw.x calculation.")
    initial_dir: str | None = Field(None, description="The directory containing the input data of the initial pw.x calculation, i.e. the same as in pw.x.")
    final_dir: str | None = Field(None, description="The directory containing the input data of the final pw.x calculation, i.e. the same as in pw.x.")
    print_matrix: bool = Field(False, description="If .TRUE., prints the occupation matrices.")
    print_eigvect: bool = Field(False, description="If .TRUE., prints the occupation eigenvectors.")
    print_debug: bool = Field(False, description="If .TRUE., prints additional debug informations.")


class OSCDFT_ETEspressoInput(EspressoInput):
    """Pydantic model for the input of `oscdft_et.x.`"""

    oscdft_et_namelist: Oscdft_et_namelistNamelist = Field(default_factory=Oscdft_et_namelistNamelist)
