"""Pydantic model for the input of `pprism.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class InputppNamelist(Namelist):
    """Pydantic model for the `INPUTPP` namelist."""

    prefix: str = Field("pwscf", description="prefix of files saved by program pw.x")
    outdir: Path | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "ESPRESSO_TMPDIR is set",
                    "value": "value of the ESPRESSO_TMPDIR environment variable",
                },
                {"when": None, "value": "current directory ('./')"},
            ],
        },
        description="directory containing the input data, i.e. the same as in pw.x",
    )
    filplot: str | None = Field(
        None,
        json_schema_extra={"default_expr": '"prefix".pprism'},
        description=(
            "file 'filplot' contains solvent's quantities (can be saved for further processing)"
        ),
    )
    lpunch: bool = Field(False, description="punch solvent's quantities to fileplot, or not")


class _PlotNamelistBase(Namelist):
    """Shared fields for the `PLOT` namelist (all variants)."""

    output_format: Literal[None, 0, 2, 3, 5, 6, 7] = Field(
        None, description="Output format for the plot (ignored on 1D plot)."
    )
    fileout: str | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "0 <= output_format <= 7",
                    "value": '"prefix".3drism_* with a format-dependent extension',
                },
                {"when": None, "value": '"prefix".3drism'},
            ],
        },
        description="name of the file to which the plot is written",
    )
    interpolation: Literal["fourier", "bspline"] = Field(
        "fourier", description="Type of interpolation:"
    )


class PlotIflag0Namelist(_PlotNamelistBase):
    """`PLOT` namelist when `iflag` == 0."""

    iflag: Literal[0] = Field(0, description="Discriminator: iflag")
    nx: int = Field(0, description="number of radial grids")
    lebedev: int = Field(
        302,
        description=(
            "number of spherical grids of Lebedev quadrature (only for interpolation = 'bspline')"
        ),
    )
    x0: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field((0.0, 0.0, 0.0), description="3D vector, origin of the line")
    )


class PlotIflag1Namelist(_PlotNamelistBase):
    """`PLOT` namelist when `iflag` == 1."""

    iflag: Literal[1] = Field(1, description="Discriminator: iflag")
    nx: int | None = Field(
        None,
        description=(
            "number of points in the line:  rho(i) = rho( x0 + e1 * (i-1)/(nx-1) ), i=1, nx"
        ),
    )
    e1: Annotated[
        tuple[float, float, float] | None, Quantity(units="alat", dimensionality="length")
    ] = Field(None, description="3D vector which determines the plotting line")
    x0: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field((0.0, 0.0, 0.0), description="3D vector, origin of the line")
    )


class PlotIflag2Namelist(_PlotNamelistBase):
    """`PLOT` namelist when `iflag` == 2."""

    iflag: Literal[2] = Field(2, description="Discriminator: iflag")
    nx: int | None = Field(None, description="")
    ny: int | None = Field(None, description="")
    e1: Annotated[
        tuple[float, float, float] | None, Quantity(units="alat", dimensionality="length")
    ] = Field(None, description="")
    e2: Annotated[
        tuple[float, float, float] | None, Quantity(units="alat", dimensionality="length")
    ] = Field(None, description="")
    x0: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field((0.0, 0.0, 0.0), description="3D vector, origin of the plane")
    )


class PlotIflag3Namelist(_PlotNamelistBase):
    """`PLOT` namelist when `iflag` == 3."""

    iflag: Literal[3] = Field(3, description="Discriminator: iflag")
    nx: int | None = Field(None, description="")
    ny: int | None = Field(None, description="")
    nz: int | None = Field(None, description="")
    e1: Annotated[
        tuple[float, float, float] | None, Quantity(units="alat", dimensionality="length")
    ] = Field(None, description="")
    e2: Annotated[
        tuple[float, float, float] | None, Quantity(units="alat", dimensionality="length")
    ] = Field(None, description="")
    e3: Annotated[
        tuple[float, float, float] | None, Quantity(units="alat", dimensionality="length")
    ] = Field(None, description="")
    x0: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field((0.0, 0.0, 0.0), description="3D vector, origin of the parallelepiped")
    )


class PlotIflag4Namelist(_PlotNamelistBase):
    """`PLOT` namelist when `iflag` == 4."""

    iflag: Literal[4] = Field(4, description="Discriminator: iflag")
    radius: Annotated[float, Quantity(units="alat", dimensionality="length")] = Field(
        1.0, description="Radius of the sphere, centered at (0,0,0)"
    )
    nx: int | None = Field(None, description="")
    ny: int | None = Field(None, description="")


PlotNamelist = Annotated[
    PlotIflag0Namelist
    | PlotIflag1Namelist
    | PlotIflag2Namelist
    | PlotIflag3Namelist
    | PlotIflag4Namelist,
    Field(discriminator="iflag"),
]


class PPRISMEspressoInput(EspressoInput):
    """Pydantic model for the input of `pprism.x`."""

    inputpp: InputppNamelist = Field(default_factory=lambda: InputppNamelist())
    plot: PlotNamelist = Field(default_factory=lambda: PlotIflag0Namelist(), discriminator="iflag")
