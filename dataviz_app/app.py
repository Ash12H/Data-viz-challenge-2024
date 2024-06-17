from dash import Dash, html, dcc
import geopandas as gpd
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

from dataviz_app.id import PACIFIC_MAP, CHART, TITLE_ROW, CONTENT_ROW, MAIN_LAYOUT
from dataviz_app.component.pacific_map import pacific_map
from dataviz_app.component.chart import chart


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# LOAD DATA

pacific_eez = gpd.read_file(
    "/Users/ash/Documents/Workspaces/Python/Data-viz-challenge-2024/data/shapes/2_clean/pacific_eez.geojson"
)
pacific_eez = pacific_eez.drop(columns=["index"]).set_index("pacific_island")
df_pacific = pd.DataFrame(
    {"eez_id": pacific_eez.index, "value": np.random.rand(19) * 10}
)

ratio = pd.read_parquet(
    "/Users/ash/Documents/Workspaces/Python/Data-viz-challenge-2024/data/3_product/education_attainment_ratio.parquet"
)

# SETUP MAP -----------------------------------------------------------

map_figure = pacific_map(df_pacific, pacific_eez)


# SETUP LAYOUT -----------------------------------------------------------

title_div = html.Div(
    children=[
        html.H1(children="DataViz Challenge 2024"),
    ],
    style={"textAlign": "center", "backgroundColor": "blue"},
)

map_div = html.Div(
    children=[
        html.H2(
            "Répartition des niveaux d'éducation atteints par genre et par territoire",
            style={"textAlign": "center"},
        ),
        dcc.Graph(figure=map_figure, id=PACIFIC_MAP),
    ],
    style={"justifyContent": "center", "backgroundColor": "red"},
)

text_div = html.Div(
    children=[
        html.P(
            "Click or select multiple countries to get more information (double click to reset)."
        ),
    ],
    style={"textAlign": "center"},
)

chart_div = chart(ratio=ratio, id_in=PACIFIC_MAP, id_out=CHART)


# CALLBACKS ---------------------------------------------------------------


# APP LAYOUT

main_layout = html.Div(
    children=[
        dbc.Row(id=TITLE_ROW, children=[title_div], style={"height": "10vh"}),
        dbc.Row(
            id=CONTENT_ROW,
            children=[
                dbc.Col(
                    children=[map_div, text_div],
                    style={
                        "maxHeight": "90vh",
                        "maxWidth": "50wh",
                        "margin": "0px",
                        "padding": "0px",
                        "backgroundColor": "yellow",
                        "border": "5px dashed purple",
                    },
                ),
                dbc.Col(
                    children=[chart_div],
                    style={
                        "maxHeight": "90vh",
                        "maxWidth": "50wh",
                        "margin": "0px",
                        "padding": "0px",
                        "overflow": "scroll",
                        "backgroundColor": "green",
                        "border": "5px dashed red",
                    },
                ),
            ],
        ),
    ],
    style={
        "maxHeight": "100vh",
        "maxWidth": "100wh",
        "margin": "0px",
        "padding": "0px",
        "backgroundColor": "pink",
        "border": "5px dashed blue",
        "overflow": "hidden",
    },
    id=MAIN_LAYOUT,
)

app.layout = main_layout

if __name__ == "__main__":
    app.run_server(debug=True)
