"""Pydantic model for the input of `d3hess.x` version `e6621af`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInputTemplate


class D3HESSEspressoInput(EspressoInputTemplate):
    """Pydantic model for the input of `d3hess.x.`"""

    prefix: str = Field(" 'pwscf'
         ", description="prefix of input file produced by pw.x (wavefunctions are not needed)")
    outdir: str = Field("
value of the ", description="directory containing the input data, i.e. the same as in pw.x")
    filhess: str = Field(" 'prefix.hess'
         ", description="output file where the D3 hessian matrix is written (should match dftd3_hess keyword in phonon calculation)")
    step: float = Field( 1.d-3
         , description="step for numerical differentiation in a.u.")
