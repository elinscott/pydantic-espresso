from pydantic_espresso.cards.pw.k_points import KPointsGammaCard, KPointsGridCard, KPointsListCard
import numpy as np

def test_kpoints_gamma_card():
    """Test the KPointsGammaCard class."""
    card = KPointsGammaCard()
    assert card.kind == "gamma"

    card_list = card.to_kpoints_list()
    assert len(card_list.k_points) == 1
    assert card_list.k_points[0].coordinate == (0.0, 0.0, 0.0)

def test_kpoints_grid_card():
    """Test the KPointsGridCard class."""
    card = KPointsGridCard(grid=[2, 2, 2], offset=[0, 0, 1])

    assert card.kind == "automatic"
    assert card.grid == (2, 2, 2)
    assert card.offset == (0, 0, 1)
    assert str(card) == "K_POINTS {automatic}\n  2 2 2 0 0 1"

    card_list = card.to_kpoints_list()
    assert len(card_list.k_points) == np.prod(card.grid)
    assert card_list.k_points[0].coordinate == (0.0, 0.0, 0.25)
    assert card_list.k_points[0].weight == 1.0

def test_kpoints_list_card():
    """Test the KPointsListCard class."""

    card = KPointsListCard(k_points=[{"coordinate": [0.0, 0.0, 0.0], "weight": 1.0},
                                     {"coordinate": [0.5, 0.5, 0.5], "weight": 2.0}],
                           kind="crystal")
    
    assert len(card.k_points) == 2
    assert card.k_points[0].coordinate == (0.0, 0.0, 0.0)
    assert card.k_points[0].weight == 1.0
    assert card.k_points[1].coordinate == (0.5, 0.5, 0.5)
    assert card.k_points[1].weight == 2.0
    assert card.kind == "crystal"
    assert str(card) == "K_POINTS {crystal}\n  2\n  0.0 0.0 0.0 1.0\n  0.5 0.5 0.5 2.0"
