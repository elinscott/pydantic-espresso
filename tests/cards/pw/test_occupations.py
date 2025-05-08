from pydantic_espresso.cards.pw.occupations import OccupationsList

def test_occupations_list():
    """Test the OccupationsList class."""
    occupations = OccupationsList([0.5 for _ in range(11)])
    assert len(occupations) == 11
    assert str(occupations) == "  0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5\n  0.5"