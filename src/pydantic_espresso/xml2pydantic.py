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
    namelist_field_definitions: list[str] = []
    namelist_field_validators: list[list[str]] = []
    uses_quantity = False

    for var in namelist.findall("var"):
        field_definition, field_validator, var_uses_quantity = _parse_var(var)

        if field_definition is None:
            continue
        uses_quantity = uses_quantity or var_uses_quantity

        # Manual fixes for duplicate entries from the historical schema.
        if field_definition.startswith("abivol:") and any(
            x.startswith("abivol:") for x in namelist_field_definitions
        ):
            continue
        if field_definition.startswith("restart:") and any(
            x.startswith("restart:") for x in namelist_field_definitions
        ):
            field_definition = field_definition.replace("restart:", "restart_step:")

        namelist_field_definitions.append(field_definition)

        if field_validator:
            namelist_field_validators.append(field_validator)

    for dim in namelist.findall("dimension"):
        field_definition, dim_uses_quantity = _parse_dimension(dim)
        uses_quantity = uses_quantity or dim_uses_quantity
        namelist_field_definitions.append(field_definition)

    name = namelist.attrib["name"]
    type_name = f"{camel_case(name)}Namelist"
    field_line = _format_simple_field(
        name.lower(),
        type_name,
        f"Field(default_factory=lambda: {type_name}())",
    )
    namelist_block = _generate_namelist(name, namelist_field_definitions, namelist_field_validators)
    return field_line, namelist_block, uses_quantity


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
    it is returned as-is. Otherwise the text is split into space-separated chunks
    and emitted as ``description=(\n    "chunk1 "\n    "chunk2"\n)`` so adjacent
    string-literal concatenation reconstructs the original.
    """
    single = f'description="{text}"'
    budget = _MAX_LINE_LEN - (1 if trailing_comma else 0)
    if indent + len(single) <= budget:
        return single

    inner_indent = indent + 4
    # Each emitted line: ``<inner_indent spaces>"chunk"``. Budget for the bare
    # chunk text (between the quotes) is the remaining columns.
    chunk_budget = _MAX_LINE_LEN - inner_indent - 2  # 2 for the surrounding quotes
    if chunk_budget < 10:
        # Pathological case (very deep nesting); fall back to single line.
        return single

    chunks = _wrap_string_literal(text, chunk_budget)
    pad = " " * inner_indent
    close_pad = " " * indent
    body = "\n".join(f'{pad}"{chunk}"' for chunk in chunks)
    return "description=(\n" + body + "\n" + close_pad + ")"


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

    # If the default is None we need to widen the type accordingly.
    if default_str == "None":
        if options is None:
            type_str += " | None"
        elif "None" not in type_str:
            type_str = type_str.replace("Literal[", "Literal[None, ")

    return name, type_str, default_str, extra_payload, validator


def _parse_var(var: Element) -> tuple[str | None, list[str], bool]:
    """Parse a ``<var>`` element into a ``name: type = Field(...)`` line.

    Returns the field-definition string (or ``None`` to skip the var), an
    optional ``@field_validator`` block, and a flag indicating whether a
    ``Quantity`` annotation was used (so we know whether to import it).
    """
    name = var.attrib["name"]
    description_element = var.find("info")
    python_type = _get_var_type(name, var)

    # Pydantic does not support float literals
    options = None if python_type is float else var.find("options")
    default = var.find("default")

    description = _get_var_description(name, description_element, options)
    if description in ["OBSOLETE - NO LONGER IMPLEMENTED"]:
        return None, [], False

    name, type_str, default_str, extra_payload, validator = _resolve_var_type_and_default(
        name, var, python_type, options, default
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


def _parse_dimension(dim: Element) -> tuple[str, bool]:
    """Parse a ``<dimension>`` element into a field-definition string."""
    name = dim.attrib["name"]
    python_type = _get_var_type(name, dim)
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

    default = dim.find("default")

    # Detect a list-style default like ``[0.0, 0.0, 0.0]`` that already spans the
    # whole dimension. We splice it into a python tuple literal directly without
    # going through the scalar-sanitizer.
    list_default = _maybe_list_default(default, python_type)
    if list_default is not None:
        default_str = list_default
        extra_payload: dict[str, Any] | None = None
    else:
        default_str, extra_payload = _get_default(name, python_type, default)

    if default_str == "None":
        type_str += " | None"
    elif list_default is not None:
        pass  # already a tuple-of-values literal
    elif length is not None and extra_payload is None:
        default_str = f"({', '.join([default_str for _ in range(length)])})"
    elif length is None and extra_payload is None:
        default_str = "default_factory=list"

    quantity_str = _build_quantity(dim)
    uses_quantity = quantity_str is not None
    if quantity_str is not None:
        type_str = f"Annotated[{type_str}, {quantity_str}]"

    return (
        _format_field(name, type_str, default_str, extra_payload, description.strip()),
        uses_quantity,
    )


def _get_var_type(name: str, var: Element) -> type:
    xml_type_str = var.attrib.get("type", None)
    if xml_type_str is None:
        name = var.attrib["name"]
        raise InvalidXMLStructureError(f"`{name}` is missing the `type` field.")
    python_type = type_mapping[xml_type_str]
    if name in ["pseudo_dir", "outdir", "wfcdir", "atom_proj_dir"]:
        python_type = Path
    return python_type


def _get_var_description(
    name: str, description_element: Element | None, options: Element | None
) -> str:
    """Collect the description text for a variable.

    Walks the ``<info>`` element so that any ``<ref>`` children (which we keep
    intact at parse time) are flattened back into plain text.
    """
    description = _element_text(description_element)
    if options is not None:
        for info in options.findall("info"):
            text = _element_text(info)
            if not text and info.text is None:
                raise InvalidXMLStructureError(f"Missing text in <info> field for `{name}`.")
            description += text

    description = " ".join(
        line.strip() for line in description.strip(" \n'" + '"').replace('"', "'").split("\n")
    )
    description = description.replace(r"\p", "p").replace(r"\l", "l")
    return description


def _element_text(element: Element | None) -> str:
    """Return the concatenated text content of ``element`` (including ``<ref>`` children)."""
    if element is None:
        return ""
    return "".join(element.itertext())


# ---------------------------------------------------------------------------
# Type / options
# ---------------------------------------------------------------------------


def _get_type_str(
    name: str, python_type: type, options: Element | None
) -> tuple[str, list[str], dict[str, str]]:
    """Determine the python annotation string, validator lines, and alias mapping."""
    if options is not None:
        type_str, mapping = _get_options_str_and_mapping(options, python_type)
    elif name == "ibrav":
        type_str = (
            "Literal[0, 1, 2, 3, -3, 4, 5, -5, 6, 7, 8, 9, -9, 91, 10, 11, 12, -12, 13, -13, 14]"
        )
        mapping = {}
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
        if name == "ibrav":
            return "0", None
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
        pad + _py_literal(v, start_col=inner_indent, line_indent=inner_indent) for v in value
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

    Returns a python tuple-literal string if the default text parses as a list of
    values of ``python_type``, else ``None``.
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
        try:
            python_type(piece)
        except ValueError:
            return None
        formatted.append(piece)
    return "(" + ", ".join(formatted) + ")"


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
