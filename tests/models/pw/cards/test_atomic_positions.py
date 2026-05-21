"""Test `pydantic_espresso.models.pw.cards.atomic_positions`."""

import pytest
from pydantic import ValidationError

from pydantic_espresso.models.pw.cards.atomic_positions import (
    AtomicPositionAlat,
    AtomicPositionAngstrom,
    AtomicPositionBohr,
    AtomicPositionCrystal,
    AtomicPositionCrystalSG,
    AtomicPositionsAlatCard,
    AtomicPositionsAngstromCard,
    AtomicPositionsBohrCard,
    AtomicPositionsCrystalCard,
    AtomicPositionsCrystalSGCard,
)
from pydantic_espresso.models.pw.develop import PWInput


def test_atomic_positions_card() -> None:
    """Test the AtomicPositionsAlatCard variant."""
    card = AtomicPositionsAlatCard(
        positions=[
            {"species": "H", "position": [0.0, 0.0, 0.0]},
            {"species": "H", "position": [1.0, 1.0, 1.0]},
        ],
    )
    assert card.unit == "alat"
    assert card.positions[0].species == "H"
    assert card.positions[0].position == (0.0, 0.0, 0.0)
    assert card.positions[1].species == "H"
    assert card.positions[1].position == (1.0, 1.0, 1.0)
    assert str(card) == "ATOMIC_POSITIONS (alat)\n  H 0.0 0.0 0.0\n  H 1.0 1.0 1.0"


def test_atomic_positions_bohr_card() -> None:
    """Test the AtomicPositionsBohrCard variant."""
    card = AtomicPositionsBohrCard(
        positions=[
            {"species": "H", "position": [0.0, 0.0, 0.0]},
            {"species": "O", "position": [2.0, 2.0, 2.0]},
        ],
    )
    assert card.unit == "bohr"
    assert isinstance(card.positions[0], AtomicPositionBohr)
    assert card.positions[0].position == (0.0, 0.0, 0.0)
    assert card.positions[1].species == "O"
    assert "ATOMIC_POSITIONS (bohr)" in str(card)


def test_atomic_positions_angstrom_card() -> None:
    """Test the AtomicPositionsAngstromCard variant."""
    card = AtomicPositionsAngstromCard(
        positions=[{"species": "Si", "position": [0.5, 0.5, 0.5]}],
    )
    assert card.unit == "angstrom"
    assert isinstance(card.positions[0], AtomicPositionAngstrom)
    assert card.positions[0].species == "Si"
    assert "ATOMIC_POSITIONS (angstrom)" in str(card)


def test_atomic_positions_crystal_card() -> None:
    """Test the AtomicPositionsCrystalCard variant."""
    card = AtomicPositionsCrystalCard(
        positions=[
            {"species": "C", "position": [0.0, 0.0, 0.0]},
            {"species": "C", "position": [0.25, 0.25, 0.25]},
        ],
    )
    assert card.unit == "crystal"
    assert isinstance(card.positions[0], AtomicPositionCrystal)
    assert card.positions[1].position == (0.25, 0.25, 0.25)
    assert "ATOMIC_POSITIONS (crystal)" in str(card)


def test_atomic_positions_crystal_sg_card() -> None:
    """Test the AtomicPositionsCrystalSGCard variant."""
    card = AtomicPositionsCrystalSGCard(
        positions=[{"species": "Na", "position": [0.0, 0.0, 0.0]}],
    )
    assert card.unit == "crystal_sg"
    assert isinstance(card.positions[0], AtomicPositionCrystalSG)
    assert "ATOMIC_POSITIONS (crystal_sg)" in str(card)


def test_alat_inner_type() -> None:
    """The alat card stores positions in the alat inner class."""
    card = AtomicPositionsAlatCard(positions=[{"species": "H", "position": [0.0, 0.0, 0.0]}])
    assert isinstance(card.positions[0], AtomicPositionAlat)


def test_pwinput_routes_bohr_atomic_positions() -> None:
    """Constructing PWInput with a bohr-unit dict routes to the bohr card."""
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
    assert isinstance(inp.atomic_positions, AtomicPositionsBohrCard)


def test_pwinput_routes_angstrom_atomic_positions() -> None:
    """Constructing PWInput with an angstrom-unit dict routes to the angstrom card."""
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
    assert isinstance(inp.atomic_positions, AtomicPositionsAngstromCard)


def test_atomic_positions_invalid_unit_raises() -> None:
    """An invalid ``unit`` literal raises ``ValidationError``."""
    with pytest.raises(ValidationError):
        AtomicPositionsBohrCard.model_validate(
            {
                "unit": "bogus",
                "positions": [{"species": "H", "position": [0.0, 0.0, 0.0]}],
            }
        )
