"""Pydantic model for the input of `projwfc.x` version `qe.6.3-rc2`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class ProjwfcNamelist(Namelist):
    """Pydantic model for the `Projwfc` namelist."""

    prefix: str = Field("pwscf", description="prefix of input file produced by pw.x (wavefunctions are needed)")
    outdir: Path = Field(default_factory=get_tmp_dir, description="directory containing the input data, i.e. the same as in pw.x")
    ngauss: int = Field(0, description="Type of gaussian broadening: 0 ... Simple Gaussian (default) 1 ... Methfessel-Paxton of order 1 -1 ... Marzari-Vanderbilt 'cold smearing' -99 ... Fermi-Dirac function")
    degauss: float = Field(0.0, description="gaussian broadening, Ry (not eV!)")
    DeltaE: float | None = Field(None, description="energy grid step (eV)")
    lsym: bool = Field(True, description="if .true.  the projections are symmetrized, the partial density of states are computed if .false. the projections are not symmetrized, the partial DOS can be computed only in the k-resolved case")
    pawproj: bool = Field(False, description="if .true. use PAW projectors and all-electron PAW basis functions to calculate weight factors for the partial densities of states. Following Bloechl, PRB 50, 17953 (1994) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.50.17953), Eq. (4 & 6), the weight factors thus approximate the real charge within the augmentation sphere of each atom. Only for PAW, not implemented in the noncolinear case.")
    filpdos: str | None = Field(None, description="prefix for output files containing PDOS(E)")
    filproj: str | None = Field(None, description="file containing the projections")
    lwrite_overlaps: bool = Field(False, description="if .true., the overlap matrix of the atomic orbitals prior to orthogonalization is written to the atomic_proj datafile.")
    lbinary_data: bool = Field(False, description="if .true., the atomic_proj datafile is written in binary fmt.")
    kresolveddos: bool = Field(False, description="if .true. the k-resolved DOS is computed: not summed over all k-points but written as a function of the k-point index. In this case all k-point weights are set to unity")
    tdosinboxes: bool = Field(False, description="if .true. compute the local DOS integrated in volumes  Volumes are defined as boxes with edges parallel to the unit cell, containing the points of the (charge density) FFT grid included within irmin and irmax, in the three dimensions:  from irmin(j,n) to irmax(j,n) for j=1,2,3 (n=1,n_proj_boxes).")
    n_proj_boxes: int = Field(1, description="number of boxes where the local DOS is computed")
    irmin(3,n_proj_boxes): int | None = Field(None, description="first point of the given box  BEWARE: irmin is a 2D array of the form: irmin(3,n_proj_boxes)")
    irmax(3,n_proj_boxes): int | None = Field(None, description="last point of the given box; ( 0 stands for the last point in the FFT grid )  BEWARE: irmax is a 2D array of the form: irmax(3,n_proj_boxes)")
    plotboxes: bool = Field(False, description="if .true., the boxes are written in output as xsf files with 3D datagrids, valued 1.0 inside the box volume and 0 outside (visualize them as isosurfaces with isovalue 0.5)")


class PROJWFCEspressoInput(EspressoInput):
    """Pydantic model for the input of `projwfc.x.`"""

    projwfc: ProjwfcNamelist = Field(default_factory=ProjwfcNamelist)
