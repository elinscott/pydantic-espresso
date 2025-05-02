"""Pydantic model for the input of `wannier2pw.x` version `e6621af`.

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

    prefix: str | None = Field(None, description="prefix of files saved by program pw.x")
    outdir: Path = Field(
        Path("value of the"),
        description="directory containing the input data, i.e. the same as in pw.x",
    )
    seedname: str = Field("wannier", description="Seedname, same as for the wannier90 calculation.")
    spin_component: str = Field(
        "none",
        description="Spin component. 'up': spin up for collinear spin calculation 'down': spin down for collinear spin calculation 'none': for no-spin or non-collinear calculation",
    )
    hubbard: bool = Field(
        False,
        description="Set to .true. to use the interface between Wannier90 and PW. This will use the Wannier functions as a basis to build the Hubbard projectors for DFT+U.",
    )
    exclude_ks_bands: int = Field(
        0,
        description="This variable is used only when hubbard = .true. This variable specifies how many lowest-lying Kohn-Sham bands must be excluded from the summation when building the Wannier functions using Umn matrices from Wannier90 (those bands which are below the energy where the wannierization starts)",
    )
    wan2hub: list[bool] | None = Field(
        None,
        description="Set wan2hub(i) to .true. for those Wannier functions (i) which you want to use as a basis to build the Hubbard projectors for DFT+U calculations. Note that the total number of selected Wannier functions must match the expected number of basis functions (e.g. 5 for d states, 3 for p states, etc per atom). In order to selected the Wannier functions, one has to inspect the output of Wannier90 calculations and see in which oredr the Wannier functions were generated.",
    )


class WANNIER2PWEspressoInput(EspressoInput):
    """Pydantic model for the input of `wannier2pw.x.`"""

    inputpp: InputppNamelist = Field(default_factory=lambda: InputppNamelist())
