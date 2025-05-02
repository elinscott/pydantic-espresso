"""Testing qe_7_3_1 models."""

import pytest

from pydantic_espresso.models.develop.pw import PWEspressoInput
from pydantic_espresso.models.qe_7_3_1.pw import PWEspressoInput as PWEspressoInput731
from pydantic_espresso.models.template import EspressoInput


@pytest.mark.parametrize(
    "model",
    [
        PWEspressoInput731,
        PWEspressoInput,
    ],
)
def test_pw_espresso_input(model: type[EspressoInput]) -> None:
    """Test if the PWEspressoInput model can be instantiated."""
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
