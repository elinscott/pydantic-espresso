"""Pydantic models for Quantum ESPRESSO inputs."""

from pathlib import Path
from types import ModuleType

from packaging.version import Version

versions = sorted(
    [Version(p.name[3:].replace("_", ".")) for p in Path(__file__).parent.glob("qe_*")]
)
# Add development version
versions.append(Version(f"{versions[-1].major}.{versions[-1].minor + 1}.dev0"))

# Create a lookup table of the directory for each version
version_module_names = {
    v: "qe_" + str(v).replace(".", "_") if not v.is_devrelease else "develop" for v in versions
}

directory = Path(__file__).parent


def get_module(version: Version | str, executable: str) -> ModuleType:
    """Get the module for the specified version and the executable of interest."""
    if version == "develop":
        version = max(versions)
    elif isinstance(version, str):
        version = Version(version)

    version_module_name = version_module_names[version]

    module = __import__(
        f"pydantic_espresso.models.{version_module_name}.{executable}", fromlist=[""]
    )

    return module
