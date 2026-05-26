"""Pydantic model for the OCCUPATION card in `pw.x` input files."""

# ruff: noqa

from typing import Annotated, TypeAlias
from pydantic import Field
from pydantic_espresso.utils import INDENT

PositiveFloat0to1: TypeAlias = Annotated[float, Field(ge=0, le=1)]
PositiveFloat0to2: TypeAlias = Annotated[float, Field(ge=0, le=2)]
