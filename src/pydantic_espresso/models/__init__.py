"""Pydantic models for Quantum ESPRESSO inputs."""

from pathlib import Path
from types import ModuleType

from packaging.version import Version

# Minimum QE version supporting the new INPUT_*.def schema (structured defaults,
# explicit <units>/<dimensionality>, <opt alias=...>). Used by ``fetch.py`` to
# skip older tags; we never ship generated models below this version, so we do
# not re-check it during enumeration.
MIN_VERSION = Version("7.6.dev0")

directory = Path(__file__).parent


def _enumerate_versions() -> list[Version]:
    """Discover the available QE versions from the per-executable directories.

    Each executable directory (e.g. ``models/pw/``) holds one Python file per
    version: ``develop.py`` for the in-tree development version and
    ``qe_X_Y[_Z].py`` for tagged releases. We pick any one executable that we
    know exists in every version (``pw`` is fine) and inspect its contents.
    """
    reference_dir = directory / "pw"
    if not reference_dir.is_dir():
        return []
    found: list[Version] = []
    for child in reference_dir.iterdir():
        if not child.is_file() or child.suffix != ".py":
            continue
        stem = child.stem
        if stem in ("__init__", "develop"):
            continue
        if not stem.startswith("qe_"):
            continue
        try:
            found.append(Version(stem[3:].replace("_", ".")))
        except ValueError:
            continue
    return sorted(found)


versions = _enumerate_versions()
# Always expose the in-tree development version on top of any tagged ones
_dev_version = (
    Version(f"{versions[-1].major}.{versions[-1].minor + 1}.dev0") if versions else MIN_VERSION
)
versions.append(_dev_version)

# Create a lookup table of the per-version module-name suffix.
version_module_names = {
    v: "qe_" + str(v).replace(".", "_") if not v.is_devrelease else "develop" for v in versions
}


def get_module(version: Version | str, executable: str) -> ModuleType:
    """Get the module for the specified version and the executable of interest."""
    if version == "develop":
        version = max(versions)
    elif isinstance(version, str):
        version = Version(version)

    version_module_name = version_module_names[version]

    module = __import__(
        f"pydantic_espresso.models.{executable}.{version_module_name}", fromlist=[""]
    )

    return module
