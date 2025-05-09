"""Pydantic model for the input of `pp.x` version `qe-6.7MaX-Release`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputppNamelist(Namelist):
    """Pydantic model for the `INPUTPP` namelist."""

    prefix: str | None = Field(None, description="prefix of files saved by program pw.x")
    outdir: Path = Field(
        Path("value of the"),
        description="directory containing the input data, i.e. the same as in pw.x",
    )
    filplot: str | None = Field(
        None,
        description="file 'filplot' contains the quantity selected by plot_num (can be saved for further processing)",
    )
    plot_num: int | None = Field(
        None,
        description="Selects what to save in filplot:  0  = electron (pseudo-)charge density  1  = total potential V_bare + V_H + V_xc  2  = local ionic potential V_bare  3  = local density of states at specific energy or grid of energies (number of states per volume, in bohr^3, per energy unit, in Ry)  4  = local density of electronic entropy  5  = STM images Tersoff and Hamann, PRB 31, 805 (1985) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.31.805)  6  = spin polarization (rho(up)-rho(down))  7  = contribution of selected wavefunction(s) to the (pseudo-)charge density. For norm-conserving PPs, |psi|^2 (psi=selected wavefunction). Noncollinear case: contribution of the given state to the charge or to the magnetization along the direction indicated by spin_component (0 = charge, 1 = x, 2 = y, 3 = z )  8  = electron localization function (ELF)  9  = charge density minus superposition of atomic densities  10 = integrated local density of states (ILDOS) from emin to emax (emin, emax in eV) if emax is not specified, emax=E_fermi  11 = the V_bare + V_H potential  12 = the sawtooth electric field potential (if present)  13 = the noncollinear magnetization.  17 = all-electron valence charge density can be performed for PAW calculations only requires a very dense real-space grid!  18 = The exchange and correlation magnetic field in the noncollinear case  19 = Reduced density gradient ( J. Chem. Theory Comput. 7, 625 (2011), doi:10.1021/ct100641a (https://doi.org/10.1021/ct100641a) ) Set the isosurface between 0.3 and 0.6 to plot the non-covalent interactions (see also plot_num = 20)  20 = Product of the electron density (charge) and the second eigenvalue of the electron-density Hessian matrix; used to colorize the RDG plot (plot_num = 19)  21 = all-electron charge density (valence+core). For PAW calculations only; requires a very dense real-space grid.  22 = kinetic energy density (for meta-GGA and XDM only)",
    )


class PlotNamelist(Namelist):
    """Pydantic model for the `PLOT` namelist."""

    nfile: int = Field(1, description="the number of data files to read")
    iflag: int | None = Field(
        None,
        description="0 = 1D plot of the spherical average 1 = 1D plot 2 = 2D plot 3 = 3D plot 4 = 2D polar plot on a sphere",
    )
    output_format: int | None = Field(
        None,
        description="(ignored on 1D plot)  0  = format suitable for gnuplot   (1D)  1  = obsolete format no longer supported  2  = format suitable for plotrho   (2D)  3  = format suitable for XCRYSDEN  (2D or user-supplied 3D region)  4  = obsolete format no longer supported  5  = format suitable for XCRYSDEN  (3D, using entire FFT grid)  6  = format as gaussian cube file  (3D) (can be read by many programs)  7  = format suitable for gnuplot   (2D) x, y, f(x,y)",
    )
    fileout: str | None = Field(None, description="name of the file to which the plot is written")
    interpolation: Literal["fourier", "bspline"] = Field(
        "fourier", description="Type of interpolation:"
    )


class PPEspressoInput(EspressoInput):
    """Pydantic model for the input of `pp.x`"""

    inputpp: InputppNamelist = Field(default_factory=lambda: InputppNamelist())
    plot: PlotNamelist = Field(default_factory=lambda: PlotNamelist())
