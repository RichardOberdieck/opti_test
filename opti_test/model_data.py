from pydantic import BaseModel

from opti_test.classes import CableType, Connection, Link, Unit


class ModelData(BaseModel):
    links: set[Link]
    connections: set[Connection]
    cable_types: set[CableType]
    turbines: set[Unit]

    @classmethod
    def create(cls, units: set[Unit], cable_types: set[CableType]):
        turbines = set([u for u in units if u.is_turbine()])
        links = {Link(origin=o, destination=d) for o in units for d in units if o != d and o.is_turbine()}
        connections = {Connection(link=link, cable_type=c) for link in links for c in cable_types}
        return cls(links=links, connections=connections, cable_types=cable_types, turbines=turbines)

    def get_connections_for_link(self, link: Link) -> set[Connection]:
        return {c for c in self.connections if c.link == link}

    def get_incoming_into_unit(self, u: Unit) -> set[Link]:
        return {link for link in self.links if link.destination == u}

    def get_outgoing_from_unit(self, u: Unit) -> set[Link]:
        return {link for link in self.links if link.origin == u}

    def get_crossing_links_from_units(self, o: Unit, d: Unit) -> set[Link]:
        first_set = [
            link
            for link in self.links
            if (link.origin == o and link.destination == d) or (link.origin == d and link.destination == o)
        ]
        link1 = first_set[0]

        second_set = {link for link in self.links if link.check_if_crossing(link1)}

        return second_set.union(first_set)

    def get_connections_with_same_cable_type(self, cable_type: CableType) -> set[Connection]:
        return {c for c in self.connections if c.cable_type == cable_type}
