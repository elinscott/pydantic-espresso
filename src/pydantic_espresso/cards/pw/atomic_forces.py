"""Pydantic model for the ATOMIC_FORCES card in `pw.x` input files."""

# ruff: noqa

from pydantic import Field
from pydantic_espresso.cards.card import Card
from pydantic_espresso.utils import INDENT


class AtomicForce(Card):
    species: str = Field(..., description="label of the atom as specified in ATOMIC_SPECIES")
    force: tuple[float, float, float] = Field(..., description="x, y, z components of the force on the atom")

    def __str__(self):
        return f"{INDENT}{self.species} {' '.join([str(x) for x in self.force])}"

        return f"{self.species} {self.mass} {self.pseudopotential}"
