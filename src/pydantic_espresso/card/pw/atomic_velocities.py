"""Pydantic model for the ATOMIC_VELOCITIES card in `pw.x` input files."""

# ruff: noqa

from pydantic import Field
from pydantic_espresso.utils import BaseModel, INDENT


class AtomicVelocity(BaseModel):
    """Pydantic model for entries in the ATOMIC_VELOCITIES card.

    The card itself is a list of AtomicVelocity objects."""

    species: str = Field(..., description="label of the atom as specified in ATOMIC_SPECIES")
    velocity: tuple[float, float, float] = Field(
        ..., description="x, y, z components of the velocity of the atom"
    )

    def __str__(self) -> str:
        return f"{INDENT}{self.species} {' '.join([str(x) for x in self.velocity])}"
