"""Pydantic model for the ATOMIC_VELOCITIES card in `pw.x` input files."""

# ruff: noqa

from typing import Annotated
from pydantic import Field
from pydantic_espresso.quantity import Quantity
from pydantic_espresso.utils import BaseModel, INDENT


_VelocityComponent = Annotated[
    float,
    Quantity(units="electron_mass^-1/2 Ry^1/2", dimensionality="length time^-1"),
]


class AtomicVelocity(BaseModel):
    """Pydantic model for entries in the ATOMIC_VELOCITIES card.

    The card itself is a list of AtomicVelocity objects."""

    species: str = Field(..., description="label of the atom as specified in ATOMIC_SPECIES")
    velocity: tuple[_VelocityComponent, _VelocityComponent, _VelocityComponent] = Field(
        ..., description="x, y, z components of the velocity of the atom"
    )

    def __str__(self) -> str:
        return f"{INDENT}{self.species} {' '.join([str(x) for x in self.velocity])}"
