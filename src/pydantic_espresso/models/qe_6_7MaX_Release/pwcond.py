"""Pydantic model for the input of `pwcond.x` version `qe-6.7MaX-Release`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputcondNamelist(Namelist):
    """Pydantic model for the `INPUTCOND` namelist."""

    outdir: Path | None = Field(None, description="temporary directory (as in PWscf)")
    prefixt: str | None = Field(
        None,
        description="prefix for the file (as in PWscf) containing all the regions (left lead + scatt. reg. + right lead)",
    )
    prefixl: str | None = Field(
        None, description="prefix for the file containing only the        left lead"
    )
    prefixs: str | None = Field(
        None, description="prefix for the file containing the scattering region"
    )
    prefixr: str | None = Field(
        None, description="prefix for the file containing only the right lead"
    )
    tran_prefix: str = Field(
        "none",
        description="if tran_prefix is specified the program will save partial results of a transmission calculation (ikind .GE. 1) in a specific directory (outdir/tran_prefix.cond_save)",
    )
    max_seconds: float | None = Field(
        None,
        description="jobs stops after max_seconds elapsed time (wallclock time). It can be enabled only if tran_prefix is specified.",
    )
    recover: bool = Field(
        False,
        description="restarts a previously interrupted transmission calculation (only if tran_prefix was specified). It can also be used to gather partial results from a calculation that was split by using start_e,last_e and/or start_k,last_k (see corresponding keywords).",
    )
    band_file: str | None = Field(None, description="file on which the complex bands are saved")
    tran_file: str | None = Field(None, description="file where the transmission is written")
    save_file: str | None = Field(
        None,
        description="file where the data necessary for PWCOND are written so that no prefix files of PW are longer needed",
    )
    fil_loc: str | None = Field(
        None, description="file on/from which the 2D eigenvalue problem data are saved/read"
    )
    lwrite_cond: bool | None = Field(
        None, description="if .t. save the data necessary for PWCOND in save_file"
    )
    loop_ek: bool | None = Field(
        None, description="if .t. the energy loop is outside the k-point loop"
    )
    lread_cond: bool | None = Field(
        None, description="if .t. read the data necessary for PWCOND from save_file"
    )
    lwrite_loc: bool | None = Field(
        None, description="if .t. save 2D eigenvalue problem result in fil_loc"
    )
    lread_loc: bool | None = Field(
        None, description="if .t. read 2D eigenvalue problem result from fil_loc"
    )
    ikind: int | None = Field(
        None,
        description="The kind of conductance calculation:  ikind=0  - just complex band structure (CBS) calculation  ikind=1  - conductance calculation with identical left and right leads  ikind=2  - conductance calculation with different left and right leads",
    )
    iofspin: int | None = Field(
        None, description="spin index for which the calculations are performed"
    )
    tk_plot: int | None = Field(
        None, description="if > 0, plot T(kx,ky) at each energy in the region [tk_plot x full BZ]"
    )
    llocal: bool | None = Field(
        None, description="if .t. calculations are done with only local part of PP"
    )
    bdl: float | None = Field(
        None,
        description="right boundary of the left lead (left one is supposed to be at 0) (in units of lattice parameter 'alat' defined in the scf run)",
    )
    bds: float | None = Field(
        None,
        description="right boundary of the scatt. reg. (left one is at 0 if prefixs is used and = bdl if prefixt is used) (in units of lattice parameter 'alat' defined in the scf run)",
    )
    bdr: float | None = Field(
        None,
        description="right boundary of the right lead (left one is at 0 if prefixr is used and = bds if prefixt is used) (in units of lattice parameter 'alat' defined in the scf run)",
    )
    nz1: int | None = Field(
        None, description="the number of subslabs in the slab (to calculate integrals)"
    )
    energy0: float | None = Field(None, description="initial energy")
    denergy: float | None = Field(
        None, description="energy step (if denergy=0.0 the energy is read from the list)"
    )
    nenergy: int | None = Field(
        None,
        description="number of energies  WARNING: the energy in input file is given in eV taken from Ef, and denergy should be negative",
    )
    start_e: int = Field(
        1,
        description="if start_e > 1, the scattering problem is solved only for those energies with index between start_e and last_e in the energy list.  NOTE: start_e <= last_e and start_e <= nenergy must be satisfied",
    )
    last_e: int | None = Field(
        None,
        description="index of the last energy to be computed. If last_e > nenergy, then last_e will be automatically set to nenergy.",
    )
    start_k: int = Field(
        1,
        description="if start_k > 1, the scattering problem is solved only for those k-points with index between start_k and last_k in the k-point list. In order to recover the full transmission (i.e. integrated over the full Brillouin Zone) at the end, perform the partial runs specifying a value for tran_prefix (the restart directory), then put all the partial transmission files 'transmission_k#_e#' inside a unique restart directory and run pwcond.x with recover=.TRUE. (without specifying any value for start_k and last_k).  NOTE: start_k <= last_k must be satisfied and start_k must also not be greater than the actual number of k-point in the list (if you compute the grid automatically by specifying the grid size and shifts, you can use kpoints.x to check that number).",
    )
    last_k: int | None = Field(
        None,
        description="index of the last k-point to be computed. If last_k is bigger than the actual number of points in the list, then it will be set to that number.",
    )
    ecut2d: float | None = Field(None, description="2-D cutoff")
    ewind: float | None = Field(
        None, description="the energy window for reduction of 2D plane wave basis set (in XY)"
    )
    epsproj: float | None = Field(None, description="accuracy of 2D basis set reduction")
    orbj_in: float | None = Field(
        None, description="the initial orbital for projecting the transmission"
    )
    orbj_fin: float | None = Field(
        None, description="the final orbital for projecting the transmission"
    )


class PWCONDEspressoInput(EspressoInput):
    """Pydantic model for the input of `pwcond.x`"""

    inputcond: InputcondNamelist = Field(default_factory=lambda: InputcondNamelist())
