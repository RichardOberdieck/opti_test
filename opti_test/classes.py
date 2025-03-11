from pydantic import BaseModel
import numpy as np
import pandas as pd
from shapely.geometry import LineString


class Unit(BaseModel):
    name: str
    x: float
    y: float

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    def __hash__(self):
        return 100 * hash(self.x) - hash(self.y)

    def is_turbine(self):
        return self.name[:3] == "WTG"


class CableType(BaseModel):
    name: str
    max_mw_on_cable: float
    cost_per_km: float

    def __str__(self):
        return str(self.name)

    def __hash__(self):
        return hash(self.name) + hash(self.max_mw_on_cable) + 5 * hash(self.cost_per_km)


class Link(BaseModel):
    origin: Unit
    destination: Unit

    def __eq__(self, other):
        return self.origin == other.origin and self.destination == other.destination

    def __str__(self):
        return str(self.origin) + "->" + str(self.destination)

    def __hash__(self):
        return hash(self.origin) + 5 * hash(self.destination)

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
            (link.origin.x, link.origin.y),
            (link.destination.x, link.destination.y),
        ]
    )


class Connection(BaseModel):
    link: Link
    cable_type: CableType

    def __str__(self):
        return str(self.link) + "_" + str(self.cable_type)

    def __hash__(self):
        return hash(self.link) + 15 * hash(self.cable_type)

    def get_cost(self):
        return self.link.get_distance_in_km() * self.cable_type.cost_per_km


class Layout(BaseModel):
    connections: list[Connection]

    def to_dataframe(self):
        columns = ["Origin", "Destination", "CableType"]

        data = [[c.link.origin.name, c.link.destination.name, c.cable_type.name] for c in self.connections]
        return pd.DataFrame(data=data, columns=columns)

    def to_excel(self, filename: str):
        df = self.to_dataframe()
        df.to_excel(filename)
