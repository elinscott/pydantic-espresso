"""Utility functions."""

import os
from typing import Any, Annotated
from pathlib import Path
from pydantic import BaseModel as _BaseModel, ConfigDict, Field

type PositiveFloat = Annotated[float, Field(gt=0)]
type PositiveInt = Annotated[int, Field(gt=0)]

INDENT = " " * 2

class BaseModel(_BaseModel):
    """Base model with pre-set configuration."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    def __init__(self, *args: Any, **kwargs: Any):
        field_names = list(self.__annotations__)
        if args:
            if len(args) > len(field_names):
                raise TypeError(f"Expected at most {len(field_names)} positional arguments, got {len(args)}")
            for name, value in zip(field_names, args):
                if name in kwargs:
                    raise TypeError(f"Got multiple values for argument '{name}'")
                kwargs[name] = value
        super().__init__(**kwargs)





def get_tmp_dir() -> Path:
    """Get the environment variable for the temporary directory."""
    return Path(os.getenv("ESPRESSO_TMPDIR", "./"))


def get_pseudo_dir() -> Path:
    """Get the environment variable for the pseudo directory."""
    return Path(os.getenv("ESPRESSO_PSEUDO", str(Path.home() / "espresso/pseudo")))
