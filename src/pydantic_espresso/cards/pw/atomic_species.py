"""Pydantic model for the cards in `pw.x` input files."""

# ruff: noqa

from pathlib import Path
from abc import ABC, abstractmethod
from typing import Annotated, ClassVar, Literal
import itertools
from pydantic import Field, field_validator
from pydantic_espresso.cards.card import Card
from pydantic_espresso.utils import get_tmp_dir, get_pseudo_dir, BaseModel

INDENT = " " * 2

type PositiveFloat = Annotated[float, Field(gt=0)]
type PositiveInt = Annotated[int, Field(gt=0)]

class AtomicSpecies(BaseModel):
    species: str = Field(..., description="label of the atom. Acceptable syntax: chemical symbol X (1 or 2 characters, case-insensitive) or chemical symbol plus a number or a letter, as in 'Xn' (e.g. Fe1) or 'X_*' or 'X-*' (e.g. C1, C_h; max total length cannot exceed 3 characters)")
    mass: PositiveFloat = Field(..., description="mass of the atomic species [amu: mass of C = 12] Used only when performing Molecular Dynamics run or structural optimization runs using Damped MD. Not actually used in all other cases (but stored in data files, so phonon calculations will use these values unless other values are provided)")
    pseudopotential: str = Field(..., description="File containing PP for this species.  The pseudopotential file is assumed to be in the new UPF format. If it doesn't work, the pseudopotential format is determined by the file name:  *.vdb or *.van     Vanderbilt US pseudopotential code *.RRKJ3            Andrea Dal Corso's code (old format) none of the above  old PWscf norm-conserving format")

    def __str__(self) -> str:
        return f"{self.species} {self.mass} {self.pseudopotential}"

class AtomicPositionsCard(Card):
    """Pydantic model for the ATOMIC_POSITIONS card."""

    class AtomicPosition(BaseModel):
        species: str = Field(..., description="label of the atom as specified in ATOMIC_SPECIES")
        position: tuple[float, float, float] = Field(..., description="x, y, z coordinates of the atom")
    units: Literal["alat", "bohr", "angstrom", "crystal", "crystal_sg"] = Field(..., description="Units for ATOMIC_POSITIONS")
    positions: list[AtomicPosition]

    def __str__(self) -> str:
        return "ATOMIC_POSITIONS {" + self.units + "}\n" + "\n".join([f"{INDENT}{x.species} {' '.join([str(y) for y in x.position])}" for x in self.positions])


class KPointsCard(Card, ABC):
    """Abstract base class for the K_POINTS card."""

    kind: "str"

    def __str__(self) -> str:
        return "K_POINTS {" + self.kind + "}"

class KPointsListCard(KPointsCard):
    """Pydantic model for the K_POINTS card with an explicit list of k-points."""

    class KPoint(BaseModel):
        """Pydantic model for a single k-point"""

        coordinate: tuple[float, float, float] = Field(..., description="")
        weight: float = Field(1, description="")

        def __str__(self) -> str:
            return f"{' '.join([str(x) for x in self.coordinate])} {self.weight}"

    k_points: list[KPoint] = Field(default_factory=list)
    kind: Literal["tpiba", "crystal", "tpiba_b", "crystal_b", "tpiba_c", "crystal_c"] = Field("tbipa", description="")

    @field_validator("kind", mode="after")
    @classmethod
    def check_kind(cls, value: str) -> str:
        if value in ['tpiba_c', 'crystal_c']:
            raise NotImplementedError(f"{value} is a valid choice of kind but it is not yet implemented.")
        return value

    def __str__(self):
        return super().__str__() + '\n' + f"{INDENT}{len(self.k_points)}" + "\n" + '\n'.join([f"{INDENT}{x}" for x in self.k_points])

class KPointsGammaCard(KPointsCard):
    """Pydantic model for the K_POINTS card with kind == gamma."""

    kind: Literal["gamma"] = Field("gamma", description="")

    def to_kpoints_list(self) -> KPointsListCard:
        """Convert to KPointsListCard."""
        return KPointsListCard(k_points=[KPointsListCard.KPoint(coordinate=(0.0, 0.0, 0.0), weight=1.0)])

class KPointsGridCard(KPointsCard):
    """Pydantic model for the K_POINTS card with kind == automatic."""

    grid: tuple[PositiveInt, PositiveInt, PositiveInt] = Field(..., description="")
    offset: tuple[Literal[0, 1], Literal[0, 1], Literal[0, 1]] = Field((0, 0, 0), description="")
    kind: Literal["automatic"] = Field("automatic", description="")

    def to_kpoints_list(self) -> KPointsListCard:
        """Convert to KPointsListCard."""
        k_points = []
        for (i, j, k) in itertools.product(*[range(x) for x in self.grid]):
            # Calculate the coordinate
            coordinate = ((i + self.offset[0] / 2) / self.grid[0],
                          (j + self.offset[1] / 2) / self.grid[1],
                          (k + self.offset[2] / 2) / self.grid[2])
            
            # Wrap coordinates to the range (0.5, 0.5]
            wrapped_coordinate = tuple(x - 1 if x > 0.5 else x for x in coordinate)

            # Construct the k-point and add it to the list
            k_point = KPointsListCard.KPoint(coordinate=wrapped_coordinate, weight=1.0)
            k_points.append(k_point)

        return KPointsListCard(k_points=k_points, kind="crystal")

    def __str__(self) -> str:
        return super().__str__() + '\n' + INDENT + f"{' '.join([str(x) for x in self.grid])} {' '.join([str(x) for x in self.offset])}"


class CellParametersCard(Card):
    """Pydantic model for the CELL_PARAMETERS card."""

    units: Literal["alat", "bohr", "angstrom"] = Field(..., description="Unit for lattice vectors; options are:  'bohr' / 'angstrom': lattice vectors in bohr-radii / angstrom. In this case the lattice parameter alat = sqrt(v1*v1).  'alat' / nothing specified: lattice vectors in units of the lattice parameter (either celldm(1) or A). Not specifying units is DEPRECATED and will not be allowed in the future.  If neither unit nor lattice parameter are specified, 'bohr' is assumed - DEPRECATED, will no longer be allowed")
    vectors: tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]] = Field(..., description="lattice vectors")

    def __str__(self) -> str:
        return "CELL_PARAMETERS {" + self.units + "}\n" + INDENT + f"\n{INDENT}".join([" ".join([str(x) for x in v]) for v in self.vectors])


class Constraint(BaseModel, ABC):
    kind: ClassVar[str]  # no default -- must be set in subclasses

    @property
    @abstractmethod
    def indices(self) -> tuple[PositiveInt | PositiveFloat]:
        ...

    def __str__(self) -> str:
        return self.kind + ' ' + ' '.join([str(x) for x in self.indices])

class TypeCoordConstraint(Constraint):
    atom_type_indices: tuple[PositiveInt, PositiveInt]
    cutoff_radius: PositiveFloat
    smoothing: PositiveFloat
    kind: ClassVar[str] = "type_coord"

    @property
    def indices(self):
        return (*self.atom_type_indices, self.cutoff_radius, self.smoothing)

class AtomCoordConstraint(Constraint):
    atom_indices: tuple[PositiveInt, PositiveInt]
    cutoff_radius: PositiveFloat
    smoothing: PositiveFloat
    kind: ClassVar[str] = "atom_coord"                                                                           

    @property
    def indices(self):
        return (*self.atom_indices, self.cutoff_radius, self.smoothing)

class DistanceConstraint(Constraint):
    atom_indices: tuple[PositiveInt, PositiveInt]
    kind: ClassVar[str] = "distance"

    @property
    def indices(self):
        return self.atom_indices

class PlanarAngleConstraint(Constraint):
    atom_indices: tuple[PositiveInt, PositiveInt, PositiveInt]
    kind: ClassVar[str] = "planar_angle"

    @property
    def indices(self):
        return self.atom_indices

class TorsionalAngleConstraint(Constraint):
    atom_indices: tuple[PositiveInt, PositiveInt, PositiveInt, PositiveInt]
    kind: ClassVar[str] = "torsional_angle"

    @property
    def indices(self):
        return self.atom_indices

type PositiveFloat0to2 = Annotated[float, Field(ge=0, le=2)]

class OccupationsList(list[PositiveFloat0to2]):

    def __str__(self) -> str:
        """Return a string of the occupations list with at most 10 entries per line."""
        lines = []
        for i in range(0, len(self), 10):
            line = INDENT + " ".join([str(x) for x in self[i:i + 10]])
            lines.append(line)
        return "\n".join(lines)


class AtomicVelocity(BaseModel):
    """Pydantic model for the ATOMIC_VELOCITIES card."""

    species: str = Field(..., description="label of the atom as specified in ATOMIC_SPECIES")
    velocity: tuple[float, float, float] = Field(..., description="x, y, z components of the velocity of the atom")

    def __str__(self):
        return f"{INDENT}{self.species} {' '.join([str(x) for x in self.velocity])}"


class AtomicForce(Card):
    species: str = Field(..., description="label of the atom as specified in ATOMIC_SPECIES")
    force: tuple[float, float, float] = Field(..., description="x, y, z components of the force on the atom")

    def __str__(self):
        return f"{INDENT}{self.species} {' '.join([str(x) for x in self.force])}"

class SolventCardABC(Card, ABC):
    units: Literal["1/cell", "mol/L", "g/cm^3"] = Field(..., description="")
    solvents: list

    def __str__(self):
        return "SOLVENTS {" + self.units + "}\n" + "\n".join([f"{INDENT}{x}" for x in self.solvents])


class SolventsCard(SolventCardABC):
    """Pydantic model for the SOLVENTS card when laue_both_hands == False."""

    class Solvent(BaseModel):
        label: str = Field(..., description="label of the solvent molecule.")
        density: float = Field(..., description="density of the solvent molecule. if not positive value is set, density is read from MOL-file.")
        molecule: Path = Field(..., description="MOL-file of the solvent molecule. in the MOL-file, molecular structure and some other data are written.")

        def __str__(self) -> str:
            return f"{self.label} {self.density} {self.molecule}"

    solvents: list[Solvent] = Field(default_factory=list)

class SolventsLRCard(SolventCardABC):
    """Pydantic model for the SOLVENTS card when laue_both_hands == True."""

    class SolventLR(BaseModel):
        label: str = Field(..., description="label of the solvent molecule.")
        density_left: float = Field(..., description="density of the solvent molecule in the left-hand side. if not positive value is set, density is read from MOL-file.")
        density_right: float = Field(..., description="density of the solvent molecule in the right-hand side. if not positive value is set, density is read from MOL-file.")
        molecule: Path = Field(..., description="MOL-file of the solvent molecule. in the MOL-file, molecular structure and some other data are written.")

        def __str__(self) -> str:
            return f"{self.label} {self.density_left} {self.density_right} {self.molecule}"

    solvents: list[SolventLR] = Field(default_factory=list)


class HubbardSite(BaseModel):
    """Pydantic model for a single Hubbard site."""
    label: str = Field(..., description="label of the atom as specified in ATOMIC_SPECIES")
    manifold: str = Field(..., description="subshell of the manifold (e.g. 3d, 2p, 4f, etc.)")

    def __str__(self) -> str:
        return f"{self.label}-{self.manifold}"


class HubbardCard(Card):
    """Pydantic model for the HUBBARD card."""

    class HubbardParameter(BaseModel, ABC):
        """Pydantic model for a single Hubbard parameter."""
        name: ClassVar[str]  # no default -- must be set in subclasses
        value: float = Field(..., description="value of the Hubbard parameter")

        @property
        @abstractmethod
        def _subspace_str(self) -> str:
            ...
        
        def __str__(self) -> str:
            return f"{self.name} {self._subspace_str} {self.value}"

    class HubbardU(HubbardParameter):
        """Pydantic model for the Hubbard U parameter."""
        name: ClassVar[str] = "U"
        site: HubbardSite

        @property
        def _subspace_str(self) -> str:
            return str(self.site)
    
    class HubbardJ0(HubbardU):
        """Pydantic model for the Hubbard J0 parameter."""
        name: ClassVar[str] = "J0"

    class HubbardJ(HubbardU):
        """Pydantic model for the Hubbard J parameter."""
        name: ClassVar[str] = "J"
    
    class HubbardB(HubbardU):
        """Pydantic model for the Hubbard B parameter."""
        name: ClassVar[str] = "B"

    class HubbardV(HubbardParameter):
        """Pydantic model for the Hubbard V parameter."""
        name: ClassVar[str] = "V"
        sites: tuple[HubbardSite, HubbardSite]
        atom_indices: tuple[PositiveInt, PositiveInt] = Field(..., description="indices of the two atoms coupled by the Hubbard V parameter")

        @property
        def _subspace_str(self) -> str:
            return f"{self.sites[0]} {self.sites[1]} {self.atom_indices[0]} {self.atom_indices[1]}"

    kind: Literal["atomic", "ortho-atomic", "norm-atomic", "wf", "pseudo"] = Field(..., description="HUBBARD options are:  NB: forces and stress are currently implemented only for the 'atomic', 'ortho-atomic', and 'pseudo' Hubbard projectors.  Check Doc/Hubbard_input.pdf to see how to specify Hubbard parameters U, J0, J, B, E2, E3, V in the HUBBARD card.")
    parameters: list[HubbardParameter] = Field(default_factory=list)


prebuilt_cards = {'atomic_species': 'list[AtomicSpecies] = Field(default_factory=list)',
                  'atomic_positions': 'AtomicPositionsCard = Field(default_factory=AtomicPositionsCard)',
                  'k_points': 'KPointsCard = Field(...)',
                  'additional_k_points': 'KPointsCard | None = Field(None)',
                  'cell_parameters': 'CellParametersCard = Field(default_factory=CellParametersCard)',
                  'constraints': 'list[Constraint] = Field(default_factory=ConstraintsCard)',
                  'occupations': 'list[Occupations[float]] = Field(default_factory=list)',
                  'atomic_velocities': 'list[AtomicVelocity] = Field(default_factory=AtomicVelocitiesCard)',
                  'atomic_forces': 'list[AtomicForce] = Field(default_factory=AtomicForcesCard)',
                  'solvents': 'SolventsCard | SolventsLRCard | None = None',
                  'hubbard': 'HubbardCard | None = None'}

