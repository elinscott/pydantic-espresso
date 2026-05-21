"""Pydantic model for the input of `dos.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from textwrap import dedent
from typing import Annotated, Literal

from pydantic import Field

from pydantic_espresso.base import EspressoInput
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
        description=dedent(
            """\
            By default this is set to 'smearing' if degauss is given in input; otherwise the method
            is read from the xml data file. Keyword selecting  the method for BZ summation.
            Available options are:
            - 'smearing': integration using gaussian smearing. In fact currently any string not
              related to tetrahedra defaults to smearing;.
            - 'tetrahedra': Tetrahedron method, Bloechl's version: P.E. Bloechl, PRB 49, 16223
              (1994) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.49.16223) Requires
              uniform grid of k-points, to be automatically generated in pw.x.
            - 'tetrahedra_lin': Original linear tetrahedron method. To be used only as a reference;
              the optimized tetrahedron method is more efficient.
            - 'tetrahedra_opt': Optimized tetrahedron method: see M. Kawamura, PRB 89, 094515
              (2014) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.89.094515)."""
        ),
    )
    ngauss: Literal[0, 1, -1, -99] = Field(
        0,
        description=dedent(
            """\
            Type of gaussian broadening.
            - '0': Simple Gaussian.
            - '1': Methfessel-Paxton of order 1.
            - '-1': cold smearing' (Marzari-Vanderbilt-DeVita-Payne).
            - '-99': Fermi-Dirac function."""
        ),
    )
    degauss: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.0, description="gaussian broadening, Ry (not eV!) (see below)"
    )
    Emin: Annotated[float | None, Quantity(units="eV", dimensionality="energy")] = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            min, max energy for DOS plot. If unspecified, the lower and/or upper band value,
            plus/minus 3 times the value of the gaussian smearing if present, will be used."""
        ),
    )
    Emax: Annotated[float | None, Quantity(units="eV", dimensionality="energy")] = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=dedent(
            """\
            min, max energy for DOS plot. If unspecified, the lower and/or upper band value,
            plus/minus 3 times the value of the gaussian smearing if present, will be used."""
        ),
    )
    DeltaE: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(
        0.01, description="energy grid step"
    )
    fildos: str | None = Field(
        None,
        json_schema_extra={"default_expr": "prefix // '.dos'"},
        description="output file containing DOS(E)",
    )


class DOSInput(EspressoInput):
    """Pydantic model for the input of `dos.x`."""

    dos: DosNamelist = Field(default_factory=lambda: DosNamelist())
