"""Class from which all cards should inherit.

For the moment this is just an alias for pydantic_espresso.utils.BaseModel,
but in the future we may want to add some functionality.
"""

from pydantic_espresso.utils import BaseModel as Card

__all__ = ["Card"]
