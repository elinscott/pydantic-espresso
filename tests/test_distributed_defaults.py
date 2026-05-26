"""Test that vargroup list defaults are distributed onto individual fields."""

import pytest

from pydantic_espresso.models.ld1.develop import TestNamelist as _LD1TestNamelist
from pydantic_espresso.models.turbo_eels.develop import LrControlNamelist


@pytest.mark.parametrize(
    ("field_name", "expected"),
    [("q1", 1.0), ("q2", 1.0), ("q3", 1.0)],
)
def test_turbo_eels_q_defaults_distributed(field_name: str, expected: float) -> None:
    """``q1``, ``q2``, ``q3`` each receive the same scalar from the list default."""
    field = LrControlNamelist.model_fields[field_name]
    assert field.default == expected


@pytest.mark.parametrize(
    ("field_name", "expected"),
    [("ecutmin", 0), ("ecutmax", 0), ("decut", 5.0)],
)
def test_ld1_ecut_defaults_distributed(field_name: str, expected: float) -> None:
    """LD1's ``[0, 0, 5.0]`` vargroup default distributes positionally."""
    field = _LD1TestNamelist.model_fields[field_name]
    assert field.default == expected
