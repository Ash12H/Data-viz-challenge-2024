import plotly.express as px
import geopandas as gpd
from dash import callback, Output, Input, State
from dash import dcc
import pandas as pd
from dataviz_app import id


def _helper_pacific_map(pacific_eez: gpd.GeoDataFrame, selected: pd.Series):
    data = pacific_eez.set_index("pacific_island")
    data["Selected"] = selected
    data = data.rename(columns={"ile_du_pacifique": "Nom français"})
    # rename index
    data.index.name = "English name"

    figure = px.choropleth(
        data_frame=data,
        geojson=data.geometry,
        locations=data.index,
        color="Selected",
        color_discrete_map={False: "grey", True: "#433279"},
        hover_data={"Nom français": True, "Selected": False},
    )
    figure.update_traces(marker_opacity=0.5)
    figure.update_geos(
        projection=dict(type="natural earth", scale=1, rotation=dict(lon=180)),
        bgcolor="rgba(0,0,0,0)",
        oceancolor="#4878AD",
        landcolor="#F6BA45",
        lakecolor="#4878AD",
        showland=True,
        showlakes=True,
        showocean=True,
        showcoastlines=True,
    )
    figure.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0, pad=0, autoexpand=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return figure


def pacific_map(pacific_eez: gpd.GeoDataFrame) -> dcc.Graph:
    selected = pd.Series({i: False for i in pacific_eez["pacific_island"]})
    map_div = dcc.Graph(
        figure=_helper_pacific_map(pacific_eez, selected=selected),
        id=id.PACIFIC_MAP,
        style={"height": "70vh", "margin": "0px", "padding": "0px"},
        config={"displayModeBar": False},
    )

    @callback(
        Output(id.STORE, "data"),
        Input(id.PACIFIC_MAP, "clickData"),
        State(id.STORE, "data"),
    )
    def update_storage(clickData, rowData: dict):
        if clickData is None:
            return rowData
        territory = clickData["points"][0]["location"]
        if territory not in rowData:
            return rowData
        rowData[territory] = False if rowData[territory] else True
        return rowData

    @callback(
        Output(id.PACIFIC_MAP, "figure"),
        Input(id.STORE, "data"),
    )
    def update_content(data: dict):
        selected = pd.Series(data)
        return _helper_pacific_map(pacific_eez, selected=selected)

    return map_div
