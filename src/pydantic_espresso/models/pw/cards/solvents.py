"""Pydantic model for the card in `pw.x` input files."""

# ruff: noqa

from pathlib import Path
from abc import ABC, abstractmethod
from typing import Literal
from pydantic import Field
from pydantic_espresso.utils import BaseModel as Card
from pydantic_espresso.utils import BaseModel, INDENT


class Solvent(BaseModel):
    """Model for one solvent in the SOLVENTS card when laue_both_hands == False."""

    label: str = Field(..., description="label of the solvent molecule.")
    density: float = Field(
        ...,
        description="density of the solvent molecule. if not positive value is set, density is read from MOL-file.",
    )
    molecule: Path = Field(
        ...,
        description="MOL-file of the solvent molecule. in the MOL-file, molecular structure and some other data are written.",
    )

    def __str__(self) -> str:
        return f"{self.label} {self.density} {self.molecule}"


class SolventLR(BaseModel):
    """Model for one solvent in the SOLVENTS card when laue_both_hands == True."""

    label: str = Field(..., description="label of the solvent molecule.")
    density_left: float = Field(
        ...,
        description="density of the solvent molecule in the left-hand side. if not positive value is set, density is read from MOL-file.",
    )
    density_right: float = Field(
        ...,
        description="density of the solvent molecule in the right-hand side. if not positive value is set, density is read from MOL-file.",
    )
    molecule: Path = Field(
        ...,
        description="MOL-file of the solvent molecule. in the MOL-file, molecular structure and some other data are written.",
    )

    def __str__(self) -> str:
        return f"{self.label} {self.density_left} {self.density_right} {self.molecule}"


class SolventCardABC(Card, ABC):
    """Abstract base class for the SOLVENTS card."""

    units: Literal["1/cell", "mol/L", "g/cm^3"] = Field(..., description="")
    solvents: list[Solvent] | list[SolventLR]

    def __str__(self) -> str:
        return f"SOLVENTS ({self.units})\n" + "\n".join([f"{INDENT}{x}" for x in self.solvents])


class SolventsCard(SolventCardABC):
    """Pydantic model for the SOLVENTS card when laue_both_hands == False."""

    solvents: list[Solvent] = Field(default_factory=list)


class SolventsLRCard(SolventCardABC):
    """Pydantic model for the SOLVENTS card when laue_both_hands == True."""

    solvents: list[SolventLR] = Field(default_factory=list)
