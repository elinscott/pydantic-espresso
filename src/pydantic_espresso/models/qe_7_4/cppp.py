"""Pydantic model for the input of `cppp.x` version `qe-7.4`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Annotated, Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputppNamelist(Namelist):
    """Pydantic model for the `Inputpp` namelist."""

    prefix: str = Field("cp", description="basename prepended to cp.x output filenames: cp.evp, cp.pos ....")
    fileout: str = Field("out", description="basename of the cppp.x output files")
    output: str = Field("xsf", description="a string describing the output format to be performed, allowed values: 'xsf', 'xyz'  xsf     xcrysden format xyz     XMOL format")
    outdir: Path = Field(./, description="directory containing the CP trajectory files (.evp .pos .cel ...) and restart files ( .save ) to be processed")
    lcharge: bool = Field(False, description="OBSOLETE - no longer implemented. Use 'pp.x' instead.")
    lforces: bool = Field(False, description="This logical flag control the processing of forces.  .TRUE.  extract forces from trajectory files and write them to xcrysden file  .FALSE. do not process forces")
    ldynamics: bool = Field(True, description="This logical flag control the processing of atoms trajectory.  .TRUE.  process CP trajectory files and generate a trajectory file for xcrysden (.axsf)  .FALSE. do not process trajectory")
    lpdb: bool = Field(False, description="This logical flag control the generation of a pdb file.  .TRUE.  generate a pdb file containing positions and cell of the simulated system  .FALSE. do not generate pdb file")
    lrotation: bool = Field(False, description="This logical flag control the rotation of the cell  .TRUE.  rotate the system cell in space in order to have the a lattice parameter laying on the x axis, the b lattice parameter laying on the xy plane  .FALSE. do not rotate cell")
    nframes: int = Field(1, description="number of MD step to be read to build the trajectory CURRENTLY MUST BE > 1")
    ndr: int = Field(51, description="CP restart file number to post process")


class CPPPEspressoInput(EspressoInput):
    """Pydantic model for the input of `cppp.x.`"""

    inputpp: InputppNamelist = Field(default_factory=InputppNamelist)
