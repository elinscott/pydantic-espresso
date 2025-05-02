"""Pydantic model for the input of `dynmat.x` version `qe-6.3MaX`.

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

    fildyn: str = Field("matdyn", description="input file containing the dynamical matrix")
    asr: Literal["no", "simple", "crystal", "one-dim", "zero-dim"] = Field(
        "no",
        description="Indicates the type of Acoustic Sum Rule imposed.  Allowed values:  Note that in certain cases, not all the rotational asr can be applied (e.g. if there are only 2 atoms in a molecule or if all the atoms are aligned, etc.).  In these cases the supplementary asr are canceled during the orthonormalization procedure (see below).  Finally, in all cases except 'no' a simple correction on the effective charges is performed (same as in the previous implementation).",
    )
    axis: int = Field(
        3, description="indicates the rotation axis for a 1D system (1=Ox, 2=Oy, 3=Oz)"
    )
    lperm: bool = Field(
        False,
        description="if .true. then calculate Gamma-point mode contributions to dielectric permittivity tensor",
    )
    lplasma: bool = Field(
        False,
        description="if .true. then calculate Gamma-point mode effective plasma frequencies, automatically triggers lperm = .true.",
    )
    filout: str = Field(
        "dynmat.out",
        description="output file containing phonon frequencies and normalized phonon displacements (i.e. eigenvectors divided by the square root of the mass and then normalized; they are not orthogonal)",
    )
    fileig: str | None = Field(
        None,
        description="output file containing phonon frequencies and eigenvectors of the dynamical matrix (they are orthogonal)",
    )
    filmol: str = Field("dynmat.mold", description="as above, in a format suitable for molden")
    filxsf: str = Field("dynmat.axsf", description="as above, in axsf format suitable for xcrysden")
    loto_2d: bool = Field(
        False, description="set to .true. to activate two-dimensional treatment of LO-TO splitting."
    )


class DYNMATEspressoInput(EspressoInput):
    """Pydantic model for the input of `dynmat.x.`"""

    input: InputNamelist = Field(default_factory=lambda: InputNamelist())
