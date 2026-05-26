"""Turn a pydantic :class:`ValidationError` into a readable 'missing inputs' report.

Follows pydantic's recommended pattern — catch the error and process
``error.errors()`` — rather than intercepting validation. Construction still
raises the usual :class:`pydantic.ValidationError`; call :func:`explain` on the
caught error to get a grouped, recursive summary that names each missing field
together with its type, units, and help text::

    from pydantic import ValidationError
    from pydantic_espresso.missing import explain

    try:
        inp = PWInput(**data)
    except ValidationError as exc:
        print(explain(exc, PWInput))
"""

from __future__ import annotations

import textwrap
from collections.abc import Sequence
from typing import Any, Literal, get_args, get_origin

from pydantic import BaseModel, ValidationError
from pydantic.fields import FieldInfo

from pydantic_espresso.quantity import quantity_for

# Error categories rendered as the recursive missing-inputs summary; anything
# else (a wrong type, a failed constraint) is listed verbatim from pydantic.
_MISSING_ERROR_TYPES = {"missing", "union_tag_not_found"}
_WIDTH = 96
# Some QE help strings are pages long (e.g. ibrav documents every Bravais
# lattice). Truncate to a sensible lead so the report stays scannable; the full
# text remains on the field's ``description``.
_DESC_MAX = 200


def explain(error: ValidationError, model: type[BaseModel]) -> str:
    """Render ``error`` (from validating ``model``) as a readable report.

    ``model`` is the class whose construction failed; it is needed to resolve
    each missing field's type/units/help (a ``ValidationError`` only carries
    locations, not field metadata).
    """
    errors = error.errors()
    missing = [e for e in errors if e["type"] in _MISSING_ERROR_TYPES]
    other = [e for e in errors if e["type"] not in _MISSING_ERROR_TYPES]

    lines: list[str] = []
    if missing:
        lines.append(f"{model.__name__} is missing required inputs:")
        for top, group in _group_errors(model, missing).items():
            lines.extend(_render_group(model, top, group))
    if other:
        if lines:
            lines.append("")
        lines.append("Other validation errors:")
        for err in other:
            loc = ".".join(str(s) for s in err["loc"])
            lines.append(f"  {loc}: {err['msg']}")
    return "\n".join(lines)


def _union_members(annotation: Any) -> list[type[BaseModel]]:
    """Return the BaseModel members of a (possibly ``X | Y``) field annotation."""
    args = get_args(annotation)
    candidates = args if args else (annotation,)
    return [c for c in candidates if isinstance(c, type) and issubclass(c, BaseModel)]


def _discriminator_name(field: FieldInfo | None) -> str | None:
    """Return the field's discriminator name when it is a plain string key."""
    if field is None:
        return None
    discriminator = field.discriminator
    return discriminator if isinstance(discriminator, str) else None


def _discriminator_options(field: FieldInfo) -> list[Any]:
    """List the discriminator tag values across a discriminated-union field's variants."""
    discriminator = _discriminator_name(field)
    if discriminator is None:
        return []
    options: list[Any] = []
    for member in _union_members(field.annotation):
        info = member.model_fields.get(discriminator)
        if info is not None and info.default is not None:
            options.append(info.default)
    return options


def _annotation_str(annotation: Any) -> str:
    """Render a field annotation compactly (basic type, container, or trimmed Literal)."""
    if hasattr(annotation, "__metadata__"):  # Annotated[X, ...] -> X
        annotation = annotation.__origin__
    origin = get_origin(annotation)
    if origin is Literal:
        values = get_args(annotation)
        shown = ", ".join(repr(v) for v in values[:6])
        if len(values) > 6:
            shown += f", … ({len(values)} options)"
        return f"Literal[{shown}]"
    if origin in (tuple, list, set, frozenset):
        inner = ", ".join(_annotation_str(arg) for arg in get_args(annotation))
        return f"{origin.__name__}[{inner}]" if inner else origin.__name__
    if origin is None and isinstance(annotation, type):
        return annotation.__name__
    return str(annotation).replace("typing.", "")


def _field_summary(name: str, info: FieldInfo | None, indent: int) -> list[str]:
    """Render ``- name (type[, units]): help`` wrapped to the report width."""
    bullet = " " * indent + "- "
    if info is None:
        return [bullet + name]
    type_str = _annotation_str(info.annotation)
    quantity = quantity_for(info)
    units = f", {quantity.units}" if quantity and quantity.units else ""
    head = f"{name} ({type_str}{units})"
    description = " ".join((info.description or "").split())
    if len(description) > _DESC_MAX:
        description = description[:_DESC_MAX].rsplit(" ", 1)[0] + " …"
    text = head if not description else f"{head}: {description}"
    return textwrap.wrap(
        text,
        width=_WIDTH,
        initial_indent=bullet,
        subsequent_indent=" " * (indent + 2),
        break_long_words=False,
        break_on_hyphens=False,
    ) or [bullet + head]


def _resolve_field_info(model_cls: type[BaseModel], loc: Sequence[Any]) -> FieldInfo | None:
    """Walk a pydantic error ``loc`` to the target field's :class:`FieldInfo`.

    Handles discriminated-union segments: when a field carries a discriminator
    the following ``loc`` segment is the variant tag, which selects the member
    model to descend into.
    """
    current: type[BaseModel] | None = model_cls
    info: FieldInfo | None = None
    i = 0
    segments = list(loc)
    while i < len(segments) and current is not None:
        info = current.model_fields.get(str(segments[i]))
        if info is None:
            return None
        i += 1
        if i >= len(segments):
            break
        members = _union_members(info.annotation)
        if not members:
            return None
        discriminator = _discriminator_name(info)
        if discriminator is not None and len(members) > 1:
            tag = str(segments[i])
            i += 1
            current = next(
                (m for m in members if str(m.model_fields[discriminator].default) == tag),
                members[0],
            )
        else:
            current = members[0]
    return info


def _required_subfields(field: FieldInfo | None) -> list[tuple[str, FieldInfo]]:
    """Return required (name, info) pairs of an absent block's (first variant) member."""
    if field is None:
        return []
    members = _union_members(field.annotation)
    if not members:
        return []
    return [(n, f) for n, f in members[0].model_fields.items() if f.is_required()]


def _group_errors(model_cls: type[BaseModel], errors: Sequence[Any]) -> dict[str, dict[str, Any]]:
    """Bucket missing/discriminator errors by top-level field into render-ready groups."""
    groups: dict[str, dict[str, Any]] = {}
    for err in errors:
        loc = list(err["loc"])
        top = str(loc[0])
        field = model_cls.model_fields.get(top)
        group = groups.setdefault(top, {"tag": None, "discriminator": None, "leaves": []})

        discriminator = _discriminator_name(field)
        if err["type"] == "union_tag_not_found":
            # Prefer the field's own discriminator name; pydantic's ctx value is
            # quote-wrapped (e.g. "'unit'").
            group["discriminator"] = discriminator or (err.get("ctx") or {}).get("discriminator")
            continue

        rest = loc[1:]
        if discriminator is not None and rest:
            group["tag"] = f"{discriminator}={rest[0]!r}"
            rest = rest[1:]
        group["leaves"].append(loc if rest else None)  # None => the whole block is absent
    return groups


def _render_group(model_cls: type[BaseModel], top: str, group: dict[str, Any]) -> list[str]:
    """Render one top-level field's missing-input lines."""
    field = model_cls.model_fields.get(top)
    head = f"  {top}" + (f" [{group['tag']}]" if group["tag"] else "")

    if group["discriminator"] is not None:
        options = _discriminator_options(field) if field is not None else []
        note = f"missing discriminator {group['discriminator']!r}"
        if options:
            note += f" (one of {options})"
        return [f"{head}: {note}"]

    # A single ``None`` leaf means the whole block is absent.
    if group["leaves"] == [None]:
        discriminator = _discriminator_name(field)
        options = _discriminator_options(field) if field is not None else []
        suffix = f" — choose {discriminator!r}: {options}" if options and discriminator else ""
        lines = [f"{head}: required{suffix}"]
        lines.extend(
            line
            for name, info in _required_subfields(field)
            for line in _field_summary(name, info, indent=6)
        )
        return lines

    lines = [f"{head}:"]
    for loc in group["leaves"]:
        info = _resolve_field_info(model_cls, loc)
        lines.extend(_field_summary(str(loc[-1]), info, indent=6))
    return lines
