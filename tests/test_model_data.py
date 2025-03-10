from opti_test.classes import CableType, Link, Unit
from opti_test.model_data import ModelData
from pytest import fixture, mark


@fixture
def model_data():
    units = {Unit(name="WTG_1", x=0, y=0), Unit(name="WTG_2", x=1, y=1), Unit(name="OSS_1", x=2, y=0)}
    cable_types = {
        CableType(name="1", max_mw_on_cable=5, cost_per_km=10),
        CableType(name="2", max_mw_on_cable=8, cost_per_km=20),
    }
    return ModelData.create(units, cable_types)


def test_get_connections_for_link(model_data):
    # Arrange
    link = Link(origin=Unit(name="WTG_1", x=0, y=0), destination=Unit(name="WTG_2", x=1, y=1))
    # Act
    connections = model_data.get_connections_for_link(link)

    # Assert
    assert 2 == len(connections)
    assert link == connections.pop().link


def test_get_incoming_into_unit(model_data):
    # Arrange
    unit = Unit(name="OSS_1", x=2, y=0)

    # Act
    links = model_data.get_incoming_into_unit(unit)

    # Assert
    assert 2 == len(links)
    assert unit == links.pop().destination


@mark.parametrize("unit, expected", [(Unit(name="WTG_2", x=1, y=1), 2), (Unit(name="OSS_1", x=2, y=0), 0)])
def test_get_outgoing_into_unit(model_data, unit, expected):
    # Act
    links = model_data.get_outgoing_from_unit(unit)

    # Assert
    assert expected == len(links)


def test_get_crossing_links_from_units(model_data):
    # Arrange
    origin = Unit(name="WTG_1", x=0, y=0)
    destination = Unit(name="OSS_1", x=2, y=0)

    # Act
    links = model_data.get_crossing_links_from_units(origin, destination)

    # Assert
    assert 1 == len(links)


def test_get_connections_with_same_cable_type(model_data):
    # Arrange
    cable_type = CableType(name="1", max_mw_on_cable=5, cost_per_km=10)

    # Act
    connections = model_data.get_connections_with_same_cable_type(cable_type)

    # Assert
    assert 4 == len(connections)
    assert cable_type == connections.pop().cable_type
