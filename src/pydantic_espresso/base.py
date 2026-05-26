"""Base model for the input of different programs and versions of `Quantum ESPRESSO`."""

from pydantic_espresso.namelist import Namelist
from pydantic_espresso.utils import INDENT, BaseModel


class EspressoInput(BaseModel):
    """Template pydantic model for the input of a Quantum ESPRESSO executable.

    Construction raises the usual :class:`pydantic.ValidationError` when inputs
    are missing or invalid; pass the caught error to
    :func:`pydantic_espresso.errors.explain` for a readable, recursive summary.
    """

    def __str__(self) -> str:
        out = ""
        for k in self.__class__.model_fields.keys():
            attr = getattr(self, k, None)
            if k == "occupations":
                out += occupations_to_str(attr)
            elif isinstance(attr, Namelist):
                namelist_str = str(attr)
                if namelist_str.count("\n") > 1:
                    out += "\n\n" + namelist_str
            elif isinstance(attr, list):
                if attr:
                    raise ValueError()
            elif attr is None:
                continue
            else:
                out += "\n\n" + str(attr)

        return out.strip("\n")


def occupations_to_str(occupations: list[list[float]] | None) -> str:
    """Convert a list of occupations to a string with max 10 entries per line."""
    out = ""
    if occupations is None:
        return out
    out += "\n\nOCCUPATIONS"
    for occupation_by_spin in occupations:
        for stride in [
            occupation_by_spin[i : i + 10] for i in range(0, len(occupation_by_spin), 10)
        ]:
            out += f"\n{INDENT}" + " ".join(str(x) for x in stride)
    return out
