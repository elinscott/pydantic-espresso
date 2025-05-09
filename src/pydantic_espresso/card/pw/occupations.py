"""Pydantic model for the OCCUPATION card in `pw.x` input files."""

# ruff: noqa

from typing import Annotated
from pydantic import Field
from pydantic_espresso.utils import INDENT

type PositiveFloat0to1 = Annotated[float, Field(ge=0, le=1)]
type PositiveFloat0to2 = Annotated[float, Field(ge=0, le=2)]
