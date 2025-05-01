"""Pydantic model for the input of `pw2bgw.x` version `e6621af`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pydantic import Field
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInputTemplate


class PW2BGWEspressoInput(EspressoInputTemplate):
    """Pydantic model for the input of `pw2bgw.x.`"""

    prefix: str = Field(..., description="prefix of files saved by program pw.x")
    outdir: str = Field(" './'
         ", description="the scratch directory where the massive data-files are written")
    real_or_complex: int = Field( 2
         , description="1 | 2")
    symm_type: Literal["'cubic'", "'hexagonal'"] = Field(" 'cubic'
         ", description="Options are:")
    wfng_flag: bool = Field(False, description="write wavefunctions in G-space to BerkeleyGW WFN file")
    wfng_file: str = Field(" 'WFN'
         ", description="name of BerkeleyGW WFN output file. Not used if")
    wfng_kgrid: bool = Field(False, description="overwrite k-grid parameters in BerkeleyGW WFN file. If pw.x input file contains an explicit list of k-points, the k-grid parameters in the output of pw.x will be set to zero. Since sigma and absorption in BerkeleyGW both need to know the k-grid dimensions, we patch these parameters into BerkeleyGW WFN file")
    wfng_nk1: int = Field( 0
         , description="number of k-points along b_1 reciprocal lattice vector. Not used if")
    wfng_nk2: int = Field( 0
         , description="number of k-points along b_2 reciprocal lattice vector. Not used if")
    wfng_nk3: int = Field( 0
         , description="number of k-points along b_3 reciprocal lattice vector. Not used if")
    wfng_dk1: float = Field( 0.0
         , description="k-grid offset (0.0 unshifted, 0.5 shifted by half a grid step) along b_1 reciprocal lattice vector. Not used if")
    wfng_dk2: float = Field( 0.0
         , description="k-grid offset (0.0 unshifted, 0.5 shifted by half a grid step) along b_2 reciprocal lattice vector. Not used if")
    wfng_dk3: float = Field( 0.0
         , description="k-grid offset (0.0 unshifted, 0.5 shifted by half a grid step) along b_3 reciprocal lattice vector. Not used if")
    wfng_occupation: bool = Field(False, description="overwrite occupations in BerkeleyGW WFN file")
    wfng_nvmin: int = Field( 0
         , description="index of the lowest occupied band (normally = 1). Not used if")
    wfng_nvmax: int = Field( 0
         , description="index of the highest occupied band (normally = number of occupied bands). Not used if")
    rhog_flag: bool = Field(False, description="write charge density in G-space to BerkeleyGW RHO file. Only used for the GPP model in sigma code in BerkeleyGW")
    rhog_file: str = Field(" 'RHO'
         ", description="name of BerkeleyGW RHO output file. Only used for the GPP model in sigma code in BerkeleyGW. Not used if")
    rhog_nvmin: int = Field( 0
         , description="index of the lowest band used for calculation of charge density. This is needed if one wants to exclude semicore states from charge density used for the GPP model in sigma code in BerkeleyGW. Make sure to include the same k-points as in scf calculation. Self-consistent charge density is used if rhog_nvmin = 0 and rhog_nvmax = 0. Not used if")
    rhog_nvmax: int = Field( 0
         , description="index of the highest band used for calculation of charge density. See description of rhog_nvmin for more details")
    vxcg_flag: bool = Field(False, description="write local part of exchange-correlation potential in G-space to BerkeleyGW VXC file. Only used in sigma code in BerkeleyGW, it is recommended to use")
    vxcg_file: str = Field(" 'VXC'
         ", description="name of BerkeleyGW VXC output file. Only used in sigma code in BerkeleyGW, it is recommended to use")
    vxc0_flag: bool = Field(False, description="write Vxc(G = 0) to text file. Only for testing, not required for BerkeleyGW")
    vxc0_file: str = Field(" 'vxc0.dat'
         ", description="name of output text file for Vxc(G = 0). Only for testing, not required for BerkeleyGW. Not used if")
    vxc_flag: bool = Field(False, description="write matrix elements of exchange-correlation potential to text file. Only used in sigma code in BerkeleyGW")
    vxc_file: str = Field(" 'vxc.dat'
         ", description="name of output text file for Vxc matrix elements. Only used in sigma code in BerkeleyGW. Not used if")
    vxc_integral: str = Field(" 'g'
         ", description="'g' | 'r' 'g' to compute matrix elements of exchange-correlation potential in G-space. 'r' to compute matrix elements of the local part of exchange-correlation potential in R-space. It is recommended to use 'g'. Not used if")
    vxc_diag_nmin: int = Field( 0
         , description="minimum band index for diagonal Vxc matrix elements. Not used if")
    vxc_diag_nmax: int = Field( 0
         , description="maximum band index for diagonal Vxc matrix elements. Not used if")
    vxc_offdiag_nmin: int = Field( 0
         , description="minimum band index for off-diagonal Vxc matrix elements. Not used if")
    vxc_offdiag_nmax: int = Field( 0
         , description="maximum band index for off-diagonal Vxc matrix elements. Not used if")
    vxc_zero_rho_core: bool = Field(True, description="set to .TRUE. to zero out NLCC or to .FALSE. to keep NLCC when computing exchange-correlation potential. This flag has no effect for pseudopotentials without NLCC.")
    vscg_flag: bool = Field(False, description="write local part of self-consistent potential in G-space to BerkeleyGW VSC file. Only used in SAPO code in BerkeleyGW")
    vscg_file: str = Field(" 'VSC'
         ", description="name of BerkeleyGW VSC output file. Only used in SAPO code in BerkeleyGW. Not used if")
    vkbg_flag: bool = Field(False, description="write Kleinman-Bylander projectors in G-space to BerkeleyGW VKB file. Only used in SAPO code in BerkeleyGW")
    vkbg_file: str = Field(" 'VKB'
         ", description="name of BerkeleyGW VKB output file. Only used in SAPO code in BerkeleyGW. Not used if")
