"""Pydantic model for the input of `oscdft_et.x` version `latest`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import BaseModel


class Oscdft_et_namelistNamelist(BaseModel):
   """Pydantic model for the `Oscdft_et_namelist` namelist."""

    initial_prefix: str | None = Field(None, description="prefix of the initial pw.x calculation.")
    final_prefix: str | None = Field(None, description="prefix of the final pw.x calculation.")
    initial_dir: str | None = Field(None, description="The directory containing the input data of the initial pw.x calculation, i.e. the same as in pw.x.")
    final_dir: str | None = Field(None, description="The directory containing the input data of the final pw.x calculation, i.e. the same as in pw.x.")
    print_matrix: bool = Field(False, description="If .TRUE., prints the occupation matrices.")
    print_eigvect: bool = Field(False, description="If .TRUE., prints the occupation eigenvectors.")
    print_debug: bool = Field(False, description="If .TRUE., prints additional debug informations.")


class OSCDFT_ETEspressoInput(BaseModel):
    """Pydantic model for the input of `oscdft_et.x.`"""

    Oscdft_et_namelist: Oscdft_et_namelistNamelist
