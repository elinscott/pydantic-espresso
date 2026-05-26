"""Test that alias values are normalized onto the canonical form."""

import pytest

from pydantic_espresso.models.pw.develop import ControlNamelist, SystemNamelist


@pytest.mark.parametrize(
    ("alias", "canonical"),
    [
        ("gauss", "gaussian"),
        ("m-p", "methfessel-paxton"),
        ("mp", "methfessel-paxton"),
        ("cold", "marzari-vanderbilt"),
        ("m-v", "marzari-vanderbilt"),
        ("fd", "fermi-dirac"),
        ("f-d", "fermi-dirac"),
    ],
)
def test_smearing_alias_mapping(alias: str, canonical: str) -> None:
    """Comma-separated legacy aliases for ``smearing`` map onto canonical values."""
    inp = SystemNamelist(ibrav=1, nat=1, ntyp=1, ecutwfc=30.0, smearing=alias)
    assert inp.smearing == canonical


@pytest.mark.parametrize(
    ("alias", "canonical"),
    [
        ("medium", "high"),
        ("debug", "high"),
        ("default", "low"),
        ("minimal", "low"),
    ],
)
def test_verbosity_alias_mapping(alias: str, canonical: str) -> None:
    """``<opt alias=...>`` aliases for ``verbosity`` map onto canonical values."""
    inp = ControlNamelist(verbosity=alias)
    assert inp.verbosity == canonical


def test_canonical_value_round_trips() -> None:
    """Already-canonical values pass through unchanged."""
    inp = SystemNamelist(ibrav=1, nat=1, ntyp=1, ecutwfc=30.0, smearing="gaussian")
    assert inp.smearing == "gaussian"
