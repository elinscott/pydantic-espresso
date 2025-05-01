"""Pydantic model for the input of `pw2gw.x` version `qe-7.2-omp5`.

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

    prefix: str | None = Field(None, description="the first part of the name of all the file written by the code should be equal to the value given in the main calculations.")
    outdir: Path = Field(./, description="the scratch directory where the massive data-files are written")
    what: str = Field("gw", description="gw' : Calculate dipole optical matrix elements (use for norm-conserving pseudopotentials) and imaginary part of the dielectric function.  'gmaps': write g-maps for each processor in a file 'fort.'100 + processor number")
    qplda: bool = Field(False, description="if .TRUE. write the interface file 'QPLDA' to GW and BSE codes (chisig, dpforexc).")
    vxcdiag: bool = Field(False, description="if .TRUE. calculates the expectation value of the exchange and correlation potential on all the Kohn-Sham states and write it into the 'vxcdiag.dat' file.")
    vkb: bool = Field(False, description="if .TRUE. use Kleyman-Bylander projectors to write additional informatio into fort.15 file (Still in development)")
    Emin: float = Field(0.0, description="Starting photon energy for which the dielectric function is calculated (in eV)")
    Emax: float = Field(30.0, description="Highest photon energy for which the dielectric function is calculated (in eV)")
    DeltaE: float = Field(0.05, description="Energy step with which the dielectric function is calculated (in eV)")


class PW2GWEspressoInput(EspressoInput):
    """Pydantic model for the input of `pw2gw.x.`"""

    inputpp: InputppNamelist = Field(default_factory=InputppNamelist)
