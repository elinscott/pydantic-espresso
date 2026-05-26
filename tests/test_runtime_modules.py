"""Tests for small runtime-module gaps (namelist, base, utils, models, cards)."""

from pathlib import Path

import numpy as np
import pytest

from pydantic_espresso import utils
from pydantic_espresso.models import get_module, versions
from pydantic_espresso.models.pw.cards.constraints import DistanceConstraint
from pydantic_espresso.models.pw.develop import ControlNamelist, PWInput


def test_namelist_str_renders_set_fields() -> None:
    """``Namelist.__str__`` emits a Fortran namelist with only the user-set fields."""
    nl = ControlNamelist(prefix="mycalc", tprnfor=True)
    rendered = str(nl)
    lines = rendered.splitlines()
    assert lines[0] == "&CONTROL"
    assert lines[-1] == "/"
    assert '  prefix = "mycalc"' in lines
    assert "  tprnfor = .true." in lines
    # An unset field is not rendered.
    assert "calculation" not in rendered


def test_namelist_str_renders_false_bool() -> None:
    """A user-set False boolean renders as ``.false.``."""
    nl = ControlNamelist(tprnfor=False)
    assert "  tprnfor = .false." in str(nl)


def test_namelist_str_renders_numeric() -> None:
    """A user-set numeric field renders via ``str(value)`` (the non-bool/str branch)."""
    nl = ControlNamelist(nstep=42)
    assert "  nstep = 42" in str(nl)


def test_espresso_input_str_includes_namelists_and_cards() -> None:
    """``EspressoInput.__str__`` renders set namelists and card text."""
    inp = PWInput(
        cell_parameters={"unit": "alat", "vectors": np.identity(3)},
        atomic_positions={
            "unit": "alat",
            "positions": [{"species": "H", "position": [0.0, 0.0, 0.0]}],
        },
        k_points={"kind": "gamma"},
    )
    # A namelist with a user-set field surfaces in the rendering.
    inp.control.calculation = "bands"
    rendered = str(inp)
    assert "&CONTROL" in rendered
    assert "bands" in rendered
    # The cards render their own text.
    assert "CELL_PARAMETERS" in rendered
    assert "ATOMIC_POSITIONS" in rendered


def test_get_tmp_dir_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without the env var, ``get_tmp_dir`` falls back to ``./``."""
    monkeypatch.delenv("ESPRESSO_TMPDIR", raising=False)
    assert utils.get_tmp_dir() == Path("./")


def test_get_tmp_dir_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """With the env var set, ``get_tmp_dir`` returns that path."""
    monkeypatch.setenv("ESPRESSO_TMPDIR", "/scratch/tmp")
    assert utils.get_tmp_dir() == Path("/scratch/tmp")


def test_get_pseudo_dir_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without the env var, ``get_pseudo_dir`` falls back to the home-relative default."""
    monkeypatch.delenv("ESPRESSO_PSEUDO", raising=False)
    assert utils.get_pseudo_dir() == Path.home() / "espresso/pseudo"


def test_get_pseudo_dir_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """With the env var set, ``get_pseudo_dir`` returns that path."""
    monkeypatch.setenv("ESPRESSO_PSEUDO", "/opt/pseudos")
    assert utils.get_pseudo_dir() == Path("/opt/pseudos")


def test_get_module_develop_alias() -> None:
    """``get_module("develop", "pw")`` resolves the development module with ``PWInput``."""
    module = get_module("develop", "pw")
    assert hasattr(module, "PWInput")


def test_get_module_by_version() -> None:
    """``get_module`` accepts a concrete ``Version`` from the enumerated list."""
    module = get_module(versions[0], "pw")
    assert hasattr(module, "PWInput")


def test_get_module_version_string() -> None:
    """A bare version string is coerced to a ``Version`` and resolved."""
    module = get_module(str(versions[0]), "pw")
    assert hasattr(module, "PWInput")


def test_get_module_unknown_executable_raises() -> None:
    """An unknown executable raises ``ModuleNotFoundError``."""
    with pytest.raises(ModuleNotFoundError):
        get_module("develop", "not_an_executable")


def test_constraint_str_renders_kind_and_parameters() -> None:
    """``Constraint.__str__`` renders the kind followed by the flattened parameters."""
    constraint = DistanceConstraint(atom_indices=(1, 2))
    assert str(constraint) == "distance 1 2"
