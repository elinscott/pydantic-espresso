"""Pydantic model for the input of `matdyn.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from textwrap import dedent
from typing import Annotated, Literal

from pydantic import Field

from pydantic_espresso.base import EspressoInput
from pydantic_espresso.namelist import Namelist
from pydantic_espresso.quantity import Quantity


class InputNamelist(Namelist):
    """Pydantic model for the `INPUT` namelist."""

    flfrc: str | None = Field(
        None,
        description=dedent(
            """\
            File produced by q2r containing force constants (needed) It is the same as in the input
            of q2r.x (+ the .xml extension if the dynamical matrices produced by ph.x were in xml
            format). No default value: must be specified."""
        ),
    )
    asr: Literal["no", "simple", "crystal", "all", "one-dim", "zero-dim"] = Field(
        "no",
        description=dedent(
            """\
            Indicates the type of Acoustic Sum Rule imposed.  Allowed values:  Note that in certain
            cases, not all the rotational asr can be applied (e.g. if there are only 2 atoms in a
            molecule or if all the atoms are aligned, etc.). In these cases the supplementary asr
            are cancelled during the orthonormalization procedure (see below).
            - 'no': no Acoustic Sum Rules imposed.
            - 'simple': previous implementation of the asr used (3 translational asr imposed by
              correction of the diagonal elements of the force constants matrix).
            - 'crystal': 3 translational asr imposed by optimized correction of the force constants
              (projection).
            - 'all': 3 translational asr + 3 rotational asr + 15 Huang conditions for vanishing
              stress tensor, imposed by optimized correction of the force constants (projection).
              Remember to set write_lr = .true. to write long-range force constants into file when
              running q2r and set read_lr = .true. when running matdyn in the case of
              infrared-active solids. (See npj Comput Mater 8, 236 (2022)).
            - 'one-dim': 3 translational asr + 1 rotational asr imposed by optimized correction of
              the dyn. mat. (the rotation axis is the direction of periodicity; it will work only
              if this axis considered is one of the Cartesian axis).
            - 'zero-dim': 3 translational asr + 3 rotational asr imposed by optimized correction of
              the dyn. mat."""
        ),
    )
    huang: bool = Field(
        True,
        description=dedent(
            """\
            if .true. 15 Huang conditions for vanishing stress tensor are included in asr =
            'all'."""
        ),
    )
    dos: bool = Field(
        False,
        description=dedent(
            """\
            if .true. calculate phonon Density of States (DOS) using tetrahedra and a uniform
            q-point grid (see below) NB: may not work properly in noncubic materials  if .false.
            calculate phonon bands from the list of q-points supplied in input"""
        ),
    )
    nk1: int = Field(
        0,
        description=dedent(
            """\
            uniform q-point grid for DOS calculation (includes q=0) (must be specified if dos =
            .true., ignored otherwise)"""
        ),
    )
    nk2: int = Field(
        0,
        description=dedent(
            """\
            uniform q-point grid for DOS calculation (includes q=0) (must be specified if dos =
            .true., ignored otherwise)"""
        ),
    )
    nk3: int = Field(
        0,
        description=dedent(
            """\
            uniform q-point grid for DOS calculation (includes q=0) (must be specified if dos =
            .true., ignored otherwise)"""
        ),
    )
    deltaE: Annotated[float, Quantity(units="cm-1", dimensionality="energy")] = Field(  # noqa: N815
        1.0,
        description=dedent(
            """\
            energy step for DOS calculation: from min to max phonon energy (used if ndos, see
            below, is not specified)"""
        ),
    )
    ndos: int | None = Field(
        None,
        description=dedent(
            """\
            number of energy steps for DOS calculations (default: calculated from deltaE if not
            specified)"""
        ),
    )
    degauss: Annotated[float, Quantity(units="cm-1", dimensionality="energy")] = Field(
        0.0, description="DOS broadening in cm-1  A value of 0 means use tetrahedra."
    )
    fldos: str = Field(
        "matdyn.dos",
        description=dedent(
            """\
            output file for dos. the dos is in states/cm-1 plotted vs omega in cm(-1) and is
            normalised to 3*nat, i.e. the number of phonons"""
        ),
    )
    flfrq: str = Field("matdyn.freq", description="output file for frequencies")
    flvec: str = Field(
        "matdyn.modes",
        description=dedent(
            """\
            output file for normalized phonon displacements. The normalized phonon displacements
            are the eigenvectors divided by the square root of the mass, then normalized. As such
            they are not orthogonal."""
        ),
    )
    fleig: str | None = Field(
        None,
        description=dedent(
            """\
            output file for phonon eigenvectors. The phonon eigenvectors are the eigenvectors of
            the dynamical matrix. They are orthogonal."""
        ),
    )
    fldyn: str | None = Field(
        None, description="output file for dynamical matrix (' ' means it is not written)"
    )
    l1: int = Field(
        1,
        description=dedent(
            """\
            supercell lattice vectors are original cell vectors times l1, l2, l3 respectively
            (ignored if at specified)"""
        ),
    )
    l2: int = Field(
        1,
        description=dedent(
            """\
            supercell lattice vectors are original cell vectors times l1, l2, l3 respectively
            (ignored if at specified)"""
        ),
    )
    l3: int = Field(
        1,
        description=dedent(
            """\
            supercell lattice vectors are original cell vectors times l1, l2, l3 respectively
            (ignored if at specified)"""
        ),
    )
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
        description=dedent(
            """\
            read  atomic positions of the supercell from input (used to specify different masses)"""
        ),
    )
    fltau: str | None = Field(
        None,
        description=dedent(
            """\
            write atomic positions of the supercell to file fltau (if fltau = ' ', do not write)"""
        ),
    )
    la2F: bool = Field(False, description="if .true. interpolates also the el-ph coefficients")  # noqa: N815
    q_in_band_form: bool = Field(
        False,
        description=dedent(
            """\
            if .true. the q points are given in band form: only the first and last point of one or
            more lines are given. See below."""
        ),
    )
    q_in_cryst_coord: bool = Field(
        False, description="if .true. input q points are in crystalline coordinates"
    )
    eigen_similarity: bool = Field(
        False,
        description=dedent(
            """\
            use similarity of the displacements to order frequencies  NB: You cannot use this
            option with the symmetry analysis of the modes."""
        ),
    )
    fd: bool = Field(
        False, description="if .true. the ifc come from the finite displacement calculation"
    )
    na_ifc: bool = Field(
        False,
        description=dedent(
            """\
            add non analitic contributions to the interatomic force constants if finite
            displacement method is used (as in Wang et al. PRB 85, 224303 (2012)
            (https://journals.aps.org/prb/abstract/10.1103/PhysRevB.85.224303)) [to be used in
            conjunction with fd.x]"""
        ),
    )
    nosym: bool = Field(
        False, description="if .true., no symmetry and no time reversal are imposed"
    )
    loto_2d: bool = Field(
        False, description="set to .true. to activate two-dimensional treatment of LO-TO splitting"
    )
    loto_disable: bool = Field(False, description="if .true. do not apply LO-TO splitting for q=0")
    read_lr: bool = Field(
        False,
        description=dedent(
            """\
            if .true. read also long-range force constants when they exist in force constant file.
            This is required when enforcing asr = 'all' for infrared-active solids."""
        ),
    )
    write_frc: bool = Field(
        False,
        description=dedent(
            """\
            if .true. write force constants with asr imposed into file. The filename would be
            flfrc+'.matdyn'. The long-range part of force constants will be not written."""
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


class MATDYNInput(EspressoInput):
    """Pydantic model for the input of `matdyn.x`."""

    input: InputNamelist = Field(default_factory=lambda: InputNamelist())
