"""Test per-option ``<opt>`` text appears in field descriptions."""

from pydantic_espresso.models.pw.develop import ControlNamelist


def test_restart_mode_description_lists_both_opts() -> None:
    """Both ``from_scratch`` and ``restart`` opts appear as bullet entries."""
    description = ControlNamelist.model_fields["restart_mode"].description
    assert description is not None
    assert "'from_scratch':" in description
    assert "'restart':" in description


def test_restart_mode_description_has_newlines() -> None:
    """The description contains literal newlines between bullets."""
    description = ControlNamelist.model_fields["restart_mode"].description
    assert description is not None
    assert "\n" in description


def test_restart_mode_description_has_intro() -> None:
    """The ``<options><info>`` intro precedes the bullets."""
    description = ControlNamelist.model_fields["restart_mode"].description
    assert description is not None
    assert "Available options are:" in description


def test_calculation_description_no_empty_bullets() -> None:
    """An opts-with-no-text case (PW's ``calculation``) emits no stray empty entries."""
    description = ControlNamelist.model_fields["calculation"].description
    assert description is not None
    # No bullet that introduces an empty quoted value.
    assert "''" not in description
    assert "- ''" not in description
