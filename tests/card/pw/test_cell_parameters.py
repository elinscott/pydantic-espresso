"""Test `pydantic_espresso.card.pw.cell_parameters`."""

from pydantic_espresso.card.pw.cell_parameters import CellParametersCard


def test_cell_parameters_card() -> None:
    """Test the CellParametersCard class."""
    card = CellParametersCard(
        vectors=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], units="alat"
    )

    assert card.vectors[0][0] == 1.0
    assert card.vectors[0][1] == 0.0
    assert card.vectors[0][2] == 0.0
    assert card.vectors[1][0] == 0.0
    assert card.vectors[1][1] == 1.0
    assert card.vectors[1][2] == 0.0
    assert card.vectors[2][0] == 0.0
    assert card.vectors[2][1] == 0.0
    assert card.vectors[2][2] == 1.0
    assert str(card) == "CELL_PARAMETERS (alat)\n  1.0 0.0 0.0\n  0.0 1.0 0.0\n  0.0 0.0 1.0"
