"""Pydantic model for the card in `pw.x` input files."""

prebuilt_cards = {
    "atomic_species": {
        "type": "list[AtomicSpecies]",
        "default": "Field(default_factory=list)",
        "import_str": "from pydantic_espresso.card.pw.atomic_species import AtomicSpecies",
    },
    "atomic_positions": {
        "type": "AtomicPositionsCard",
        "default": "Field(...)",
        "import_str": "from pydantic_espresso.card.pw.atomic_positions import AtomicPositionsCard",
    },
    "k_points": {
        "type": "KPointsCard",
        "default": 'Field(discriminator="kind")',
        "import_str": "from pydantic_espresso.card.pw.k_points import KPointsCard",
    },
    "additional_k_points": {
        "type": "KPointsCard | None",
        "default": 'Field(None, discriminator="kind")',
        "import_str": "from pydantic_espresso.card.pw.k_points import KPointsCard",
    },
    "cell_parameters": {
        "type": "CellParametersCard",
        "default": "Field(...)",
        "import_str": "from pydantic_espresso.card.pw.cell_parameters import CellParametersCard",
    },
    "constraints": {
        "type": "list[Constraint]",
        "default": "Field(default_factory=list)",
        "import_str": "from pydantic_espresso.card.pw.constraints import Constraint",
    },
    "occupations": {
        "type": "tuple[list[PositiveFloat0to2]] | tuple[list[PositiveFloat0to1], "
        "list[PositiveFloat0to1]] | None",
        "default": "Field(None)",
        "import_str": "from pydantic_espresso.card.pw.occupations import PositiveFloat0to1, "
        "PositiveFloat0to2",
    },
    "atomic_velocities": {
        "type": "list[AtomicVelocity]",
        "default": "Field(default_factory=list)",
        "import_str": "from pydantic_espresso.card.pw.atomic_velocities import AtomicVelocity",
    },
    "atomic_forces": {
        "type": "list[AtomicForce]",
        "default": "Field(default_factory=list)",
        "import_str": "from pydantic_espresso.card.pw.atomic_forces import AtomicForce",
    },
    "solvents": {
        "type": "SolventsCard | SolventsLRCard | None",
        "default": "Field(None)",
        "import_str": "from pydantic_espresso.card.pw.solvents import SolventsCard, SolventsLRCard",
    },
    "hubbard": {
        "type": "HubbardCard | None",
        "default": "Field(None)",
        "import_str": "from pydantic_espresso.card.pw.hubbard import HubbardCard",
    },
}
