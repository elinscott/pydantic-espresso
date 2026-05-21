"""Pydantic model for the input of `matdyn.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from typing import Annotated, Literal

from pydantic import Field

from pydantic_espresso.models.template import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class InputNamelist(Namelist):
    """Pydantic model for the `INPUT` namelist."""

    flfrc: str | None = Field(
        None,
        description=(
            "File produced by q2r containing force constants (needed) It is the same as in the "
            "input of q2r.x (+ the .xml extension if the dynamical matrices produced by ph.x were "
            "in xml format). No default value: must be specified."
        ),
    )
    asr: Literal["no", "simple", "crystal", "all", "one-dim", "zero-dim"] = Field(
        "no",
        description=(
            "Indicates the type of Acoustic Sum Rule imposed.  Allowed values:  Note that in "
            "certain cases, not all the rotational asr can be applied (e.g. if there are only 2 "
            "atoms in a molecule or if all the atoms are aligned, etc.). In these cases the "
            "supplementary asr are cancelled during the orthonormalization procedure (see below)."
        ),
    )
    huang: bool | None = Field(
        None,
        description=(
            "if .true. 15 Huang conditions for vanishing stress tensor are included in asr = 'all'."
        ),
    )
    dos: bool = Field(
        False,
        description=(
            "if .true. calculate phonon Density of States (DOS) using tetrahedra and a uniform "
            "q-point grid (see below) NB: may not work properly in noncubic materials  if .false. "
            "calculate phonon bands from the list of q-points supplied in input"
        ),
    )
    nk1: int | None = Field(None, description="")
    nk2: int | None = Field(None, description="")
    nk3: int | None = Field(None, description="")
    deltaE: Annotated[float, Quantity(units="cm-1", dimensionality="energy")] = Field(  # noqa: N815
        1.0,
        description=(
            "energy step for DOS calculation: from min to max phonon energy (used if ndos, see "
            "below, is not specified)"
        ),
    )
    ndos: int | None = Field(
        None,
        description=(
            "number of energy steps for DOS calculations (default: calculated from deltaE if not "
            "specified)"
        ),
    )
    degauss: Annotated[float, Quantity(units="cm-1", dimensionality="energy")] = Field(
        0.0, description="DOS broadening in cm-1  A value of 0 means use tetrahedra."
    )
    fldos: str = Field(
        "matdyn.dos",
        description=(
            "output file for dos. the dos is in states/cm-1 plotted vs omega in cm(-1) and is "
            "normalised to 3*nat, i.e. the number of phonons"
        ),
    )
    flfrq: str = Field("matdyn.freq", description="output file for frequencies")
    flvec: str = Field(
        "matdyn.modes",
        description=(
            "output file for normalized phonon displacements. The normalized phonon displacements "
            "are the eigenvectors divided by the square root of the mass, then normalized. As such "
            "they are not orthogonal."
        ),
    )
    fleig: str | None = Field(
        None,
        description=(
            "output file for phonon eigenvectors. The phonon eigenvectors are the eigenvectors of "
            "the dynamical matrix. They are orthogonal."
        ),
    )
    fldyn: str | None = Field(
        None, description="output file for dynamical matrix (' ' means it is not written)"
    )
    l1: int | None = Field(None, description="")
    l2: int | None = Field(None, description="")
    l3: int | None = Field(None, description="")
    ntyp: int | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "ntyp == 0", "value": "ntyp of the original cell (ntyp_blk)"},
                {"when": None, "value": "0"},
            ],
        },
        description="number of atom types in the supercell",
    )
    readtau: bool = Field(
        False,
        description=(
            "read  atomic positions of the supercell from input (used to specify different masses)"
        ),
    )
    fltau: str | None = Field(
        None,
        description=(
            "write atomic positions of the supercell to file fltau (if fltau = ' ', do not write)"
        ),
    )
    la2F: bool = Field(False, description="if .true. interpolates also the el-ph coefficients")  # noqa: N815
    q_in_band_form: bool = Field(
        False,
        description=(
            "if .true. the q points are given in band form: only the first and last point of one "
            "or more lines are given. See below."
        ),
    )
    q_in_cryst_coord: bool = Field(
        False, description="if .true. input q points are in crystalline coordinates"
    )
    eigen_similarity: bool = Field(
        False,
        description=(
            "use similarity of the displacements to order frequencies  NB: You cannot use this "
            "option with the symmetry analysis of the modes."
        ),
    )
    fd: bool = Field(
        False, description="if .true. the ifc come from the finite displacement calculation"
    )
    na_ifc: bool = Field(
        False,
        description=(
            "add non analitic contributions to the interatomic force constants if finite "
            "displacement method is used (as in Wang et al. PRB 85, 224303 (2012) "
            "(https://journals.aps.org/prb/abstract/10.1103/PhysRevB.85.224303)) [to be used in "
            "conjunction with fd.x]"
        ),
    )
    nosym: bool = Field(
        False, description="if .true., no symmetry and no time reversal are imposed"
    )
    loto_2d: bool = Field(
        False, description="set to .true. to activate two-dimensional treatment of LO-TO splitting"
    )
    loto_disable: bool = Field(False, description="if .true. do not apply LO-TO splitting for q=0")
    read_lr: bool | None = Field(
        None,
        description=(
            "if .true. read also long-range force constants when they exist in force constant "
            "file. This is required when enforcing asr = 'all' for infrared-active solids."
        ),
    )
    write_frc: bool | None = Field(
        None,
        description=(
            "if .true. write force constants with asr imposed into file. The filename would be "
            "flfrc+'.matdyn'. The long-range part of force constants will be not written."
        ),
    )
    amass: Annotated[list[float] | None, Quantity(units="amu", dimensionality="mass")] = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {"when": "amass(it) == 0.0", "value": "masses read from force-constant file flfrc"},
                {"when": None, "value": "0.0"},
            ],
        },
        description="masses of atoms in the supercell, one per atom type (start = 1, end = ntyp)",
    )


class MATDYNEspressoInput(EspressoInput):
    """Pydantic model for the input of `matdyn.x`."""

    input: InputNamelist = Field(default_factory=lambda: InputNamelist())
