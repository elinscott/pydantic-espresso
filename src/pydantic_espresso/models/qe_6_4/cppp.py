"""Pydantic model for the input of `cppp.x` version `qe-6.4`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir


class InputppNamelist(Namelist):
    """Pydantic model for the `Inputpp` namelist."""

    prefix: str = Field(
        "cp", description="basename prepended to cp.x output filenames: cp.evp, cp.pos ...."
    )
    fileout: str = Field("out", description="basename of the cppp.x output files")
    output: str = Field(
        "xsf",
        description="a string describing the output format to be performed, allowed values: 'xsf', 'grd', 'xyz'  xsf     xcrysden format grd     GRD gaussian 3D grid format xyz     XMOL format",
    )
    outdir: Path = Field(
        Path("./"),
        description="directory containing the CP trajectory files (.evp .pos .cel ...) and restart files ( .save ) to be processed",
    )
    lcharge: bool = Field(
        False,
        description="This logical flag control the processing of charge density.  .TRUE.  generate output file containing charge density. The file format is controlled by the 'output' parameter  .FALSE. do not generate charge density file",
    )
    lforces: bool = Field(
        False,
        description="This logical flag control the processing of forces.  .TRUE.  extract forces from trajectory files and write them to xcrysden file  .FALSE. do not proces forces",
    )
    ldynamics: bool = Field(
        False,
        description="This logical flag control the processing of atoms trajectory.  .TRUE.  process CP trajectory files and generate a trajectory file for xcrysden (.axsf)  .FALSE. do not process trajectory",
    )
    lpdb: bool = Field(
        False,
        description="This logical flag control the generation of a pdb file.  .TRUE.  generate a pdb file containing positions and cell of the simulated system  .FALSE. do not generate pdb file",
    )
    lrotation: bool = Field(
        False,
        description="This logical flag control the rotation of the cell  .TRUE.  rotate the system cell in space in order to have the a lattice parameter laying on the x axis, the b lattice parameter laying on the xy plane  .FALSE. do not rotate cell",
    )
    nframes: int = Field(1, description="number of MD step to be read to build the trajectory")
    ndr: int = Field(51, description="CP restart file number to post process")
    charge_density: str = Field(
        "full",
        description="specify the component of the charge density to plot, allowed values:  'full'   print the full electronic charge 'spin'   print the spin polarization (for LSD calculations)",
    )
    state: str | None = Field(
        None, description="specify the Kohn-Sham state to plot, example: 'KS_1"
    )
    lbinary: bool = Field(
        True,
        description="specify the file format of the wave function files to be read and plotted",
    )


class CPPPEspressoInput(EspressoInput):
    """Pydantic model for the input of `cppp.x.`"""

    inputpp: InputppNamelist = Field(default_factory=lambda: InputppNamelist())
