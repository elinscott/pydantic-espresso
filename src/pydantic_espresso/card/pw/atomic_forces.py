"""Pydantic model for the ATOMIC_FORCES card in `pw.x` input files."""

# ruff: noqa

from pydantic import Field
from pydantic_espresso.card.card import Card
from pydantic_espresso.utils import INDENT


class AtomicForce(Card):
    """Pydantic model for entries in the ATOMIC_FORCES card.

    The card itself is a list of AtomicForce objects."""

    species: str = Field(..., description="label of the atom as specified in ATOMIC_SPECIES")
    force: tuple[float, float, float] = Field(
        ..., description="x, y, z components of the force on the atom"
    )

    def __str__(self) -> str:
        return f"{INDENT}{self.species} {' '.join([str(x) for x in self.force])}"

        return f"{self.species} {self.mass} {self.pseudopotential}"
