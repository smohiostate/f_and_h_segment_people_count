from common.abstract.cartesian.coordinate import Coordinate

# Coordinate

def test_coordinate_components():
    coordinate = Coordinate(1, 1)
    coordinate_components = coordinate.dimensional_components()
    assert coordinate_components[0] == 1
    assert coordinate_components[1] == 1

def test_coordinate_magnitude():
    coordinate = Coordinate(3, 4)
    assert coordinate.magnitude() == 5

def test_coordinate_length():
    coordinate = Coordinate(3, 4)
    assert len(coordinate) == 5

def test_coordinate_addition():
    coordinate1 = Coordinate(1, 2)
    coordinate2 = Coordinate(2, 2)
    assert len(coordinate1 + coordinate2) == 5

def test_coordinate_subtraction():
    coordinate1 = Coordinate(1, 2)
    coordinate2 = Coordinate(2, 2)
    assert len(coordinate1 + coordinate2) == 5
