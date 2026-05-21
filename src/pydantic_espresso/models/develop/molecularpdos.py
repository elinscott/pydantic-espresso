"""Pydantic model for the input of `molecularpdos.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from typing import Annotated

from pydantic import Field

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class InputmopdosNamelist(Namelist):
    """Pydantic model for the `INPUTMOPDOS` namelist."""

    xmlfile_full: str | None = Field(None, description="")
    xmlfile_part: str | None = Field(None, description="")
    i_atmwfc_beg_full: int = Field(
        1, description="first atomic wavefunction of the full system considered for the projection"
    )
    i_atmwfc_end_full: int | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "i_atmwfc_end_full < 1",
                    "value": "natomwfc_full (all atomic wavefunctions)",
                },
                {"when": None, "value": "0"},
            ],
        },
        description="last atomic wavefunction of the full system considered for the projection",
    )
    i_atmwfc_beg_part: int = Field(
        1,
        description="first atomic wavefunction of the molecular part considered for the projection",
    )
    i_atmwfc_end_part: int | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "i_atmwfc_end_part < 1",
                    "value": "natomwfc_part (all atomic wavefunctions)",
                },
                {"when": None, "value": "0"},
            ],
        },
        description="last atomic wavefunction of the molecular part considered for the projection",
    )
    i_bnd_beg_full: int = Field(
        1,
        description=(
            "first eigenstate of the full system to be taken into account for the projection"
        ),
    )
    i_bnd_end_full: int | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "i_bnd_end_full < 1", "value": "nbnd_full (all eigenstates)"},
                {"when": None, "value": "0"},
            ],
        },
        description=(
            "last eigenstate of the full system to be taken into account for the projection"
        ),
    )
    i_bnd_beg_part: int = Field(
        1,
        description=(
            "first eigenstate of the molecular part to be taken into account for the projection"
        ),
    )
    i_bnd_end_part: int | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "i_bnd_end_part < 1", "value": "nbnd_part (all eigenstates)"},
                {"when": None, "value": "0"},
            ],
        },
        description=(
            "last eigenstate of the molecular part to be taken into account for the projection"
        ),
    )
    fileout: str = Field(
        "molecularpdos", description="prefix for output files containing molecular PDOS(E)"
    )
    ngauss: int = Field(
        0,
        description=(
            "Type of gaussian broadening: 0 ... Simple Gaussian 1 ... Methfessel-Paxton of order 1 "
            "-1 ... 'cold smearing' (Marzari-Vanderbilt-DeVita-Payne) -99 ... Fermi-Dirac function"
        ),
    )
    degauss: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.0, description="gaussian broadening (not eV!)"
    )
    Emin: float | None = Field(None, description="")
    Emax: float | None = Field(None, description="")
    DeltaE: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(
        0.01, description="energy grid step"
    )
    kresolveddos: bool = Field(
        False,
        description=(
            "if .true. the k-resolved DOS is computed: not summed over all k-points but written as "
            "a function of the k-point index. In this case all k-point weights are set to unity"
        ),
    )


class MOLECULARPDOSEspressoInput(EspressoInput):
    """Pydantic model for the input of `molecularpdos.x`."""

    inputmopdos: InputmopdosNamelist = Field(default_factory=lambda: InputmopdosNamelist())
