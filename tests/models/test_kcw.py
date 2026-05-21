"""Testing the `pw` models."""

from typing import Any

import pytest
from packaging.version import Version

from pydantic_espresso.models import get_module, versions


@pytest.mark.parametrize("version", [v for v in versions if v >= Version("7.1")])
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
def test_kcw_espresso_input(version: Version, k_points: dict[str, Any]) -> None:
    """Test if the KCWInput model can be instantiated."""
    # Import the model dynamically from pydantic_espresso.models.kcw.<version>
    try:
        module = get_module(version, "kcw")
    except ModuleNotFoundError:
        pytest.skip(f"Module for version {version} not found.")
        return
    model = module.KCWInput

    # Instantiate the model
    inp = model(
        control={
            "calculation": "wann2kcw",
        },
        k_points=k_points,
    )

    # Check the string representation of the input
    assert "wann2kcw" in str(inp)

    # Check the default value of the kcw_at_ks attribute
    assert hasattr(inp, "control")
    assert inp.control.kcw_at_ks
