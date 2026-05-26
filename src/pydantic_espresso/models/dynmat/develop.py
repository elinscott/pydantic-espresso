"""Pydantic model for the input of `dynmat.x` version `develop`.

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

    fildyn: str = Field("matdyn", description="input file containing the dynamical matrix")
    asr: Literal["no", "simple", "crystal", "one-dim", "zero-dim"] = Field(
        "no",
        description=dedent(
            """\
            Indicates the type of Acoustic Sum Rule imposed.  Allowed values:  Note that in certain
            cases, not all the rotational asr can be applied (e.g. if there are only 2 atoms in a
            molecule or if all the atoms are aligned, etc.).  In these cases the supplementary asr
            are canceled during the orthonormalization procedure (see below).  Finally, in all
            cases except 'no' a simple correction on the effective charges is performed (same as in
            the previous implementation).
            - 'no': no Acoustic Sum Rules imposed.
            - 'simple': previous implementation of the asr used (3 translational asr imposed by
              correction of the diagonal elements of the dynamical matrix).
            - 'crystal': 3 translational asr imposed by optimized correction of the dyn. matrix
              (projection).
            - 'one-dim': 3 translational asr + 1 rotational asr imposed by optimized correction of
              the dyn. mat. (the rotation axis is the direction of periodicity; it will work only
              if this axis considered is one of the Cartesian axis).
            - 'zero-dim': 3 translational asr + 3 rotational asr imposed by optimized correction of
              the dyn. mat."""
        ),
    )
    remove_interaction_blocks: bool = Field(
        False,
        description=dedent(
            """\
            If .true. lines and rows corresponding to atoms that are not displaced are set to 0.
            This can be used for ph.x calculations with nat_todo set in ph.x, to remove the
            interaction between the diplaced and fixed parts of the system."""
        ),
    )
    axis: int = Field(
        3, description="indicates the rotation axis for a 1D system (1=Ox, 2=Oy, 3=Oz)"
    )
    lperm: bool = Field(
        False,
        description=dedent(
            """\
            if .true. then calculate Gamma-point mode contributions to dielectric permittivity
            tensor"""
        ),
    )
    lplasma: bool = Field(
        False,
        description=dedent(
            """\
            if .true. then calculate Gamma-point mode effective plasma frequencies, automatically
            triggers lperm = .true."""
        ),
    )
    filout: str = Field(
        "dynmat.out",
        description=dedent(
            """\
            output file containing phonon frequencies and normalized phonon displacements (i.e.
            eigenvectors divided by the square root of the mass and then normalized; they are not
            orthogonal)"""
        ),
    )
    fileig: str | None = Field(
        None,
        description=dedent(
            """\
            output file containing phonon frequencies and eigenvectors of the dynamical matrix
            (they are orthogonal)"""
        ),
    )
    filmol: str = Field("dynmat.mold", description="as above, in a format suitable for molden")
    filxsf: str = Field("dynmat.axsf", description="as above, in axsf format suitable for xcrysden")
    loto_2d: bool = Field(
        False, description="set to .true. to activate two-dimensional treatment of LO-TO splitting."
    )
    el_ph_nsig: int | None = Field(
        None,
        description=dedent(
            """\
            The number of double-delta smearing values used in an electron-phonon coupling
            calculation."""
        ),
    )
    el_ph_sigma: Annotated[float | None, Quantity(units="Ry", dimensionality="energy")] = Field(
        None,
        description=dedent(
            """\
            The spacing of double-delta smearing values used in an electron-phonon coupling
            calculation."""
        ),
    )
    q: tuple[float, float, float] = Field(
        (0.0, 0.0, 0.0),
        description=dedent(
            """\
            calculate LO modes (add non-analytic terms) along the direction q (Cartesian axis)"""
        ),
    )
    amass: Annotated[list[float] | None, Quantity(units="amu", dimensionality="mass")] = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "amass(nt) <= 0.0",
                    "value": (
                        "read from file fildyn (amass_(nt); divided by amu_ry for non-XML files)"
                    ),
                },
                {"when": None, "value": "0.0"},
            ],
        },
        description="mass for each atom type (start = 1, end = ntyp)",
    )


class DYNMATInput(EspressoInput):
    """Pydantic model for the input of `dynmat.x`."""

    input: InputNamelist = Field(default_factory=lambda: InputNamelist())
