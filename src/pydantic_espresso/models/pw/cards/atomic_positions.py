"""Pydantic model for the ATOMIC_POSITIONS card in `pw.x` input files."""

# ruff: noqa

from abc import ABC
from typing import Annotated, Literal, Union
from pydantic import Field
from pydantic_espresso.utils import BaseModel as Card
from pydantic_espresso.quantity import Quantity
from pydantic_espresso.utils import BaseModel, INDENT


# A single atomic position carries a species label, an (x, y, z) tuple, and an
# optional ``if_pos`` flag that selects components frozen during MD/relaxation.
class _AtomicPositionBase(BaseModel, ABC):
    """Abstract base for an atom and its position in the ATOMIC_POSITIONS card."""

    species: str = Field(..., description="label of the atom as specified in ATOMIC_SPECIES")
    if_pos: tuple[Literal[0, 1], Literal[0, 1], Literal[0, 1]] | None = Field(
        None,
        description=(
            "component i of the force for this atom is multiplied by if_pos(i), which must be "
            "either 0 or 1. Used to keep selected atoms and/or selected components fixed in MD "
            "dynamics or structural optimization run."
        ),
    )

    def __str__(self) -> str:
        position = getattr(self, "position", ())
        coord_str = " ".join(str(coord) for coord in position)
        if self.if_pos is None:
            return f"{self.species} {coord_str}"
        if_pos_str = " ".join(str(x) for x in self.if_pos)
        return f"{self.species} {coord_str} {if_pos_str}"


# Length-valued position variants (alat / bohr / angstrom share the same dimensionality)
class AtomicPositionAlat(_AtomicPositionBase):
    """An atomic position whose coordinates are in units of ``alat``."""

    position: tuple[
        Annotated[float, Quantity(units="alat", dimensionality="length")],
        Annotated[float, Quantity(units="alat", dimensionality="length")],
        Annotated[float, Quantity(units="alat", dimensionality="length")],
    ] = Field(..., description="x, y, z coordinates of the atom (in alat)")


class AtomicPositionBohr(_AtomicPositionBase):
    """An atomic position whose coordinates are in bohr."""

    position: tuple[
        Annotated[float, Quantity(units="bohr", dimensionality="length")],
        Annotated[float, Quantity(units="bohr", dimensionality="length")],
        Annotated[float, Quantity(units="bohr", dimensionality="length")],
    ] = Field(..., description="x, y, z coordinates of the atom (in bohr)")


class AtomicPositionAngstrom(_AtomicPositionBase):
    """An atomic position whose coordinates are in angstrom."""

    position: tuple[
        Annotated[float, Quantity(units="angstrom", dimensionality="length")],
        Annotated[float, Quantity(units="angstrom", dimensionality="length")],
        Annotated[float, Quantity(units="angstrom", dimensionality="length")],
    ] = Field(..., description="x, y, z coordinates of the atom (in angstrom)")


class AtomicPositionCrystal(_AtomicPositionBase):
    """An atomic position in crystal (fractional) coordinates."""

    position: tuple[float, float, float] = Field(
        ..., description="x, y, z fractional coordinates of the atom"
    )


class AtomicPositionCrystalSG(_AtomicPositionBase):
    """An atomic position in crystal_sg coordinates (symmetry-inequivalent atoms only)."""

    position: tuple[float, float, float] = Field(
        ..., description="x, y, z fractional coordinates of the symmetry-inequivalent atom"
    )


class _AtomicPositionsCardBase(Card, ABC):
    """Abstract base for the ATOMIC_POSITIONS card."""

    unit: str

    def __str__(self) -> str:
        positions = getattr(self, "positions", [])
        return f"ATOMIC_POSITIONS ({self.unit})\n" + "\n".join([INDENT + str(x) for x in positions])


class AtomicPositionsAlatCard(_AtomicPositionsCardBase):
    """ATOMIC_POSITIONS card with unit == 'alat'."""

    unit: Literal["alat"] = "alat"
    positions: list[AtomicPositionAlat] = Field(default_factory=list)


class AtomicPositionsBohrCard(_AtomicPositionsCardBase):
    """ATOMIC_POSITIONS card with unit == 'bohr'."""

    unit: Literal["bohr"] = "bohr"
    positions: list[AtomicPositionBohr] = Field(default_factory=list)


class AtomicPositionsAngstromCard(_AtomicPositionsCardBase):
    """ATOMIC_POSITIONS card with unit == 'angstrom'."""

    unit: Literal["angstrom"] = "angstrom"
    positions: list[AtomicPositionAngstrom] = Field(default_factory=list)


class AtomicPositionsCrystalCard(_AtomicPositionsCardBase):
    """ATOMIC_POSITIONS card with unit == 'crystal'."""

    unit: Literal["crystal"] = "crystal"
    positions: list[AtomicPositionCrystal] = Field(default_factory=list)


class AtomicPositionsCrystalSGCard(_AtomicPositionsCardBase):
    """ATOMIC_POSITIONS card with unit == 'crystal_sg'."""

    unit: Literal["crystal_sg"] = "crystal_sg"
    positions: list[AtomicPositionCrystalSG] = Field(default_factory=list)


AtomicPositionsCard = Union[
    AtomicPositionsAlatCard,
    AtomicPositionsBohrCard,
    AtomicPositionsAngstromCard,
    AtomicPositionsCrystalCard,
    AtomicPositionsCrystalSGCard,
]
