"""Pydantic model for the CELL_PARAMETERS card in `pw.x` input files."""

# ruff: noqa

from typing import Literal
from pydantic import Field
from pydantic_espresso.card.card import Card
from pydantic_espresso.utils import INDENT


class CellParametersCard(Card):
    """Pydantic model for the CELL_PARAMETERS card."""

    units: Literal["alat", "bohr", "angstrom"] = Field(
        ...,
        description="Unit for lattice vectors; options are:  'bohr' / 'angstrom': lattice vectors in bohr-radii / angstrom. In this case the lattice parameter alat = sqrt(v1*v1).  'alat' / nothing specified: lattice vectors in units of the lattice parameter (either celldm(1) or A). Not specifying units is DEPRECATED and will not be allowed in the future.  If neither unit nor lattice parameter are specified, 'bohr' is assumed - DEPRECATED, will no longer be allowed",
    )
    vectors: tuple[
        tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]
    ] = Field(..., description="lattice vectors")

    def __str__(self) -> str:
        return (
            f"CELL_PARAMETERS ({self.units})\n"
            + INDENT
            + f"\n{INDENT}".join([" ".join([str(x) for x in v]) for v in self.vectors])
        )
