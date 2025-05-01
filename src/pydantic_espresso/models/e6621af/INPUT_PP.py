"""Pydantic model for the input of `pp.x` version `e6621af`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInputTemplate


class PPEspressoInput(EspressoInputTemplate):
    """Pydantic model for the input of `pp.x.`"""

    title: str = Field(" ' '
         ", description="reprinted on output, CUB files and other places")
    prefix: str = Field(..., description="prefix of files saved by program pw.x")
    outdir: str = Field("
value of the ", description="directory containing the input data, i.e. the same as in pw.x")
    filplot: str = Field(" 'tmp.pp'
         ", description="file 'filplot' contains the quantity selected by plot_num. Typically this is a temporary file and may be ignored, unless you want to save it for further processing")
    plot_num: int = Field( -1
         , description="Selects what to save in filplot:    -1  = do not do anything, skip step (1) (see header)     0  = electron (pseudo-)charge density     1  = total potential V_bare + V_H + V_xc     2  = local ionic potential V_bare     3  = local density of states at specific energy or grid of energies         (number of states per volume, in bohr^3, per energy unit, in Ry)     4  = local density of electronic entropy     5  = STM images         Tersoff and Hamann,")
    nfile: int = Field( 1
         , description="the number of data files to read")
    iflag: int = Field(..., description="0 = 1D plot of the spherical average 1 = 1D plot 2 = 2D plot 3 = 3D plot 4 = 2D polar plot on a sphere")
    output_format: int = Field(..., description="(ignored on 1D plot)  0  = format suitable for gnuplot   (1D)  1  = obsolete format no longer supported  2  = format suitable for plotrho   (2D)  3  = format suitable for XCRYSDEN  (2D or user-supplied 3D region)  4  = obsolete format no longer supported  5  = format suitable for XCRYSDEN  (3D, using entire FFT grid)  6  = format as gaussian cube file  (3D)      (can be read by many programs)  7  = format suitable for gnuplot   (2D) x, y, f(x,y)")
    fileout: str = Field(" standard output
         ", description="name of the file to which the plot is written")
    interpolation: Literal["'fourier'", "'bspline'"] = Field(" 'fourier'
         ", description="Type of interpolation:")
