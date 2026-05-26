"""Pydantic model for the input of `bgw2pw.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from textwrap import dedent
from typing import Literal

from pydantic import Field

from pydantic_espresso.base import EspressoInput
from pydantic_espresso.namelist import Namelist


class InputBgw2pwNamelist(Namelist):
    """Pydantic model for the `INPUT_BGW2PW` namelist."""

    prefix: str = Field(..., description="prefix of files saved by program pw.x")
    outdir: Path | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "ESPRESSO_TMPDIR environment variable is set and non-blank",
                    "value": "value of the ESPRESSO_TMPDIR environment variable",
                },
                {"when": None, "value": "'./'"},
            ],
        },
        description="the scratch directory where the massive data-files are written",
    )
    real_or_complex: Literal[1, 2] = Field(
        2,
        description=dedent(
            """\
            BerkeleyGW data flavor.
            - '1': Real flavor of BerkeleyGW (for systems with inversion symmetry and time-reversal
              symmetry).
            - '2': Complex flavor of BerkeleyGW (for systems without inversion symmetry and
              time-reversal symmetry)."""
        ),
    )
    wfng_flag: bool = Field(
        False, description="read wavefunctions in G-space from BerkeleyGW WFN file"
    )
    wfng_file: str = Field(
        "WFN", description="name of BerkeleyGW WFN input file. Not used if wfng_flag = .FALSE."
    )
    wfng_nband: int = Field(
        0, description="number of bands to write (0 = all). Not used if wfng_flag = .FALSE."
    )
    rhog_flag: bool = Field(
        False, description="read charge density in G-space from BerkeleyGW RHO file"
    )
    rhog_file: str = Field(
        "RHO", description="name of BerkeleyGW RHO input file. Not used if rhog_flag = .FALSE."
    )


class BGW2PWInput(EspressoInput):
    """Pydantic model for the input of `bgw2pw.x`."""

    input_bgw2pw: InputBgw2pwNamelist | None = Field(None)
