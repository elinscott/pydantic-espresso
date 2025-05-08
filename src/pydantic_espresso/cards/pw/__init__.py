"""Pydantic model for the cards in `pw.x` input files."""

prebuilt_cards = {'atomic_species': {'type': 'list[AtomicSpecies]', 'default': 'Field(default_factory=list)', 'import_str': 'from pydantic_espresso.cards.pw.atomic_species import AtomicSpecies'},
                  'atomic_positions': {'type': 'AtomicPositionsCard', 'default': 'Field(default_factory=AtomicPositionsCard)', 'import_str': 'from pydantic_espresso.cards.pw.atomic_positions import AtomicPositionsCard'},
                  'k_points': {'field': 'KPointsCard', 'default': 'Field(...)', 'import_str': 'pydantic_espresso.cards.pw.k_points import KPointsCard'},
                  'additional_k_points': {'field': 'KPointsCard | None', 'default': 'Field(None)', 'import_str': 'pydantic_espresso.cards.pw.k_points import KPointsCard'},
                  'cell_parameters': {'field': 'CellParametersCard', 'default': 'Field(default_factory=CellParametersCard)', 'import_str': 'pydantic_espresso.cards.pw.cell_parameters import CellParametersCard'},
                  'constraints': {'field': 'list[Constraint]', 'default': 'Field(default_factory=list)', 'import_str': 'pydantic_espresso.cards.pw.constraints import Constraint'},
                  'occupations': {'field': 'list[Occupations[float]]', 'default': 'Field(default_factory=list)', 'import_str': 'pydantic_espresso.cards.pw.occupations import Occupations'},
                  'atomic_velocities': {'field': 'list[AtomicVelocity]', 'default': 'Field(default_factory=AtomicVelocitiesCard)', 'import_str': 'pydantic_espresso.cards.pw.atomic_velocities import AtomicVelocitiesCard'},
                  'atomic_forces': {'field': 'list[AtomicForce]', 'default': 'Field(default_factory=AtomicForcesCard)', 'import_str': 'pydantic_espresso.cards.pw.atomic_forces import AtomicForcesCard'},
                  'solvents': {'field': 'SolventsCard | SolventsLRCard | None', 'default': 'Field(None)', 'import_str': 'pydantic_espresso.cards.pw.solvents import SolventsCard, SolventsLRCard'},
                  'hubbard': {'field': 'HubbardCard | None', 'default': 'Field(None)', 'import_str': 'pydantic_espresso.cards.pw.hubbard import HubbardCard'}}