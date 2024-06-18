from dash import Dash, html, dcc
import geopandas as gpd
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

from dataviz_app.id import (
    PACIFIC_MAP,
    CHART,
    CONTENT_ROW,
    MAIN_LAYOUT,
    PIE,
    MAP_ROW,
    MENU,
)
from dataviz_app.component.pacific_map import pacific_map
from dataviz_app.component.chart_educ import chart
from dataviz_app.component.pie_unemploy import pie_unemploy
from dataviz_app.component.country_charts import country_charts
from dataviz_app.component.menu import menu


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

# LOAD DATA-----------------------------------------------------------

## 1. SHAPES
pacific_eez = gpd.read_file(
    "/Users/ash/Documents/Workspaces/Python/Data-viz-challenge-2024/data/shapes/2_clean/pacific_eez.geojson"
)
pacific_eez = pacific_eez.drop(columns=["index"]).set_index("pacific_island")
df_pacific = pd.DataFrame(
    {"eez_id": pacific_eez.index, "value": np.random.rand(19) * 10}
)

## 2. EDUCATION

education = pd.read_parquet(
    "/Users/ash/Documents/Workspaces/Python/Data-viz-challenge-2024/data/3_product/education_attainment.parquet"
)

## 3. UNEMPLOYMED

unemployed = pd.read_parquet(
    "/Users/ash/Documents/Workspaces/Python/Data-viz-challenge-2024/data/3_product/unemployed.parquet"
)

## 4. ALPHABETISATION
alphabetisation = pd.read_parquet(
    "/Users/ash/Documents/Workspaces/Python/Data-viz-challenge-2024/data/3_product/alphabetisation.parquet"
)

# SETUP MAP -----------------------------------------------------------

map_figure = pacific_map(df_pacific, pacific_eez)


# SETUP LAYOUT -----------------------------------------------------------

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


# chart_div = chart(education=education, id_out=CHART, id_in=PACIFIC_MAP)

# pie_div = pie_unemploy(unemployed_by_country=unemployed, id_out=PIE, id_in=PACIFIC_MAP)
charts_div = country_charts(
    unemployed=unemployed,
    education=education,
    alphabetisation=alphabetisation,
    id_out=CHART,
    id_in=PACIFIC_MAP,
)

offcanvas = menu(id_out=MENU)


# APP LAYOUT

main_layout = html.Div(
    children=[
        offcanvas,
        dbc.Row(
            id=MAP_ROW,
            children=[map_div],
            style={
                "backgroundColor": "yellow",
                "margin": "2%",
                "padding": "2%",
            },
        ),
        dbc.Row(
            id=CONTENT_ROW,
            children=[
                # dbc.Col(
                #     children=[pie_div],
                #     style={
                #         "maxWidth": "50wh",
                #         "backgroundColor": "yellow",
                #         "border": "5px dashed purple",
                #     },
                # ),
                # dbc.Col(
                #     children=[chart_div],
                #     style={
                #         "maxWidth": "50wh",
                #         "backgroundColor": "green",
                #         "border": "5px dashed red",
                #     },
                # ),
                dbc.Col(charts_div, style={"backgroundColor": "blue"})
            ],
        ),
    ],
    style={
        "margin": "0px",
        "padding": "0px",
        "backgroundColor": "pink",
        "border": "5px dashed blue",
        "overflow": "scroll",
    },
    id=MAIN_LAYOUT,
)

app.layout = main_layout

if __name__ == "__main__":
    app.run_server(debug=True)
