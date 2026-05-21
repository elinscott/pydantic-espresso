"""Testing the `pw` models."""

from typing import Any

import numpy as np
import pytest
from packaging.version import Version

from pydantic_espresso.models import get_module, versions


@pytest.mark.parametrize("version", versions)
@pytest.mark.parametrize(
    "k_points",
    [
        {"kind": "gamma"},
        {"kind": "automatic", "grid": [2, 2, 2], "offset": [0, 0, 1]},
        {
            "kind": "crystal",
            "k_points": [
                {"coordinate": [0.0, 0.0, 0.0], "weight": 1.0},
                {"coordinate": [0.5, 0.5, 0.5], "weight": 2.0},
            ],
        },
    ],
)
def test_pw_espresso_input(version: Version, k_points: dict[str, Any]) -> None:
    """Test if the PWInput model can be instantiated."""
    # Import the model dynamically from pydantic_espresso.models.pw.<version>
    try:
        module = get_module(version, "pw")
    except ModuleNotFoundError:
        pytest.skip(f"Module for version {version} not found.")
        return
    model = module.PWInput

    # Instantiate the model
    inp = model(
        cell_parameters={"unit": "alat", "vectors": np.identity(3)},
        atomic_positions={
            "unit": "alat",
            "positions": [{"species": "H", "position": [0.0, 0.0, 0.0]}],
        },
        k_points=k_points,
        occupations=[[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0]],
    )

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

    # Check that the occupations are not printed over too many lines
    assert max([len(x.split()) for x in str(inp).split("\n")]) <= 10
