import plotly.express as px
import geopandas as gpd
from dash import callback, Output, Input, State
from dash import dcc
import pandas as pd


def _helper_pacific_map(
    pacific_eez: gpd.GeoDataFrame, selected: pd.Series, id_out: str
):
    data = pacific_eez.set_index("pacific_island")
    data["Selected"] = selected
    data = data.rename(
        columns={"ile_du_pacifique": "Nom français"},
        index={"pacific_island": "English name"},
    )
    figure = px.choropleth(
        data_frame=data,
        geojson=data.geometry,
        locations=data.index,
        color="Selected",
        # color grey when select is False or blue
        color_discrete_map={False: "grey", True: "blue"},
        hover_data={
            "Nom français": True,
            "Selected": False,
        },
    )
    figure.update_layout(showlegend=False)
    figure.update_geos(fitbounds="locations", projection_type="equirectangular")
    figure.update_layout(margin={"r": 10, "t": 0, "l": 10, "b": 0, "pad": 0})
    figure.update_traces(marker_opacity=0.5)

    return figure


def pacific_map(pacific_eez: gpd.GeoDataFrame, id_out: str, storage: str) -> dcc.Graph:
    selected = pd.Series({i: False for i in pacific_eez["pacific_island"]})
    map_div = dcc.Graph(
        figure=_helper_pacific_map(pacific_eez, selected=selected, id_out=id_out),
        id=id_out,
        style={"justifyContent": "center", "backgroundColor": "red"},
        config={"displayModeBar": False},
    )

    @callback(
        Output(storage, "data"),
        Input(id_out, "clickData"),
        State(storage, "data"),
    )
    def update_storage(clickData, rowData: dict):
        print("Log : Callback update_storage")
        if clickData is None:
            return rowData
        territory = clickData["points"][0]["location"]
        if territory not in rowData:
            return rowData
        rowData[territory] = ~rowData[territory]
        return rowData

    @callback(
        Output(id_out, "figure"),
        Input(storage, "data"),
    )
    def update_content(data: dict):
        print("Log : Callback update_content")
        selected = pd.Series(data)
        return _helper_pacific_map(pacific_eez, selected=selected, id_out=id_out)

    return map_div
