"""Pydantic model for the input of `pprism.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from textwrap import dedent
from typing import Annotated, Literal

from pydantic import Field

from pydantic_espresso.base import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class InputppNamelist(Namelist):
    """Pydantic model for the `INPUTPP` namelist."""

    prefix: str = Field("pwscf", description="prefix of files saved by program pw.x")
    outdir: Path | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "ESPRESSO_TMPDIR is set", "value": "from_environment"},
                {"when": None, "value": "./"},
            ],
        },
        description="directory containing the input data, i.e. the same as in pw.x",
    )
    filplot: str | None = Field(
        None,
        json_schema_extra={"default_expr": '"prefix".pprism'},
        description=dedent(
            """\
            file 'filplot' contains solvent's quantities (can be saved for further processing)"""
        ),
    )
    lpunch: bool = Field(False, description="punch solvent's quantities to fileplot, or not")


class _PlotNamelistBase(Namelist):
    """Shared fields for the `PLOT` namelist (all variants)."""

    output_format: Literal[0, 2, 3, 5, 6, 7] = Field(
        ...,
        description=dedent(
            """\
            Output format for the plot (ignored on 1D plot).
            - '0': Format suitable for gnuplot (1D).
            - '2': Format suitable for plotrho (2D).
            - '3': Format suitable for XCRYSDEN (2D or user-supplied 3D region).
            - '5': Format suitable for XCRYSDEN (3D, using entire FFT grid).
            - '6': Format as gaussian cube file (3D) (can be read by many programs).
            - '7': Format suitable for gnuplot (2D) x, y, f(x,y)."""
        ),
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
        "fourier",
        description=dedent(
            """\
            Type of interpolation:
            - 'bspline': (EXPERIMENTAL)."""
        ),
    )


class PlotIflag0Namelist(_PlotNamelistBase):
    """`PLOT` namelist when `iflag` == 0."""

    iflag: Literal[0] = Field(0, description="Discriminator: iflag")
    nx: int = Field(..., description="number of radial grids")
    lebedev: int = Field(
        ...,
        description=dedent(
            """\
            number of spherical grids of Lebedev quadrature (only for interpolation = 'bspline')"""
        ),
    )
    x0: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field(..., description="3D vector, origin of the line")
    )


class PlotIflag1Namelist(_PlotNamelistBase):
    """`PLOT` namelist when `iflag` == 1."""

    iflag: Literal[1] = Field(1, description="Discriminator: iflag")
    nx: int = Field(
        ...,
        description=dedent(
            """\
            number of points in the line:  rho(i) = rho( x0 + e1 * (i-1)/(nx-1) ), i=1, nx"""
        ),
    )
    e1: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field(..., description="3D vector which determines the plotting line")
    )
    x0: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field(..., description="3D vector, origin of the line")
    )


class PlotIflag2Namelist(_PlotNamelistBase):
    """`PLOT` namelist when `iflag` == 2."""

    iflag: Literal[2] = Field(2, description="Discriminator: iflag")
    nx: int = Field(
        ...,
        description=dedent(
            """\
            Number of points in the plane:  rho(i,j) = rho( x0 + e1 * (i-1)/(nx-1) + e2 *
            (j-1)/(ny-1) ), i=1,nx ; j=1,ny"""
        ),
    )
    ny: int = Field(
        ...,
        description=dedent(
            """\
            Number of points in the plane:  rho(i,j) = rho( x0 + e1 * (i-1)/(nx-1) + e2 *
            (j-1)/(ny-1) ), i=1,nx ; j=1,ny"""
        ),
    )
    e1: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field(
            ...,
            description=dedent(
                """\
                3D vectors which determine the plotting plane  BEWARE: e1 and e2 must be
                orthogonal"""
            ),
        )
    )
    e2: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field(
            ...,
            description=dedent(
                """\
                3D vectors which determine the plotting plane  BEWARE: e1 and e2 must be
                orthogonal"""
            ),
        )
    )
    x0: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field(..., description="3D vector, origin of the plane")
    )


class PlotIflag3Namelist(_PlotNamelistBase):
    """`PLOT` namelist when `iflag` == 3."""

    iflag: Literal[3] = Field(3, description="Discriminator: iflag")
    nx: int = Field(
        ...,
        description=dedent(
            """\
            Number of points in the parallelepiped:  rho(i,j,k) = rho( x0 + e1 * (i-1)/nx + e2 *
            (j-1)/ny + e3 * (k-1)/nz ), i = 1, nx ; j = 1, ny ; k = 1, nz  - If output_format = 3
            (XCRYSDEN), the above variables are used to determine the grid to plot.  - If
            output_format = 5 (XCRYSDEN), the above variables are ignored, the entire FFT grid is
            written in the XCRYSDEN format - works for any crystal axis (VERY FAST)  - If e1, e2,
            e3, x0 are present, and e1, e2, e3 are parallel to xyz and parallel to crystal axis, a
            subset of the FFT grid that approximately covers the parallelepiped defined by e1, e2,
            e3, x0, is written - untested, might be obsolete  - Otherwise, the required 3D grid is
            generated from the Fourier components (may be VERY slow)"""
        ),
    )
    ny: int = Field(
        ...,
        description=dedent(
            """\
            Number of points in the parallelepiped:  rho(i,j,k) = rho( x0 + e1 * (i-1)/nx + e2 *
            (j-1)/ny + e3 * (k-1)/nz ), i = 1, nx ; j = 1, ny ; k = 1, nz  - If output_format = 3
            (XCRYSDEN), the above variables are used to determine the grid to plot.  - If
            output_format = 5 (XCRYSDEN), the above variables are ignored, the entire FFT grid is
            written in the XCRYSDEN format - works for any crystal axis (VERY FAST)  - If e1, e2,
            e3, x0 are present, and e1, e2, e3 are parallel to xyz and parallel to crystal axis, a
            subset of the FFT grid that approximately covers the parallelepiped defined by e1, e2,
            e3, x0, is written - untested, might be obsolete  - Otherwise, the required 3D grid is
            generated from the Fourier components (may be VERY slow)"""
        ),
    )
    nz: int = Field(
        ...,
        description=dedent(
            """\
            Number of points in the parallelepiped:  rho(i,j,k) = rho( x0 + e1 * (i-1)/nx + e2 *
            (j-1)/ny + e3 * (k-1)/nz ), i = 1, nx ; j = 1, ny ; k = 1, nz  - If output_format = 3
            (XCRYSDEN), the above variables are used to determine the grid to plot.  - If
            output_format = 5 (XCRYSDEN), the above variables are ignored, the entire FFT grid is
            written in the XCRYSDEN format - works for any crystal axis (VERY FAST)  - If e1, e2,
            e3, x0 are present, and e1, e2, e3 are parallel to xyz and parallel to crystal axis, a
            subset of the FFT grid that approximately covers the parallelepiped defined by e1, e2,
            e3, x0, is written - untested, might be obsolete  - Otherwise, the required 3D grid is
            generated from the Fourier components (may be VERY slow)"""
        ),
    )
    e1: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field(
            ...,
            description=dedent(
                """\
                3D vectors which determine the plotting parallelepiped (if present, must be
                orthogonal)"""
            ),
        )
    )
    e2: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field(
            ...,
            description=dedent(
                """\
                3D vectors which determine the plotting parallelepiped (if present, must be
                orthogonal)"""
            ),
        )
    )
    e3: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field(
            ...,
            description=dedent(
                """\
                3D vectors which determine the plotting parallelepiped (if present, must be
                orthogonal)"""
            ),
        )
    )
    x0: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field((0.0, 0.0, 0.0), description="3D vector, origin of the parallelepiped")
    )


class PlotIflag4Namelist(_PlotNamelistBase):
    """`PLOT` namelist when `iflag` == 4."""

    iflag: Literal[4] = Field(4, description="Discriminator: iflag")
    radius: Annotated[float, Quantity(units="alat", dimensionality="length")] = Field(
        ..., description="Radius of the sphere, centered at (0,0,0)"
    )
    nx: int = Field(
        ...,
        description=dedent(
            """\
            Number of points in the polar plane:  phi(i)   = 2 pi * (i - 1)/(nx-1), i=1, nx
            theta(j) =   pi * (j - 1)/(ny-1), j=1, ny"""
        ),
    )
    ny: int = Field(
        ...,
        description=dedent(
            """\
            Number of points in the polar plane:  phi(i)   = 2 pi * (i - 1)/(nx-1), i=1, nx
            theta(j) =   pi * (j - 1)/(ny-1), j=1, ny"""
        ),
    )


PlotNamelist = Annotated[
    PlotIflag0Namelist
    | PlotIflag1Namelist
    | PlotIflag2Namelist
    | PlotIflag3Namelist
    | PlotIflag4Namelist,
    Field(discriminator="iflag"),
]


class PPRISMInput(EspressoInput):
    """Pydantic model for the input of `pprism.x`."""

    inputpp: InputppNamelist = Field(default_factory=lambda: InputppNamelist())
    plot: PlotNamelist = Field(..., discriminator="iflag")
