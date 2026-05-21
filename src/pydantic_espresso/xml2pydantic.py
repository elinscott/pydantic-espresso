"""Functions for converting the content of XML files to Pydantic models as raw strings.

We generate static python code (cf. dynamic model creation) because we want to be able to
inspect the models statically.

The XML format consumed here is the new ``INPUT_*.xml`` shape produced by Quantum ESPRESSO
>= 7.6: structured ``<default kind="...">`` elements, sibling ``<units>`` /
``<dimensionality>`` elements, and explicit ``alias="..."`` attributes on ``<opt>``.
"""

import re
import warnings
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import Element, ParseError

from defusedxml.ElementTree import parse

from pydantic_espresso.models import directory as model_directory
from pydantic_espresso.xml_files import directory as xml_directory

# Matches pep8-naming's notion of ``mixedCase``: name starts with a lowercase
# letter or underscore and contains at least one uppercase letter elsewhere.
# Names matching this are flagged by ruff's N815 rule.
_MIXED_CASE_RE = re.compile(r"^[a-z_][a-zA-Z0-9_]*[A-Z][a-zA-Z0-9_]*$")
_MAX_LINE_LEN = 100

type_mapping = {
    "INTEGER": int,
    "REAL": float,
    "LOGICAL": bool,
    "CHARACTER": str,
    "STRING": str,
    "integer": int,
    "real": float,
    "logical": bool,
    "character": str,
    "string": str,
    "DOUBLE": float,
    "CHARATER": str,
}


INDENT = "    "

# Tags whose markup we strip pre-parse because they are purely presentational and
# would otherwise interfere with reading ``<info>`` text. ``<ref>`` is deliberately
# excluded: the new schema uses it as structured data inside ``<default kind="ref">``
# and ``<default kind="expr">``.
_PRESENTATIONAL_TAGS = ("b", "link")


class InvalidXMLStructureError(Exception):
    """Raised when the structure of the XML file is not as expected."""


def sanitize_xml(xml_path: Path) -> Path:
    """Strip presentational markup from ``xml_path`` and write a sanitized copy.

    We drop ``<b>``, ``<link>``, ``<br/>`` and inline ``<a href="...">...</a>`` tags
    that only appear inside free-text ``<info>`` blocks. ``<ref>`` is preserved so
    that ``<default kind="ref">`` / ``<default kind="expr">`` can be parsed as
    structured data.
    """
    with open(xml_path) as f:
        xmlstr = f.read()

    for tag in _PRESENTATIONAL_TAGS:
        xmlstr = xmlstr.replace(f"<{tag}>", "").replace(f"</{tag}>", "")

    xmlstr = xmlstr.replace("<br/>", "")

    # Replace inline links <a href="url">text</a> with "text (url)".
    while '<a href="' in xmlstr:
        start = xmlstr.find('<a href="')
        end = xmlstr.find('">', start)
        url = xmlstr[start + 9 : end]
        text_end = xmlstr.find("</a>", end)
        text = xmlstr[end + 2 : text_end]
        xmlstr = xmlstr[:start] + f"{text} ({url})" + xmlstr[text_end + 4 :]

    sanitized_path = xml_path.with_stem(xml_path.stem + "_sanitized")
    with open(sanitized_path, "w") as f:
        f.write(xmlstr)

    return sanitized_path


def convert_all_xml_files_to_models() -> None:
    """Convert all XML files in the xml_files directory to Pydantic models."""
    for xml_path in xml_directory.rglob("*.xml"):
        try:
            model_str, executable_str = convert_xml_file_to_model(
                xml_path, version=xml_path.parent.name
            )
        except ParseError as e:
            warnings.warn(f"Processing {xml_path} failed: {e}", stacklevel=2)
            continue
        except InvalidXMLStructureError as e:
            warnings.warn(f"Processing {xml_path} failed: {e}", stacklevel=2)
            continue

        model_file = (
            model_directory
            / xml_path.parent.name.replace(".", "_").replace("-", "_")
            / f"{executable_str}.py"
        )
        model_dir = Path(model_file).parent
        if not model_dir.exists():
            model_dir.mkdir(parents=True, exist_ok=True)
            with open(model_dir / "__init__.py", "w") as f:
                f.write(
                    '"""Pydantic models for Quantum ESPRESSO executables.\n\nThis file is '
                    'automatically generated; do not edit.\n"""'
                )
        with open(model_file, "w") as f:
            f.write(model_str)


def convert_xml_file_to_model(xml_file: Path, version: str = "develop") -> tuple[str, str]:
    """Convert an XML file to raw python code that defines the corresponding Pydantic model."""
    sanitized_xml = sanitize_xml(xml_file)
    try:
        tree = parse(sanitized_xml)
    finally:
        sanitized_xml.unlink(missing_ok=True)

    root = tree.getroot()
    executable_name = root.attrib["program"].lower()
    executable_name = executable_name.replace(".x", "").replace("-", "_").replace(" ", "_")
    return convert_xml_tree_to_model(root, version=version), executable_name


def convert_xml_tree_to_model(root: Element, version: str = "develop") -> str:
    """Convert an XML tree to raw python code that defines the corresponding Pydantic model."""
    program = root.attrib["program"][:-2]

    fields: list[str] = []
    subclasses: list[str] = []
    imports: set[str] = set()
    needs_quantity = False

    for namelist in root.findall("namelist"):
        field_line, namelist_block, uses_quantity = _process_namelist(namelist)
        needs_quantity = needs_quantity or uses_quantity
        fields.append(field_line)
        subclasses += namelist_block

    for card in root.findall("card"):
        try:
            field_def, import_str = load_prebuilt_card(card, program)
            fields.append(field_def)
            imports.add(import_str)
        except ImportError as e:
            warnings.warn(f"Failed to load prebuilt card: {e}", stacklevel=2)

    return _generate_model_string(
        root.attrib["program"],
        fields,
        subclasses,
        imports,
        version=version,
        needs_quantity=needs_quantity,
    )


def _process_namelist(namelist: Element) -> tuple[str, list[str], bool]:
    """Process one ``<namelist>`` element.

    Returns ``(field_line, namelist_block, uses_quantity)`` where ``field_line``
    is the EspressoInput-level field referring to the namelist subclass and
    ``namelist_block`` is the subclass definition lines.
    """
    _propagate_group_attributes(namelist)

    # Detect a discriminated ``<choose>`` child: a single ``<choose>`` whose
    # branches are mutually-exclusive alternatives keyed on the value of one
    # other variable. PPACF-style ``<choose>``s with a lone ``<when>`` and no
    # ``<elsewhen>``/``<otherwise>`` are *not* discriminated; they (and any
    # subsequent ``<choose>``s) fall through to the single-class path.
    discriminated_choose = _find_discriminated_choose(namelist)
    if discriminated_choose is not None:
        return _process_discriminated_namelist(namelist, discriminated_choose)

    field_definitions, field_validators, uses_quantity = _collect_fields(
        namelist.findall(".//var"), namelist.findall(".//dimension")
    )

    name = namelist.attrib["name"]
    type_name = f"{camel_case(name)}Namelist"
    # If any ``<var>`` in this namelist is REQUIRED (and has no default) the
    # namelist cannot be auto-constructed with zero args; expose it as
    # ``Optional[...]`` defaulting to None so the user must supply it (or omit
    # it entirely when not needed).
    if _namelist_has_required_var(namelist):
        field_line = _format_simple_field(
            name.lower(),
            f"{type_name} | None",
            "Field(None)",
        )
    else:
        field_line = _format_simple_field(
            name.lower(),
            type_name,
            f"Field(default_factory=lambda: {type_name}())",
        )
    namelist_block = _generate_namelist(name, field_definitions, field_validators)
    return field_line, namelist_block, uses_quantity


def _namelist_has_required_var(namelist: Element) -> bool:
    """Return True if any ``<var>`` / ``<dimension>`` in ``namelist`` is REQUIRED.

    Only counts elements that have no ``<default>``; one that is REQUIRED but
    also supplies a literal default is effectively optional from pydantic's
    point of view. The "REQUIRED" status comes either from an explicit
    ``<status>REQUIRED</status>`` child or from the element living inside a
    ``<choose>`` branch without a ``<default>`` (see ``_var_is_required``).
    """
    branch_member_ids: set[int] = set()
    for choose in namelist.findall(".//choose"):
        for branch in choose:
            if branch.tag in ("when", "elsewhen", "otherwise"):
                for el in branch.iter():
                    branch_member_ids.add(id(el))

    for element in (*namelist.findall(".//var"), *namelist.findall(".//dimension")):
        if element.find("default") is not None:
            continue
        in_branch = id(element) in branch_member_ids
        if _var_is_required(element, in_choose_branch=in_branch):
            return True
    return False


def _collect_fields(
    vars_: list[Element], dims: list[Element], in_choose_branch: bool = False
) -> tuple[list[str], list[list[str]], bool]:
    """Collect field definitions and validators from a list of ``<var>`` / ``<dimension>``.

    Encapsulates the duplicate-handling that previously lived inline in
    ``_process_namelist`` so we can reuse the same logic when partitioning a
    namelist into a base class plus discriminated variants. When
    ``in_choose_branch`` is True the children come from inside a ``<when>`` /
    ``<elsewhen>`` / ``<otherwise>`` branch and the "no <default> means
    REQUIRED" rule applies to each one.
    """
    field_definitions: list[str] = []
    field_validators: list[list[str]] = []
    uses_quantity = False

    for var in vars_:
        field_definition, field_validator, var_uses_quantity = _parse_var(
            var, in_choose_branch=in_choose_branch
        )
        if field_definition is None:
            continue
        uses_quantity = uses_quantity or var_uses_quantity

        # Manual fixes for duplicate entries from the historical schema.
        if field_definition.startswith("abivol:") and any(
            x.startswith("abivol:") for x in field_definitions
        ):
            continue
        if field_definition.startswith("restart:") and any(
            x.startswith("restart:") for x in field_definitions
        ):
            field_definition = field_definition.replace("restart:", "restart_step:")

        field_definitions.append(field_definition)
        if field_validator:
            field_validators.append(field_validator)

    for dim in dims:
        field_definition, dim_uses_quantity = _parse_dimension(
            dim, in_choose_branch=in_choose_branch
        )
        if field_definition is None:
            continue
        uses_quantity = uses_quantity or dim_uses_quantity
        field_definitions.append(field_definition)

    return field_definitions, field_validators, uses_quantity


# ---------------------------------------------------------------------------
# Discriminated namelist variants (``<choose>`` / ``<when>`` / ``<elsewhen>``)
# ---------------------------------------------------------------------------


def _find_discriminated_choose(namelist: Element) -> Element | None:
    """Return the namelist's discriminated ``<choose>`` child, if any.

    A ``<choose>`` is "discriminated" when it contains an ``<elsewhen>`` or an
    ``<otherwise>`` (i.e. there is more than one mutually-exclusive branch).
    We require there to be *exactly one* ``<choose>`` direct child of the
    namelist — multi-``<choose>`` namelists (e.g. PPACF) are not modelled as
    discriminated unions in this pass.
    """
    chooses = namelist.findall("choose")
    if len(chooses) != 1:
        return None
    choose = chooses[0]
    has_alternatives = choose.find("elsewhen") is not None or choose.find("otherwise") is not None
    if not has_alternatives:
        return None
    return choose


def _process_discriminated_namelist(
    namelist: Element, choose: Element
) -> tuple[str, list[str], bool]:
    """Emit a base class, one variant per branch, and a discriminated-union alias."""
    branches = [b for b in choose if b.tag in ("when", "elsewhen", "otherwise")]
    name = namelist.attrib["name"]
    base_type_name = f"_{camel_case(name)}NamelistBase"

    discriminator, raw_branch_values = _parse_branch_discriminators(branches, namelist)
    discr_var = _find_discriminator_var(namelist, discriminator)
    if discr_var is None:
        raise InvalidXMLStructureError(
            f"Namelist {name!r} has a discriminated <choose> on {discriminator!r}"
            f" but no <var> definition for it."
        )
    discr_python_type = _get_var_type(discriminator, discr_var)
    if discr_python_type not in (int, str):
        raise InvalidXMLStructureError(
            f"Discriminator {discriminator!r} in namelist {name!r} has unsupported"
            f" type {discr_python_type!r}; only INTEGER and CHARACTER are supported."
        )

    # Resolve catch-all values for any <otherwise> from the discriminator's <options>.
    branch_values: list[list[str]] = _resolve_otherwise_values(
        raw_branch_values, discr_var, discr_python_type, name
    )

    # Partition vars/dimensions into unconditional (outside the <choose>) and
    # conditional (inside each branch). The discriminator itself is excluded
    # from the unconditional set; it is re-declared on each variant as a
    # ``Literal[...]`` with the appropriate value(s).
    unconditional_vars, unconditional_dims = _partition_unconditional(
        namelist, choose, discriminator
    )
    base_fields, base_validators, base_uses_quantity = _collect_fields(
        unconditional_vars, unconditional_dims
    )

    subclasses: list[str] = []
    subclasses.extend(_render_base_namelist(name, base_type_name, base_fields, base_validators))
    subclasses.extend(["", ""])

    variant_names: list[str] = []
    uses_quantity = base_uses_quantity
    for branch, values in zip(branches, branch_values, strict=True):
        variant_name = _variant_class_name(name, discriminator, values)
        variant_names.append(variant_name)
        variant_block, variant_uses_quantity = _render_variant_namelist(
            namelist_name=name,
            variant_name=variant_name,
            base_name=base_type_name,
            branch=branch,
            discriminator=discriminator,
            discriminator_values=values,
            discriminator_python_type=discr_python_type,
        )
        uses_quantity = uses_quantity or variant_uses_quantity
        subclasses.extend(variant_block)
        subclasses.extend(["", ""])

    alias_name = f"{camel_case(name)}Namelist"
    subclasses.extend(_render_variant_alias(alias_name, variant_names, discriminator))
    subclasses.extend(["", ""])

    default_variant = variant_names[0]
    # If any variant has a REQUIRED-without-default ``<var>`` (unconditional or
    # branch-local), the namelist can't be auto-constructed; expose it as
    # ``Optional[...]`` defaulting to None.
    if _namelist_has_required_var(namelist):
        field_line = _format_simple_field(
            name.lower(),
            f"{alias_name} | None",
            f'Field(None, discriminator="{discriminator}")',
        )
    else:
        field_line = _format_simple_field(
            name.lower(),
            alias_name,
            f'Field(default_factory=lambda: {default_variant}(), discriminator="{discriminator}")',
        )
    return field_line, subclasses, uses_quantity


def _parse_branch_discriminators(
    branches: list[Element], namelist: Element
) -> tuple[str, list[list[str] | None]]:
    """Parse the discriminator name and per-branch value list from ``<when>``/``<elsewhen>``.

    Returns ``(discriminator_name, branch_values)`` where ``branch_values[i]``
    is either a list of raw string values for the i-th branch or ``None`` for
    an ``<otherwise>`` branch (which is resolved later from the discriminator's
    ``<options>``).
    """
    discriminator: str | None = None
    values: list[list[str] | None] = []
    namelist_name = namelist.attrib["name"]
    for branch in branches:
        if branch.tag == "otherwise":
            values.append(None)
            continue
        test = branch.attrib.get("test", "")
        parsed = _parse_when_test(test)
        if parsed is None:
            raise InvalidXMLStructureError(
                f"Could not parse <{branch.tag} test={test!r}> in namelist {namelist_name!r}."
            )
        branch_discriminator, branch_values_raw = parsed
        if discriminator is None:
            discriminator = branch_discriminator
        elif branch_discriminator != discriminator:
            raise InvalidXMLStructureError(
                f"Namelist {namelist_name!r} has a discriminated <choose> with"
                f" inconsistent discriminators: {discriminator!r} vs"
                f" {branch_discriminator!r}."
            )
        values.append(branch_values_raw)

    if discriminator is None:
        raise InvalidXMLStructureError(
            f"Discriminated <choose> in namelist {namelist_name!r} has no"
            f" <when>/<elsewhen> branches; cannot infer discriminator."
        )
    return discriminator, values


_WHEN_TEST_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(.+?)\s*$")


def _parse_when_test(test: str) -> tuple[str, list[str]] | None:
    """Parse a ``<when test="lhs = v1 or v2 or v3">`` expression.

    Recognises forms like ``iflag = 0 or 1``, ``plot_num=1``, and
    ``iflag = 2``. Returns ``(lhs, [v1, v2, ...])`` or ``None`` if the
    expression doesn't match the supported shape.
    """
    match = _WHEN_TEST_RE.match(test)
    if match is None:
        return None
    lhs = match.group(1)
    rhs = match.group(2)
    # Split on ``or`` (case-insensitive) at word boundaries.
    raw_values = re.split(r"\s+or\s+", rhs, flags=re.IGNORECASE)
    values = [v.strip() for v in raw_values if v.strip()]
    if not values:
        return None
    return lhs, values


def _find_discriminator_var(namelist: Element, discriminator: str) -> Element | None:
    """Locate the ``<var name="discriminator">`` element (unconditional)."""
    for var in namelist.findall(".//var"):
        if var.attrib.get("name") == discriminator:
            return var
    return None


def _resolve_otherwise_values(
    branch_values: list[list[str] | None],
    discr_var: Element,
    discr_python_type: type,
    namelist_name: str,
) -> list[list[str]]:
    """Replace any ``None`` entry (``<otherwise>``) with the catch-all values."""
    if all(v is not None for v in branch_values):
        return [v for v in branch_values if v is not None]

    options = discr_var.find("options")
    enumerated: list[str] | None = None
    if options is not None:
        enumerated = [opt.attrib["val"] for opt in options.findall("opt")]

    # Build the set of already-covered values, comparing as canonical literals.
    covered: set[str] = set()
    for v in branch_values:
        if v is None:
            continue
        for item in v:
            covered.add(_format_literal(item, discr_python_type))

    resolved: list[list[str]] = []
    for v in branch_values:
        if v is not None:
            resolved.append(v)
            continue
        if enumerated is None:
            warnings.warn(
                f"<otherwise> in namelist {namelist_name!r} cannot be expanded:"
                f" the discriminator has no <options> enumeration; the branch"
                f" will accept any value.",
                stacklevel=2,
            )
            resolved.append([])
            continue
        catch_all = [
            opt for opt in enumerated if _format_literal(opt, discr_python_type) not in covered
        ]
        resolved.append(catch_all)
    return resolved


def _partition_unconditional(
    namelist: Element, choose: Element, discriminator: str
) -> tuple[list[Element], list[Element]]:
    """Return the vars/dimensions that live *outside* the discriminated ``<choose>``.

    The discriminator ``<var>`` itself is excluded — it is re-declared on each
    variant as a ``Literal[...]``.
    """
    inside_choose = {id(el) for el in choose.iter()}
    unconditional_vars: list[Element] = []
    unconditional_dims: list[Element] = []
    for var in namelist.findall(".//var"):
        if id(var) in inside_choose:
            continue
        if var.attrib.get("name") == discriminator:
            continue
        unconditional_vars.append(var)
    for dim in namelist.findall(".//dimension"):
        if id(dim) in inside_choose:
            continue
        unconditional_dims.append(dim)
    return unconditional_vars, unconditional_dims


def _variant_class_name(namelist_name: str, discriminator: str, values: list[str]) -> str:
    """Build a CamelCase variant class name like ``PlotIflag0Or1Namelist``."""
    if not values:
        suffix = "Other"
    else:
        suffix = "Or".join(_sanitize_value_suffix(v) for v in values)
    discr_part = camel_case(discriminator)
    return f"{camel_case(namelist_name)}{discr_part}{suffix}Namelist"


def _sanitize_value_suffix(value: str) -> str:
    """Sanitize a discriminator value for use in a class-name suffix."""
    text = value.strip().strip("'\"")
    text = text.replace("-", "Neg")
    # Keep only alphanumerics.
    cleaned = "".join(ch for ch in text if ch.isalnum())
    return cleaned or "Empty"


def _render_base_namelist(
    name: str, base_type_name: str, fields: list[str], validators: list[list[str]]
) -> list[str]:
    """Render the ``_<Name>NamelistBase`` class holding the unconditional fields."""
    docstring = INDENT + '"""' + f"Shared fields for the `{name}` namelist (all variants)." + '"""'
    body: list[str] = [f"class {base_type_name}(Namelist):", docstring, ""]
    body += [(INDENT + row) if row else "" for v in validators for row in v]
    if not fields:
        # Avoid an empty class body.
        body.append(INDENT + "pass")
    else:
        body += fields
    return body


def _render_variant_namelist(
    namelist_name: str,
    variant_name: str,
    base_name: str,
    branch: Element,
    discriminator: str,
    discriminator_values: list[str],
    discriminator_python_type: type,
) -> tuple[list[str], bool]:
    """Render one variant class inheriting from the base, with branch-specific fields."""
    _propagate_group_attributes(branch)
    field_definitions, field_validators, uses_quantity = _collect_fields(
        branch.findall(".//var"), branch.findall(".//dimension"), in_choose_branch=True
    )

    # Render the discriminator field. Use Literal[...] keyed on the branch's
    # value set; default to the first value so the variant can be constructed
    # with no arguments.
    literal_entries = [_format_literal(v, discriminator_python_type) for v in discriminator_values]
    if literal_entries:
        type_str = f"Literal[{', '.join(literal_entries)}]"
        default_str = literal_entries[0]
    else:
        # Catch-all <otherwise> with no enumerable values: fall back to the
        # raw python type with no default-on-the-variant restriction.
        type_str = discriminator_python_type.__name__
        default_str = "None"
        type_str += " | None"
    discr_field = _format_field(
        discriminator, type_str, default_str, None, f"Discriminator: {discriminator}"
    )

    branch_summary = _branch_summary(branch, discriminator, discriminator_values)
    docstring = INDENT + '"""' + f"`{namelist_name}` namelist when {branch_summary}." + '"""'
    body: list[str] = [
        f"class {variant_name}({base_name}):",
        docstring,
        "",
    ]
    body += [(INDENT + row) if row else "" for v in field_validators for row in v]
    body.append(discr_field)
    body += field_definitions
    return body, uses_quantity


def _branch_summary(branch: Element, discriminator: str, values: list[str]) -> str:
    """Render a short human-readable summary of which discriminator values apply."""
    if branch.tag == "otherwise" or not values:
        return f"`{discriminator}` is not covered by any other branch"
    if len(values) == 1:
        return f"`{discriminator}` == {values[0]}"
    joined = ", ".join(values)
    return f"`{discriminator}` in ({joined})"


def _render_variant_alias(
    alias_name: str, variant_names: list[str], discriminator: str
) -> list[str]:
    """Render the ``<Name>Namelist = Annotated[V1 | V2 | ..., Field(discriminator=...)]`` line."""
    if len(variant_names) == 1:
        # Degenerate case: a discriminated <choose> with a single branch.
        # Emit a simple alias so callers can still reference ``<Name>Namelist``.
        return [f"{alias_name} = {variant_names[0]}"]
    union_str = " | ".join(variant_names)
    single = f'{alias_name} = Annotated[{union_str}, Field(discriminator="{discriminator}")]'
    if len(single) <= _MAX_LINE_LEN:
        return [single]
    # If the union fits on a single indented line, keep it on one line — this
    # matches ruff format's preference (it would otherwise reformat a one-per-line
    # wrap back to this shape).
    union_inline = INDENT + union_str + ","
    if len(union_inline) <= _MAX_LINE_LEN:
        return [
            f"{alias_name} = Annotated[",
            INDENT + union_str + ",",
            INDENT + f'Field(discriminator="{discriminator}"),',
            "]",
        ]
    # Wrap onto multiple lines, one variant per line.
    lines = [f"{alias_name} = Annotated["]
    for i, variant in enumerate(variant_names):
        suffix = "," if i == len(variant_names) - 1 else ""
        if i == 0:
            lines.append(INDENT + variant + suffix)
        else:
            lines.append(INDENT + "| " + variant + suffix)
    lines.append(INDENT + f'Field(discriminator="{discriminator}"),')
    lines.append("]")
    return lines


_GROUP_SHARED_CHILD_TAGS = ("dimensionality", "units", "default", "info")


def _copy_shared_children(child: Element, shared_children: list[Element]) -> None:
    """Copy each ``shared`` child onto ``child`` when ``child`` doesn't already have one."""
    existing_tags = {c.tag for c in child}
    for shared in shared_children:
        if shared.tag not in existing_tags:
            child.append(shared)


def _propagate_group_attributes(namelist: Element) -> None:
    """Push shared attributes from ``<vargroup>`` / ``<dimensiongroup>`` onto their children.

    The new schema lets a single ``<vargroup type="INTEGER">`` cover multiple
    typeless ``<var>`` children, and ``<dimensiongroup type="REAL" start="1"
    end="3"><dimensionality/><units/>`` carry shared metadata that applies to
    each nested ``<dimension>``. Normalize the tree by copying those attributes
    (and the shared ``<dimensionality>``, ``<units>``, ``<default>`` and
    ``<info>`` elements) onto each child so the rest of the parser doesn't have
    to know about the group wrapper.
    """
    for vargroup in namelist.findall(".//vargroup"):
        group_type = vargroup.attrib.get("type")
        shared_children = [c for c in vargroup if c.tag in _GROUP_SHARED_CHILD_TAGS]
        for var in vargroup.findall("var"):
            if group_type is not None:
                var.attrib.setdefault("type", group_type)
            _copy_shared_children(var, shared_children)

    for dimgroup in namelist.findall(".//dimensiongroup"):
        shared_attrs = {k: v for k, v in dimgroup.attrib.items() if k in ("type", "start", "end")}
        shared_children = [c for c in dimgroup if c.tag in _GROUP_SHARED_CHILD_TAGS]
        for dim in dimgroup.findall("dimension"):
            for key, value in shared_attrs.items():
                dim.attrib.setdefault(key, value)
            _copy_shared_children(dim, shared_children)


def camel_case(value: str) -> str:
    """Convert a string to camel case."""
    return "".join([s.capitalize() for s in value.replace("_", " ").split()])


def load_prebuilt_card(card: Element, program: str) -> tuple[str, str]:
    """Load a prebuilt card."""
    name = card.attrib["name"].lower()
    card_module = __import__(f"pydantic_espresso.card.{program}", fromlist=[program])
    prebuilt_cards = getattr(card_module, "prebuilt_cards", None)
    if prebuilt_cards is None:
        raise ImportError(f"No prebuilt cards found for {program}.")
    card_dct = prebuilt_cards.get(name, None)
    if card_dct is None:
        raise ImportError(f"No prebuilt card found for {name} in {program}.")

    type_ = card_dct["type"]
    default = card_dct["default"]
    import_str = card_dct["import_str"]

    return _format_simple_field(name, type_, default), import_str


def _generate_namelist(name: str, fields: list[str], validators: list[list[str]]) -> list[str]:
    """Convert a list of fields and validators into a Namelist subclass definition.

    ``fields`` are produced by ``_format_field`` and already include the
    4-space class-body indent on every line, so they are emitted verbatim.
    """
    return (
        [
            f"class {camel_case(name)}Namelist(Namelist):",
            INDENT + '"""' + f"Pydantic model for the `{name}` namelist." + '"""',
        ]
        + [""]
        + [(INDENT + row) if row else "" for v in validators for row in v]
        + fields
        + ["", ""]
    )


def _format_field(
    name: str,
    type_str: str,
    default_str: str,
    json_schema_extra: dict[str, Any] | None,
    description: str,
) -> str:
    r"""Render a ``name: Type = Field(...)`` line, wrapping to satisfy ruff format.

    The returned string is *pre-indented* with the 4-space class-body indent on
    every line (including continuations), so ``_generate_namelist`` should
    embed it verbatim rather than re-prefix ``INDENT``.

    Wrapping decisions follow ruff's preference order:

    1. ``name: Type = Field(arg1, arg2)`` (single line).
    2. ``name: Type = Field(\n    args,\n)`` (opener intact, args wrapped) —
       only attempted when ``name: Type = Field(`` itself fits in 100 cols.
    3. ``name: Type = (\n    Field(\n        args,\n    )\n)`` (parens-wrap
       around ``Field(...)``) — used when the opener with ``Field(`` overflows
       but ``name: Type = (`` still fits.
    4. ``name: Type[\n    parts,\n] = Field(args)`` (subscript wrapping) —
       fallback for long subscripts (``Literal[...]``, ``Annotated[...]``).
    5. ``name: (\n    A | B | None\n) = Field(args)`` (union wrapping) —
       fallback for long ``|``-joined unions with no subscript head.
    """
    rendered = _render_field(name, type_str, default_str, json_schema_extra, description)
    return _maybe_append_noqa_n815(rendered, name)


def _render_field(
    name: str,
    type_str: str,
    default_str: str,
    json_schema_extra: dict[str, Any] | None,
    description: str,
) -> str:
    """Render a ``name: Type = Field(...)`` declaration (no noqa post-processing)."""
    description_arg = f'description="{description}"'

    def _build_args(
        json_extra_indent: int,
        trailing_comma: bool = False,
        description_indent: int | None = None,
    ) -> list[str]:
        args = [default_str]
        if json_schema_extra is not None:
            args.append(
                _format_json_schema_extra(
                    json_schema_extra,
                    line_indent=json_extra_indent,
                    trailing_comma=trailing_comma,
                )
            )
        if description_indent is not None:
            args.append(_format_description(description, description_indent, trailing_comma))
        else:
            args.append(description_arg)
        return args

    # 1) Single-line form: everything at INDENT (4 cols).
    single_args = _build_args(json_extra_indent=len(INDENT))
    single_line = f"{name}: {type_str} = Field({', '.join(single_args)})"
    if len(INDENT) + len(single_line) <= 100:
        return INDENT + single_line

    opener_field = INDENT + f"{name}: {type_str} = Field("
    inner_indent = len(INDENT) + 4
    inner_args = _build_args(
        json_extra_indent=inner_indent,
        trailing_comma=True,
        description_indent=inner_indent,
    )

    # 2) Args-wrapping with the opener kept intact.
    if len(opener_field) <= 100:
        return _render_args_block(opener_field, inner_args, inner_indent)

    # 3) Parens-wrap around the entire ``Field(...)`` call.
    opener_paren = INDENT + f"{name}: {type_str} = ("
    if len(opener_paren) <= 100 and "\n" not in type_str:
        return _render_paren_wrapped_field(
            name, type_str, json_schema_extra, single_args, description
        )

    # 4) Wrap the type's subscript (Literal[...], Annotated[...]).
    wrapped_header = _format_field_header(name, type_str)
    if wrapped_header is not None:
        return _finish_wrapped_header(wrapped_header, single_args, inner_args, inner_indent)

    # 5) Wrap a union type with explicit parens.
    union_header = _format_union_header(name, type_str)
    if union_header is not None:
        return _finish_wrapped_header(union_header, single_args, inner_args, inner_indent)

    # No wrapping strategy applies — fall back to the long opener.
    return _render_args_block(opener_field, inner_args, inner_indent)


def _finish_wrapped_header(
    header: str, single_args: list[str], inner_args: list[str], inner_indent: int
) -> str:
    """Append args inline or wrap them in a block after a multi-line type header."""
    last_line = header.rsplit("\n", 1)[-1]
    args_inline = ", ".join(single_args)
    if len(last_line) + len(args_inline) + 1 <= 100:
        return header + args_inline + ")"
    return _render_args_block(header, inner_args, inner_indent)


def _render_args_block(opener: str, inner_args: list[str], inner_indent: int) -> str:
    r"""Render ``opener\n    args\n)`` with single-line args if they fit."""
    one_line_args = " " * inner_indent + ", ".join(inner_args)
    if len(one_line_args) <= 100 and "\n" not in one_line_args:
        return "\n".join([opener, one_line_args, INDENT + ")"])
    args_block = "\n".join(_format_arg_line(arg, inner_indent) for arg in inner_args)
    return "\n".join([opener, args_block, INDENT + ")"])


def _format_arg_line(arg: str, indent: int) -> str:
    """Format a single arg into a line (or block of lines) ending with a comma.

    Single-line args are indented and have a trailing comma. Multi-line args
    (their text already contains newlines, e.g. a wrapped description) have
    the first line indented and the trailing comma appended to the final line.
    """
    pad = " " * indent
    if "\n" not in arg:
        return f"{pad}{arg},"
    return pad + arg + ","


def _render_paren_wrapped_field(
    name: str,
    type_str: str,
    json_schema_extra: dict[str, Any] | None,
    single_args: list[str],
    description: str,
) -> str:
    r"""Render ``name: Type = (\n    Field(...)\n)`` with appropriate inner wrapping.

    ``single_args`` is the list of arguments rendered for the single-line
    (untrailing-comma) form, used when ``Field(args)`` fits on one inner line.
    """
    inner_field_indent = len(INDENT) + 4  # 8: indent of ``Field(``
    arg_indent = inner_field_indent + 4  # 12: indent of args inside ``Field(``

    # Try ``Field(args)`` on a single inner line.
    field_inline = "Field(" + ", ".join(single_args) + ")"
    if inner_field_indent + len(field_inline) <= 100 and "\n" not in field_inline:
        return "\n".join(
            [
                INDENT + f"{name}: {type_str} = (",
                " " * inner_field_indent + field_inline,
                INDENT + ")",
            ]
        )

    # Multi-line ``Field(...)`` with one arg per line. Re-render the
    # ``json_schema_extra`` payload at the deeper indent so its closing brace
    # aligns with the surrounding args.
    inner_args: list[str] = [single_args[0]]
    if json_schema_extra is not None:
        inner_args.append(
            _format_json_schema_extra(
                json_schema_extra, line_indent=arg_indent, trailing_comma=True
            )
        )
    inner_args.append(_format_description(description, arg_indent, trailing_comma=True))
    args_block = "\n".join(_format_arg_line(arg, arg_indent) for arg in inner_args)
    return "\n".join(
        [
            INDENT + f"{name}: {type_str} = (",
            " " * inner_field_indent + "Field(",
            args_block,
            " " * inner_field_indent + ")",
            INDENT + ")",
        ]
    )


def _format_union_header(name: str, type_str: str) -> str | None:
    r"""Render the ``name: (\n    A\n    | B\n) = Field(`` opener for a union type.

    Returns ``None`` if ``type_str`` is not a top-level ``|``-union.
    """
    parts = _split_union(type_str)
    if len(parts) < 2:
        return None
    inner_indent = len(INDENT) + 4
    lines = [INDENT + f"{name}: ("]
    lines.append(" " * inner_indent + parts[0])
    for part in parts[1:]:
        lines.append(" " * inner_indent + "| " + part)
    lines.append(INDENT + ") = Field(")
    return "\n".join(lines)


def _split_union(text: str) -> list[str]:
    """Split a type expression on top-level ``|`` operators."""
    parts: list[str] = []
    depth = 0
    buf = ""
    i = 0
    while i < len(text):
        ch = text[i]
        if ch in "([{":
            depth += 1
            buf += ch
        elif ch in ")]}":
            depth -= 1
            buf += ch
        elif ch == "|" and depth == 0:
            parts.append(buf.strip())
            buf = ""
        else:
            buf += ch
        i += 1
    if buf.strip():
        parts.append(buf.strip())
    return parts


def _format_simple_field(name: str, type_str: str, field_call: str) -> str:
    """Render a ``name: Type = Field(...)`` line for non-``<var>`` fields.

    ``field_call`` is the already-rendered ``Field(...)`` call (or any other
    right-hand-side expression). Wrapping mirrors ``_format_field`` but does
    not need to introspect arguments — only the type / overall length.
    """
    single = f"{name}: {type_str} = {field_call}"
    if len(INDENT) + len(single) <= 100:
        return INDENT + single

    # Try wrapping just the Field(...) arguments, if the call starts with ``Field(``.
    inner_indent = len(INDENT) + 4
    if field_call.startswith("Field(") and field_call.endswith(")"):
        inner = field_call[len("Field(") : -1]
        opener_field = INDENT + f"{name}: {type_str} = Field("
        if len(opener_field) <= 100:
            wrapped_inner = " " * inner_indent + inner
            if len(wrapped_inner) <= 100 and "\n" not in wrapped_inner:
                return "\n".join([opener_field, wrapped_inner, INDENT + ")"])

    # Parens-wrap the whole call.
    opener_paren = INDENT + f"{name}: {type_str} = ("
    if len(opener_paren) <= 100 and "\n" not in type_str:
        return "\n".join(
            [
                opener_paren,
                " " * inner_indent + field_call,
                INDENT + ")",
            ]
        )

    # Wrap a union type.
    union_header = _format_union_header(name, type_str)
    if union_header is not None:
        # ``_format_union_header`` ends with ``) = Field(``; we need to swap
        # that tail for ``) = field_call``.
        body = union_header.rsplit("\n", 1)[0]
        return body + "\n" + INDENT + f") = {field_call}"

    return INDENT + single


def _format_field_header(name: str, type_str: str, args_inline: bool = False) -> str | None:
    """Render the ``name: Type = Field(`` opener with a wrapped type subscript.

    Returns ``None`` if the type has no subscript brackets to wrap (caller
    should fall back to the unwrapped single-line opener). When ``args_inline``
    is ``True`` the returned string ends with ``Field(`` on the last line with
    no trailing newline, so that arguments can be appended on the same line.
    Otherwise the returned string ends with ``Field(`` on its own line, ready
    for a newline-joined args block.
    """
    open_idx = type_str.find("[")
    if open_idx == -1 or not type_str.endswith("]"):
        return None
    head = type_str[: open_idx + 1]  # e.g. ``Literal[``
    body = type_str[open_idx + 1 : -1]
    parts = _split_top_level(body)
    inner_indent = len(INDENT) + 4
    joined = ", ".join(parts)
    if inner_indent + len(joined) <= 100:
        body_block = " " * inner_indent + joined
    else:
        body_block = "\n".join(f"{' ' * inner_indent}{p}," for p in parts)
    return "\n".join([INDENT + f"{name}: {head}", body_block, INDENT + "] = Field("])


def _maybe_append_noqa_n815(field_text: str, name: str) -> str:
    """Append ``# noqa: N815`` to the assignment line when ``name`` isn't snake_case.

    The assignment line is always the first line of ``field_text`` (it contains
    ``name: Type = ...``). For multi-line declarations the noqa lives on that
    first line so ruff sees it where the symbol is defined.
    """
    if not _MIXED_CASE_RE.match(name):
        return field_text
    lines = field_text.split("\n", 1)
    lines[0] = lines[0] + "  # noqa: N815"
    return "\n".join(lines)


def _format_description(text: str, indent: int, trailing_comma: bool) -> str:
    r"""Render the ``description=...`` argument, wrapping long strings.

    When the single-line form ``description="text"`` fits within ``_MAX_LINE_LEN``
    at column ``indent`` (allowing one column for a trailing comma if requested),
    it is returned as-is. Otherwise the text is emitted as a
    ``textwrap.dedent``-wrapped triple-quoted string. The leading ``\`` after
    the opening triple-quote swallows the first newline and there is no trailing
    newline before the closing triple-quote, so the runtime string starts and
    ends on a content character. ``dedent()`` strips the uniform indent applied
    to every line at runtime.

    Real newlines in ``text`` are treated as logical-line boundaries. Each
    logical line is hard-wrapped at word boundaries within the per-line content
    budget; bullet lines (those beginning with ``"- "``) carry a 2-space hanging
    indent on any continuation lines.
    """
    if "\n" not in text:
        single = f'description="{text}"'
        budget = _MAX_LINE_LEN - (1 if trailing_comma else 0)
        if indent + len(single) <= budget:
            return single

    content_indent = indent + 4
    content_budget = _MAX_LINE_LEN - content_indent
    if content_budget < 10:
        # Pathological case (very deep nesting); fall back to single line.
        return f'description="{text}"'

    logical_lines = text.split("\n")
    rendered_lines: list[str] = []
    for line in logical_lines:
        hanging = "  " if line.startswith("- ") else ""
        rendered_lines.extend(_wrap_logical_line(line, content_budget, hanging))

    # The closing ``"""`` is appended directly to the last rendered line, so it
    # contributes 3 extra source columns. If the last line would exceed the
    # line-length limit once the closing triple-quote is attached, re-wrap with
    # a tightened budget on the last logical line.
    if rendered_lines and len(rendered_lines[-1]) > content_budget - 3:
        last_hanging = "  " if logical_lines[-1].startswith("- ") else ""
        # Drop the previously-rendered wrap of the final logical line and redo
        # it with a content budget that reserves 3 cols for the closing quote.
        # The simplest way to identify "lines belonging to the final logical
        # line" is to re-wrap *just* that logical line with the tightened
        # budget. The earlier lines were unaffected by the tightening because
        # each logical line is wrapped independently.
        final_lines = _wrap_logical_line(logical_lines[-1], content_budget - 3, last_hanging)
        # Remove the lines that originally came from the final logical line.
        original_final_count = len(
            _wrap_logical_line(logical_lines[-1], content_budget, last_hanging)
        )
        rendered_lines = rendered_lines[:-original_final_count] + final_lines

    pad = " " * content_indent
    close_pad = " " * indent
    body = "\n".join(pad + rendered for rendered in rendered_lines)
    return "description=dedent(\n" + pad + '"""\\\n' + body + '"""\n' + close_pad + ")"


def _wrap_logical_line(text: str, content_budget: int, hanging: str) -> list[str]:
    """Hard-wrap ``text`` at word boundaries to fit ``content_budget`` per line.

    Continuation lines (caused by wrapping a single logical line) are prefixed
    with ``hanging`` so bullet bodies stay visually aligned in IDE tooltips.
    Returns a list of rendered content lines (no trailing newline, no leading
    indent — the caller pads each line to the desired column).
    """
    if not text:
        return [""]
    words = text.split(" ")
    if len(words) == 1:
        return [text]
    tokens = [w + " " for w in words[:-1]] + [words[-1]]
    lines: list[str] = []
    current = ""
    for token in tokens:
        if not current:
            current = token
            continue
        if len(current) + len(token) <= content_budget:
            current += token
        else:
            lines.append(current.rstrip(" "))
            current = hanging + token
    if current:
        lines.append(current.rstrip(" "))
    return lines


def _wrap_string_literal(text: str, max_chunk_len: int) -> list[str]:
    r"""Split ``text`` at word boundaries into chunks of at most ``max_chunk_len`` chars.

    Trailing spaces are preserved on all but the final chunk so that adjacent
    string-literal concatenation in the emitted Python reproduces the original
    text exactly. Words longer than ``max_chunk_len`` are emitted as their own
    (over-budget) chunk — the wrapped form will still satisfy ruff's E501 in
    nearly all real cases since such tokens are rare in QE descriptions.

    The text is treated as already-escaped (``\\"`` and ``\\\\`` sequences are
    counted as multi-character substrings but never split). The chunk-length
    metric measures the *visible* characters as they will appear inside the
    quoted literal (including the backslashes from any escape).
    """
    if not text:
        return [""]

    # Split on single spaces while preserving the separator on the previous word
    # (so concatenation reproduces the original string verbatim).
    words = text.split(" ")
    if len(words) == 1:
        return [text]

    # Re-attach the trailing space to every word except the last.
    tokens = [w + " " for w in words[:-1]] + [words[-1]]

    chunks: list[str] = []
    current = ""
    for token in tokens:
        # Avoid splitting inside an escape sequence: tokens already preserve
        # ``\\"`` and ``\\\\`` as contiguous substrings because we only split
        # on spaces.
        if not current:
            current = token
            continue
        if len(current) + len(token) <= max_chunk_len:
            current += token
        else:
            chunks.append(current)
            current = token
    if current:
        chunks.append(current)
    return chunks


def _split_top_level(text: str) -> list[str]:
    """Split ``text`` on commas that are not nested inside brackets/parens/braces."""
    parts: list[str] = []
    depth = 0
    buf = ""
    for ch in text:
        if ch in "([{":
            depth += 1
            buf += ch
        elif ch in ")]}":
            depth -= 1
            buf += ch
        elif ch == "," and depth == 0:
            parts.append(buf.strip())
            buf = ""
        else:
            buf += ch
    if buf.strip():
        parts.append(buf.strip())
    return parts


# ---------------------------------------------------------------------------
# Variable / dimension parsing
# ---------------------------------------------------------------------------


def _resolve_var_type_and_default(
    name: str,
    var: Element,
    python_type: type,
    options: Element | None,
    default: Element | None,
    in_choose_branch: bool = False,
) -> tuple[str, str, str, dict[str, Any] | None, list[str]]:
    """Resolve the annotation, default literal, and extra kwargs for a ``<var>``.

    Returns ``(name, type_str, default_str, json_schema_extra, validator)``
    where ``name`` may be rewritten (e.g. ``keyword(i)`` -> ``keyword``).
    """
    type_str, validator, alias_map = _get_type_str(name, python_type, options)

    if "(" in name:
        # keyword(i) notation: emit a list with no static default
        name = name.split("(")[0]
        type_str = f"list[{type_str}]"
        default_str = "None"
        extra_payload: dict[str, Any] | None = None
    else:
        default_str, extra_payload = _get_default(name, python_type, default)
        # If the literal default matches an alias, canonicalize it so that the
        # default itself is a valid member of the emitted ``Literal[...]``.
        if alias_map and extra_payload is None and default_str.startswith('"'):
            unquoted = default_str.strip('"')
            if unquoted in alias_map:
                default_str = '"' + alias_map[unquoted] + '"'

    # ``<status>REQUIRED</status>`` on a <var> with no <default>, OR a <var>
    # inside a <choose> branch with no <default> (the upstream convention for
    # branches that document themselves as REQUIRED): emit a pydantic required
    # field (``Field(...)``) rather than ``Field(None, ...)``, and keep the
    # type narrow (no ``| None`` / ``Literal[None, ...]`` widening).
    if default_str == "None" and _var_is_required(var, in_choose_branch=in_choose_branch):
        return name, type_str, "...", extra_payload, validator

    # If the default is None we need to widen the type accordingly.
    if default_str == "None":
        if options is None:
            type_str += " | None"
        elif "None" not in type_str:
            type_str = type_str.replace("Literal[", "Literal[None, ")

    return name, type_str, default_str, extra_payload, validator


def _parse_var(var: Element, in_choose_branch: bool = False) -> tuple[str | None, list[str], bool]:
    """Parse a ``<var>`` element into a ``name: type = Field(...)`` line.

    Returns the field-definition string (or ``None`` to skip the var), an
    optional ``@field_validator`` block, and a flag indicating whether a
    ``Quantity`` annotation was used (so we know whether to import it).
    """
    name = var.attrib["name"]
    description_element = var.find("info")
    python_type = _get_var_type(name, var)
    if python_type is None:
        # STRUCTURE-typed vars have no atomic pydantic representation.
        return None, [], False

    # Pydantic does not support float literals
    options = None if python_type is float else var.find("options")
    default = var.find("default")

    description = _get_var_description(name, description_element, options)
    if description in ["OBSOLETE - NO LONGER IMPLEMENTED"]:
        return None, [], False

    name, type_str, default_str, extra_payload, validator = _resolve_var_type_and_default(
        name, var, python_type, options, default, in_choose_branch=in_choose_branch
    )

    # Wrap with Annotated[..., Quantity(...)] iff both units and dimensionality exist
    # and are simple literal strings (not conditional, which only occurs in cards).
    quantity_str = _build_quantity(var)
    uses_quantity = quantity_str is not None
    if quantity_str is not None:
        type_str = f"Annotated[{type_str}, {quantity_str}]"

    if name == "lambda":
        name = "Lambda"

    return (
        _format_field(name, type_str, default_str, extra_payload, description),
        validator,
        uses_quantity,
    )


def _resolve_dimension_default(
    name: str,
    dim: Element,
    python_type: type,
    length: int | None,
    type_str: str,
    in_choose_branch: bool,
) -> tuple[str, str, dict[str, Any] | None]:
    """Return ``(default_str, type_str, extra_payload)`` for a dimension's default.

    Handles list-style defaults like ``[0.0, 0.0, 0.0]``, scalar defaults
    broadcast across the tuple, the REQUIRED-without-default case, and the
    fallback ``| None`` widening.
    """
    default = dim.find("default")
    list_default = _maybe_list_default(default, python_type)
    extra_payload: dict[str, Any] | None
    if list_default is not None:
        if length is not None and list_default.startswith("["):
            default_str = "(" + list_default[1:-1] + ")"
        else:
            default_str = list_default
        extra_payload = None
    else:
        default_str, extra_payload = _get_default(name, python_type, default)

    if default_str == "None" and _var_is_required(dim, in_choose_branch=in_choose_branch):
        # REQUIRED dimension with no default: emit a pydantic required field
        # without widening the annotation with ``| None``.
        return "...", type_str, extra_payload
    if default_str == "None":
        return default_str, type_str + " | None", extra_payload
    if list_default is not None:
        return default_str, type_str, extra_payload
    if length is not None and extra_payload is None:
        return f"({', '.join([default_str for _ in range(length)])})", type_str, extra_payload
    if length is None and extra_payload is None:
        return "default_factory=list", type_str, extra_payload
    return default_str, type_str, extra_payload


def _parse_dimension(dim: Element, in_choose_branch: bool = False) -> tuple[str | None, bool]:
    """Parse a ``<dimension>`` element into a field-definition string."""
    name = dim.attrib["name"]
    python_type = _get_var_type(name, dim)
    if python_type is None:
        return None, False
    start = dim.attrib["start"]
    end = dim.attrib["end"]
    description = _get_var_description(name, dim.find("info"), None)
    length: int | None
    try:
        tuple_length = int(end) - int(start) + 1
        length = tuple_length
        type_str = "tuple[" + ", ".join([python_type.__name__ for _ in range(tuple_length)]) + "]"
    except ValueError:
        length = None
        type_str = f"list[{python_type.__name__}]"
        description += f" (start = {start}, end = {end})"

    default_str, type_str, extra_payload = _resolve_dimension_default(
        name, dim, python_type, length, type_str, in_choose_branch
    )

    quantity_str = _build_quantity(dim)
    uses_quantity = quantity_str is not None
    if quantity_str is not None:
        type_str = f"Annotated[{type_str}, {quantity_str}]"

    return (
        _format_field(name, type_str, default_str, extra_payload, description.strip()),
        uses_quantity,
    )


def _get_var_type(name: str, var: Element) -> type | None:
    """Map an XML ``type=`` attribute to a python type.

    Returns ``None`` for ``type="STRUCTURE"`` — a meta-type used in QE's schema
    for variables that are records with sub-fields documented only in prose
    (e.g. ``dvscf_star%open``). Those aren't representable as a single pydantic
    field, so callers should skip them.
    """
    xml_type_str = var.attrib.get("type", None)
    if xml_type_str is None:
        name = var.attrib["name"]
        raise InvalidXMLStructureError(f"`{name}` is missing the `type` field.")
    if xml_type_str == "STRUCTURE":
        return None
    python_type = type_mapping[xml_type_str]
    if name in ["pseudo_dir", "outdir", "wfcdir", "atom_proj_dir"]:
        python_type = Path
    return python_type


def _get_var_description(
    name: str, description_element: Element | None, options: Element | None
) -> str:
    """Collect the description text for a variable.

    Walks the ``<info>`` element so that any ``<ref>`` children (which we keep
    intact at parse time) are flattened back into plain text. Per-``<opt>``
    descriptions are emitted as a newline-separated bullet list so the rendered
    text is readable in IDE tooltips and ``help()``. Real newlines are
    preserved in the returned string; ``_format_description`` is responsible
    for deciding how those newlines surface in the emitted python source.
    """
    prose = _collect_prose(name, description_element, options)
    opt_items = _collect_opt_items(options)

    description = prose
    if opt_items:
        if description:
            description += "\n"
        description += "\n".join(opt_items)

    return description


def _collect_prose(name: str, description_element: Element | None, options: Element | None) -> str:
    """Concatenate the ``<info>`` text plus any ``<options><info>`` text."""
    prose = _element_text(description_element)
    if options is not None:
        for info in options.findall("info"):
            text = _element_text(info)
            if not text and info.text is None:
                raise InvalidXMLStructureError(f"Missing text in <info> field for `{name}`.")
            prose += text
    return _normalize_prose(prose)


def _collect_opt_items(options: Element | None) -> list[str]:
    """Build the per-``<opt>`` bullet list for the description text."""
    opt_items: list[str] = []
    if options is None:
        return opt_items
    for opt in options.findall("opt"):
        opt_text = _element_text(opt).strip()
        if not opt_text:
            continue
        val = opt.attrib.get("val", "").strip().strip("'\"")
        if not val:
            continue
        opt_text_normalized = _normalize_prose(opt_text)
        if not opt_text_normalized:
            continue
        if not opt_text_normalized.endswith((".", "!", "?")):
            opt_text_normalized += "."
        opt_items.append(f"- '{val}': {opt_text_normalized}")
    return opt_items


def _normalize_prose(text: str) -> str:
    """Collapse whitespace and strip LaTeX-style backslash sigils from prose text."""
    collapsed = " ".join(
        line.strip() for line in text.strip(" \n'" + '"').replace('"', "'").split("\n")
    )
    # Drop the backslash from any ``\<letter>`` sequence so the emitted string
    # literal doesn't trip ruff's invalid-escape-sequence rule (W605). Done
    # before any newline escaping below so we don't strip our own ``\n``s.
    return re.sub(r"\\([A-Za-z])", r"\1", collapsed)


def _element_text(element: Element | None) -> str:
    """Return the concatenated text content of ``element`` (including ``<ref>`` children)."""
    if element is None:
        return ""
    return "".join(element.itertext())


def _var_is_required(var: Element, in_choose_branch: bool = False) -> bool:
    """Return True if the ``<var>`` / ``<dimension>`` element should be REQUIRED.

    A var/dimension is REQUIRED if either:

    * it carries an explicit ``<status>REQUIRED</status>`` child, or
    * ``in_choose_branch`` is ``True`` and it has no ``<default>`` child. Inside
      a ``<when>``/``<elsewhen>``/``<otherwise>`` branch the upstream convention
      (see PP's "drop misleading defaults from REQUIRED entries" commit) is
      that the absence of a ``<default>`` element is the structural signal that
      the value must be supplied by the user for that branch.
    """
    status = var.find("status")
    if status is not None and (status.text or "").strip().upper() == "REQUIRED":
        return True
    if in_choose_branch and var.find("default") is None:
        return True
    return False


# ---------------------------------------------------------------------------
# Type / options
# ---------------------------------------------------------------------------


def _get_type_str(
    name: str, python_type: type, options: Element | None
) -> tuple[str, list[str], dict[str, str]]:
    """Determine the python annotation string, validator lines, and alias mapping."""
    if options is not None:
        type_str, mapping = _get_options_str_and_mapping(options, python_type)
    else:
        type_str = python_type.__name__
        mapping = {}

    validator = _get_validator(name, mapping, python_type)
    return type_str, validator, mapping


def _get_validator(name: str, mapping: dict[str, str], python_type: type) -> list[str]:
    """Generate an ``@field_validator`` block that maps aliases onto canonical values."""
    if not mapping:
        return []
    # The method body sits at one class-body INDENT plus one function-body INDENT
    # (`_generate_namelist` prepends a class-body INDENT to each row). Render the
    # mapping dict so any wrapped continuation lines / closing brace land at the
    # method-body column.
    body_indent = 2 * len(INDENT)
    mapping_prefix = "mapping = "
    mapping_str = _py_literal(
        mapping, start_col=body_indent + len(mapping_prefix), line_indent=body_indent
    )
    mapping_line = INDENT + mapping_prefix + mapping_str
    docstring = INDENT + f'"""Map equivalent values for `{name}` onto a canonical value."""'
    return [
        f'@field_validator("{name}", mode="before")',
        "@classmethod",
        f"def map_{name}(cls, v: {python_type.__name__}) -> {python_type.__name__}:",
        docstring,
        mapping_line,
        INDENT + "return mapping.get(v, v)",
        "",
    ]


def _get_options_str_and_mapping(options: Element, python_type: type) -> tuple[str, dict[str, str]]:
    """Build the ``Literal[...]`` annotation and the alias-to-canonical mapping."""
    options_list: list[str] = []
    mapping: dict[str, str] = {}
    for opt in options.findall("opt"):
        val = opt.attrib["val"]
        canonical = _format_literal(val, python_type)
        options_list.append(canonical)

        alias_attr = opt.attrib.get("alias")
        if alias_attr:
            # Aliases are quoted, comma-separated, e.g. "'medium', 'debug'"
            for raw_alias in _split_alias_attr(alias_attr):
                alias_formatted = _format_literal(raw_alias, python_type)
                # The mapping keys/values are stored as bare strings (the validator
                # quotes them via the mapping dict literal), matching the historical
                # convention used in _get_validator.
                mapping[alias_formatted.strip('"')] = canonical.strip('"')

    return "Literal[" + ", ".join(options_list) + "]", mapping


def _split_alias_attr(alias_attr: str) -> list[str]:
    """Split a comma-separated, possibly quoted, ``alias`` attribute into entries."""
    parts: list[str] = []
    buf = ""
    in_quote = False
    for ch in alias_attr:
        if ch == "'":
            in_quote = not in_quote
            buf += ch
        elif ch == "," and not in_quote:
            if buf.strip():
                parts.append(buf.strip())
            buf = ""
        else:
            buf += ch
    if buf.strip():
        parts.append(buf.strip())
    return parts


def _format_literal(raw: str, python_type: type) -> str:
    """Format an option value or alias for use inside a ``Literal[...]``."""
    text = raw.strip()
    if python_type is str:
        # Strip surrounding single-quotes (the schema wraps strings in apostrophes).
        if text.startswith("'") and text.endswith("'"):
            text = text[1:-1]
        return '"' + text + '"'
    # Numeric literals (int/float) are passed through as-is.
    return text


# ---------------------------------------------------------------------------
# Default-value parsing
# ---------------------------------------------------------------------------


def _get_default(
    name: str, python_type: type, default: Element | None
) -> tuple[str, dict[str, Any] | None]:
    """Return ``(default_str, json_schema_extra_payload)`` for a variable's default.

    ``default_str`` is either a python literal (e.g. ``"0.5"``, ``'"scf"'``,
    ``"True"``), the sentinel ``"None"``, or a ``default_factory=list`` kwarg.
    The payload, when not ``None``, is rendered later as
    ``json_schema_extra={...}`` (the rendering is deferred so that the caller
    can decide on indentation).
    """
    if default is None:
        return "None", None

    kind = default.attrib.get("kind")
    if kind is None:
        # Literal default: read just the element's own text (children, if any, are
        # whitespace or stray markup we don't care about).
        text = (default.text or "").strip()
        return _literal_default(text, python_type), None

    if kind == "conditional":
        cases = []
        for case in default.findall("case"):
            value_text = _element_text(case).strip()
            when = case.attrib.get("test")
            if when is not None:
                when = _strip_ref_prefix(when)
            cases.append({"when": when, "value": value_text})
        return "None", {"conditional_default": cases}

    if kind == "ref":
        ref_element = default.find("ref")
        ref_name = (ref_element.text or "").strip() if ref_element is not None else ""
        return "None", {"default_ref": ref_name}

    if kind == "computed":
        return "None", {"computed_default": True}

    if kind == "expr":
        expr_text = _element_text(default).strip()
        return "None", {"default_expr": expr_text}

    warnings.warn(
        f"Unknown <default kind={kind!r}> for `{name}`; falling back to None.", stacklevel=2
    )
    return "None", None


def _strip_ref_prefix(test: str) -> str:
    """Strip ``@ref`` tokens from a TCL-style conditional test expression."""
    # ``@ref calculation=='scf'`` -> ``calculation=='scf'``
    return " ".join(word for word in test.split() if word != "@ref")


def _format_json_schema_extra(
    payload: dict[str, Any], line_indent: int = 0, trailing_comma: bool = False
) -> str:
    """Render ``json_schema_extra={...}`` with line-aware wrapping.

    ``line_indent`` is the column at which the current line begins (i.e. the
    column at which ``json_schema_extra=`` is written); used both for the
    inline-fit check and for aligning the closing brace of any wrapped dict.
    When ``trailing_comma`` is set, the inline-fit check reserves one column
    for the comma that the caller will append, matching ``ruff format``'s
    behaviour for arguments in a multi-line ``Field(...)`` call.
    """
    prefix = "json_schema_extra="
    start_col = line_indent + len(prefix)
    return prefix + _py_literal(
        payload,
        start_col=start_col,
        line_indent=line_indent,
        trailing_comma=trailing_comma,
    )


def _py_literal(
    value: object, start_col: int = 0, line_indent: int = 0, trailing_comma: bool = False
) -> str:
    """Render a JSON-ish python value (dict/list/str/None/bool) as a python literal.

    ``start_col`` is the column at which the value's first character will be
    placed (used to test whether the inline form fits in the 100-char limit).
    ``line_indent`` is the indentation of the line on which this value starts;
    it determines the column at which a wrapped closing brace is aligned, to
    match ruff's formatting style. Inner items get indented one level
    (``line_indent + 4``) past the line indent.
    """
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str):
        return _py_literal_str(value, start_col, line_indent, trailing_comma)
    if isinstance(value, list):
        return _py_literal_list(value, start_col, line_indent, trailing_comma)
    if isinstance(value, dict):
        return _py_literal_dict(value, start_col, line_indent, trailing_comma)
    raise TypeError(f"Cannot render {type(value).__name__} as a python literal: {value!r}")


def _py_literal_str(
    value: str, start_col: int = 0, line_indent: int = 0, trailing_comma: bool = False
) -> str:
    """Render a python string literal, mirroring ``ruff format``'s quote selection.

    When ``start_col + len(literal)`` exceeds the line-length budget, the string
    is wrapped using adjacent-string-literal concatenation inside parentheses,
    matching the same approach used for long descriptions.
    """
    # Prefer double quotes, but switch to single quotes when the value contains
    # a double quote and no single quote (avoiding pointless escapes).
    if '"' in value and "'" not in value:
        quote = "'"
        body = value.replace("\\", "\\\\")
    else:
        quote = '"'
        body = value.replace("\\", "\\\\").replace('"', '\\"')
    literal = quote + body + quote

    budget = _MAX_LINE_LEN - (1 if trailing_comma else 0)
    if start_col + len(literal) <= budget:
        return literal

    inner_indent = line_indent + 4
    chunk_budget = _MAX_LINE_LEN - inner_indent - 2  # 2 for surrounding quotes
    if chunk_budget < 10:
        return literal

    chunks = _wrap_string_literal(body, chunk_budget)
    pad = " " * inner_indent
    close_pad = " " * line_indent
    body_lines = "\n".join(f"{pad}{quote}{chunk}{quote}" for chunk in chunks)
    return "(\n" + body_lines + "\n" + close_pad + ")"


def _py_literal_list(
    value: list[Any], start_col: int, line_indent: int, trailing_comma: bool
) -> str:
    """Render a python list literal, wrapping if needed to satisfy the 100-char limit."""
    inline = "[" + ", ".join(_py_literal(v) for v in value) + "]"
    budget = 100 - (1 if trailing_comma else 0)
    if start_col + len(inline) <= budget or not value:
        return inline
    inner_indent = line_indent + 4
    pad = " " * inner_indent
    close_pad = " " * line_indent
    items = ",\n".join(
        pad + _py_literal(v, start_col=inner_indent, line_indent=inner_indent, trailing_comma=True)
        for v in value
    )
    return "[\n" + items + ",\n" + close_pad + "]"


def _py_literal_dict(
    value: dict[str, Any], start_col: int, line_indent: int, trailing_comma: bool
) -> str:
    """Render a python dict literal, wrapping if needed to satisfy the 100-char limit."""
    inline = "{" + ", ".join(f"{_py_literal(k)}: {_py_literal(v)}" for k, v in value.items()) + "}"
    budget = 100 - (1 if trailing_comma else 0)
    if start_col + len(inline) <= budget or not value:
        return inline
    inner_indent = line_indent + 4
    pad = " " * inner_indent
    close_pad = " " * line_indent
    item_lines: list[str] = []
    for k, v in value.items():
        key_str = _py_literal(k)
        value_str = _py_literal(
            v,
            start_col=inner_indent + len(key_str) + 2,
            line_indent=inner_indent,
            trailing_comma=True,
        )
        item_lines.append(f"{pad}{key_str}: {value_str}")
    items = ",\n".join(item_lines)
    return "{\n" + items + ",\n" + close_pad + "}"


def _maybe_list_default(default: Element | None, python_type: type) -> str | None:
    """Recognize list-literal defaults like ``[0.0, 0.0, 0.0]`` on ``<dimension>``s.

    Returns a python list-literal string if the default text parses as a list of
    values of ``python_type``, else ``None``. Strings are re-quoted with double
    quotes so the emitted literal is valid python.
    """
    if default is None or default.attrib.get("kind") is not None:
        return None
    text = (default.text or "").strip()
    if not (text.startswith("[") and text.endswith("]")):
        return None
    body = text[1:-1].strip()
    if not body:
        return None
    pieces = [p.strip() for p in body.split(",")]
    formatted: list[str] = []
    for piece in pieces:
        if not piece:
            return None
        if python_type is str:
            # Strip the surrounding single quotes that QE uses in its XML, then
            # re-emit with double quotes to keep the generated python literal
            # ruff-clean.
            stripped = piece.strip("'\"")
            formatted.append(f'"{stripped}"')
        else:
            try:
                python_type(piece)
            except ValueError:
                return None
            formatted.append(piece)
    return "[" + ", ".join(formatted) + "]"


def _literal_default(text: str, python_type: type) -> str:
    """Format a literal default value (no ``kind=`` attribute) as a python expression."""
    text = text.strip(" \n")
    if python_type is bool:
        return _sanitize_bool(text)
    if python_type is Path:
        return _sanitize_path(text)
    if python_type is str:
        return _sanitize_string(text)
    return _sanitize_numeric(text, python_type)


def _sanitize_bool(text: str) -> str:
    lowered = text.lower().strip(".")
    if lowered == "false":
        return "False"
    if lowered == "true":
        return "True"
    return "None"


def _sanitize_path(text: str) -> str:
    return 'Path("' + text + '")'


def _sanitize_string(text: str) -> str:
    text = text.strip()
    if text == "":
        return "None"
    if text.startswith("'") and text.endswith("'"):
        text = text[1:-1]
    elif text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    # Strip whitespace inside the quoted literal (matches the historical behaviour
    # for defaults like ``' '`` or ``'  '``).
    text = text.strip()
    if text == "":
        return "None"
    if '"' in text:
        return "None"
    return '"' + text + '"'


def _sanitize_numeric(text: str, python_type: type) -> str:
    if python_type is float and "d" in text.lower():
        sanitized = text.lower().replace("d", "e")
    elif python_type is float:
        # Ruff format prefers a lowercase ``e`` in scientific notation.
        sanitized = text.replace("E", "e")
    else:
        sanitized = text
    try:
        python_type(sanitized)
    except ValueError:
        warnings.warn(
            f'Failed to convert "{text}" to a {python_type.__name__}; defaulting to None.',
            stacklevel=2,
        )
        return "None"
    if python_type is float:
        # Ruff format prefers ``1.0e-11`` over ``1.e-11``: a bare trailing dot
        # immediately followed by the exponent is rewritten as ``.0e``.
        sanitized = sanitized.replace(".e", ".0e")
        # Ruff format also strips a redundant ``+`` after the exponent
        # (``1.0e+7`` -> ``1.0e7``).
        sanitized = sanitized.replace("e+", "e")
    return sanitized


# ---------------------------------------------------------------------------
# Quantity (units + dimensionality) annotation
# ---------------------------------------------------------------------------


def _build_quantity(element: Element) -> str | None:
    """Return ``"Quantity(units=..., dimensionality=...)"`` if both are present.

    Only literal (non-``kind="conditional"``) ``<units>`` and ``<dimensionality>``
    children are wrapped. In namelist ``<var>``/``<dimension>`` elements the
    schema is always literal; conditional ones only appear inside ``<card>``
    column definitions (which we don't generate code for).
    """
    units_el = element.find("units")
    dim_el = element.find("dimensionality")
    if units_el is None or dim_el is None:
        return None
    if units_el.attrib.get("kind") == "conditional":
        return None
    if dim_el.attrib.get("kind") == "conditional":
        return None
    units = (units_el.text or "").strip()
    dim = (dim_el.text or "").strip()
    if not units or not dim:
        return None
    return f'Quantity(units="{units}", dimensionality="{dim}")'


# ---------------------------------------------------------------------------
# Top-level code generation
# ---------------------------------------------------------------------------


# Mapping of (module, [symbols]) to the substring marker that triggers including
# each symbol. ``None`` means the symbol is always included when the module is.
_CONDITIONAL_IMPORTS: tuple[tuple[str, tuple[tuple[str, str], ...]], ...] = (
    ("pydantic", (("Field", "Field("), ("field_validator", "field_validator("))),
    ("typing", (("Annotated", "Annotated["), ("Literal", "Literal["))),
    (
        "pydantic_espresso.utils",
        (("get_tmp_dir", "get_tmp_dir"), ("get_pseudo_dir", "get_pseudo_dir")),
    ),
)


def _collect_symbols(body: str, symbols: tuple[tuple[str, str], ...]) -> list[str]:
    """Return the subset of ``symbols`` whose marker substring occurs in ``body``."""
    return [name for name, marker in symbols if marker in body]


def _build_import_lines(body: str, extra_imports: set[str], needs_quantity: bool) -> list[str]:
    """Build the conditional import block based on which symbols ``body`` actually uses.

    Imports are grouped by ruff's isort convention (stdlib, third-party,
    first-party) with a blank line between groups.
    """
    stdlib: list[str] = []
    if re.search(r"\bPath\b", body):
        stdlib.append("from pathlib import Path")
    if "dedent(" in body:
        stdlib.append("from textwrap import dedent")
    typing_syms = _collect_symbols(body, _CONDITIONAL_IMPORTS[1][1])
    if typing_syms:
        stdlib.append("from typing import " + ", ".join(typing_syms))

    third_party: list[str] = []
    pydantic_syms = _collect_symbols(body, _CONDITIONAL_IMPORTS[0][1])
    if pydantic_syms:
        third_party.append("from pydantic import " + ", ".join(pydantic_syms))

    first_party: list[str] = ["from pydantic_espresso.models.template import EspressoInput"]
    if re.search(r"\bNamelist\b", body):
        first_party.append("from pydantic_espresso.namelist import Namelist")
    if needs_quantity:
        first_party.append("from pydantic_espresso.quantity import Quantity")
    used_utils = _collect_symbols(body, _CONDITIONAL_IMPORTS[2][1])
    if used_utils:
        first_party.append("from pydantic_espresso.utils import " + ", ".join(used_utils))
    first_party.extend(extra_imports)
    first_party = sorted(first_party)

    groups = [g for g in (stdlib, third_party, first_party) if g]
    result: list[str] = []
    for i, group in enumerate(groups):
        result.extend(group)
        if i < len(groups) - 1:
            result.append("")
    return result


def _generate_model_string(
    executable: str,
    fields: list[str],
    subclasses: list[str],
    imports: set[str],
    version: str,
    needs_quantity: bool = False,
) -> str:
    """Render the whole file: docstring, imports, namelist subclasses, input model."""
    executable_str = executable.upper().replace(".X", "")
    for char in " -_":
        executable_str = executable_str.replace(char, "")

    input_header = [
        f"class {executable_str}EspressoInput(EspressoInput):",
        INDENT + f'"""Pydantic model for the input of `{executable}`."""',
        "",
        "",
    ]

    body = ("\n".join(subclasses + input_header) + "\n".join(fields) + "\n").strip("\n") + "\n"

    import_lines = _build_import_lines(body, imports, needs_quantity=needs_quantity)

    header = (
        '"""'
        + f"""Pydantic model for the input of `{executable.lower()}` version `{version}`.

This file has been generated automatically. Do not edit it manually.
"""
        + '"""'
        + "\n\n"
        + "\n".join(import_lines)
        + "\n\n\n"
    )

    return header + body
