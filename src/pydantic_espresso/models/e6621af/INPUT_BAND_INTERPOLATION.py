"""Pydantic model for the input of `band_interpolation.x` version `e6621af`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInputTemplate


class BAND_INTERPOLATIONEspressoInput(EspressoInputTemplate):
    """Pydantic model for the input of `band_interpolation.x.`"""

    method: Literal["'fourier-diff'", "'fourier'", "'idw'", "'idw-sphere'"] = Field(" 'fourier-diff'
         ", description="The interpolation method to be used")
    miller_max: int = Field( 6
         , description="The maximum Miller index used to automatically generate the set of symmetry inequivalent Star vectors                   (only for")
    check_periodicity: bool = Field(False, description="If .TRUE. a (time consuming) step is performed, to check whether all the Star functions have                   the correct lattice periodicity (only for")
    p_metric: int = Field( 2
         , description="The exponent of the distance in the IDW method ( only for")
    scale_sphere: int = Field( 4.0d0
         , description="The search radius for")
