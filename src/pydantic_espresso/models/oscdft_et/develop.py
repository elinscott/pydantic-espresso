"""Pydantic model for the input of `oscdft_et.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from textwrap import dedent

from pydantic import Field

from pydantic_espresso.base import EspressoInput
from pydantic_espresso.namelist import Namelist


class OscdftEtNamelistNamelist(Namelist):
    """Pydantic model for the `OSCDFT_ET_NAMELIST` namelist."""

    initial_prefix: str = Field(..., description="prefix of the initial pw.x calculation.")
    final_prefix: str = Field(..., description="prefix of the final pw.x calculation.")
    initial_dir: str = Field(
        ...,
        description=dedent(
            """\
            The directory containing the input data of the initial pw.x calculation, i.e. the same
            as in pw.x."""
        ),
    )
    final_dir: str = Field(
        ...,
        description=dedent(
            """\
            The directory containing the input data of the final pw.x calculation, i.e. the same as
            in pw.x."""
        ),
    )
    print_matrix: bool = Field(False, description="If .TRUE., prints the occupation matrices.")
    print_eigvect: bool = Field(False, description="If .TRUE., prints the occupation eigenvectors.")
    print_debug: bool = Field(False, description="If .TRUE., prints additional debug informations.")


class OSCDFTETInput(EspressoInput):
    """Pydantic model for the input of `oscdft_et.x`."""

    oscdft_et_namelist: OscdftEtNamelistNamelist = Field(...)
