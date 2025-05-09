"""Pydantic model for the input of `matdyn.x` version `qe-7.2-omp5-1.0`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputNamelist(Namelist):
    """Pydantic model for the `INPUT` namelist."""

    flfrc: str | None = Field(
        None,
        description="File produced by q2r containing force constants (needed) It is the same as in the input of q2r.x (+ the .xml extension if the dynamical matrices produced by ph.x were in xml format). No default value: must be specified.",
    )
    asr: Literal["no", "simple", "crystal", "all", "one-dim", "zero-dim"] = Field(
        "no",
        description="Indicates the type of Acoustic Sum Rule imposed.  Allowed values:  Note that in certain cases, not all the rotational asr can be applied (e.g. if there are only 2 atoms in a molecule or if all the atoms are aligned, etc.). In these cases the supplementary asr are cancelled during the orthonormalization procedure (see below).",
    )
    huang: bool | None = Field(
        None,
        description="if .true. 15 Huang conditions for vanishing stress tensor are included in asr = 'all'.",
    )
    dos: bool | None = Field(
        None,
        description="if .true. calculate phonon Density of States (DOS) using tetrahedra and a uniform q-point grid (see below) NB: may not work properly in noncubic materials  if .false. calculate phonon bands from the list of q-points supplied in input (default)",
    )
    deltaE: float | None = Field(None, description="energy step, in cm")
    ndos: int | None = Field(
        None,
        description="number of energy steps for DOS calculations (default: calculated from deltaE if not specified)",
    )
    degauss: float | None = Field(None, description="DOS broadening in cm")
    fldos: str | None = Field(None, description="output file for dos (default:")
    flfrq: str | None = Field(None, description="output file for frequencies (default:")
    flvec: str | None = Field(
        None, description="output file for normalized phonon displacements (default:"
    )
    fleig: str | None = Field(None, description="output file for phonon eigenvectors (default:")
    fldyn: str | None = Field(
        None, description="output file for dynamical matrix (default: ' ' i.e. not written)"
    )
    ntyp: int | None = Field(
        None,
        description="number of atom types in the supercell (default: ntyp of the original cell)",
    )
    readtau: bool | None = Field(
        None,
        description="read  atomic positions of the supercell from input (used to specify different masses) (default:",
    )
    fltau: str | None = Field(None, description="write atomic positions of the supercell to file")
    la2F: bool | None = Field(
        None, description="if .true. interpolates also the el-ph coefficients"
    )
    q_in_band_form: bool | None = Field(
        None,
        description="if .true. the q points are given in band form: only the first and last point of one or more lines are given. See below. (default:",
    )
    q_in_cryst_coord: bool | None = Field(
        None, description="if .true. input q points are in crystalline coordinates (default:"
    )
    eigen_similarity: bool | None = Field(
        None, description="use similarity of the displacements to order frequencies  (default:"
    )
    fd: bool | None = Field(
        None, description="if .true. the ifc come from the finite displacement calculation"
    )
    na_ifc: bool | None = Field(
        None,
        description="add non analitic contributions to the interatomic force constants if finite displacement method is used (as in Wang et al. PRB 85, 224303 (2012) (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.85.224303)) [to be used in conjunction with fd.x]",
    )
    nosym: bool | None = Field(
        None, description="if .true., no symmetry and no time reversal are imposed"
    )
    loto_2d: bool | None = Field(
        None, description="set to .true. to activate two-dimensional treatment of LO-TO splitting"
    )
    loto_disable: bool | None = Field(
        None, description="if .true. do not apply LO-TO splitting for q=0 (default:"
    )
    read_lr: bool | None = Field(
        None,
        description="if .true. read also long-range force constants when they exist in force constant file. This is required when enforcing asr = 'all' for infrared-active solids.",
    )
    write_frc: bool | None = Field(
        None,
        description="if .true. write force constants with asr imposed into file. The filename would be flfrc+'.matdyn'. The long-range part of force constants will be not written.",
    )


class MATDYNEspressoInput(EspressoInput):
    """Pydantic model for the input of `matdyn.x`"""

    input: InputNamelist = Field(default_factory=lambda: InputNamelist())
