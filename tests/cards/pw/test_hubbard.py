from pydantic_espresso.cards.pw.hubbard import HubbardCard, HubbardB, HubbardU, HubbardJ, HubbardV

def test_hubbard_card():
    """Test the HubbardCard class."""
    card = HubbardCard(kind="atomic", parameters=[HubbardU(site={"label": "Fe", "manifold": "3d"}, value=5.0),
                                                  HubbardV(sites=[{"label": "Fe", "manifold": "3d"}, {"label": "O", "manifold": "2p"}],
                                                           atom_indices=(1, 2), value=1.0)])

    assert card.kind == "atomic"
    assert str(card) == "HUBBARD {atomic}\n  U Fe-3d 5.0\n  V Fe-3d O-2p 1 2 1.0"

def test_hubbard_b():
    """Test the HubbardB class."""
    b = HubbardB(site={"label": "Fe", "manifold": "3d"}, value=5.0)
    assert b.name == "B"
    assert str(b) == "B Fe-3d 5.0"

def test_hubbard_u():
    """Test the HubbardU class."""
    u = HubbardU(site={"label": "Fe", "manifold": "3d"}, value=5.0)
    assert u.name == "U"
    assert str(u) == "U Fe-3d 5.0"

def test_hubbard_j():
    """Test the HubbardJ class."""
    j = HubbardJ(site={"label": "Fe", "manifold": "3d"}, value=5.0)
    assert j.name == "J"
    assert str(j) == "J Fe-3d 5.0"

def test_hubbard_v():
    """Test the HubbardV class."""
    v = HubbardV(sites=[{"label": "Fe", "manifold": "3d"}, {"label": "O", "manifold": "2p"}], 
                 atom_indices=(1, 2), value=1.0)
    assert v.name == "V"
    assert str(v) == "V Fe-3d O-2p 1 2 1.0"