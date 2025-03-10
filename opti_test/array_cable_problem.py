from opti_test.model_builder import ModelBuilder
from opti_test.model_data import ModelData
from pydantic import BaseModel
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from opti_test.classes import CableType, Unit, Layout


class ArrayCableProblem(BaseModel):
    units: list[Unit]
    cable_types: list[CableType]
    settings: dict[str, str | float]
    layout: Layout | None = None

    def create_layout(self):
        model_data = ModelData.create(self.units, self.cable_types)
        self.layout = ModelBuilder(model_data).solve()

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
