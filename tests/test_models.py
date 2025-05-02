"""Testing qe_7_3_1 models."""

import pytest

from pydantic_espresso.models import versions


@pytest.mark.parametrize("version", versions)
def test_pw_espresso_input(version: str) -> None:
    """Test if the PWEspressoInput model can be instantiated."""
    # Import the model dynamically from pydantic_espresso.models.<version>.pw
    try:
        module = __import__(f"pydantic_espresso.models.{version}.pw", fromlist=["PWEspressoInput"])
    except ModuleNotFoundError:
        pytest.skip(f"Module for version {version} not found.")
        return
    model = module.PWEspressoInput

    # Instantiate the model
    inp = model()

    # Check the string representation of the input is empty
    assert "scf" not in str(inp)

    # Check the value of the calculation attribute
    assert hasattr(inp, "control")
    assert inp.control.calculation == "scf"

    # Set the calculation attribute to bands and check it
    inp.control.calculation = "bands"
    assert inp.control.calculation == "bands"

    # Check the string representation now shows the calculation value
    assert "bands" in str(inp)


@pytest.mark.parametrize(
    "executable",
    [
        "all_currents",
        "band_interpolation",
        "bands",
        "bgw2pw",
        "cppp",
        "cp",
        "d3hess",
        "dos",
        "dynmat",
        "hp",
        "kcw",
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
        "pw",
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
def test_espresso_input(executable: str, version: str) -> None:
    """Test if the model can be instantiated."""
    # Import the model dynamically from pydantic_espresso.models.<version>.<executable>
    try:
        module = __import__(
            f"pydantic_espresso.models.{version}.{executable}", fromlist=[executable]
        )
    except ModuleNotFoundError:
        pytest.skip(f"Module for version {version} not found.")
        return
    model = getattr(module, f"{executable.upper().replace('_', '')}EspressoInput")

    # Instantiate the model
    inp = model()  # noqa: F841
