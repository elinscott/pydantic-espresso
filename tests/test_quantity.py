"""Test the ``Quantity`` metadata attached to numeric fields."""

import pytest
from pydantic import BaseModel

from pydantic_espresso.models.pw.develop import ControlNamelist, SystemNamelist
from pydantic_espresso.quantity import Quantity, quantity_for


@pytest.mark.parametrize(
    ("model", "field_name", "expected"),
    [
        (
            ControlNamelist,
            "dt",
            Quantity(units="bohr electron_mass^1/2 Ry^-1/2", dimensionality="time"),
        ),
        (SystemNamelist, "ecutwfc", Quantity(units="Ry", dimensionality="energy")),
        (ControlNamelist, "max_seconds", Quantity(units="s", dimensionality="time")),
        (
            ControlNamelist,
            "forc_conv_thr",
            Quantity(units="Ry bohr^-1", dimensionality="energy length^-1"),
        ),
    ],
)
def test_quantity_metadata(model: type[BaseModel], field_name: str, expected: Quantity) -> None:
    """The Quantity annotation is exposed via ``FieldInfo.metadata``."""
    field_info = model.model_fields[field_name]
    metadata = list(field_info.metadata)
    assert expected in metadata


@pytest.mark.parametrize(
    ("model", "field_name", "units", "dimensionality"),
    [
        (
            ControlNamelist,
            "dt",
            "bohr electron_mass^1/2 Ry^-1/2",
            "time",
        ),
        (SystemNamelist, "ecutwfc", "Ry", "energy"),
        (ControlNamelist, "max_seconds", "s", "time"),
        (ControlNamelist, "forc_conv_thr", "Ry bohr^-1", "energy length^-1"),
    ],
)
def test_quantity_in_json_schema(
    model: type[BaseModel], field_name: str, units: str, dimensionality: str
) -> None:
    """The Quantity metadata is threaded through to ``model_json_schema``."""
    schema = model.model_json_schema()
    prop = schema["properties"][field_name]
    assert prop["units"] == units
    assert prop["dimensionality"] == dimensionality


def test_quantity_for_helper() -> None:
    """``quantity_for`` returns the attached Quantity (or None)."""
    field_info = SystemNamelist.model_fields["ecutwfc"]
    q = quantity_for(field_info)
    assert q == Quantity(units="Ry", dimensionality="energy")

    # A field without a Quantity returns None.
    plain = ControlNamelist.model_fields["prefix"]
    assert quantity_for(plain) is None
