"""Pydantic model for `Quantum ESPRESSO` namelists."""

from typing import Any

from pydantic_espresso.utils import INDENT, BaseModel


class Namelist(BaseModel):
    """Template pydantic model for a namelist in Quantum ESPRESSO input files."""

    def __str__(self) -> str:
        """Return the string representation of the class for Quantum ESPRESSO.

        Only display those keywords that have been set by the user.
        """
        out = f"&{self.__class__.__name__.replace('Namelist', '').upper()}\n"
        for k, v in self.__class__.model_fields.items():
            if v is None:
                continue
            if k in self.model_fields_set:
                out += f"{INDENT}{k} = {_sanitize_value(getattr(self, k))}\n"
        out += "/"
        return out


def _sanitize_value(value: Any) -> str:
    """Convert a value to a string for printing in the format expected by `Quantum ESPRESSO`."""
    if isinstance(value, bool):
        if value:
            return ".true."
        else:
            return ".false."
    elif isinstance(value, str):
        return f'"{value}"'
    else:
        return str(value)
