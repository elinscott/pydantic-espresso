"""Test `pydantic_espresso.models.pw.cards.atomic_velocities`."""

from pydantic_espresso.models.pw.cards.atomic_velocities import AtomicVelocity


def test_atomic_velocity() -> None:
    """Test the AtomicVelocity class."""
    velocity = AtomicVelocity(species="H", velocity=[0.1, 0.2, 0.3])
    assert str(velocity) == "  H 0.1 0.2 0.3"
