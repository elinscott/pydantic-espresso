"""Testing qe_7_3_1 models."""

import pytest

from pydantic_espresso.models import versions


from pydantic_espresso.models.template import EspressoInput


@pytest.mark.parametrize(
    "version",
    versions
)
def test_pw_espresso_input(version: str) -> None:
    """Test if the PWEspressoInput model can be instantiated."""
    # Import the model dynamically from pydantic_espresso.models.<version>.pw
    try:
        module = __import__(f"pydantic_espresso.models.{version}.pw", fromlist=["PWEspressoInput"])
    except ModuleNotFoundError:
        pytest.skip(f"Module for version {version} not found.")
        return
    model = getattr(module, "PWEspressoInput")

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
    "version",
    versions
)
def test_ph_espresso_input(version: str) -> None:
    """Test if the PHEspressoInput model can be instantiated."""
    # Import the model dynamically from pydantic_espresso.models.<version>.ph
    try:
        module = __import__(f"pydantic_espresso.models.{version}.ph", fromlist=["PHEspressoInput"])
    except ModuleNotFoundError:
        pytest.skip(f"Module for version {version} not found.")
        return
    model = getattr(module, "PHEspressoInput")

    # Instantiate the model
    inp = model()
