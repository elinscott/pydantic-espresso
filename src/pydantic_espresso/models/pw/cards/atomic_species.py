"""Pydantic model for the ATOMIC_SPECIES card in `pw.x` input files."""

# ruff: noqa

from typing import Annotated
from pydantic import Field
from pydantic_espresso.quantity import Quantity
from pydantic_espresso.utils import BaseModel, PositiveFloat


class AtomicSpecies(BaseModel):
    """Pydantic model for entries in the ATOMIC_SPECIES card.

    The card itself is implemented as a list of AtomicSpecies objects."""

    species: str = Field(
        ...,
        description="label of the atom. Acceptable syntax: chemical symbol X (1 or 2 characters, case-insensitive) or chemical symbol plus a number or a letter, as in 'Xn' (e.g. Fe1) or 'X_*' or 'X-*' (e.g. C1, C_h; max total length cannot exceed 3 characters)",
    )
    mass: Annotated[PositiveFloat, Quantity(units="amu", dimensionality="mass")] = Field(
        ...,
        description="mass of the atomic species [amu: mass of C = 12] Used only when performing Molecular Dynamics run or structural optimization runs using Damped MD. Not actually used in all other cases (but stored in data files, so phonon calculations will use these values unless other values are provided)",
    )
    pseudopotential: str = Field(
        ...,
        description="File containing PP for this species.  The pseudopotential file is assumed to be in the new UPF format. If it doesn't work, the pseudopotential format is determined by the file name:  *.vdb or *.van     Vanderbilt US pseudopotential code *.RRKJ3            Andrea Dal Corso's code (old format) none of the above  old PWscf norm-conserving format",
    )

    def __str__(self) -> str:
        return f"{self.species} {self.mass} {self.pseudopotential}"
