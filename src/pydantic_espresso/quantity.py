"""Annotated metadata describing a field's physical units and dimensionality.

The new INPUT_*.def schema (QE >= 7.6) attaches ``<units>`` and
``<dimensionality>`` to every quantity-bearing variable. We surface those facts
on the pydantic field type itself so that consumers reading
``Model.model_fields`` (or hovering in an IDE) see them inline, and so that
``Model.model_json_schema()`` carries them through to JSON-schema consumers.

A field that holds, e.g., an energy in Rydberg is declared as::

    ecutwfc: Annotated[float, Quantity(units="Ry", dimensionality="energy")]

The values are the literal strings emitted by ``helpdoc`` for the QE source:
``units`` is a product-of-powers expression like ``"bohr electron_mass^1/2 Ry^-1/2"``
and ``dimensionality`` is a product-of-powers of base SI-like dimensions like
``"energy length^-1"``. No unit-conversion is performed; this metadata is
documentation that pydantic_espresso threads through to its outputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema


@dataclass(frozen=True, slots=True)
class Quantity:
    """Physical units and dimensionality metadata for a numeric field.

    Instances are attached via ``typing.Annotated`` and inspected at runtime via
    ``typing.get_args(...)``.
    """

    units: str
    dimensionality: str

    def __get_pydantic_json_schema__(
        self, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Inject ``units`` and ``dimensionality`` into the JSON schema."""
        schema = handler(core_schema)
        schema["units"] = self.units
        schema["dimensionality"] = self.dimensionality
        return schema

    def __repr__(self) -> str:
        return f"Quantity(units={self.units!r}, dimensionality={self.dimensionality!r})"


def quantity_for(field_info: Any) -> Quantity | None:
    """Return the ``Quantity`` annotation on ``field_info``, if any.

    Convenience helper for consumers that want to read the metadata without
    juggling ``typing.get_args`` themselves. Pass a ``pydantic.fields.FieldInfo``.
    """
    for meta in getattr(field_info, "metadata", ()):
        if isinstance(meta, Quantity):
            return meta
    return None
