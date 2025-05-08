"""Pydantic model for the OCCUPATION card in `pw.x` input files."""

# ruff: noqa

from typing import Annotated
from pydantic import Field
from pydantic_espresso.utils import INDENT

type PositiveFloat0to2 = Annotated[float, Field(ge=0, le=2)]

class OccupationsList(list[PositiveFloat0to2]):

    def __str__(self) -> str:
        """Return a string of the occupations list with at most 10 entries per line."""
        lines = []
        for i in range(0, len(self), 10):
            line = INDENT + " ".join([str(x) for x in self[i:i + 10]])
            lines.append(line)
        return "\n".join(lines)

