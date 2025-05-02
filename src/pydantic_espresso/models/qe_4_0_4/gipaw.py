"""Pydantic model for the input of `gipaw.x` version `qe-4.0.4`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputgipawNamelist(Namelist):
    """Pydantic model for the `Inputgipaw` namelist."""


    job: str = Field("nmr", description="select calculation to perform. The possible values are:  'f-sum'        check the f-sum rule 'nmr'          compute the magnetic suscept. and NMR chemical shifts 'g_tensor'     compute the EPR g-tensor 'efg'          compute the electric field gradients at the nuclei")
    prefix: str = Field("prefix", description="prefix of files saved by program pw.x")
    tmp_dir: str = Field("./scratch/", description="temporary directory where pw.x files resides")
    conv_threshold: float = Field(1.e-14, description="convergence threshold for the diagonalization and for the Green's function solver")
    isolve: int = Field(0, description="diagonalization method:  0 = Davidson 1 = CG")
    q_gipaw: float = Field(0.01, description="small vector for long wavelength linear response")
    iverbosity: int = Field(0, description="if iverbosity > 0 print more information in output")
    filcurr: str | None = Field(None, description="for saving the induced current (valence only)")
    filfield: str | None = Field(None, description="for saving the induced magnetic field (valence only)")
    read_recon_in_paratec_fmt: bool = Field(False, description="for reading reconstruction data from Paratec converted pseudopotentials")
    use_nmr_macroscopic_shape: bool | None = Field(None, description="correct the chemical shift by taking into account the macroscopic shape of the sample")
    nmr_macroscopic_shape: list[float] | None = Field(None, description="tensor for the macroscopic shape correction")
    spline_ps: bool = Field(True, description="interpolate pseudopotentials with cubic splines (better accuracy of the chemical shifts)")


class GIPAWEspressoInput(EspressoInput):
    """Pydantic model for the input of `gipaw.x.`"""

    inputgipaw: InputgipawNamelist = Field(default_factory=lambda: InputgipawNamelist())
