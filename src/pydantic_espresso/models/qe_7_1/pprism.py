"""Pydantic model for the input of `pprism.x` version `qe-7.1`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputppNamelist(Namelist):
    """Pydantic model for the `Inputpp` namelist."""

    prefix: str = Field("pwscf", description="prefix of files saved by program pw.x")
    outdir: Path = Field(value of the, description="directory containing the input data, i.e. the same as in pw.x")
    filplot: str = Field("prefix".pprism", description="file 'filplot' contains solvent's quantities (can be saved for further processing)")
    lpunch: bool = Field(False, description="punch solvent's quantities to fileplot, or not")


class PlotNamelist(Namelist):
    """Pydantic model for the `Plot` namelist."""

    iflag: int | None = Field(None, description="0 1D plot of the spherical average 1 1D plot 2 2D plot 3 3D plot 4 2D polar plot on a sphere")
    output_format: int | None = Field(None, description="(ignored on 1D plot)  0  = format suitable for gnuplot   (1D)  1  = obsolete format no longer supported  2  = format suitable for plotrho   (2D)  3  = format suitable for XCRYSDEN  (2D or user-supplied 3D region)  4  = obsolete format no longer supported  5  = format suitable for XCRYSDEN  (3D, using entire FFT grid)  6  = format as gaussian cube file  (3D) (can be read by many programs)  7  = format suitable for gnuplot   (2D) x, y, f(x,y)")
    fileout: str = Field("prefix".3drism", description="name of the file to which the plot is written")
    interpolation: Literal["fourier", "bspline"] = Field("fourier", description="Type of interpolation:")


class PPRISMEspressoInput(EspressoInput):
    """Pydantic model for the input of `pprism.x.`"""

    inputpp: InputppNamelist = Field(default_factory=InputppNamelist)
    plot: PlotNamelist = Field(default_factory=PlotNamelist)
