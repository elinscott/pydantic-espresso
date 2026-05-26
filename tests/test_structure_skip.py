"""Test that ``STRUCTURE``-typed variables are skipped from generated models."""

import inspect

from pydantic_espresso.models import ph
from pydantic_espresso.models.ph import develop as ph_develop
from pydantic_espresso.namelist import Namelist


def _collect_namelist_classes() -> list[type[Namelist]]:
    """Return every ``Namelist`` subclass defined in ``ph.develop``."""
    classes: list[type[Namelist]] = []
    for _, obj in inspect.getmembers(ph_develop, inspect.isclass):
        if obj is Namelist:
            continue
        if issubclass(obj, Namelist):
            classes.append(obj)
    return classes


def test_ph_module_importable() -> None:
    """The ``ph`` namespace package is importable."""
    assert hasattr(ph, "__path__")


def test_dvscf_star_and_drho_star_absent() -> None:
    """``dvscf_star`` and ``drho_star`` are STRUCTURE-typed and must be skipped."""
    classes = _collect_namelist_classes()
    assert classes, "expected at least one Namelist subclass in ph.develop"
    forbidden = {"dvscf_star", "drho_star"}
    for cls in classes:
        present = set(cls.model_fields) & forbidden
        assert not present, f"{cls.__name__} unexpectedly contains {present}"


def test_phinput_does_not_expose_skipped_fields() -> None:
    """The top-level ``PHInput`` does not surface skipped variables either."""
    forbidden = {"dvscf_star", "drho_star"}
    assert not (set(ph_develop.PHInput.model_fields) & forbidden)
