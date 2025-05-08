from pydantic_espresso.cards.pw.atomic_forces import AtomicForce


def test_atomic_force():
    """Test the AtomicForce class."""
    force = AtomicForce(species="H", force=[0.1, 0.2, 0.3])
    assert str(force) == "  H 0.1 0.2 0.3"
