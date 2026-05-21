"""Pydantic model for the input of `dos.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class DosNamelist(Namelist):
    """Pydantic model for the `DOS` namelist."""

    prefix: str = Field(
        "pwscf", description="prefix of input file produced by pw.x (wavefunctions are not needed)"
    )
    outdir: Path | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "ESPRESSO_TMPDIR is set", "value": "from_environment"},
                {"when": None, "value": "'./'"},
            ],
        },
        description="directory containing the input data, i.e. the same as in pw.x",
    )
    bz_sum: Literal[None, "smearing", "tetrahedra", "tetrahedra_lin", "tetrahedra_opt"] = Field(
        None,
        description=(
            "By default this is set to 'smearing' if degauss is given in input; otherwise the "
            "method is read from the xml data file. Keyword selecting  the method for BZ "
            "summation. Available options are:"
        ),
    )
    ngauss: Literal[0, 1, -1, -99] = Field(0, description="Type of gaussian broadening.")
    degauss: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.0, description="gaussian broadening, Ry (not eV!) (see below)"
    )
    Emin: float | None = Field(None, description="")
    Emax: float | None = Field(None, description="")
    DeltaE: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(
        0.01, description="energy grid step"
    )
    fildos: str | None = Field(
        None,
        json_schema_extra={"default_expr": "prefix // '.dos'"},
        description="output file containing DOS(E)",
    )


class DOSEspressoInput(EspressoInput):
    """Pydantic model for the input of `dos.x`."""

    dos: DosNamelist = Field(default_factory=lambda: DosNamelist())
