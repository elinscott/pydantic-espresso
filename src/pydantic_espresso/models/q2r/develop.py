"""Pydantic model for the input of `q2r.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from textwrap import dedent
from typing import Literal

from pydantic import Field

from pydantic_espresso.base import EspressoInput
from pydantic_espresso.namelist import Namelist


class InputNamelist(Namelist):
    """Pydantic model for the `INPUT` namelist."""

    fildyn: str = Field(
        ...,
        description=dedent(
            """\
            Input file name (must be specified).  'fildyn'0 contains information on the q-point
            grid  'fildyn'1-N contain force constants C_n = C(q_n), where n = 1,...N, where N is
            the number of q-points in the irreducible brillouin zone.  Normally this should be the
            same as specified on input to the phonon code.  In the non collinear/spin-orbit case
            the files produced by ph.x are in .xml format. In this case fildyn is the same as in
            the phonon code + the .xml extension."""
        ),
    )
    flfrc: str = Field(
        ..., description="Output file containing the IFC in real space (must be specified)"
    )
    zasr: Literal["no", "simple", "crystal", "one-dim", "zero-dim"] = Field(
        "no",
        description=dedent(
            """\
            Indicates the type of Acoustic Sum Rules used for the Born effective charges.  Allowed
            values:  Note that in certain cases, not all the rotational asr can be applied (e.g. if
            there are only 2 atoms in a molecule or if all the atoms are aligned, etc.). In these
            cases the supplementary asr are cancelled during the orthonormalization procedure (see
            below).
            - 'no': no Acoustic Sum Rules imposed.
            - 'simple': previous implementation of the asr used (3 translational asr imposed by
              correction of the diagonal elements of the force-constants matrix).
            - 'crystal': 3 translational asr imposed by optimized correction of the IFC
              (projection).
            - 'one-dim': 3 translational asr + 1 rotational asr imposed by optimized correction of
              the IFC (the rotation axis is the direction of periodicity; it will work only if this
              axis considered is one of the cartesian axis).
            - 'zero-dim': 3 translational asr + 3 rotational asr imposed by optimized correction of
              the IFC."""
        ),
    )
    loto_2d: bool = Field(
        False, description="set to .true. to activate two-dimensional treatment of LO-TO splitting."
    )
    write_lr: bool = Field(
        False,
        description=dedent(
            """\
            set to .true. to write long-range IFC into q2r IFC file. This is required when
            enforcing asr='all' for infrared- active solids in matdyn. An additional column will be
            written for long-range part of IFC for text format, while a tag named IFC_LR will be
            created for xml format."""
        ),
    )


class Q2RInput(EspressoInput):
    """Pydantic model for the input of `q2r.x`."""

    input: InputNamelist = Field(...)
