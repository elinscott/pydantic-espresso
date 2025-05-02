"""Pydantic model for the input of `ph.x` version `qe-4.1.1`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputphNamelist(Namelist):
    """Pydantic model for the `Inputph` namelist."""

    outdir: Path = Field(Path("./"), description="Scratch directory.")
    prefix: str = Field(
        "pwscf",
        description="Prepended to input/output filenames; must be the same used in the calculation of unperturbed system.",
    )
    niter_ph: int = Field(100, description="Maximum number of iterations in a scf step.")
    tr2_ph: float = Field(1e-12, description="Threshold for self-consistency.")
    alpha_mix: list[float] | None = Field(
        None,
        description="Mixing factor (for each iteration) for updating the scf potential:  vnew(in) = alpha_mix*vold(out) + (1-alpha_mix)*vold(in)",
    )
    nmix_ph: int = Field(4, description="Number of iterations used in potential mixing.")
    iverbosity: int = Field(0, description="0 = short output 1 = verbose output")
    reduce_io: bool = Field(False, description="Reduce I/O to the strict minimum.")
    max_seconds: float = Field(
        1.0e7, description="Maximum allowed run time before the job stops smoothly."
    )
    fildyn: str = Field("matdyn", description="File where the dynamical matrix is written.")
    fildrho: str | None = Field(
        None, description="File where the charge density responses are written."
    )
    fildvscf: str | None = Field(
        None,
        description="File where the the potential variation is written (for later use in electron-phonon calculation).",
    )
    epsil: bool = Field(
        False,
        description="If .true. in a q=0 calculation for a non metal the macroscopic dielectric constant of the system is computed. Do not set epsil to .true. if you have a metallic system or q/=0: the code will complain and stop.",
    )
    lrpa: bool = Field(
        False,
        description="If .true. the dielectric constant is calculated at the RPA level with DV_xc=0.",
    )
    lnoloc: bool = Field(
        False,
        description="If .true. the dielectric constant is calculated without local fields, i.e. by setting DV_H=0 and DV_xc=0.",
    )
    trans: bool = Field(
        True,
        description="If .true. the phonons are computed. If trans .and. epsil are .true. effective charges are calculated.",
    )
    lraman: bool = Field(
        False,
        description="If .true. calculate non-resonant Raman coefficients using second-order response as in: M. Lazzeri and F. Mauri, Phys. Rev. Lett. 90, 036401 (2003).",
    )
    recover: bool = Field(False, description="If .true. restart from an interrupted run.")
    elph: bool = Field(
        False,
        description="If .true. electron-phonon lambda coefficients are computed.  For metals only, requires gaussian smearing.  If elph .and. trans, the lambdas are calculated in the same run, using the same k-point grid for phonons and lambdas If elph.and..not.trans, the lambdas are calculated using previously saved DeltaVscf in fildvscf, previously saved dynamical matrix, and the present punch file. This allows the use of a different (larger) k-point grid.",
    )
    zue: bool = Field(
        False,
        description="If .true. in a q=0 calculation for a non metal the effective charges are computed from the phonon density responses. Note that if trans.and.epsil effective charges are calculated using a different algorithm. The results should be the same within numerical noise.",
    )
    elop: bool = Field(False, description="If .true. calculate electro-optic tensor.")
    fpol: bool = Field(
        False,
        description="If .true. calculate dynamic polarizabilities ( experimantal stage, see example33 for calculation of methane ).",
    )
    lnscf: bool = Field(
        False,
        description="If .true. the run makes first a pw.x nscf calculation. The pw.x data file should not be produced using 'calculation='phonon'' in this case.",
    )
    ldisp: bool = Field(
        False,
        description="If .true. the run calculates phonons for a grid of q-points specified by nq1, nq2, nq3 - for direct calculation of the entire phonon dispersion. The pw.x data file should not be produced using 'calculation='phonon'' in this case.",
    )
    nogg: bool = Field(
        False,
        description="If .true. disable the 'gamma_gamma' trick used to speed up calculations at q=0 (phonon wavevector) if the sum over the Brillouin Zone includes k=0 only. The gamma_gamma trick exploits symmetry and acoustic sum rule to reduce the number of linear response calculations to the strict minimum, as it is done in code phcg.x. This option MUST BE USED if a run with ph.x is to be followed by a run with d3.x for third-order terms calculation.",
    )


class PHEspressoInput(EspressoInput):
    """Pydantic model for the input of `ph.x.`"""

    inputph: InputphNamelist = Field(default_factory=lambda: InputphNamelist())
