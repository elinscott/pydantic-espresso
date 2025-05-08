from pydantic_espresso.cards.pw.solvents import SolventsCard, SolventsLRCard

def test_solvents_card():
    """Test the SolventsCard class."""
    card = SolventsCard(units="1/cell", solvents=[{"label": "water", "density": 1.0, "molecule": "water.mol"}])
    assert str(card) == "SOLVENTS {1/cell}\n  water 1.0 water.mol"

def test_solvents_lr_card():
    """Test the SolventsLRCard class."""
    card = SolventsLRCard(units="1/cell", solvents=[{"label": "water", "density_left": 1.0, "density_right": 2.0, "molecule": "water.mol"}])
    assert str(card) == "SOLVENTS {1/cell}\n  water 1.0 2.0 water.mol"