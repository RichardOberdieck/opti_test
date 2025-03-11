from opti_test.model_builder import ModelBuilder
from opti_test.model_data import ModelData, Parameters
from pydantic import BaseModel
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from opti_test.classes import CableType, Unit, Layout


class ArrayCableProblem(BaseModel):
    units: list[Unit]
    cable_types: list[CableType]
    parameters: Parameters
    layout: Layout | None = None

    def create_layout(self):
        model_data = ModelData.create(self.units, self.cable_types)
        layout_connections = ModelBuilder(model_data, self.parameters).solve()
        self.layout = Layout(connections=layout_connections)

    def plot(self, show: bool = True):
        df = self._create_dataframe_for_units()
        fig = px.scatter(df, x="Easting", y="Northing", text="Name")
        fig.update_traces(textposition="top center")

        if self.layout is not None:
            self._add_layout_to_plot(fig)

        if show:
            fig.show()

        return fig

    def _create_dataframe_for_units(self):
        columns = ["Name", "Easting", "Northing"]
        data = [[u.name, u.x, u.y] for u in self.units]

        return pd.DataFrame(data=data, columns=columns)

    def _add_layout_to_plot(self, fig):
        for c in self.layout.connections:
            fig.add_trace(
                go.Scatter(
                    x=[c.link.origin.x, c.link.destination.x],
                    y=[c.link.origin.y, c.link.destination.y],
                    line=dict(color="royalblue"),
                    name=str(c),
                )
            )
