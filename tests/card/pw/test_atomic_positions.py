"""Test `pydantic_espresso.card.pw.atomic_positions`."""

from pydantic_espresso.card.pw.atomic_positions import AtomicPositionsCard


def test_atomic_positions_card() -> None:
    """Test the AtomicPositionsCard class."""
    card = AtomicPositionsCard(
        units="alat",
        positions=[
            {"species": "H", "position": [0.0, 0.0, 0.0]},
            {"species": "H", "position": [1.0, 1.0, 1.0]},
        ],
    )
    assert card.units == "alat"
    assert card.positions[0].species == "H"
    assert card.positions[0].position == (0.0, 0.0, 0.0)
    assert card.positions[1].species == "H"
    assert card.positions[1].position == (1.0, 1.0, 1.0)
    assert str(card) == "ATOMIC_POSITIONS (alat)\n  H 0.0 0.0 0.0\n  H 1.0 1.0 1.0"
