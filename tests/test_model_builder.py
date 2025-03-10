from hypothesis import given, strategies as st

from opti_test.classes import CableType, Connection, Link, Unit
from opti_test.model_data import ModelData


# Strategies for generating valid data
@st.composite
def units(draw, include_wtg=False):
    name_part = draw(st.sampled_from(["WTG", "OSS"])) if not include_wtg else "WTG"
    name = name_part + draw(st.text(min_size=0, max_size=7))
    x = draw(st.floats(allow_nan=False, allow_infinity=False))
    y = draw(st.floats(allow_nan=False, allow_infinity=False))
    return Unit(name=name, x=x, y=y)


@st.composite
def cable_types(draw):
    name = draw(st.text(min_size=1, max_size=10))
    max_mw_on_cable = draw(st.floats(min_value=0.1, allow_nan=False, allow_infinity=False))
    cost_per_km = draw(st.floats(min_value=0.1, allow_nan=False, allow_infinity=False))
    return CableType(name=name, max_mw_on_cable=max_mw_on_cable, cost_per_km=cost_per_km)


@st.composite
def model_data_st(draw):
    # Ensure at least one unit with "WTG"
    wtg_unit = draw(units(include_wtg=True))
    other_units = draw(st.sets(units(), min_size=1, max_size=9))
    units_set = other_units.union({wtg_unit})
    cable_types_set = draw(st.sets(cable_types(), min_size=1, max_size=5))
    return ModelData.create(units=units_set, cable_types=cable_types_set)


# Test case for ModelData
@given(data=model_data_st())
def test_model_data(data):
    assert isinstance(data, ModelData)
    assert all(isinstance(link, Link) for link in data.links)
    assert all(isinstance(connection, Connection) for connection in data.connections)
    assert all(isinstance(cable_type, CableType) for cable_type in data.cable_types)
    assert all(isinstance(turbine, Unit) for turbine in data.turbines)
    assert len(data.turbines) > 0  # Ensure there are turbines in the model
