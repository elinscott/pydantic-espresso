"""Test that REQUIRED fields raise when omitted."""

from typing import Any

import pytest
from pydantic import ValidationError

from pydantic_espresso.models.pp.develop import PlotIflag2Namelist
from pydantic_espresso.models.pw.develop import SystemNamelist


def _system_required_fields() -> dict[str, Any]:
    """Return the set of values needed to construct ``SystemNamelist``."""
    return {"ibrav": 1, "nat": 1, "ntyp": 1, "ecutwfc": 30.0}


@pytest.mark.parametrize("missing", ["ibrav", "nat", "ntyp", "ecutwfc"])
def test_system_namelist_required_field_omission_raises(missing: str) -> None:
    """Omitting a required ``SystemNamelist`` field raises ``ValidationError``."""
    kwargs = _system_required_fields()
    kwargs.pop(missing)
    with pytest.raises(ValidationError) as exc:
        SystemNamelist(**kwargs)
    assert missing in str(exc.value)


@pytest.mark.parametrize("field_name", ["ibrav", "nat", "ntyp", "ecutwfc"])
def test_system_namelist_required_field_is_not_optional(field_name: str) -> None:
    """A REQUIRED field's annotation does not include ``None``."""
    field = SystemNamelist.model_fields[field_name]
    # is_required confirms the field has no default.
    assert field.is_required()
    args = getattr(field.annotation, "__args__", None)
    if args is not None:
        assert type(None) not in args


def test_plot_iflag2_required_in_branch() -> None:
    """``PlotIflag2Namelist`` requires e1/e2/x0/nx/ny when iflag==2."""
    with pytest.raises(ValidationError) as exc:
        PlotIflag2Namelist(iflag=2)  # type: ignore[call-arg]
    message = str(exc.value)
    for name in ("nx", "ny", "e1", "e2", "x0"):
        assert name in message
