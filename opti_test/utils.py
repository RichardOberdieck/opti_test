import math
import pandas as pd

from opti_test.classes import ArrayCableProblem, Unit, CableType


def read_excel(file):
    """
    :param file: This supports both a file-like object and a file name
    """
    parameters = _get_parameters(file)
    units = _get_units(file)
    cable_types = _get_cable_types(file, parameters)

    return ArrayCableProblem(units, cable_types, parameters)


def _get_parameters(file):
    df = pd.read_excel(file, "Parameters")
    return df.to_dict("records")[0]


def _get_units(file):
    df = pd.read_excel(file, "Turbine Data")
    return set([Unit(unit.Name, unit.East, unit.North) for _, unit in df.iterrows()])


def _get_cable_types(file, parameters):
    df = pd.read_excel(file, "Cable Data")

    cable_types = set([])
    for _, cable in df.iterrows():
        cable_types.add(_cast_cable_type(cable, parameters))

    return set(cable_types)


def _cast_cable_type(cable_data, parameters) -> CableType:
    mw_limit = _get_mw_limit_for_cable_type(cable_data.Rating, parameters["Voltage"])
    refined_mw_limit = _round_mw_limit_based_on_turbine_power(mw_limit, parameters["MW"])

    return CableType(cable_data.Number, refined_mw_limit, cable_data.Cost)


def _get_mw_limit_for_cable_type(current: float, voltage):
    return math.sqrt(3) * current * voltage / 1000


def _round_mw_limit_based_on_turbine_power(mw_limit, mw_turbine):
    return math.floor(mw_limit / mw_turbine) * mw_turbine
