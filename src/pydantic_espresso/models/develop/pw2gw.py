"""Pydantic model for the input of `pw2gw.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from typing import Annotated

from pydantic import Field

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class InputppNamelist(Namelist):
    """Pydantic model for the `INPUTPP` namelist."""

    prefix: str = Field(
        "pwscf",
        description=(
            "the first part of the name of all the file written by the code should be equal to the "
            "value given in the main calculations."
        ),
    )
    outdir: Path | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "ESPRESSO_TMPDIR environment variable is set and non-blank",
                    "value": "value of the ESPRESSO_TMPDIR environment variable",
                },
                {"when": None, "value": '"./"'},
            ],
        },
        description="the scratch directory where the massive data-files are written",
    )
    what: str = Field(
        "gw",
        description=(
            "gw' : Calculate dipole optical matrix elements (use for norm-conserving "
            "pseudopotentials) and imaginary part of the dielectric function.  'gmaps': write "
            "g-maps for each processor in a file 'fort.'100 + processor number"
        ),
    )
    qplda: bool = Field(
        False,
        description=(
            "if .TRUE. write the interface file 'QPLDA' to GW and BSE codes (chisig, dpforexc)."
        ),
    )
    vxcdiag: bool = Field(
        False,
        description=(
            "if .TRUE. calculates the expectation value of the exchange and correlation potential "
            "on all the Kohn-Sham states and write it into the 'vxcdiag.dat' file."
        ),
    )
    vkb: bool = Field(
        False,
        description=(
            "if .TRUE. use Kleyman-Bylander projectors to write additional informatio into fort.15 "
            "file (Still in development)"
        ),
    )
    Emin: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(
        0.0, description="Starting photon energy for which the dielectric function is calculated"
    )
    Emax: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(
        30.0, description="Highest photon energy for which the dielectric function is calculated"
    )
    DeltaE: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(
        0.05, description="Energy step with which the dielectric function is calculated"
    )


class PW2GWEspressoInput(EspressoInput):
    """Pydantic model for the input of `pw2gw.x`."""

    inputpp: InputppNamelist = Field(default_factory=lambda: InputppNamelist())
