import pyoptinterface as poi
from poi.VariableDomain import Binary, Continuous
from pyoptinterface import highs

from .model_data import ModelData


class ModelBuilder:
    def __init__(self, model_data: ModelData):
        self.model_data = model_data
        self.model = highs.Model()

    def solve(self):
        self._define_variables()
        self._define_constraints()
        self._define_objective_function()
        return self._optimize()

    def _define_variables(self):
        self.install = {
            c: self.model.add_variable(domain=Binary, name=f"install_{c}") for c in self.model_data.connections
        }
        self.is_link = {
            link: self.model.add_variable(domain=Binary, name=f"is_link_{link}_built") for link in self.model_data.links
        }
        self.flow = {
            f: self.model.add_variable(lb=0, domain=Continuous, name=f"flow_in_link_{f}") for f in self.model_data.links
        }
        self.is_cable_built = {
            c: self.model.add_variable(domain=Binary, name=f"is_cable_{c}_built") for c in self.model_data.cable_types
        }

    def _map_variables(self):
        return self.install, self.is_link, self.flow, self.is_cable_built

    def _define_constraints(self):
        x, y, f, z = self._map_variables()  # For readability

        for link in y:
            self.model.add_linear_constraint(
                sum(x[c] for c in self.model_data.get_connections_for_link(link)) - y[link],
                poi.Eq,
                0,
                name=f"Connections for link {link}",
            )
            self.model.add_linear_constraint(
                f[link]
                - sum(c.cable_type.max_mw_on_cable * x[c] for c in self.model_data.get_connections_for_link(link)),
                poi.Leq,
                0,
                name=f"Limit flow for link {link}",
            )

        for u in self.model_data.turbines:
            self.model.add_linear_constraint(
                sum(f[o] for o in self.model_data.get_outgoing_from_unit(u))
                - sum(f[i] for i in self.model_data.get_incoming_into_unit(u)),
                poi.Eq,
                self.model_data.parameters["MW"],
                name=f"Flow balance for {u}",
            )
            self.model.add_linear_constraint(
                sum(y[link] for link in self.model_data.get_outgoing_from_unit(u)),
                poi.Eq,
                1,
                name=f"Enforce link being built for {u}",
            )

        for cable_type in z:
            for c in self.model_data.get_connections_with_same_cable_type(cable_type):
                self.model.add_linear_constraint(
                    x[c] - z[cable_type],
                    poi.Leq,
                    0,
                    name=f"Enable cable type selection for cable {cable_type} and connection {c}",
                )

        self.model.add_linear_constraint(
            sum(z.values()) <= self.model_data.parameters["CableNumber"], name="Limit number of cables"
        )

        self._add_non_crossing_constraints()

    def _add_non_crossing_constraints(self):
        _, y, _, _ = self._map_variables()  # For readability

        for num1, link1 in enumerate(y):
            for num2, link2 in enumerate(y):
                if num2 > num1 and link1.check_if_crossing(link2):
                    self.model.add_linear_constraint(
                        y[link1] + y[link2], poi.Leq, 1, name=f"Non crossing for {link1},{link2}"
                    )

    def _define_objective_function(self):
        x, _, _, _ = self._map_variables()  # For readability

        self.model.set_objective(sum(c.get_cost() * x[c] for c in x), poi.ObjectiveSense.Minimize)

    def _optimize(self):
        x, _, _, _ = self._map_variables()  # For readability
        self.model.optimize()
        return [c for c in x if self.model.get_value(x[c]) > 0.5]
