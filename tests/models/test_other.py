"""Testing all other models not covered by other tests in this directory."""

import pytest
from packaging.version import Version

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
    """Test if the model can be instantiated."""
    # Import the model dynamically from pydantic_espresso.models.<version>.<executable>
    try:
        module = get_module(version, executable)
    except ModuleNotFoundError:
        pytest.skip(f"Module for version {version} not found.")
        return
    model = getattr(module, f"{executable.upper().replace('_', '')}EspressoInput")

    # Instantiate the model
    inp = model()  # noqa: F841
