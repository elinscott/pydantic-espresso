"""Pydantic model for the input of `band_interpolation.x` version `qe-7.2-omp5-1.0`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InterpolationNamelist(Namelist):
    """Pydantic model for the `Interpolation` namelist."""

    method: Literal["fourier-diff", "fourier", "idw", "idw-sphere"] = Field(
        "fourier-diff", description="The interpolation method to be used Available options are:"
    )
    miller_max: int = Field(
        6,
        description="The maximum Miller index used to automatically generate the set of symmetry inequivalent Star vectors (only for method == 'fourier-diff' or 'fourier')",
    )
    check_periodicity: bool = Field(
        False,
        description="If .TRUE. a (time consuming) step is performed, to check whether all the Star functions have the correct lattice periodicity (only for method == 'fourier-diff' or 'fourier') .  For automatically generated Star functions this should never occur by construction, and the program will stop and exit in case one Star function with wrong periodicity is found (useful for debugging and program sanity check).  If additional user-defined Star vectors are specified (see optional card USER_STARS), the program will print a WARNING in case one Star function with wrong periodicity is found.",
    )
    p_metric: int = Field(
        2,
        description="The exponent of the distance in the IDW method ( only for method == 'idw' or 'idw-sphere')",
    )
    scale_sphere: int | None = Field(
        None,
        description="The search radius for method == 'idw-sphere', is Rmin * scale_sphere, where Rmin is the minimum distance found between the uniform grid of k-points.  If scale_sphere is too small, some k-points of the path might not see enough uniform grid points to average energies, whereas for large values the method becomes equal to method == 'idw'.",
    )


class BAND_INTERPOLATIONEspressoInput(EspressoInput):
    """Pydantic model for the input of `band_interpolation.x.`"""

    interpolation: InterpolationNamelist = Field(default_factory=lambda: InterpolationNamelist())
