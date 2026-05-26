"""Test conditional/ref/computed/expr default metadata on generated fields."""

from typing import Any, cast, get_args

import pytest

from pydantic_espresso.models.pw.develop import ControlNamelist, SystemNamelist
from pydantic_espresso.namelist import Namelist


def test_nstep_conditional_default() -> None:
    """``nstep`` carries a ``conditional_default`` list of ``{when, value}`` dicts."""
    field = ControlNamelist.model_fields["nstep"]
    extra = cast(dict[str, Any], field.json_schema_extra)
    conditional = extra["conditional_default"]
    assert isinstance(conditional, list)
    assert all(isinstance(entry, dict) for entry in conditional)
    assert all({"when", "value"} <= set(entry.keys()) for entry in conditional)
    # The first branch is the scf/nscf/bands special-case.
    first = conditional[0]
    assert "scf" in str(first["when"])
    assert first["value"] == "1"


def test_wfcdir_default_ref() -> None:
    """``wfcdir`` defaults to the value of ``outdir`` via ``default_ref``."""
    field = ControlNamelist.model_fields["wfcdir"]
    extra = cast(dict[str, Any], field.json_schema_extra)
    assert extra["default_ref"] == "outdir"


def test_nbnd_computed_default() -> None:
    """``nbnd`` is flagged with ``computed_default: True``."""
    field = SystemNamelist.model_fields["nbnd"]
    extra = cast(dict[str, Any], field.json_schema_extra)
    assert extra["computed_default"] is True


def test_ecutrho_default_expr() -> None:
    """``ecutrho`` has a ``default_expr`` that references ``ecutwfc``."""
    field = SystemNamelist.model_fields["ecutrho"]
    extra = cast(dict[str, Any], field.json_schema_extra)
    assert "ecutwfc" in extra["default_expr"]


@pytest.mark.parametrize(
    ("model", "field_name", "key"),
    [
        (ControlNamelist, "nstep", "conditional_default"),
        (ControlNamelist, "wfcdir", "default_ref"),
        (SystemNamelist, "nbnd", "computed_default"),
        (SystemNamelist, "ecutrho", "default_expr"),
    ],
)
def test_structured_default_in_json_schema(
    model: type[Namelist], field_name: str, key: str
) -> None:
    """The structured default metadata is threaded through to the JSON schema."""
    schema = model.model_json_schema()
    prop = schema["properties"][field_name]
    assert key in prop
    # And the matching value matches what's on the FieldInfo.
    field_extra = cast(dict[str, Any], model.model_fields[field_name].json_schema_extra)
    assert prop[key] == field_extra[key]


@pytest.mark.parametrize(
    ("model", "field_name"),
    [
        (ControlNamelist, "nstep"),
        (ControlNamelist, "wfcdir"),
        (SystemNamelist, "nbnd"),
        (SystemNamelist, "ecutrho"),
    ],
)
def test_structured_default_widens_to_optional(model: type[Namelist], field_name: str) -> None:
    """Fields with structured defaults have a None default and an ``X | None`` annotation."""
    field = model.model_fields[field_name]
    assert field.default is None
    # The annotation is widened to include None.
    annotation = field.annotation
    assert annotation is not None
    assert type(None) in get_args(annotation)
