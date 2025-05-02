"""Pydantic model for the input of `neb.x` version `qe-6.1.0`.

This file has been generated automatically. Do not edit it manually.
"""

# ruff: noqa

from pathlib import Path
from pydantic import Field, field_validator
from typing import Literal
from pydantic_espresso.models.template import EspressoInput, Namelist
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir





class NEBEspressoInput(EspressoInput):
    """Pydantic model for the input of `neb.x.`"""


