"""Pydantic model for the input of `oscdft_pp.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path

from pydantic import Field

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist


class OscdftPpNamelistNamelist(Namelist):
    """Pydantic model for the `OSCDFT_PP_NAMELIST` namelist."""

    prefix: str = Field(..., description="prefix of the pw.x calculation.")
    outdir: Path = Field(
        ..., description="directory containing the input data, i.e. the same as in pw.x"
    )


class OSCDFTPPEspressoInput(EspressoInput):
    """Pydantic model for the input of `oscdft_pp.x`."""

    oscdft_pp_namelist: OscdftPpNamelistNamelist | None = Field(None)
