"""Test discriminated ``PLOT`` namelist variants in ``pp.x``."""

import pytest
from pydantic import ValidationError

from pydantic_espresso.models.pp.develop import (
    PlotIflag0Or1Namelist,
    PlotIflag2Namelist,
    PlotIflag3Namelist,
    PlotIflag4Namelist,
    PPInput,
)

_LINE_REQUIRED: dict[str, object] = {
    "nx": 5,
    "e1": (1.0, 0.0, 0.0),
    "x0": (0.0, 0.0, 0.0),
}

_PLANE_REQUIRED: dict[str, object] = {
    "nx": 5,
    "ny": 5,
    "e1": (1.0, 0.0, 0.0),
    "e2": (0.0, 1.0, 0.0),
    "x0": (0.0, 0.0, 0.0),
}

_SPHERE_REQUIRED: dict[str, object] = {
    "radius": 1.0,
    "nx": 10,
    "ny": 10,
}


@pytest.mark.parametrize(
    ("iflag", "extra", "expected_cls"),
    [
        (0, _LINE_REQUIRED, PlotIflag0Or1Namelist),
        (1, _LINE_REQUIRED, PlotIflag0Or1Namelist),
        (2, _PLANE_REQUIRED, PlotIflag2Namelist),
        (3, {}, PlotIflag3Namelist),
        (4, _SPHERE_REQUIRED, PlotIflag4Namelist),
    ],
)
def test_pp_plot_discriminator_routes_to_correct_class(
    iflag: int, extra: dict[str, object], expected_cls: type
) -> None:
    """Each ``iflag`` value selects the matching ``PlotIflag*Namelist`` subclass."""
    inp = PPInput(plot={"iflag": iflag, **extra})
    assert isinstance(inp.plot, expected_cls)
    assert inp.plot is not None
    assert inp.plot.iflag == iflag


def test_pp_plot_iflag3_optional_fields() -> None:
    """``iflag=3`` accepts an empty body because all branch fields have defaults."""
    inp = PPInput(plot={"iflag": 3})
    assert isinstance(inp.plot, PlotIflag3Namelist)
    assert inp.plot.nx == 0
    assert inp.plot.ny == 0
    assert inp.plot.nz == 0
    assert inp.plot.e1 == (0.0, 0.0, 0.0)


def test_pp_plot_iflag2_omitting_required_raises() -> None:
    """``iflag=2`` without ``nx`` raises ``ValidationError`` mentioning the field."""
    with pytest.raises(ValidationError) as exc:
        PPInput(plot={"iflag": 2})
    assert "nx" in str(exc.value)
