"""Pydantic model for the input of `q2r.x` version `qe-7.2rc`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputNamelist(Namelist):
    """Pydantic model for the `Input` namelist."""

    fildyn: str | None = Field(None, description="Input file name (must be specified).  'fildyn'0 contains information on the q-point grid  'fildyn'1-N contain force constants C_n = C(q_n), where n = 1,...N, where N is the number of q-points in the irreducible brillouin zone.  Normally this should be the same as specified on input to the phonon code.  In the non collinear/spin-orbit case the files produced by ph.x are in .xml format. In this case fildyn is the same as in the phonon code + the .xml extension.")
    flfrc: str | None = Field(None, description="Output file containing the IFC in real space (must be specified)")
    zasr: Literal["no", "simple", "crystal", "one-dim", "zero-dim"] = Field("no", description="Indicates the type of Acoustic Sum Rules used for the Born effective charges.  Allowed values:  Note that in certain cases, not all the rotational asr can be applied (e.g. if there are only 2 atoms in a molecule or if all the atoms are aligned, etc.). In these cases the supplementary asr are cancelled during the orthonormalization procedure (see below).")
    loto_2d: bool | None = Field(None, description="set to .true. to activate two-dimensional treatment of LO-TO splitting.")
    write_lr: bool = Field(, description="set to .true. to write long-range IFC into q2r IFC file. This is required when enforcing asr='all' for infrared- active solids in matdyn. An additional column will be written for long-range part of IFC for text format, while a tag named IFC_LR will be created for xml format.")


class Q2REspressoInput(EspressoInput):
    """Pydantic model for the input of `q2r.x.`"""

    input: InputNamelist = Field(default_factory=InputNamelist)
