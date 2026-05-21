"""Pydantic model for the input of `pp.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from typing import Literal

from pydantic import Field

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist


class InputppNamelist(Namelist):
    """Pydantic model for the `INPUTPP` namelist."""

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
    plot_num: Literal[
        -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18, 19, 20, 21, 22, 23, 24, 25, 123
    ] = Field(-1, description="Selects what to save in filplot:")


class PlotNamelist(Namelist):
    """Pydantic model for the `PLOT` namelist."""

    nfile: int = Field(1, description="the number of data files to read")
    iflag: Literal[0, 1, 2, 3, 4] = Field(0, description="Type of plot to produce:")
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


class PPEspressoInput(EspressoInput):
    """Pydantic model for the input of `pp.x`."""

    inputpp: InputppNamelist = Field(default_factory=lambda: InputppNamelist())
    plot: PlotNamelist = Field(default_factory=lambda: PlotNamelist())
