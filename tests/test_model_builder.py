from hypothesis import given, settings, strategies as st

from opti_test.classes import CableType, Unit
from opti_test.model_builder import ModelBuilder
from opti_test.model_data import ModelData, Parameters


# Strategies for generating valid data
@st.composite
def units(draw, type: str):
    # Ensure it's possible to force at least one unit with "WTG" in the name
    match type:
        case "WTG":
            name_part = "WTG"
        case "OSS":
            name_part = "OSS"
        case None:
            name_part = draw(st.sampled_from(["WTG", "OSS"]))
    name = name_part + draw(st.text(min_size=2, max_size=7))
    x = draw(st.floats(min_value=0, max_value=10, allow_nan=False, allow_infinity=False))
    y = draw(st.floats(min_value=0, max_value=10, allow_nan=False, allow_infinity=False))
    return Unit(name=name, x=x, y=y)


@st.composite
def cable_types(draw):
    name = draw(st.text(min_size=1, max_size=10))
    max_mw_on_cable = draw(st.floats(min_value=1, max_value=20, allow_nan=False, allow_infinity=False))
    cost_per_km = draw(st.floats(min_value=0.1, max_value=1e6, allow_nan=False, allow_infinity=False))
    return CableType(name=name, max_mw_on_cable=max_mw_on_cable, cost_per_km=cost_per_km)


@st.composite
def model_data_st(draw):
    wtg_units = draw(st.sets(units(type="WTG"), min_size=1, max_size=3))
    other_units = draw(st.sets(units(type=None), min_size=1, max_size=5))
    oss_units = draw(st.sets(units(type="OSS"), min_size=1, max_size=2))
    units_set = other_units.union(wtg_units)
    units_set = units_set.union(oss_units)
    cable_types_set = draw(st.sets(cable_types(), min_size=1, max_size=3))
    return ModelData.create(units=units_set, cable_types=cable_types_set)


@given(model_data=model_data_st())
@settings(deadline=None)
def test_all_turbines_connected(model_data):
    # Arrange
    parameters = Parameters(mw_produced_per_turbine=8, max_number_of_cable_types=3)
    model_builder = ModelBuilder(model_data, parameters)

    # Act
    layout = model_builder.solve()

    # Assert
    if layout is None:  # Account for possible infeasibilities
        return
    assert set([connection.link.origin for connection in layout]) == model_data.turbines


@given(model_data=model_data_st())
@settings(deadline=None)
def test_max_number_of_cable_types(model_data):
    # Arrange
    parameters = Parameters(mw_produced_per_turbine=8, max_number_of_cable_types=1)
    model_builder = ModelBuilder(model_data, parameters)

    # Act
    layout = model_builder.solve()

    # Assert
    if layout is None:  # Account for possible infeasibilities
        return
    assert 1 == len(set([c.cable_type for c in layout]))


@given(model_data=model_data_st())
@settings(deadline=None)
def test_no_cables_cross(model_data):
    # Arrange
    parameters = Parameters(mw_produced_per_turbine=8, max_number_of_cable_types=1)
    model_builder = ModelBuilder(model_data, parameters)

    # Act
    layout = model_builder.solve()

    # Assert
    if layout is None:  # Account for possible infeasibilities
        return
    for c in layout:
        for c2 in layout:
            if c != c2 and c.link.check_if_crossing(c2.link):
                assert False
