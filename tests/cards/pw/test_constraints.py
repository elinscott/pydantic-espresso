from pydantic_espresso.cards.pw.constraints import TypeCoordConstraint, AtomCoordConstraint, DistanceConstraint, PlanarAngleConstraint, TorsionalAngleConstraint

def test_type_coord_constraint():
    """Test the TypeCoordConstraint class."""
    constraint = TypeCoordConstraint(atom_type_indices=[1, 2], cutoff_radius=1.0, smoothing=0.1)
    assert str(constraint) == "type_coord 1 2 1.0 0.1"

def test_atom_coord_constraint():
    """Test the AtomCoordConstraint class."""
    constraint = AtomCoordConstraint(atom_indices=[1, 2], cutoff_radius=1.0, smoothing=0.1)
    assert str(constraint) == "atom_coord 1 2 1.0 0.1"

def test_distance_constraint():
    """Test the DistanceConstraint class."""
    constraint = DistanceConstraint(atom_indices=[1, 2])
    assert str(constraint) == "distance 1 2"

def test_planar_angle_constraint():
    """Test the PlanarAngleConstraint class."""
    constraint = PlanarAngleConstraint(atom_indices=[1, 2, 3])
    assert str(constraint) == "planar_angle 1 2 3"

def test_torsional_angle_constraint():
    """Test the TorsionalAngleConstraint class."""
    constraint = TorsionalAngleConstraint(atom_indices=[1, 2, 3, 4])
    assert str(constraint) == "torsional_angle 1 2 3 4"
