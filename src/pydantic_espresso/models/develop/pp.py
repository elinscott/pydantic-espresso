"""Pydantic model for the input of `pp.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class _InputppNamelistBase(Namelist):
    """Shared fields for the `INPUTPP` namelist (all variants)."""

    title: str | None = Field(None, description="reprinted on output, CUB files and other places")
    prefix: str = Field("pwscf", description="prefix of files saved by program pw.x")
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
    filplot: str = Field(
        "tmp.pp",
        description=(
            "file 'filplot' contains the quantity selected by plot_num. Typically this is a "
            "temporary file and may be ignored, unless you want to save it for further processing"
        ),
    )


class InputppPlotNum0Or9Namelist(_InputppNamelistBase):
    """`INPUTPP` namelist when `plot_num` in (0, 9)."""

    plot_num: Literal[0, 9] = Field(0, description="Discriminator: plot_num")
    spin_component: int = Field(
        0, description="0 = total charge, 1 = spin up charge, 2 = spin down charge."
    )


class InputppPlotNum1Namelist(_InputppNamelistBase):
    """`INPUTPP` namelist when `plot_num` == 1."""

    plot_num: Literal[1] = Field(1, description="Discriminator: plot_num")
    spin_component: int = Field(
        0,
        description="0 = spin averaged potential, 1 = spin up potential, 2 = spin down potential.",
    )


class InputppPlotNum3Namelist(_InputppNamelistBase):
    """`INPUTPP` namelist when `plot_num` == 3."""

    plot_num: Literal[3] = Field(3, description="Discriminator: plot_num")
    emin: Annotated[float | None, Quantity(units="eV", dimensionality="energy")] = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "emin == -999.0 (sentinel) and plot_num == 3", "value": "E_fermi"},
                {"when": None, "value": "-999.0"},
            ],
        },
        description="lower boundary of energy grid.  Defaults to Fermi energy.",
    )
    emax: Annotated[float | None, Quantity(units="eV", dimensionality="energy")] = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "emax == +999.0 (sentinel) and plot_num == 3", "value": "E_fermi"},
                {"when": None, "value": "999.0"},
            ],
        },
        description="upper boundary of energy grid.  Defaults to Fermi energy.",
    )
    delta_e: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(
        0.1, description="spacing of energy grid."
    )
    degauss_ldos: Annotated[float | None, Quantity(units="eV", dimensionality="energy")] = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "degauss_ldos == -999.0 (sentinel) and plot_num == 3",
                    "value": "degauss * rytoev",
                },
                {"when": None, "value": "-999.0"},
            ],
        },
        description=(
            "broadening of energy levels for LDOS.  Defaults to broadening degauss specified for "
            "electronic smearing in pw.x calculation."
        ),
    )
    use_gauss_ldos: bool = Field(
        False,
        description=(
            "If .true., gaussian broadening (ngauss=0) is used for LDOS calculation.  Defaults "
            ".false., in which case the broadening scheme of the pw.x calculation will be used."
        ),
    )


class InputppPlotNum5Namelist(_InputppNamelistBase):
    """`INPUTPP` namelist when `plot_num` == 5."""

    plot_num: Literal[5] = Field(5, description="Discriminator: plot_num")
    sample_bias: Annotated[float, Quantity(units="Ry", dimensionality="energy")] = Field(
        0.01, description="the bias of the sample in stm images"
    )


class InputppPlotNum7Namelist(_InputppNamelistBase):
    """`INPUTPP` namelist when `plot_num` == 7."""

    plot_num: Literal[7] = Field(7, description="Discriminator: plot_num")
    lsign: bool = Field(False, description="if true and k point is Gamma, plot |psi|^2 sign(psi)")
    kpoint: tuple[int, int] | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "kpoint(2) == 0", "value": "kpoint(2) = kpoint(1)"},
                {"when": None, "value": "kpoint(2) initialized to 0; kpoint(1) has no default"},
            ],
        },
        description=(
            "Unpolarized and noncollinear case: k-point(s) to be plotted LSDA: k-point(s) and spin "
            "polarization to be plotted (spin-up and spin-down correspond to different k-points!)  "
            "To plot a single kpoint ikpt, specify kpoint=ikpt or kpoint(1)=ikpt To plot a range "
            "of kpoints [imin, imax], specify kpoint(1)=imin and kpoint(2)=imax"
        ),
    )
    kband: tuple[int, int] | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "kband(2) == 0", "value": "kband(2) = kband(1)"},
                {"when": None, "value": "kband(2) initialized to 0; kband(1) has no default"},
            ],
        },
        description=(
            "Band(s) to be plotted.  To plot a single band ibnd, specify kband=ibnd or "
            "kband(1)=ibnd To plot a range of bands [imin, imax], specify kband(1)=imin and "
            "kband(2)=imax"
        ),
    )
    spin_component: tuple[int, int] | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "spin_component(2) == 0",
                    "value": "spin_component(2) = spin_component(1)",
                },
                {"when": None, "value": "0"},
            ],
        },
        description=(
            "Noncollinear case only: plot the contribution of the given state(s) to the charge or "
            "to the magnetization along the direction(s) indicated by spin_component: 0 = charge, "
            "1 = x, 2 = y, 3 = z.  Ignored in unpolarized or LSDA case  To plot a single component "
            "ispin, specify spin_component=ispin or spin_component(1)=ispin To plot a range of "
            "components [imin, imax], specify spin_component(1)=imin and spin_component(2)=imax"
        ),
    )


class InputppPlotNum10Namelist(_InputppNamelistBase):
    """`INPUTPP` namelist when `plot_num` == 10."""

    plot_num: Literal[10] = Field(10, description="Discriminator: plot_num")
    emin: Annotated[float, Quantity(units="eV", dimensionality="energy")] = Field(
        -999.0, description="lower energy boundary"
    )
    emax: Annotated[float | None, Quantity(units="eV", dimensionality="energy")] = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "emax == +999.0 (sentinel) and plot_num == 10",
                    "value": "ef * rytoev (E_fermi)",
                },
                {"when": None, "value": "999.0"},
            ],
        },
        description="upper energy boundary, i.e. compute ILDOS from emin to emax",
    )
    spin_component: int = Field(
        0,
        description=(
            "for LSDA case only: plot the contribution to ILDOS of 0 = spin-up + spin-down "
            "(default) 1 = spin-up   only 2 = spin-down only"
        ),
    )


class InputppPlotNum13Namelist(_InputppNamelistBase):
    """`INPUTPP` namelist when `plot_num` == 13."""

    plot_num: Literal[13] = Field(13, description="Discriminator: plot_num")
    spin_component: int = Field(
        0,
        description=(
            "0 = absolute value 1 = x component of the magnetization 2 = y component of the "
            "magnetization 3 = z component of the magnetization"
        ),
    )


class InputppPlotNum17Namelist(_InputppNamelistBase):
    """`INPUTPP` namelist when `plot_num` == 17."""

    plot_num: Literal[17] = Field(17, description="Discriminator: plot_num")
    spin_component: int = Field(
        0, description="0 = total charge, 1 = spin up charge, 2 = spin down charge."
    )


class InputppPlotNum22Namelist(_InputppNamelistBase):
    """`INPUTPP` namelist when `plot_num` == 22."""

    plot_num: Literal[22] = Field(22, description="Discriminator: plot_num")
    spin_component: int = Field(
        0, description="0 = total density, 1 = spin up density, 2 = spin down density."
    )


class InputppPlotNum25Namelist(_InputppNamelistBase):
    """`INPUTPP` namelist when `plot_num` == 25."""

    plot_num: Literal[25] = Field(25, description="Discriminator: plot_num")
    nc: int = Field(
        1,
        description=(
            "nc(1), nc(2), and nc(3) indicate the size of the supercell for the visualization of "
            "the squared modulus of the Hubbard projector functions. Note, this supercell must "
            "match the k-points grid size otherwise the resulting WFs are wrong."
        ),
    )
    n0: int = Field(
        0,
        description=(
            "n0(1), n0(2), and n0(3) indicate the shift of the coordinate frame in units of the "
            "lattice vectors for a better visualization of the Hubbard projector functions"
        ),
    )


InputppNamelist = Annotated[
    InputppPlotNum0Or9Namelist
    | InputppPlotNum1Namelist
    | InputppPlotNum3Namelist
    | InputppPlotNum5Namelist
    | InputppPlotNum7Namelist
    | InputppPlotNum10Namelist
    | InputppPlotNum13Namelist
    | InputppPlotNum17Namelist
    | InputppPlotNum22Namelist
    | InputppPlotNum25Namelist,
    Field(discriminator="plot_num"),
]


class _PlotNamelistBase(Namelist):
    """Shared fields for the `PLOT` namelist (all variants)."""

    nfile: int = Field(1, description="the number of data files to read")
    output_format: Literal[-1, 0, 2, 3, 5, 6, 7] = Field(
        -1,
        description=(
            "Format of the output plot file (ignored on 1D plot). Values 1 and 4 are obsolete and "
            "no longer supported."
        ),
    )
    fileout: str | None = Field(
        None,
        json_schema_extra={"computed_default": True},
        description=(
            "Name of the file to which the plot is written. If unset, the plot is written to "
            "standard output."
        ),
    )
    interpolation: Literal["fourier", "bspline"] = Field(
        "fourier", description="Type of interpolation:"
    )
    filepp: list[str] = Field(
        ["tmp.pp"],
        description=(
            "nfile = 1 : file containing the quantity to be plotted (should be the same as "
            "filplot) nfile > 1 : see weight (start = 1, end = nfile)"
        ),
    )
    weight: list[float] = Field(
        [1.0],
        description=(
            "weighing factors: assuming that rho(i) is the quantity read from filepp(i), the "
            "quantity that will be plotted is:  weight(1)*rho(1) + weight(2)*rho(2) + "
            "weight(3)*rho(3) + ... (start = 1, end = nfile)"
        ),
    )


class PlotIflag0Or1Namelist(_PlotNamelistBase):
    """`PLOT` namelist when `iflag` in (0, 1)."""

    iflag: Literal[0, 1] = Field(0, description="Discriminator: iflag")
    nx: int = Field(
        0,
        description=(
            "number of points in the line:  rho(i) = rho( x0 + e1 * (i-1)/(nx-1) ), i=1, nx"
        ),
    )
    e1: Annotated[tuple[float, float, float], Quantity(units="alat", dimensionality="length")] = (
        Field((0.0, 0.0, 0.0), description="3D vector which determines the plotting line")
    )
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
    PlotIflag0Or1Namelist | PlotIflag2Namelist | PlotIflag3Namelist | PlotIflag4Namelist,
    Field(discriminator="iflag"),
]


class PPEspressoInput(EspressoInput):
    """Pydantic model for the input of `pp.x`."""

    inputpp: InputppNamelist = Field(
        default_factory=lambda: InputppPlotNum0Or9Namelist(), discriminator="plot_num"
    )
    plot: PlotNamelist = Field(
        default_factory=lambda: PlotIflag0Or1Namelist(), discriminator="iflag"
    )
