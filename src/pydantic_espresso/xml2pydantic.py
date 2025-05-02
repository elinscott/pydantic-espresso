"""Functions for converting the content of XML files to Pydantic models as raw strings.

We generate static python code (cf. dynamic model creation) because we want to be able to
inspect the models statically.
"""

import warnings
from pathlib import Path
from xml.etree.ElementTree import Element, ParseError

from defusedxml.ElementTree import parse

from pydantic_espresso.models import directory as model_directory
from pydantic_espresso.models.inputs import import_parameter_models
from pydantic_espresso.xml_files import directory as xml_directory

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


class InvalidXMLStructureError(Exception):
    """Raised when the structure of the XML file is not as expected."""


def sanitize_xml(xml_path: Path) -> Path:
    """Remove various tags that often appear in the <info> field that we want to ignore."""
    with open(xml_path) as f:
        xmlstr = f.read()

    for tag in ["b", "ref", "link"]:
        xmlstr = xmlstr.replace(f"<{tag}>", "").replace(f"</{tag}>", "")

    for tag in ["br"]:
        xmlstr = xmlstr.replace(f"<{tag}/>", "")

    # Replace all links <a href="url">text</a> with text (url)
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
            # Create an empty __init__.py file
            with open(model_dir / "__init__.py", "w") as f:
                f.write(
                    '"""Pydantic models for Quantum ESPRESSO executables.\n\nThis file is '
                    'automatically generated; do not edit.\n"""'
                )
        with open(model_file, "w") as f:
            f.write(model_str)


def convert_xml_file_to_model(xml_file: Path, version: str = "latest") -> tuple[str, str]:
    """Convert an XML file to raw python code that defines the corresponding Pydantic model."""
    # Sanitize the XML file
    sanitized_xml = sanitize_xml(xml_file)

    try:
        tree = parse(sanitized_xml)
    finally:
        # Remove the sanitized XML file
        sanitized_xml.unlink(missing_ok=True)

    root = tree.getroot()
    executable_name = root.attrib["program"].lower()
    executable_name = executable_name.replace(".x", "").replace("-", "_").replace(" ", "_")
    return convert_xml_tree_to_model(root, version=version), executable_name


def convert_xml_tree_to_model(root: Element, version: str = "latest") -> str:
    """Convert an XML tree to raw python code that defines the corresponding Pydantic model."""
    field_definitions: dict[str, list[str]] = {}
    field_validators: dict[str, list[str]] = {}
    for namelist in root.findall("namelist"):
        namelist_name = namelist.attrib["name"].capitalize()
        field_definitions[namelist_name] = []
        field_validators[namelist_name] = []
        for var in namelist.findall("var"):
            field_definition, field_validator = _parse_var(var)

            if field_definition is None:
                continue

            # Manually fixes to duplicate entries
            if field_definition.startswith("abivol:") and any(
                x.startswith("abivol:") for x in field_definitions[namelist_name]
            ):
                continue
            elif field_definition.startswith("restart:") and any(
                x.startswith("restart:") for x in field_definitions[namelist_name]
            ):
                field_definition = field_definition.replace("restart:", "restart_step:")

            field_definitions[namelist_name].append(field_definition)

            if field_validator:
                field_validators[namelist_name].append(field_validator)

    return _generate_model_string(
        root.attrib["program"], field_definitions, field_validators, version=version
    )


def _get_var_type(name: str, var: Element) -> type:
    xml_type_str = var.attrib.get("type", None)
    if xml_type_str is None:
        name = var.attrib["name"]
        raise InvalidXMLStructureError(f"`{name}` is missing the `type` field.")
    python_type = type_mapping[xml_type_str]
    # Manual patching of directories
    if name in ["pseudo_dir", "outdir", "wfcdir"]:
        python_type = Path
    return python_type


def _get_var_description(
    name: str, description_element: Element | None, options: Element | None
) -> str:
    description = (
        ""
        if description_element is None or description_element.text is None
        else description_element.text
    )
    if options is not None:
        for info in options.findall("info"):
            if info.text is None:
                raise InvalidXMLStructureError(f"Missing text in <info> field for `{name}`.")
            description += info.text

    # Sanitize the description
    description = " ".join(
        [line.strip() for line in description.strip(" \n'" + '"').replace('"', "'").split("\n")]
    )

    description = description.replace(r"\p", "p")

    return description


def _parse_var(var: Element) -> tuple[str | None, str]:
    name = var.attrib["name"]
    description_element = var.find("info")

    python_type = _get_var_type(name, var)

    # Pydantic does not support float literals
    options = None if python_type is float else var.find("options")
    default = var.find("default")

    description = _get_var_description(name, description_element, options)
    if description in ["OBSOLETE - NO LONGER IMPLEMENTED"]:
        return None, ""

    type_str, validator_str = _get_type_str(name, python_type, options)

    if "(" in name:
        # Getting rid of the keyword(i) notation
        name = name.split("(")[0]
        type_str = f"list[{type_str}]"
        # We don't know how long the list is, so we can't provide a default value in python
        # even if the XML file has a default value
        default_str = "None"
    else:
        # Getting the default value
        default_str = _get_default_str(name, python_type, default)

    # Adapting type_str if the default value is None
    if default_str == "None":
        if options is None:
            type_str += " | None"
        elif "None" not in type_str:
            # If there are options, we need to add the None type to the options
            type_str = type_str.replace("Literal[", "Literal[None, ")

    if name == "lambda":
        # Avoid nameclash with the lambda function in Python
        name = "Lambda"

    return f'{name}: {type_str} = Field({default_str}, description="{description}")', validator_str


def _get_type_str(name: str, python_type: type, options: Element | None) -> tuple[str, str]:
    """Determine the string to add for the type of the field."""
    if options:
        type_str, mapping = _get_options_str_and_mapping(options, python_type)
    elif name == "ibrav":
        type_str = (
            "Literal[0, 1, 2, 3, -3, 4, 5, -5, 6, 7, 8, 9, -9, 91, 10, 11, 12, -12, 13, -13, 14]"
        )
        mapping = {}
    else:
        type_str = python_type.__name__
        mapping = {}

    # Manually patch vdw_corr which omits "none" as a valid option
    if name == "vdw_corr" and mapping and "none" not in mapping:
        type_str = type_str.replace("Literal[", 'Literal["none", ')
        mapping["none"] = "none"

    validator_str = _get_validator_str(name, mapping, python_type)

    return type_str, validator_str


def _get_validator_str(name: str, mapping: dict[str, str], python_type: type) -> str:
    """Generate a field validator that converts the value following the mapping."""
    if not mapping:
        return ""
    mapping_str = "{" + ", ".join([f'"{k}": "{v}"' for k, v in mapping.items()]) + "}"
    return (
        f"""
    @field_validator("{name}", mode="before")
    def map_{name}(cls, v: {python_type.__name__}) -> {python_type.__name__}:\n"""
        + f'        """Map equivalent values for {name} to the same string so that comparisons '
        + 'work as expected."""'
        + f"""
        mapping = {mapping_str}
        return mapping.get(v, v)"""
    )


def _get_options_str_and_mapping(options: Element, python_type: type) -> tuple[str, dict[str, str]]:
    options_list = []
    mapping = {}
    for opt in options.findall("opt"):
        val = opt.attrib["val"]

        # Manual patches
        if val.startswith("dftd3_version = "):
            val = val.replace("dftd3_version = ", "")
        if "lda_plus_u_kind = " in val:
            val = val.replace("lda_plus_u_kind = ", "")

        if "," in val:
            val_strs = [_get_value_str(v, python_type) for v in val.split(",")]
            val_str = val_strs[0]
            mapping.update({v.strip('"'): val_str.strip('"') for v in val_strs})
        else:
            val_str = _get_value_str(val.split(",")[0], python_type)

        options_list.append(val_str)

    return "Literal[" + ", ".join(options_list) + "]", mapping


def _sanitize_bool(text: str) -> str:
    if text.lower().strip(".") == "false":
        return "False"
    elif text.lower().strip(".") == "true":
        return "True"
    else:
        return "None"


def _sanitize_path(text: str) -> str:
    if text == "current directory ('./')":
        text = "./"
    return 'Path("' + text + '")'


def _sanitize_string(text: str) -> str:
    if text == "":
        # Encode empty strings as None
        return "None"
    elif '"' in text:
        # There is a quote in the middle of the string; avoid converting this
        return "None"
    elif " " in text:
        # In this case the default text is probably a sentence rather than a value describing
        # conditional logic which we should not use as a default value
        return "None"
    else:
        return '"' + text + '"'


def _sanitize_numeric(text: str, python_type: type) -> str:
    if python_type is float and "d" in text.lower():
        # Convert Fortran double precision to Python float
        text = text.lower().replace("d", "e")
    try:
        python_type(text)
        default_str = text
    except ValueError:
        warnings.warn(f"Failed to parse {text}; defaulting to None.", stacklevel=2)
        default_str = "None"
    return default_str


def _get_value_str(text: str, python_type: type) -> str:
    sanitized_text = text.strip(" '\n" + '"').replace("\n", " ")
    if (
        sanitized_text == "value of the $ESPRESSO_PSEUDO environment variable if set; "
        "'$HOME/espresso/pseudo/' otherwise"
    ):
        # Manual patch of pseudo_dir
        default_str = "default_factory=get_pseudo_dir"
    elif (
        sanitized_text == "value of the ESPRESSO_TMPDIR environment variable if set; current "
        "directory ('./') otherwise"
    ):
        # Manual patch of tmp_dir
        default_str = "default_factory=get_tmp_dir"
    elif sanitized_text == "same as outdir":
        default_str = "default_factory=get_tmp_dir"
    elif python_type is bool:
        default_str = _sanitize_bool(sanitized_text)
    elif python_type is Path:
        default_str = _sanitize_path(sanitized_text)
    elif python_type is str:
        default_str = _sanitize_string(sanitized_text)
    else:
        default_str = _sanitize_numeric(sanitized_text, python_type)
    return default_str


def _get_default_str(name: str, python_type: type, default: Element | None) -> str:
    if default is not None:
        if default.text is None:
            raise InvalidXMLStructureError(f"Missing text in XML file for `{name}`.")
        default_str = _get_value_str(default.text, python_type)
    elif name == "ibrav":
        # Manually patching ibrav
        default_str = "0"
    else:
        # We could do "..." here, but we want to reduce the number of required fields
        default_str = "None"

    if name == "verbosity" and default_str == '"default"':
        # Manual patching of verbosity for ph which uses "default" as the default value which we
        # map to "low"
        default_str = '"low"'
    return default_str


def _generate_namelist_string(name: str, fields: list[str], validators: list[str]) -> str:
    """Convert a dictionary of fields into a Namelist class definition."""
    return (
        f"class {name}Namelist(Namelist):\n    "
        + '"""'
        + f"Pydantic model for the `{name}` namelist."
        + '"""\n'
        + "\n".join(validators)
        + "\n\n"
        + "\n".join([f"    {f}" for f in fields])
    )


def _generate_model_string(
    executable: str,
    field_definitions: dict[str, list[str]],
    field_validators: dict[str, list[str]],
    version: str,
) -> str:
    """Convert a dictionary of class definitions to raw python code defining a Pydantic model."""
    executable_str = executable.upper().replace(".X", "").replace(" ", "_").replace("-", "_")

    header = (
        '"""'
        + f"""Pydantic model for the input of `{executable.lower()}` version `{version}`.

This file has been generated automatically. Do not edit it manually.
"""
        + '"""'
        + f"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir
{import_parameter_models}

"""
    )

    namelists = """


""".join(
        _generate_namelist_string(name, fields, field_validators[name])
        for name, fields in field_definitions.items()
    )

    input_definition = (
        f"""


class {executable_str}EspressoInput(EspressoInput):
    """
        + '"""'
        + f"Pydantic model for the input of `{executable}.`"
        + '"""'
        + """

"""
        + "\n".join(
            [
                f"    {k.lower()}: {k}Namelist = Field(default_factory=lambda: {k}Namelist())"
                for k in field_definitions.keys()
            ]
        )
        + "\n"
    )

    return header + namelists + input_definition
