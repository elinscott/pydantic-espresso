"""Pydantic model for the input of `postahc.x` version `qe-7.3`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputNamelist(Namelist):
    """Pydantic model for the `Input` namelist."""


    ahc_dir: str | None = Field(None, description="Directory where the binary files are located.")
    nk: int | None = Field(None, description="Number of k points. Must be identical to that of the preceding SCF or NSCF run.")
    nbnd: int | None = Field(None, description="Number of bands. Must be identical to nbnd of the preceding SCF or NSCF run.")
    nat: int | None = Field(None, description="Number of atoms. Must be identical to nat of the preceding pw.x and ph.x runs.")
    nq: int | None = Field(None, description="Number of q points. Must be identical to that of the preceding ph.x run with electron_phonon='ahc'.")
    ahc_nbnd: int | None = Field(None, description="Number of bands for which the electron self-energy is to be computed. Must be identical to ahc_nbnd of the ph.x run with electron_phonon='ahc'.")
    ahc_nbndskip: int = Field(0, description="Number of bands to exclude when computing the self-energy. Must be identical to ahc_nbndskip of the ph.x run with electron_phonon='ahc'.")
    flvec: str | None = Field(None, description="File containing the normalized phonon displacements written by matdyn.x.")
    eta: float | None = Field(None, description="Magnitude of the small imaginary component included to smooth the energy denominators, in Ry.")
    temp_kelvin: float | None = Field(None, description="Temperature in Kelvins at which the electron self-energy is calculated.")
    efermi: float | None = Field(None, description="Fermi energy of the electrons in Ry.")
    skip_upperfan: bool = Field(False, description="If .true., skip calculation of the upper Fan self-energy. If .false., ahc_upfan_iq#.bin files must be present in ahc_dir.")
    skip_dw: bool = Field(False, description="If .true., skip calculation of the Debye-Waller self-energy. If .false., ahc_dw.bin file must be present in ahc_dir.")


class POSTAHCEspressoInput(EspressoInput):
    """Pydantic model for the input of `postahc.x.`"""

    input: InputNamelist = Field(default_factory=lambda: InputNamelist())
