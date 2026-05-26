"""Utility functions."""

import os
from pathlib import Path
from typing import Annotated, TypeAlias

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field

PositiveFloat: TypeAlias = Annotated[float, Field(gt=0)]
PositiveInt: TypeAlias = Annotated[int, Field(gt=0)]
INDENT = " " * 2


class BaseModel(_BaseModel):
    """Base model with pre-set configuration."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")


def get_tmp_dir() -> Path:
    """Get the environment variable for the temporary directory."""
    return Path(os.getenv("ESPRESSO_TMPDIR", "./"))


def get_pseudo_dir() -> Path:
    """Get the environment variable for the pseudo directory."""
    return Path(os.getenv("ESPRESSO_PSEUDO", str(Path.home() / "espresso/pseudo")))
