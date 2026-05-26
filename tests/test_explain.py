"""Test the ``explain`` readable-error helper."""

import pytest
from pydantic import ValidationError

from pydantic_espresso.errors import explain
from pydantic_espresso.models.pw.develop import PWInput


def test_explain_partial_input() -> None:
    """A partial input is summarised per block with field annotations."""
    with pytest.raises(ValidationError) as exc:
        PWInput(  # type: ignore[call-arg]
            system={"ibrav": 0, "ecutwfc": 30.0},  # missing nat, ntyp
            cell_parameters={"vectors": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]},  # no unit tag
            k_points={"kind": "automatic"},  # missing grid
            # atomic_positions omitted entirely
        )
    report = explain(exc.value, PWInput)

    assert report.startswith("PWInput is missing required inputs:")
    # Nested missing field, with its type rendered.
    assert "- nat (int)" in report
    # A required card absent entirely lists its discriminator choices.
    assert "atomic_positions: required" in report
    assert "'alat'" in report
    # A card missing only its discriminator tag is reported as such.
    assert "missing discriminator 'unit'" in report
    # The selected variant of a partial discriminated card is shown.
    assert "k_points [kind='automatic']" in report


def test_explain_absent_namelist_expands_required_fields() -> None:
    """Omitting a mandatory namelist lists each required field it needs."""
    with pytest.raises(ValidationError) as exc:
        PWInput(  # type: ignore[call-arg]
            cell_parameters={"unit": "alat", "vectors": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]},
            atomic_positions={
                "unit": "alat",
                "positions": [{"species": "H", "position": [0.0, 0.0, 0.0]}],
            },
            k_points={"kind": "gamma"},
        )
    report = explain(exc.value, PWInput)
    assert "system: required" in report
    for field in ("ibrav", "nat", "ntyp", "ecutwfc"):
        assert field in report
    # Units are surfaced for quantity-bearing fields.
    assert "ecutwfc (float, Ry)" in report


def test_explain_units_in_report() -> None:
    """A quantity-bearing missing field shows its units."""
    with pytest.raises(ValidationError) as exc:
        PWInput(
            system={"ibrav": 0, "nat": 1, "ntyp": 1},  # missing ecutwfc (Ry)
            cell_parameters={"unit": "alat", "vectors": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]},
            atomic_positions={
                "unit": "alat",
                "positions": [{"species": "H", "position": [0.0, 0.0, 0.0]}],
            },
            k_points={"kind": "gamma"},
        )
    report = explain(exc.value, PWInput)
    assert "ecutwfc (float, Ry)" in report


def test_explain_passes_through_type_errors() -> None:
    """Non-missing errors (wrong types) are listed verbatim, not hidden."""
    with pytest.raises(ValidationError) as exc:
        PWInput(
            system={"ibrav": 0, "nat": "notanint", "ntyp": 1, "ecutwfc": 30.0},
            cell_parameters={"unit": "alat", "vectors": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]},
            atomic_positions={
                "unit": "alat",
                "positions": [{"species": "H", "position": [0.0, 0.0, 0.0]}],
            },
            k_points={"kind": "gamma"},
        )
    report = explain(exc.value, PWInput)
    assert "Other validation errors:" in report
    assert "system.nat" in report
