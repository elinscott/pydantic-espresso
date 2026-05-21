"""Test `pydantic_espresso.models.pw.cards.cell_parameters`."""

import pytest
from pydantic import ValidationError

from pydantic_espresso.models.pw.cards.cell_parameters import (
    CellParametersAlatCard,
    CellParametersAngstromCard,
    CellParametersBohrCard,
)
from pydantic_espresso.models.pw.develop import PWInput


def test_cell_parameters_card() -> None:
    """Test the CellParametersAlatCard variant."""
    card = CellParametersAlatCard(vectors=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

    assert card.unit == "alat"
    assert card.vectors[0][0] == 1.0
    assert card.vectors[0][1] == 0.0
    assert card.vectors[0][2] == 0.0
    assert card.vectors[1][0] == 0.0
    assert card.vectors[1][1] == 1.0
    assert card.vectors[1][2] == 0.0
    assert card.vectors[2][0] == 0.0
    assert card.vectors[2][1] == 0.0
    assert card.vectors[2][2] == 1.0
    assert str(card) == "CELL_PARAMETERS (alat)\n  1.0 0.0 0.0\n  0.0 1.0 0.0\n  0.0 0.0 1.0"


def test_cell_parameters_bohr_card() -> None:
    """Test the CellParametersBohrCard variant."""
    card = CellParametersBohrCard(vectors=[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]])
    assert card.unit == "bohr"
    assert card.vectors[0] == (2.0, 0.0, 0.0)
    assert "CELL_PARAMETERS (bohr)" in str(card)


def test_cell_parameters_angstrom_card() -> None:
    """Test the CellParametersAngstromCard variant."""
    card = CellParametersAngstromCard(vectors=[[3.5, 0.0, 0.0], [0.0, 3.5, 0.0], [0.0, 0.0, 3.5]])
    assert card.unit == "angstrom"
    assert card.vectors[2] == (0.0, 0.0, 3.5)
    assert "CELL_PARAMETERS (angstrom)" in str(card)


def test_pwinput_routes_bohr_cell_parameters() -> None:
    """The PWInput discriminator selects the bohr cell-parameters card."""
    inp = PWInput(
        system={
            "ibrav": 1,
            "nat": 1,
            "ntyp": 1,
            "ecutwfc": 30.0,
        },
        cell_parameters={
            "unit": "bohr",
            "vectors": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        },
        atomic_positions={
            "unit": "bohr",
            "positions": [{"species": "H", "position": [0.0, 0.0, 0.0]}],
        },
        k_points={"kind": "gamma"},
    )
    assert isinstance(inp.cell_parameters, CellParametersBohrCard)


def test_pwinput_routes_angstrom_cell_parameters() -> None:
    """The PWInput discriminator selects the angstrom cell-parameters card."""
    inp = PWInput(
        system={
            "ibrav": 1,
            "nat": 1,
            "ntyp": 1,
            "ecutwfc": 30.0,
        },
        cell_parameters={
            "unit": "angstrom",
            "vectors": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        },
        atomic_positions={
            "unit": "angstrom",
            "positions": [{"species": "H", "position": [0.0, 0.0, 0.0]}],
        },
        k_points={"kind": "gamma"},
    )
    assert isinstance(inp.cell_parameters, CellParametersAngstromCard)


def test_cell_parameters_invalid_unit_raises() -> None:
    """An invalid ``unit`` literal raises ``ValidationError``."""
    with pytest.raises(ValidationError):
        CellParametersAlatCard.model_validate(
            {
                "unit": "bogus",
                "vectors": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            }
        )
