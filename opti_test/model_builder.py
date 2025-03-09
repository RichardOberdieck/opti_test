import gurobipy as gp
from gurobipy import GRB

from .model_data import ModelData

Σ = gp.quicksum


class ModelBuilder:
    def __init__(self, model_data: ModelData):
        self.model_data = model_data
        self.model = gp.Model("CableProblem")

    def solve(self):
        self._define_variables()
        self._define_constraints()
        self._define_objective_function()
        return self._optimize()

    def _define_variables(self):
        self.install = self.model.addVars(self.model_data.connections, vtype=GRB.BINARY, name="Install")
        self.is_link = self.model.addVars(self.model_data.links, vtype=GRB.BINARY, name="Is_Link_Built")
        self.flow = self.model.addVars(self.model_data.links, name="Flow")
        self.is_cable_built = self.model.addVars(self.model_data.cable_types, vtype=GRB.BINARY, name="Is_Cable_Built")

    def _map_variables(self):
        return self.install, self.is_link, self.flow, self.is_cable_built

    def _define_constraints(self):
        x, y, f, z = self._map_variables()  # For readability

        self.model.addConstrs(
            (Σ(x[c] for c in self.model_data.get_connections_for_link(link)) == y[link] for link in y),
            name="Connect x to y",
        )

        self.model.addConstrs(
            (
                Σ(f[o] for o in self.model_data.get_outgoing_from_unit(u))
                == Σ(f[i] for i in self.model_data.get_incoming_into_unit(u)) + self.model_data.parameters["MW"]
                for u in self.model_data.turbines
            ),
            name="Flow balance",
        )

        self.model.addConstrs(
            (
                f[link]
                <= Σ(c.cable_type.max_mw_on_cable * x[c] for c in self.model_data.get_connections_for_link(link))
                for link in y
            ),
            name="Limit flow per cable type",
        )

        self.model.addConstrs(
            (Σ(y[link] for link in self.model_data.get_outgoing_from_unit(u)) == 1 for u in self.model_data.turbines),
            name="Enforce link being built",
        )

        self.model.addConstrs(
            (
                x[c] <= z[cable_type]
                for cable_type in z
                for c in self.model_data.get_connections_with_same_cable_type(cable_type)
            ),
            name="Enable cable type selection",
        )

        self.model.addConstr(z.sum() <= self.model_data.parameters["CableNumber"], name="Limit number of cables")

        self._add_non_crossing_constraints()

    def _add_non_crossing_constraints(self):
        _, y, _, _ = self._map_variables()  # For readability

        for num1, link1 in enumerate(y):
            for num2, link2 in enumerate(y):
                if num2 > num1 and link1.check_if_crossing(link2):
                    self.model.addConstr(y[link1] + y[link2] <= 1, name=f"Non crossing for {link1},{link2}")

    def _define_objective_function(self):
        x, _, _, _ = self._map_variables()  # For readability

        self.model.setObjective(Σ(c.get_cost() * x[c] for c in x))

    def _optimize(self):
        x, _, f, _ = self._map_variables()  # For readability

        self.model.Params.Cuts = 2
        self.model.optimize()

        return [c for c in x if x[c].x > 0.5]
