"""Pydantic model for the K_POINT card in `pw.x` input files."""

# ruff: noqa

from abc import ABC
from typing import Literal, Union
import itertools
from pydantic import Field, field_validator
from pydantic_espresso.card.card import Card
from pydantic_espresso.utils import BaseModel, INDENT, PositiveInt


class KPointsCardABC(Card, ABC):
    """Abstract base class for the K_POINTS card."""

    kind: "str"

    def __str__(self) -> str:
        return f"K_POINTS ({self.kind})"


class KPointsListCard(KPointsCardABC):
    """Pydantic model for the K_POINTS card with an explicit list of k-points."""

    class KPoint(BaseModel):
        """Pydantic model for a single k-point"""

        coordinate: tuple[float, float, float] = Field(..., description="")
        weight: float = Field(1, description="")

        def __str__(self) -> str:
            return f"{' '.join([str(x) for x in self.coordinate])} {self.weight}"

    k_points: list[KPoint] = Field(default_factory=list)
    kind: Literal["tpiba", "crystal", "tpiba_b", "crystal_b", "tpiba_c", "crystal_c"] = "tpiba"

    @field_validator("kind", mode="after")
    @classmethod
    def check_kind(cls, value: str) -> str:
        """Return an error if kind is allowed by Quantum ESPRESSO but yet not implemented."""
        if value in ["tpiba_c", "crystal_c"]:
            raise NotImplementedError(
                f"{value} is a valid choice for `kind` but it is not yet implemented."
            )
        return value

    def __str__(self) -> str:
        return (
            super().__str__()
            + "\n"
            + f"{INDENT}{len(self.k_points)}"
            + "\n"
            + "\n".join([f"{INDENT}{x}" for x in self.k_points])
        )


class KPointsGammaCard(KPointsCardABC):
    """Pydantic model for the K_POINTS card with kind == gamma."""

    kind: Literal["gamma"] = Field("gamma", description="")

    def to_kpoints_list(self) -> KPointsListCard:
        """Convert to KPointsListCard."""
        return KPointsListCard(
            k_points=[KPointsListCard.KPoint(coordinate=(0.0, 0.0, 0.0), weight=1.0)]
        )


class KPointsGridCard(KPointsCardABC):
    """Pydantic model for the K_POINTS card with kind == automatic."""

    grid: tuple[PositiveInt, PositiveInt, PositiveInt] = Field(..., description="")
    offset: tuple[Literal[0, 1], Literal[0, 1], Literal[0, 1]] = Field((0, 0, 0), description="")
    kind: Literal["automatic"] = Field("automatic", description="")

    def to_kpoints_list(self) -> KPointsListCard:
        """Convert to KPointsListCard."""
        k_points = []
        for i, j, k in itertools.product(*[range(x) for x in self.grid]):
            # Calculate the coordinate
            coordinate = (
                (i + self.offset[0] / 2) / self.grid[0],
                (j + self.offset[1] / 2) / self.grid[1],
                (k + self.offset[2] / 2) / self.grid[2],
            )

            # Wrap coordinates to the range (0.5, 0.5]
            wrapped_coordinate = tuple(x - 1 if x > 0.5 else x for x in coordinate)

            # Construct the k-point and add it to the list
            k_point = KPointsListCard.KPoint(coordinate=wrapped_coordinate, weight=1.0)
            k_points.append(k_point)

        return KPointsListCard(k_points=k_points, kind="crystal")

    def __str__(self) -> str:
        return (
            super().__str__()
            + "\n"
            + INDENT
            + f"{' '.join([str(x) for x in self.grid])} {' '.join([str(x) for x in self.offset])}"
        )


KPointsCard = Union[KPointsListCard, KPointsGammaCard, KPointsGridCard]
