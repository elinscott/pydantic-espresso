"""Pydantic model for the input of `pw2wannier90.x` version `qe-7.4.1`.

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
    outdir: Path = Field(Path("value of the"), description="directory containing the input data, i.e. the same as in pw.x")
    seedname: str = Field("wannier", description="Seedname for the wannier90 calculation.")
    spin_component: str = Field("none", description="Spin component. 'up': spin up for collinear spin calculation 'down': spin down for collinear spin calculation 'none': for no-spin or non-collinear calculation")
    wan_mode: str = Field("standalone", description="standalone': for standalone execution of wannier90 'library': for wannier90 library mode")
    write_unk: bool = Field(False, description="if .TRUE. write the periodic part of the Bloch functions in real space for plotting the Wannier functions in wannier90.")
    reduce_unk: bool = Field(False, description="if .TRUE. reduce file-size (and resolution) of the real-space Bloch functions by a factor of reduce_unk_factor along each direction. Only relevant if write_unk = .true.")
    reduce_unk_factor: int | None = Field(None, description="The reduction factor per direction for reduce_unk. Default 2 means a reduction of 2x2x2 = 8 of the total number of grid points. Only relevant if write_unk = .true.")
    wvfn_formatted: bool = Field(False, description="if .TRUE. write the wavefunctions in Fortran formatted form. Only relevant if write_unk = .true.")
    write_amn: bool = Field(True, description="Set to .false. if A(k) is not required.")
    scdm_proj: bool = Field(False, description="Set to .true. to compute amn using the SCDM projection.")
    scdm_entanglement: str = Field("isolated", description="isolated': use SCDM for isolated bands. 'erfc': use erfc function as the SCDM occupation for entanglement bands. 'gaussian': use gaussian function as the SCDM occupation for entanglement bands.")
    scdm_mu: float | None = Field(None, description="Set to the chemical potential for the SCDM occupation. Only relevant if scdm_entanglement = 'erfc' or 'gaussian'.")
    scdm_sigma: float | None = Field(None, description="Set to the smearing for the SCDM occupation. Only relevant if scdm_entanglement = 'erfc' or 'gaussian'.")
    atom_proj: bool = Field(False, description="Set to .true. to compute amn using the pseudo-atomic wavefunctions from pseudopotentials as the initial projection.")
    atom_proj_ext: bool = Field(False, description="Set to .true. to use the external pseudo-atomic wavefunctions from the files stored in atom_proj_dir as the initial projection. Only relevant if atom_proj = .true.")
    atom_proj_dir: str | None = Field(None, description="Set to the directory containing the external pseudo-atomic wavefunctions. The file names should be of the form SPECIES.dat, where SPECIES is the species name of the atom. For more details, see the wannier90 user guide and examples. Only relevant if atom_proj_ext = .true.")
    atom_proj_ortho: bool = Field(True, description="Set to .true. to orthonormalize the pseudo-atomic wavefunctions before computing the inner product between Bloch states and the pseudo-atomic wavefunctions. It is recommended to keep this to .true., set it to .false. only if you know what you are doing. Only relevant if atom_proj = .true.")
    write_mmn: bool = Field(True, description="Set to .false. if M(k,b) is not required.")
    write_spn: bool = Field(False, description="Set to .true. to write out the matrix elements of spin operator S between Bloch states (non-collinear spin calculation only).")
    spn_formatted: bool = Field(False, description="Set to .true. to write spn data as a formatted file. Only relevant if write_spn = .true.")
    write_uHu: bool = Field(False, description="Set to .true. to write out the matrix elements of < unk+b1 | Hk | umk+b2 >.")
    uHu_formatted: bool = Field(False, description="Set to .true. to write uHu data as a Fortran formatted file. Only relevant if write_uHu = .true.")
    write_uIu: bool = Field(False, description="Set to .true. to write out the matrix elements of < unk+b1 | umk+b2 >.")
    uIu_formatted: bool = Field(False, description="Set to .true. to write uIu data as a Fortran formatted file. Only relevant if write_uIu = .true.")
    write_sHu: bool = Field(False, description="Set to .true. to write out the matrix elements of < unk | s H | umk+b >, which is used in the Ryoo's method to compute spin Hall conductivity. For more details, see the wannier90 user guide and examples.")
    sHu_formatted: bool = Field(False, description="Set to .true. to write sHu data as a Fortran formatted file. Only relevant if write_sHu = .true.")
    write_sIu: bool = Field(False, description="Set to .true. to write out the matrix elements of < unk | s | umk+b >, which is used in the Ryoo's method to compute spin Hall conductivity. For more details, see the wannier90 user guide and examples.")
    sIu_formatted: bool = Field(False, description="Set to .true. to write sIu data as a Fortran formatted file. Only relevant if write_sIu = .true.")
    write_unkg: bool = Field(False, description="Set to .true. to write the first few Fourier components of the periodic parts of the Bloch functions.")
    irr_bz: bool = Field(False, description="Set to .true. to use irreducible BZ for computing amn/mmn/eig files. To differentiate from the standard full BZ case, the files will use the extension names iamn/immn/ieig, respectively. For more details, see the wannier90 user guide and examples.")
    write_dmn: bool = Field(False, description="Set to .true. to construct symmetry-adapted Wannier functions.")
    read_sym: bool = Field(False, description="Set to .true. to customize symmetry operations to be used in symmetry-adapted mode. When read_sym = .true., an additional input seedname.sym is required. Only relevant if write_dmn = .true.")


class PW2WANNIER90EspressoInput(EspressoInput):
    """Pydantic model for the input of `pw2wannier90.x.`"""

    inputpp: InputppNamelist = Field(default_factory=lambda: InputppNamelist())
