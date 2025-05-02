"""Pydantic model for the input of `pp.x` version `qe-4.0.4`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputppNamelist(Namelist):
    """Pydantic model for the `Inputpp` namelist."""


    prefix: str | None = Field(None, description="prefix of files saved by program pw.x")
    outdir: Path | None = Field(None, description="temporary directory where pw.x files resides")
    filplot: str | None = Field(None, description="file 'filplot' contains the quantity selected by plot_num (can be saved for further processing)")
    plot_num: int | None = Field(None, description="selects what to save in filplot:  0  = charge  1  = total potential V_bare+V_H + V_xc  2  = local ionic potential  3  = local density of states at e_fermi  4  = local density of electronic entropy  5  = STM images  6  = spin polarization (rho(up)-rho(down))  7  = |psi|^2  8  = electron localization function (ELF)  9  = planar average of all |psi|^2  10 = integrated local density of states (ILDOS) from emin to emax (emin, emax in eV) if emax is not specified, emax=E_fermi  11 = the V_bare + V_H potential  12 = the electric field potential  13 = the noncollinear magnetization.")


class PlotNamelist(Namelist):
    """Pydantic model for the `Plot` namelist."""


    nfile: int = Field(1, description="the number of data files")
    iflag: int | None = Field(None, description="0 1D plot of the spherical average 1 1D plot 2 2D plot 3 3D plot 4 2D polar plot on a sphere")
    output_format: int | None = Field(None, description="(ignored on 1D plot) 0  format suitable for gnuplot   (1D) 1  format suitable for contour.x (2D) 2  format suitable for plotrho   (2D) 3  format suitable for XCRYSDEN  (1D, 2D, 3D) 4  format suitable for gOpenMol  (3D) (formatted: convert to unformatted *.plt) 5  format suitable for XCRYSDEN  (3D) 6  format as gaussian cube file  (3D) (can be read by many programs)")
    fileout: str | None = Field(None, description="name of the file to which the plot is written")


class PPEspressoInput(EspressoInput):
    """Pydantic model for the input of `pp.x.`"""

    inputpp: InputppNamelist = Field(default_factory=lambda: InputppNamelist())
    plot: PlotNamelist = Field(default_factory=lambda: PlotNamelist())
