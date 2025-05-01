"""Base model for the input of different versions of `Wannier90`."""

from typing import Any
from pydantic import BaseModel as _BaseModel, ConfigDict, Field


class BaseModel(_BaseModel):
    """Base model with pre-set configuration."""

    model_config = ConfigDict(validate_assignment=True, extra="forbid")


class Namelist(BaseModel):

    def __str__(self) -> str:
        """Return the string representation of the class for Quantum ESPRESSO.
        
        Only display those keywords that have been set by the user.
        """

        out = f"&{self.__class__.__name__.replace('Namelist', '').lower()}\n"
        for k, v in self.__class__.model_fields.items():
            if v is None:
                continue
            if k in self.model_fields_set:
                out += f"    {k} = {_sanitize_value(getattr(self, k))}\n"
        out += "&end\n"
        return out 


class EspressoInput(BaseModel):
    def __str__(self) -> str:
        namelist_strs = []
        for k in self.__class__.model_fields.keys():
            namelist_str = str(getattr(self, k))
            if namelist_str.count('\n') > 2:
                namelist_strs.append(namelist_str)
        return "\n".join(namelist_strs)
    
    
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