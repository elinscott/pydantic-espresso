"""Pydantic model for the ATOMIC_POSITIONS card in `pw.x` input files."""

# ruff: noqa

from typing import Literal
from pydantic import Field
from pydantic_espresso.card.card import Card
from pydantic_espresso.utils import BaseModel, INDENT


class AtomicPositionsCard(Card):
    """Pydantic model for the ATOMIC_POSITIONS card."""

    class AtomicPosition(BaseModel):
        """Pydantic model for an atom and its position."""

        species: str = Field(..., description="label of the atom as specified in ATOMIC_SPECIES")
        position: tuple[float, float, float] = Field(
            ..., description="x, y, z coordinates of the atom"
        )

        def __str__(self) -> str:
            return f"{self.species} {' '.join([str(coord) for coord in self.position])}"

    units: Literal["alat", "bohr", "angstrom", "crystal", "crystal_sg"] = Field(
        ..., description="Units for ATOMIC_POSITIONS"
    )
    positions: list[AtomicPosition] = Field(default_factory=list)

    def __str__(self) -> str:
        return f"ATOMIC_POSITIONS ({self.units})\n" + f"\n".join(
            [INDENT + str(x) for x in self.positions]
        )
