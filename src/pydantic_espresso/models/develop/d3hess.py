"""Pydantic model for the input of `d3hess.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from textwrap import dedent
from typing import Annotated

from pydantic import Field

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class InputNamelist(Namelist):
    """Pydantic model for the `INPUT` namelist."""

    prefix: str = Field(
        "pwscf", description="prefix of input file produced by pw.x (wavefunctions are not needed)"
    )
    outdir: Path | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "ESPRESSO_TMPDIR is set and non-blank",
                    "value": "value of the ESPRESSO_TMPDIR environment variable",
                },
                {"when": None, "value": "current directory ('./')"},
            ],
        },
        description="directory containing the input data, i.e. the same as in pw.x",
    )
    filhess: str | None = Field(
        None,
        json_schema_extra={"default_expr": "trim(prefix)//'.hess'"},
        description=dedent(
            """\
            output file where the D3 hessian matrix is written (should match dftd3_hess keyword in
            phonon calculation)"""
        ),
    )
    step: Annotated[float, Quantity(units="bohr", dimensionality="length")] = Field(
        2.0e-5, description="step for numerical differentiation"
    )


class D3HESSEspressoInput(EspressoInput):
    """Pydantic model for the input of `d3hess.x`."""

    input: InputNamelist = Field(default_factory=lambda: InputNamelist())
