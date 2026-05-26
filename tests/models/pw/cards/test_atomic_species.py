"""Test `pydantic_espresso.models.pw.cards.atomic_species`."""

from pydantic_espresso.models.pw.cards.atomic_species import AtomicSpecies


def test_atomic_species_card() -> None:
    """Test the AtomicSpecies class."""
    atomic_species = AtomicSpecies(species="H", mass=1.0, pseudopotential="H.upf")
    assert atomic_species.species == "H"
    assert atomic_species.mass == 1.0
    assert atomic_species.pseudopotential == "H.upf"
    assert str(atomic_species) == "H 1.0 H.upf"
