from opti_test.classes import CableType, Connection, Link, Unit
from pytest import mark, approx


@mark.parametrize("name, expected", [("OSS_1", False), ("WTG_1", True)])
def test_is_turbine(name, expected):
    # Arrange
    unit = Unit(name=name, x=1, y=1)

    # Act
    is_turbine = unit.is_turbine()

    # Assert
    assert is_turbine == expected


def test_link_get_distance_in_km():
    # Arrange
    link_a = Link(origin=Unit(name="1", x=0, y=0), destination=Unit(name="2", x=1000, y=1000))

    # Act
    distance = link_a.get_distance_in_km()

    # Assert
    assert distance == approx(1.414213)


@mark.parametrize("x, y, expected", [(1, 0, True), (0, 0, False), (0.5, 0.5, False), (1, 1, False), (0, 2, False)])
def test_link_check_if_crossing(x, y, expected):
    # Arrange
    # We assume the other three units to be (0,0) - (1,1) and (0,1)
    link_a = Link(origin=Unit(name="1", x=0, y=0), destination=Unit(name="2", x=1, y=1))
    link_b = Link(origin=Unit(name="3", x=0, y=1), destination=Unit(name="4", x=x, y=y))

    # Act
    is_crossing = link_a.check_if_crossing(link_b)

    # Assert
    assert is_crossing == expected


def test_connection_get_cost():
    # Arrange
    link = Link(origin=Unit(name="1", x=0, y=0), destination=Unit(name="2", x=1000, y=1000))
    cable_type = CableType(name="A", max_mw_on_cable=8, cost_per_km=1000)
    connection = Connection(link=link, cable_type=cable_type)

    # Act
    cost = connection.get_cost()

    # Assert
    assert cost == approx(1414.213)
