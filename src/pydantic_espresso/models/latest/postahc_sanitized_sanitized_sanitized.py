"""Pydantic model for the input of `postahc.x` version `latest`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import BaseModel


class InputNamelist(BaseModel):
   """Pydantic model for the `Input` namelist."""

    prefix: str = Field("pwscf", description="Prepended to input/output filenames; must be the same used in the calculation of unperturbed system.")
    outdir: str = Field("value of the", description="Directory containing input, output, and scratch files; must be the same as specified in the calculation of the unperturbed system.")
    ahc_dir: str | None = Field(None, description="Directory where the binary files are located.")
    use_irr_q: bool = Field(False, description="If .true., assume that the q points are on the irreducible grid. In this case, the data in ahc_dir must have been actually generated from a calculation on an irreducible q grid. Off-diagonal self-energies cannot be computed if use_irr_q = .true.")
    ahc_nbnd: int | None = Field(None, description="Number of bands for which the electron self-energy is to be computed. Must be identical to ahc_nbnd of the ph.x run with electron_phonon='ahc'.")
    ahc_nbndskip: int = Field(0, description="Number of bands to exclude when computing the self-energy. Must be identical to ahc_nbndskip of the ph.x run with electron_phonon='ahc'.")
    flvec: str | None = Field(None, description="File containing the normalized phonon displacements written by matdyn.x.")
    eta_eV: float | None = Field(None, description="Magnitude of the small imaginary component included to smooth the energy denominators, in eV.")
    temp_kelvin: float | None = Field(None, description="Temperature in Kelvins at which the electron self-energy is calculated.")
    efermi_eV: float | None = Field(None, description="Fermi energy of the electrons in eV.")
    ahc_win_min_eV: float | None = Field(None, description="Lower bound of active AHC window for the lower Fan term in eV.")
    ahc_win_max_eV: float | None = Field(None, description="Upper bound of active AHC window for the lower Fan term in eV.")
    skip_upper: bool = Field(False, description="If .true., skip calculation of the upper Fan self-energy. Also, truncate the Debye-Waller self-energy to include only the low-energy band contribution. (Corresponds to the second term (lower Fan + lower DW) of Eq. (G1-revised) of J.-M. Lihm and C.-H. Park, PRX 12, 039901(E) (2022).) If .false., calculate the contribution of both the high-energy and low-energy bands. In this case, ahc_upfan_iq#.bin files must be present in ahc_dir.")
    skip_dw: bool = Field(False, description="If .true., skip calculation of the Debye-Waller self-energy. If .false., ahc_dw.bin file must be present in ahc_dir.")
    adiabatic: bool = Field(False, description="If .true., use the adiabatic approximation when computing the Fan self-energy by ignoring the phonon frequency in the denominator. This approximation is known to be inaccurate and even divergent in some materials (S. PoncÃ© et al., J. Chem. Phys. 143, 102813 (2015)). Therefore, this keyword should be used only for experimental or debugging purposes.")


class POSTAHCEspressoInput(BaseModel):
    """Pydantic model for the input of `postahc.x.`"""

    Input: InputNamelist
