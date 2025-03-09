from typing import Dict, Set

from .domain_classes import CableType, Connection, Link, Unit


class ModelData:
    def __init__(self, units: Set, cable_types: Set, parameters: Dict):
        self.units = units
        self.turbines = set([u for u in self.units if u.is_turbine()])
        self.cable_types = cable_types
        self.parameters = parameters
        self.links = self._get_links_from_units()
        self.connections = self._get_connections_from_units()

    def _get_links_from_units(self) -> Set:
        return {Link(o, d) for o in self.units for d in self.units if o != d and o.is_turbine()}

    def _get_connections_from_units(self) -> Set:
        return {Connection(link, c) for link in self.links for c in self.cable_types}

    def get_connections_for_link(self, link: Link) -> Set:
        return {c for c in self.connections if c.link == link}

    def get_incoming_into_unit(self, u: Unit) -> Set:
        return {link for link in self.links if link.destination == u}

    def get_outgoing_from_unit(self, u: Unit) -> Set:
        return {link for link in self.links if link.origin == u}

    def get_crossing_links_from_units(self, o: Unit, d: Unit) -> Set:
        first_set = [
            link
            for link in self.links
            if (link.origin == o and link.destination == d) or (link.origin == d and link.destination == o)
        ]
        link1 = first_set[0]

        second_set = {link for link in self.links if link.check_if_crossing(link1)}

        return second_set.union(first_set)

    def get_connections_with_same_cable_type(self, cable_type: CableType) -> Set:
        return {c for c in self.connections if c.cable_type == cable_type}
