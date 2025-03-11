from hypothesis import given, settings, Verbosity, strategies as st

from opti_test.classes import CableType, Connection, Link, Unit
from opti_test.model_builder import ModelBuilder
from opti_test.model_data import ModelData, Parameters


# Strategies for generating valid data
@st.composite
def units(draw, include_wtg=False):
    # Ensure it's possible to force at least one unit with "WTG" in the name
    name_part = draw(st.sampled_from(["WTG", "OSS"])) if not include_wtg else "WTG"
    name = name_part + draw(st.text(min_size=0, max_size=7))
    x = draw(st.floats(min_value=0, max_value=1e8, allow_nan=False, allow_infinity=False))
    y = draw(st.floats(min_value=0, max_value=1e8, allow_nan=False, allow_infinity=False))
    return Unit(name=name, x=x, y=y)


@st.composite
def cable_types(draw):
    name = draw(st.text(min_size=1, max_size=10))
    max_mw_on_cable = draw(st.floats(min_value=1, max_value=20, allow_nan=False, allow_infinity=False))
    cost_per_km = draw(st.floats(min_value=0.1, max_value=1e6, allow_nan=False, allow_infinity=False))
    return CableType(name=name, max_mw_on_cable=max_mw_on_cable, cost_per_km=cost_per_km)


@st.composite
def model_data_st(draw):
    wtg_units = draw(st.sets(units(include_wtg=False), min_size=1, max_size=9))
    other_units = draw(st.sets(units(include_wtg=True), min_size=1, max_size=9))
    units_set = other_units.union(wtg_units)
    cable_types_set = draw(st.sets(cable_types(), min_size=1, max_size=3))
    return ModelData.create(units=units_set, cable_types=cable_types_set)


# Test case for ModelData
@given(model_data=model_data_st())
@settings(verbosity=Verbosity.verbose, deadline=None)
def test_model_builder(model_data):
    # Arrange
    if not any(model_data.links):
        return
    parameters = Parameters(mw_produced_per_turbine=8, max_number_of_cable_types=3)
    model_builder = ModelBuilder(model_data, parameters)

    # Act
    model_builder.solve()

    assert True


def test_something():
    model_data = ModelData(
        links={
            Link(origin=Unit(name="WTG", x=1.0, y=0.0), destination=Unit(name="WTG+", x=0.25, y=0.0)),
            Link(origin=Unit(name="WTG00000", x=0.0625, y=1.0), destination=Unit(name="WTG+", x=0.25, y=0.0)),
            Link(origin=Unit(name="WTG0", x=1.0, y=0.0), destination=Unit(name="WTG+", x=0.25, y=0.0)),
            Link(origin=Unit(name="WTG0", x=1.0, y=0.0), destination=Unit(name="WTG", x=0.0, y=0.0)),
            Link(origin=Unit(name="WTG00000", x=0.0625, y=1.0), destination=Unit(name="WTG", x=0.0, y=0.0)),
            Link(origin=Unit(name="WTG", x=1.0, y=0.0), destination=Unit(name="WTG0", x=1.0, y=0.0)),
            Link(origin=Unit(name="WTG00000", x=0.0625, y=1.0), destination=Unit(name="WTG0", x=1.0, y=0.0)),
            Link(origin=Unit(name="WTG+", x=0.25, y=0.0), destination=Unit(name="WTG", x=1.0, y=0.0)),
            Link(origin=Unit(name="WTG+", x=0.25, y=0.0), destination=Unit(name="WTG0", x=1.0, y=0.0)),
            Link(origin=Unit(name="WTG+", x=0.25, y=0.0), destination=Unit(name="WTG00000", x=0.0625, y=1.0)),
            Link(origin=Unit(name="WTG", x=0.0, y=0.0), destination=Unit(name="WTG0", x=1.0, y=0.0)),
            Link(origin=Unit(name="WTG0", x=1.0, y=0.0), destination=Unit(name="WTG00000", x=0.0625, y=1.0)),
            Link(origin=Unit(name="WTG", x=1.0, y=0.0), destination=Unit(name="WTG00000", x=0.0625, y=1.0)),
            Link(origin=Unit(name="WTG+", x=0.25, y=0.0), destination=Unit(name="WTG", x=0.0, y=0.0)),
            Link(origin=Unit(name="WTG0", x=1.0, y=0.0), destination=Unit(name="WTG", x=1.0, y=0.0)),
            Link(origin=Unit(name="WTG00000", x=0.0625, y=1.0), destination=Unit(name="WTG", x=1.0, y=0.0)),
            Link(origin=Unit(name="WTG", x=0.0, y=0.0), destination=Unit(name="WTG+", x=0.25, y=0.0)),
            Link(origin=Unit(name="WTG", x=0.0, y=0.0), destination=Unit(name="WTG00000", x=0.0625, y=1.0)),
        },
        connections={
            Connection(
                link=Link(origin=Unit(name="WTG+", x=0.25, y=0.0), destination=Unit(name="WTG", x=1.0, y=0.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG+", x=0.25, y=0.0), destination=Unit(name="WTG00000", x=0.0625, y=1.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG", x=0.0, y=0.0), destination=Unit(name="WTG0", x=1.0, y=0.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG0", x=1.0, y=0.0), destination=Unit(name="WTG", x=1.0, y=0.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG00000", x=0.0625, y=1.0), destination=Unit(name="WTG", x=1.0, y=0.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG00000", x=0.0625, y=1.0), destination=Unit(name="WTG0", x=1.0, y=0.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG", x=1.0, y=0.0), destination=Unit(name="WTG0", x=1.0, y=0.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG", x=0.0, y=0.0), destination=Unit(name="WTG00000", x=0.0625, y=1.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG", x=0.0, y=0.0), destination=Unit(name="WTG+", x=0.25, y=0.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG0", x=1.0, y=0.0), destination=Unit(name="WTG00000", x=0.0625, y=1.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG", x=1.0, y=0.0), destination=Unit(name="WTG00000", x=0.0625, y=1.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG+", x=0.25, y=0.0), destination=Unit(name="WTG", x=0.0, y=0.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG", x=1.0, y=0.0), destination=Unit(name="WTG+", x=0.25, y=0.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG00000", x=0.0625, y=1.0), destination=Unit(name="WTG+", x=0.25, y=0.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG0", x=1.0, y=0.0), destination=Unit(name="WTG+", x=0.25, y=0.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG0", x=1.0, y=0.0), destination=Unit(name="WTG", x=0.0, y=0.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG00000", x=0.0625, y=1.0), destination=Unit(name="WTG", x=0.0, y=0.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
            Connection(
                link=Link(origin=Unit(name="WTG+", x=0.25, y=0.0), destination=Unit(name="WTG0", x=1.0, y=0.0)),
                cable_type=CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1),
            ),
        },
        cable_types={CableType(name="0", max_mw_on_cable=1.0, cost_per_km=0.1)},
        turbines={
            Unit(name="WTG", x=0.0, y=0.0),
            Unit(name="WTG", x=1.0, y=0.0),
            Unit(name="WTG0", x=1.0, y=0.0),
            Unit(name="WTG00000", x=0.0625, y=1.0),
            Unit(name="WTG+", x=0.25, y=0.0),
        },
    )
    parameters = Parameters(mw_produced_per_turbine=8, max_number_of_cable_types=3)
    model_builder = ModelBuilder(model_data, parameters)

    # Act
    model_builder.solve()
