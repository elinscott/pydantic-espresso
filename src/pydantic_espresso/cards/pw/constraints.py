"""Pydantic model for the CONSTRAINTS card in `pw.x` input files."""

# ruff: noqa

from abc import ABC, abstractmethod
from typing import ClassVar
from pydantic_espresso.utils import BaseModel, INDENT, PositiveFloat, PositiveInt

class Constraint(BaseModel, ABC):
    kind: ClassVar[str]  # no default -- must be set in subclasses

    @property
    @abstractmethod
    def indices(self) -> tuple[PositiveInt | PositiveFloat]:
        ...

    def __str__(self) -> str:
        return self.kind + ' ' + ' '.join([str(x) for x in self.indices])

class TypeCoordConstraint(Constraint):
    atom_type_indices: tuple[PositiveInt, PositiveInt]
    cutoff_radius: PositiveFloat
    smoothing: PositiveFloat
    kind: ClassVar[str] = "type_coord"

    @property
    def indices(self):
        return (*self.atom_type_indices, self.cutoff_radius, self.smoothing)

class AtomCoordConstraint(Constraint):
    atom_indices: tuple[PositiveInt, PositiveInt]
    cutoff_radius: PositiveFloat
    smoothing: PositiveFloat
    kind: ClassVar[str] = "atom_coord"                                                                           

    @property
    def indices(self):
        return (*self.atom_indices, self.cutoff_radius, self.smoothing)

class DistanceConstraint(Constraint):
    atom_indices: tuple[PositiveInt, PositiveInt]
    kind: ClassVar[str] = "distance"

    @property
    def indices(self):
        return self.atom_indices

class PlanarAngleConstraint(Constraint):
    atom_indices: tuple[PositiveInt, PositiveInt, PositiveInt]
    kind: ClassVar[str] = "planar_angle"

    @property
    def indices(self):
        return self.atom_indices

class TorsionalAngleConstraint(Constraint):
    atom_indices: tuple[PositiveInt, PositiveInt, PositiveInt, PositiveInt]
    kind: ClassVar[str] = "torsional_angle"

    @property
    def indices(self):
        return self.atom_indices
