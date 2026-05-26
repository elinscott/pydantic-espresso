"""Pydantic model for the input of `cppp.x` version `develop`.

This file has been generated automatically. Do not edit it manually.
"""

from pathlib import Path
from textwrap import dedent
from typing import Literal

from pydantic import Field

from pydantic_espresso.base import EspressoInput
from pydantic_espresso.namelist import Namelist


class InputppNamelist(Namelist):
    """Pydantic model for the `INPUTPP` namelist."""

    prefix: str = Field(
        "cp", description="basename prepended to cp.x output filenames: cp.evp, cp.pos ...."
    )
    fileout: str = Field("out", description="basename of the cppp.x output files")
    output: Literal["xsf", "xyz"] = Field(
        "xsf",
        description=dedent(
            """\
            A string describing the output format to be performed.
            - 'xsf': xcrysden format.
            - 'xyz': XMOL format."""
        ),
    )
    outdir: Path | None = Field(
        None,
        json_schema_extra={
            "conditional_default": [
                {
                    "when": "ESPRESSO_TMPDIR environment variable is set",
                    "value": "value of the ESPRESSO_TMPDIR environment variable",
                },
                {"when": None, "value": "'./'"},
            ],
        },
        description=dedent(
            """\
            directory containing the CP trajectory files (.evp .pos .cel ...) and restart files (
            .save ) to be processed"""
        ),
    )
    lcharge: bool = Field(
        False, description="OBSOLETE - no longer implemented. Use 'pp.x' instead."
    )
    lforces: bool = Field(
        False,
        description=dedent(
            """\
            This logical flag control the processing of forces.  .TRUE.  extract forces from
            trajectory files and write them to xcrysden file  .FALSE. do not process forces"""
        ),
    )
    ldynamics: bool = Field(
        True,
        description=dedent(
            """\
            This logical flag control the processing of atoms trajectory.  .TRUE.  process CP
            trajectory files and generate a trajectory file for xcrysden (.axsf)  .FALSE. do not
            process trajectory"""
        ),
    )
    lpdb: bool = Field(
        False,
        description=dedent(
            """\
            This logical flag control the generation of a pdb file.  .TRUE.  generate a pdb file
            containing positions and cell of the simulated system  .FALSE. do not generate pdb
            file"""
        ),
    )
    lrotation: bool = Field(
        False,
        description=dedent(
            """\
            This logical flag control the rotation of the cell  .TRUE.  rotate the system cell in
            space in order to have the a lattice parameter laying on the x axis, the b lattice
            parameter laying on the xy plane  .FALSE. do not rotate cell"""
        ),
    )
    np1: int = Field(
        1,
        description=dedent(
            """\
            Number of replicas of atomic positions along cell parameters. CURRENTLY DISABLED  If
            np1, np2, np3 are 1 or not specified, cppp.x does not replicate atomic positions in
            space.  If np1, np2, np3 are > 1 cppp.x replicates the atomic positions used in the
            simulation np1 times along 'a', np2 times along 'b', np3 times along 'c'."""
        ),
    )
    np2: int = Field(
        1,
        description=dedent(
            """\
            Number of replicas of atomic positions along cell parameters. CURRENTLY DISABLED  If
            np1, np2, np3 are 1 or not specified, cppp.x does not replicate atomic positions in
            space.  If np1, np2, np3 are > 1 cppp.x replicates the atomic positions used in the
            simulation np1 times along 'a', np2 times along 'b', np3 times along 'c'."""
        ),
    )
    np3: int = Field(
        1,
        description=dedent(
            """\
            Number of replicas of atomic positions along cell parameters. CURRENTLY DISABLED  If
            np1, np2, np3 are 1 or not specified, cppp.x does not replicate atomic positions in
            space.  If np1, np2, np3 are > 1 cppp.x replicates the atomic positions used in the
            simulation np1 times along 'a', np2 times along 'b', np3 times along 'c'."""
        ),
    )
    nframes: int = Field(
        1, description="number of MD step to be read to build the trajectory CURRENTLY MUST BE > 1"
    )
    ndr: int = Field(51, description="CP restart file number to post process")
    atomic_number: list[int] = Field(
        default_factory=list,
        description=dedent(
            """\
            Specify the atomic number of the species in CP trajectory and restart file.
            atomic_number(1)  specify the atomic number of the first specie atomic_number(2)
            specify the atomic number of the second specie .... (start = 1, end = ntyp)"""
        ),
    )


class CPPPInput(EspressoInput):
    """Pydantic model for the input of `cppp.x`."""

    inputpp: InputppNamelist = Field(default_factory=lambda: InputppNamelist())
