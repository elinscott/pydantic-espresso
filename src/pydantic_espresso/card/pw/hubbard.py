"""Pydantic model for the HUBBARD card in `pw.x` input files."""

# ruff: noqa

from abc import ABC, abstractmethod
from typing import Annotated, ClassVar, Literal
from pydantic import Field
from pydantic_espresso.card.card import Card
from pydantic_espresso.quantity import Quantity
from pydantic_espresso.utils import BaseModel, INDENT, PositiveInt


class HubbardSite(BaseModel):
    """Pydantic model for a single Hubbard site."""

    label: str = Field(..., description="label of the atom as specified in ATOMIC_SPECIES")
    manifold: str = Field(..., description="subshell of the manifold (e.g. 3d, 2p, 4f, etc.)")

    def __str__(self) -> str:
        return f"{self.label}-{self.manifold}"


class HubbardParameter(BaseModel, ABC):
    """Pydantic model for a single Hubbard parameter."""

    name: ClassVar[str]  # no default -- must be set in subclasses
    value: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(
        ..., description="value of the Hubbard parameter (in eV)"
    )

    @property
    @abstractmethod
    def _subspace_str(self) -> str: ...

    def __str__(self) -> str:
        return f"{self.name} {self._subspace_str} {self.value}"


class HubbardU(HubbardParameter):
    """Pydantic model for the Hubbard U parameter."""

    name: ClassVar[str] = "U"
    site: HubbardSite

    @property
    def _subspace_str(self) -> str:
        return str(self.site)


class HubbardJ0(HubbardU):
    """Pydantic model for the Hubbard J0 parameter."""

    name: ClassVar[str] = "J0"


class HubbardJ(HubbardU):
    """Pydantic model for the Hubbard J parameter."""

    name: ClassVar[str] = "J"


class HubbardB(HubbardU):
    """Pydantic model for the Hubbard B parameter."""

    name: ClassVar[str] = "B"


class HubbardV(HubbardParameter):
    """Pydantic model for the Hubbard V parameter."""

    name: ClassVar[str] = "V"
    sites: tuple[HubbardSite, HubbardSite]
    atom_indices: tuple[PositiveInt, PositiveInt] = Field(
        ..., description="indices of the two atoms coupled by the Hubbard V parameter"
    )

    @property
    def _subspace_str(self) -> str:
        return f"{self.sites[0]} {self.sites[1]} {self.atom_indices[0]} {self.atom_indices[1]}"


class HubbardCard(Card):
    """Pydantic model for the HUBBARD card."""

    kind: Literal["atomic", "ortho-atomic", "norm-atomic", "wf", "pseudo"] = Field(
        ...,
        description="HUBBARD options are:  NB: forces and stress are currently implemented only for the 'atomic', 'ortho-atomic', and 'pseudo' Hubbard projectors.  Check Doc/Hubbard_input.pdf to see how to specify Hubbard parameters U, J0, J, B, E2, E3, V in the HUBBARD card.",
    )
    parameters: list[HubbardParameter] = Field(default_factory=list)

    def __str__(self) -> str:
        return f"HUBBARD ({self.kind})\n" + "\n".join([INDENT + str(x) for x in self.parameters])
