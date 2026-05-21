"""Pydantic model for the CELL_PARAMETERS card in `pw.x` input files."""

# ruff: noqa

from abc import ABC
from typing import Annotated, Literal, Union
from pydantic import Field
from pydantic_espresso.card.card import Card
from pydantic_espresso.quantity import Quantity
from pydantic_espresso.utils import INDENT


_CELL_PARAMETERS_DOC = (
    "Unit for lattice vectors; options are:  'bohr' / 'angstrom': lattice vectors in "
    "bohr-radii / angstrom. In this case the lattice parameter alat = sqrt(v1*v1).  "
    "'alat' / nothing specified: lattice vectors in units of the lattice parameter (either "
    "celldm(1) or A). Not specifying units is DEPRECATED and will not be allowed in the future."
)


_AlatLength = Annotated[float, Quantity(units="alat", dimensionality="length")]
_AlatVec3 = tuple[_AlatLength, _AlatLength, _AlatLength]
_BohrLength = Annotated[float, Quantity(units="bohr", dimensionality="length")]
_BohrVec3 = tuple[_BohrLength, _BohrLength, _BohrLength]
_AngstromLength = Annotated[float, Quantity(units="angstrom", dimensionality="length")]
_AngstromVec3 = tuple[_AngstromLength, _AngstromLength, _AngstromLength]


class _CellParametersCardBase(Card, ABC):
    """Abstract base for the CELL_PARAMETERS card."""

    unit: str

    def __str__(self) -> str:
        vectors = getattr(self, "vectors", ())
        return (
            f"CELL_PARAMETERS ({self.unit})\n"
            + INDENT
            + f"\n{INDENT}".join([" ".join([str(x) for x in v]) for v in vectors])
        )


class CellParametersAlatCard(_CellParametersCardBase):
    """CELL_PARAMETERS card with unit == 'alat'."""

    unit: Literal["alat"] = Field("alat", description=_CELL_PARAMETERS_DOC)
    vectors: tuple[_AlatVec3, _AlatVec3, _AlatVec3] = Field(
        ..., description="lattice vectors (in units of alat)"
    )


class CellParametersBohrCard(_CellParametersCardBase):
    """CELL_PARAMETERS card with unit == 'bohr'."""

    unit: Literal["bohr"] = Field("bohr", description=_CELL_PARAMETERS_DOC)
    vectors: tuple[_BohrVec3, _BohrVec3, _BohrVec3] = Field(
        ..., description="lattice vectors (in bohr)"
    )


class CellParametersAngstromCard(_CellParametersCardBase):
    """CELL_PARAMETERS card with unit == 'angstrom'."""

    unit: Literal["angstrom"] = Field("angstrom", description=_CELL_PARAMETERS_DOC)
    vectors: tuple[_AngstromVec3, _AngstromVec3, _AngstromVec3] = Field(
        ..., description="lattice vectors (in angstrom)"
    )


CellParametersCard = Union[
    CellParametersAlatCard, CellParametersBohrCard, CellParametersAngstromCard
]
