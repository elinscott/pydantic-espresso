"""Testing all other models not covered by other tests in this directory."""

import pytest
from packaging.version import Version

from pydantic_espresso.base import EspressoInput
from pydantic_espresso.models import get_module, versions


@pytest.mark.parametrize(
    "executable",
    [
        "all_currents",
        "band_interpolation",
        "bands",
        "bgw2pw",
        "cppp",
        "cp",
        "d3",
        "d3hess",
        "dos",
        "dynmat",
        "gipaw",
        "hp",
        "ld1",
        "matdyn",
        "molecularpdos",
        "neb",
        "oscdft_et",
        "oscdft_pp",
        "ph",
        "postahc",
        "ppacf",
        "pp",
        "pprism",
        "projwfc",
        "pw2bgw",
        "pw2gw",
        "pw2wannier90",
        "pwcond",
        "pw_with_os_cdft",
        "q2r",
        "turbo_davidson",
        "turbo_eels",
        "turbo_lanczos",
        "turbo_magnon",
        "turbo_spectrum",
        "wannier2pw",
    ],
)
@pytest.mark.parametrize("version", versions)
def test_espresso_input(executable: str, version: Version) -> None:
    """The generated model is a valid, well-formed EspressoInput subclass.

    We can no longer construct every model with no args — executables with a
    mandatory namelist that has required fields (e.g. pw's SYSTEM) require those
    inputs by design. Instead, smoke-test that the generated code produces a
    structurally valid pydantic model by building its JSON schema, which
    exercises every field and validator.
    """
    # Import the model dynamically from pydantic_espresso.models.<executable>.<version>
    try:
        module = get_module(version, executable)
    except ModuleNotFoundError:
        pytest.skip(f"Module for version {version} not found.")
        return
    model = getattr(module, f"{executable.upper().replace('_', '')}Input")

    assert issubclass(model, EspressoInput)
    # Building the JSON schema exercises every field/validator. (neb has no
    # namelists or cards, so its property set is legitimately empty.)
    assert "properties" in model.model_json_schema()
