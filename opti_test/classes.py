from opti_test.model_builder import ModelBuilder
from pydantic import BaseModel
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from shapely.geometry import LineString


class Unit(BaseModel):
    name: str
    x: float
    y: float

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    def is_turbine(self):
        return self.name[:3] == "WTG"


class CableType(BaseModel):
    name: str
    max_mw_on_cable: float
    cost_per_km: float

    def __str__(self):
        return str(self.name)


class Link(BaseModel):
    origin: Unit
    destination: Unit

    def __eq__(self, other):
        return self.origin == other.origin and self.destination == other.destination

    def __str__(self):
        return str(self.origin) + "->" + str(self.destination)

    def get_distance_in_km(self):
        return np.sqrt((self.origin.x - self.destination.x) ** 2 + (self.origin.y - self.destination.y) ** 2) / 1000

    def check_if_crossing(self, link2) -> bool:
        line1 = _convert_link_to_line_string(self)
        line2 = _convert_link_to_line_string(link2)

        if self.origin in [link2.origin, link2.destination] or self.destination in [link2.origin, link2.destination]:
            return False
        return line1.crosses(line2)


def _convert_link_to_line_string(link: Link) -> LineString:
    return LineString(
        [
            (link.origin.coordinate.easting, link.origin.coordinate.northing),
            (link.destination.coordinate.easting, link.destination.coordinate.northing),
        ]
    )


class Connection(BaseModel):
    link: Link
    cable_type: CableType

    def __str__(self):
        return str(self.link) + "_" + str(self.cable_type)

    def get_cost(self):
        return self.link.get_distance_in_km() * self.cable_type.cost_per_km


class Layout(BaseModel):
    connections: list[Connection]


class ArrayCableProblem(BaseModel):
    units: list[Unit]
    cable_types: list[CableType]
    settings: dict[str, str | float]
    layout: Layout | None = None

    def create_layout(self):
        self.layout = ModelBuilder(self.connections).solve()

    def write_to_dataframe(self):
        columns = ["Origin", "Destination", "CableType"]
        if self.layout is None:
            return pd.DataFrame(columns=columns)

        data = [[c.link.origin.name, c.link.destination.name, c.cable_type.name] for c in self.layout]
        return pd.DataFrame(data=data, columns=columns)

    def plot(self, show: bool = True):
        df = self._create_dataframe_for_units()
        fig = px.scatter(df, x="Easting", y="Northing")

        if self.layout is not None:
            self._add_layout_to_plot(fig)

        if show:
            fig.show()

        return fig

    def _create_dataframe_for_units(self):
        columns = ["Name", "Easting", "Northing"]
        data = [[u.name, u.coordinate.easting, u.coordinate.northing] for u in self.units]

        return pd.DataFrame(data=data, columns=columns)

    def _add_layout_to_plot(self, fig):
        for c in self.layout:
            fig.add_trace(
                go.Scatter(
                    x=[c.link.origin.coordinate.x, c.link.destination.coordinate.x],
                    y=[c.link.origin.coordinate.y, c.link.destination.coordinate.y],
                    line=dict(color="royalblue", width=float(c.cable_type.name)),
                )
            )

    def write_solution_to_excel(self, filename: str):
        df = self.write_to_dataframe()
        df.to_excel(filename)
