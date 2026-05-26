"""Tests for the XML-to-Pydantic model generator (``xml2pydantic``)."""

from pathlib import Path

import pytest

# ``xml2pydantic`` is a dev-only tool that depends on ``defusedxml`` (an optional
# ``dev`` extra rather than a runtime/tests dependency). Skip the whole module when
# it is unavailable so the lean ``tests`` environment still passes.
pytest.importorskip("defusedxml")

from defusedxml.ElementTree import fromstring

from pydantic_espresso.xml2pydantic import (
    InvalidXMLStructureError,
    _build_quantity,
    _distribute_list_default,
    _format_description,
    _format_literal,
    _get_default,
    _get_var_type,
    _maybe_list_default,
    _parse_when_test,
    _py_literal,
    _resolve_otherwise_values,
    _sanitize_bool,
    _sanitize_numeric,
    _sanitize_path,
    _sanitize_string,
    _sanitize_value_suffix,
    _split_alias_attr,
    _split_top_level,
    _strip_ref_prefix,
    _variant_class_name,
    _wrap_logical_line,
    camel_case,
    convert_xml_file_to_model,
    convert_xml_tree_to_model,
    sanitize_xml,
)
from pydantic_espresso.xml_files import directory as xml_directory

XML_FILES = sorted((xml_directory / "develop").glob("*.xml"))


def _stem(path: Path) -> str:
    """Return the file stem for use as a parametrize id."""
    return path.stem


# ---------------------------------------------------------------------------
# A. Whole-file generation sweep
# ---------------------------------------------------------------------------


def test_xml_files_discovered() -> None:
    """Sanity check that the develop XML files are discoverable."""
    assert len(XML_FILES) >= 30


@pytest.mark.parametrize("xml_path", XML_FILES, ids=_stem)
def test_convert_xml_file_compiles(xml_path: Path) -> None:
    """Every develop XML file generates non-empty python source that compiles."""
    source, executable = convert_xml_file_to_model(xml_path, version="develop")
    assert source.strip()
    assert executable
    compile(source, str(xml_path), "exec")


@pytest.mark.parametrize("xml_path", XML_FILES, ids=_stem)
def test_generated_lines_within_limit(xml_path: Path) -> None:
    """Generated source respects the 100-column limit (modulo trailing ``# noqa``).

    The committed generated models tolerate the same overflow: ruff's E501 does
    not split a line whose overflow is solely a trailing ``# noqa`` directive, so
    a handful of mixedCase fields exceed 100 columns once the noqa is appended.
    """
    source, _ = convert_xml_file_to_model(xml_path, version="develop")
    over_limit = [line for line in source.splitlines() if len(line) > 100 and "# noqa" not in line]
    assert not over_limit, over_limit[:3]


# ---------------------------------------------------------------------------
# B. Targeted unit tests
# ---------------------------------------------------------------------------


def test_get_default_none() -> None:
    """A missing <default> yields the ``None`` sentinel and no payload."""
    assert _get_default("foo", int, None) == ("None", None)


def test_get_default_literal() -> None:
    """A literal <default> with no kind returns the formatted literal."""
    elem = fromstring("<default>42</default>")
    assert _get_default("foo", int, elem) == ("42", None)


def test_get_default_conditional() -> None:
    """``kind="conditional"`` yields a ``conditional_default`` payload and None default."""
    elem = fromstring(
        '<default kind="conditional">'
        "<case test=\"@ref calculation=='scf'\">1</case>"
        "<case>0</case>"
        "</default>"
    )
    default_str, payload = _get_default("nstep", int, elem)
    assert default_str == "None"
    assert payload is not None
    cases = payload["conditional_default"]
    assert len(cases) == 2
    assert "calculation" in str(cases[0]["when"])
    assert cases[0]["value"] == "1"
    # The fallback <case> has no test.
    assert cases[1]["when"] is None
    assert cases[1]["value"] == "0"


def test_get_default_ref() -> None:
    """``kind="ref"`` yields a ``default_ref`` payload."""
    elem = fromstring('<default kind="ref"><ref>outdir</ref></default>')
    default_str, payload = _get_default("wfcdir", str, elem)
    assert default_str == "None"
    assert payload == {"default_ref": "outdir"}


def test_get_default_computed() -> None:
    """``kind="computed"`` yields a ``computed_default`` payload."""
    elem = fromstring('<default kind="computed">nat</default>')
    default_str, payload = _get_default("nbnd", int, elem)
    assert default_str == "None"
    assert payload == {"computed_default": True}


def test_get_default_expr() -> None:
    """``kind="expr"`` yields a ``default_expr`` payload."""
    elem = fromstring('<default kind="expr"><ref>ecutwfc</ref> * 4</default>')
    default_str, payload = _get_default("ecutrho", float, elem)
    assert default_str == "None"
    assert payload is not None
    assert "ecutwfc" in payload["default_expr"]


@pytest.mark.parametrize(
    ("test", "expected"),
    [
        # ``a or b`` and ``a=b`` are the canonical QE discriminator-test forms.
        ("iflag = 0 or 1", ("iflag", ["0", "1"])),
        ("plot_num=2", ("plot_num", ["2"])),
        ("iflag = 2", ("iflag", ["2"])),
    ],
)
def test_parse_when_test(test: str, expected: tuple[str, list[str]]) -> None:
    """``_parse_when_test`` parses the canonical ``lhs = v1 or v2`` discriminator forms."""
    assert _parse_when_test(test) == expected


def test_distribute_list_default_matching() -> None:
    """A list default of matching length distributes one element per child."""
    elem = fromstring("<default>[1.0, 2.0, 3.0]</default>")
    result = _distribute_list_default(elem, 3)
    assert result is not None
    assert [c.text for c in result] == ["1.0", "2.0", "3.0"]


def test_distribute_list_default_mismatch() -> None:
    """A list default of the wrong length returns None."""
    elem = fromstring("<default>[1.0, 2.0]</default>")
    assert _distribute_list_default(elem, 3) is None


def test_distribute_list_default_non_list() -> None:
    """A non-bracketed default returns None."""
    elem = fromstring("<default>0.0</default>")
    assert _distribute_list_default(elem, 3) is None


def test_distribute_list_default_with_kind() -> None:
    """A structured default (with ``kind``) is never distributed."""
    elem = fromstring('<default kind="ref"><ref>x</ref></default>')
    assert _distribute_list_default(elem, 1) is None


def test_resolve_otherwise_values() -> None:
    """``<otherwise>`` is expanded to the complement of covered option values."""
    discr_var = fromstring(
        '<var name="iflag" type="INTEGER">'
        "<options>"
        '<opt val="0"/><opt val="1"/><opt val="2"/><opt val="3"/>'
        "</options>"
        "</var>"
    )
    branch_values: list[list[str] | None] = [["0", "1"], None]
    resolved = _resolve_otherwise_values(branch_values, discr_var, int, "plot")
    assert resolved[0] == ["0", "1"]
    assert sorted(resolved[1]) == ["2", "3"]


def test_resolve_otherwise_values_no_otherwise() -> None:
    """When there is no ``<otherwise>`` the branch values pass through unchanged."""
    discr_var = fromstring('<var name="iflag" type="INTEGER"><options/></var>')
    resolved = _resolve_otherwise_values([["0"], ["1"]], discr_var, int, "plot")
    assert resolved == [["0"], ["1"]]


@pytest.mark.parametrize(
    ("attr", "expected"),
    [
        ("'a', 'b', 'c'", ["'a'", "'b'", "'c'"]),
        ("'x,y', 'z'", ["'x,y'", "'z'"]),
        ("'solo'", ["'solo'"]),
    ],
)
def test_split_alias_attr(attr: str, expected: list[str]) -> None:
    """``_split_alias_attr`` splits on top-level commas, respecting quotes."""
    assert _split_alias_attr(attr) == expected


def test_format_literal_str() -> None:
    """A str literal strips surrounding single quotes and re-quotes with double quotes."""
    assert _format_literal("'scf'", str) == '"scf"'


def test_format_literal_numeric() -> None:
    """Int/float literals pass through unchanged."""
    assert _format_literal("3", int) == "3"
    assert _format_literal("1.5", float) == "1.5"


@pytest.mark.parametrize(
    ("text", "expected"),
    [(".true.", "True"), (".false.", "False")],
)
def test_sanitize_bool(text: str, expected: str) -> None:
    """Fortran logicals map to Python booleans."""
    assert _sanitize_bool(text) == expected


def test_sanitize_path() -> None:
    """A path default is wrapped in a ``Path(...)`` call."""
    assert _sanitize_path("./tmp") == 'Path("./tmp")'


@pytest.mark.parametrize(
    ("text", "expected"),
    [("'scf'", '"scf"'), ("", "None"), ("'  '", "None"), ("plain", '"plain"')],
)
def test_sanitize_string(text: str, expected: str) -> None:
    """Quoted/empty string defaults sanitize to a python literal or None."""
    assert _sanitize_string(text) == expected


def test_sanitize_numeric_fortran() -> None:
    """A Fortran ``1.D-4`` literal parses into a python float literal."""
    assert _sanitize_numeric("1.D-4", float) == "1.0e-4"


def test_sanitize_numeric_int() -> None:
    """An integer literal passes through unchanged."""
    assert _sanitize_numeric("7", int) == "7"


def test_maybe_list_default_float() -> None:
    """A float list default is rendered verbatim."""
    elem = fromstring("<default>[1.0, 2.0]</default>")
    assert _maybe_list_default(elem, float) == "[1.0, 2.0]"


def test_maybe_list_default_str() -> None:
    """A string list default is re-quoted with double quotes."""
    elem = fromstring("<default>['a', 'b']</default>")
    assert _maybe_list_default(elem, str) == '["a", "b"]'


def test_maybe_list_default_non_bracketed() -> None:
    """A non-bracketed default returns None (handled as a scalar elsewhere)."""
    elem = fromstring("<default>0.0</default>")
    assert _maybe_list_default(elem, float) is None


def test_build_quantity_literal() -> None:
    """An element with literal units + dimensionality yields a ``Quantity(...)`` string."""
    elem = fromstring(
        '<var name="ecutwfc" type="REAL">'
        "<units>Ry</units><dimensionality>energy</dimensionality>"
        "</var>"
    )
    assert _build_quantity(elem) == 'Quantity(units="Ry", dimensionality="energy")'


def test_build_quantity_conditional() -> None:
    """A conditional units kind suppresses the Quantity annotation."""
    elem = fromstring(
        '<var name="x" type="REAL">'
        '<units kind="conditional">Ry</units><dimensionality>energy</dimensionality>'
        "</var>"
    )
    assert _build_quantity(elem) is None


def test_build_quantity_dimensionless() -> None:
    """A dimensionality-only element (no units) yields no Quantity (legitimate)."""
    elem = fromstring('<var name="x" type="REAL"><dimensionality>energy</dimensionality></var>')
    assert _build_quantity(elem) is None


def test_wrap_logical_line_bullet() -> None:
    """A long bullet line wraps with a 2-space hanging indent on continuations."""
    text = ("- " + "word " * 40).strip()
    lines = _wrap_logical_line(text, 40, "  ")
    assert len(lines) > 1
    assert lines[0].startswith("- ")
    for cont in lines[1:]:
        assert cont.startswith("  ")
    for line in lines:
        assert len(line) <= 40


def test_wrap_logical_line_single_word() -> None:
    """A single word (no spaces) is returned as-is even when over budget."""
    assert _wrap_logical_line("supercalifragilistic", 5, "") == ["supercalifragilistic"]


def test_format_description_short_single_line() -> None:
    """A short prose description stays a single ``description="..."`` argument."""
    rendered = _format_description("A short description.", indent=4, trailing_comma=False)
    assert rendered == 'description="A short description."'


def test_format_description_long_wraps() -> None:
    """A long description wraps into a ``dedent(...)`` block within the line limit."""
    text = "This is a long description. " * 6
    rendered = _format_description(text.strip(), indent=8, trailing_comma=True)
    assert rendered.startswith("description=dedent(")
    for line in rendered.split("\n"):
        assert len(line) <= 100


def test_split_top_level() -> None:
    """Commas inside brackets are not split."""
    assert _split_top_level("a, b[1, 2], c") == ["a", "b[1, 2]", "c"]


def test_camel_case() -> None:
    """``camel_case`` converts snake_case to CamelCase."""
    assert camel_case("electrons") == "Electrons"
    assert camel_case("ion_dynamics") == "IonDynamics"


def test_variant_class_name() -> None:
    """``_variant_class_name`` builds a CamelCase variant name from values."""
    assert _variant_class_name("plot", "iflag", ["0", "1"]) == "PlotIflag0Or1Namelist"
    assert _variant_class_name("plot", "iflag", []) == "PlotIflagOtherNamelist"


@pytest.mark.parametrize(
    ("value", "expected"),
    [("-1", "Neg1"), ("'gauss'", "gauss"), ("", "Empty")],
)
def test_sanitize_value_suffix(value: str, expected: str) -> None:
    """Negative values become ``Neg`` and quotes are stripped."""
    assert _sanitize_value_suffix(value) == expected


def test_strip_ref_prefix() -> None:
    """``@ref`` tokens are removed from a conditional test expression."""
    assert _strip_ref_prefix("@ref calculation=='scf'") == "calculation=='scf'"


def test_get_var_type_known() -> None:
    """Known XML types map to python types."""
    elem = fromstring('<var name="nstep" type="INTEGER"/>')
    assert _get_var_type("nstep", elem) is int
    real = fromstring('<var name="dt" type="REAL"/>')
    assert _get_var_type("dt", real) is float


def test_get_var_type_structure_is_none() -> None:
    """A STRUCTURE-typed var maps to None (no atomic representation)."""
    elem = fromstring('<var name="rec" type="STRUCTURE"/>')
    assert _get_var_type("rec", elem) is None


def test_get_var_type_missing_raises() -> None:
    """A var missing a ``type`` attribute raises ``InvalidXMLStructureError``."""
    elem = fromstring('<var name="oops"/>')
    with pytest.raises(InvalidXMLStructureError, match="missing the `type` field"):
        _get_var_type("oops", elem)


def test_get_var_type_path_override() -> None:
    """Directory-like names are coerced to ``Path`` regardless of XML type."""
    elem = fromstring('<var name="pseudo_dir" type="CHARACTER"/>')
    assert _get_var_type("pseudo_dir", elem) is Path


def test_py_literal_basic() -> None:
    """``_py_literal`` renders scalars/None/bool/containers as python literals."""
    assert _py_literal(None) == "None"
    assert _py_literal(True) == "True"
    assert _py_literal(False) == "False"
    assert _py_literal(3) == "3"
    assert _py_literal("hi") == '"hi"'
    assert _py_literal([1, 2]) == "[1, 2]"
    assert _py_literal({"a": 1}) == '{"a": 1}'


def test_py_literal_unsupported_raises() -> None:
    """An unsupported type raises a TypeError."""
    with pytest.raises(TypeError, match="Cannot render"):
        _py_literal(object())


# ---------------------------------------------------------------------------
# sanitize_xml and tree-level conversion
# ---------------------------------------------------------------------------


def test_sanitize_xml_strips_presentational(tmp_path: Path) -> None:
    """``sanitize_xml`` strips presentational markup but preserves ``<ref>``."""
    raw = (
        '<input program="test.x">'
        '<namelist name="control">'
        '<var name="x" type="INTEGER">'
        '<info>See <b>this</b> and <a href="http://example.com">the docs</a><br/> for '
        "details.</info>"
        '<default kind="ref"><ref>outdir</ref></default>'
        "</var>"
        "</namelist>"
        "</input>"
    )
    xml_path = tmp_path / "input_test.xml"
    xml_path.write_text(raw)
    sanitized = sanitize_xml(xml_path)
    try:
        content = sanitized.read_text()
    finally:
        sanitized.unlink(missing_ok=True)
    assert "<b>" not in content
    assert "</b>" not in content
    assert "<br/>" not in content
    assert '<a href="' not in content
    # The link text and url survive as "text (url)".
    assert "the docs (http://example.com)" in content
    # <ref> inside <default> is preserved.
    assert "<ref>outdir</ref>" in content


def test_convert_xml_tree_minimal() -> None:
    """A minimal valid tree converts to compilable source."""
    root = fromstring(
        '<input program="test.x">'
        '<namelist name="control">'
        '<var name="prefix" type="CHARACTER"><default>&apos;pwscf&apos;</default></var>'
        "</namelist>"
        "</input>"
    )
    source = convert_xml_tree_to_model(root, version="develop")
    assert "class ControlNamelist(Namelist):" in source
    assert "class TESTInput(EspressoInput):" in source
    compile(source, "<tree>", "exec")


def test_convert_xml_tree_malformed_var_raises() -> None:
    """A var missing its ``type`` propagates ``InvalidXMLStructureError``."""
    root = fromstring(
        '<input program="test.x"><namelist name="control"><var name="oops"/></namelist></input>'
    )
    with pytest.raises(InvalidXMLStructureError):
        convert_xml_tree_to_model(root, version="develop")


def test_discriminated_choose_generates_variants() -> None:
    """A discriminated ``<choose>`` emits a base class plus per-branch variants."""
    root = fromstring(
        '<input program="plot.x">'
        '<namelist name="plot">'
        '<var name="iflag" type="INTEGER">'
        "<default>3</default>"
        '<options><opt val="0"/><opt val="1"/><opt val="2"/><opt val="3"/></options>'
        "</var>"
        "<choose>"
        '<when test="iflag = 0 or 1">'
        '<var name="e1" type="REAL"><default>1.0</default></var>'
        "</when>"
        "<otherwise>"
        '<var name="nx" type="INTEGER"><default>10</default></var>'
        "</otherwise>"
        "</choose>"
        "</namelist>"
        "</input>"
    )
    source = convert_xml_tree_to_model(root, version="develop")
    assert "_PlotNamelistBase" in source
    assert "discriminator=" in source
    assert "Annotated[" in source
    compile(source, "<choose>", "exec")
