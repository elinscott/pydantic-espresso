"""Pydantic model for the CONSTRAINTS card in `pw.x` input files."""

# ruff: noqa

from abc import ABC, abstractmethod
from typing import ClassVar
from pydantic_espresso.utils import BaseModel, INDENT, PositiveFloat, PositiveInt


class Constraint(BaseModel, ABC):
    """Abstract base class for constraints in the CONSTRAINTS card."""

    kind: ClassVar[str]  # no default -- must be set in subclasses

    @property
    @abstractmethod
    def parameters(self) -> list[PositiveInt | PositiveFloat]:
        """Return a flattened list of the constraint parameters."""
        ...

    def __str__(self) -> str:
        return self.kind + " " + " ".join([str(x) for x in self.parameters])


class TypeCoordConstraint(Constraint):
    """Pydantic model for a coordinate constraint by atom type in the CONSTRAINTS card."""

    atom_type_indices: tuple[PositiveInt, PositiveInt]
    cutoff_radius: PositiveFloat
    smoothing: PositiveFloat
    kind: ClassVar[str] = "type_coord"

    @property
    def parameters(self) -> list[PositiveInt | PositiveFloat]:
        """Return a flattened list of the constraint parameters."""
        return [*self.atom_type_indices, self.cutoff_radius, self.smoothing]


class AtomCoordConstraint(Constraint):
    """Pydantic model for an atom coordinate constraint in the CONSTRAINTS card."""

    atom_indices: tuple[PositiveInt, PositiveInt]
    cutoff_radius: PositiveFloat
    smoothing: PositiveFloat
    kind: ClassVar[str] = "atom_coord"

    @property
    def parameters(self) -> list[PositiveInt | PositiveFloat]:
        """Return a flattened list of the constraint parameters."""
        return [*self.atom_indices, self.cutoff_radius, self.smoothing]


class DistanceConstraint(Constraint):
    """Pydantic model for a distance constraint in the CONSTRAINTS card."""

    atom_indices: tuple[PositiveInt, PositiveInt]
    kind: ClassVar[str] = "distance"

    @property
    def parameters(self) -> list[PositiveInt | PositiveFloat]:
        """Return a flattened list of the constraint parameters."""
        return [*self.atom_indices]


class PlanarAngleConstraint(Constraint):
    """Pydantic model for a planar angle constraint in the CONSTRAINTS card."""

    atom_indices: tuple[PositiveInt, PositiveInt, PositiveInt]
    kind: ClassVar[str] = "planar_angle"

    @property
    def parameters(self) -> list[PositiveInt | PositiveFloat]:
        """Return a flattened list of the constraint parameters."""
        return [*self.atom_indices]


class TorsionalAngleConstraint(Constraint):
    """Pydantic model for a torsional angle constraint in the CONSTRAINTS card."""

    atom_indices: tuple[PositiveInt, PositiveInt, PositiveInt, PositiveInt]
    kind: ClassVar[str] = "torsional_angle"

    @property
    def parameters(self) -> list[PositiveInt | PositiveFloat]:
        """Return a flattened list of the constraint parameters."""
        return [*self.atom_indices]
