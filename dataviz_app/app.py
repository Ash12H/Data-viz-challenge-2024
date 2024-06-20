from dash import Dash, html, dcc
import geopandas as gpd
import pandas as pd
import dash_bootstrap_components as dbc


from dataviz_app.id import (
    PACIFIC_MAP,
    CHART,
    CONTENT_ROW,
    MAIN_LAYOUT,
    MAP_ROW,
    MENU,
    STORE,
)
from dataviz_app.component.pacific_map import pacific_map
from dataviz_app.component.country_charts import country_charts
from dataviz_app.component.menu import menu


app = Dash(external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP])


# LOAD DATA-----------------------------------------------------------

## 1. SHAPES
pacific_eez = gpd.read_file(
    "/Users/ash/Documents/Workspaces/Python/Data-viz-challenge-2024/data/shapes/2_clean/pacific_eez.geojson"
)
pacific_eez = pacific_eez.drop(columns=["index"])

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
## 5. CLIENT STORAGE
storage_data = {i: False for i in pacific_eez["pacific_island"]}
storage = dcc.Store(id=STORE, data=storage_data)

# SETUP LAYOUT -----------------------------------------------------------
title_div = html.H1(
    "Répartition des niveaux d'éducation atteints par genre et par territoire",
    style={
        "textAlign": "center",
        "fontFamily": "Georgia, serif",
        "fontSize": "3em",
        "letterSpacing": "-0.6px",
        "wordSpacing": "0.6px",
        "color": "#000000",
        "fontWeight": "700",
        "textDecoration": "none",
        "fontStyle": "normal",
        "fontVariant": "small-caps",
        "textTransform": "capitalize",
        # font color
        "fontColor": "#0F0A31",
    },
)

sub_title_div = html.H2(
    "Informations sur le pays sélectionné",
    className="fancy all_text",
    style={"--b": "6px", "--w": "80px", "--g": "15px"},
)


map_div = pacific_map(pacific_eez, id_out=PACIFIC_MAP, storage=STORE)

charts_div = country_charts(
    unemployed=unemployed,
    education=education,
    alphabetisation=alphabetisation,
    id_out=CHART,
    storage=STORE,
)

offcanvas = menu(id_out=MENU)

# APP LAYOUT

main_layout = dbc.Container(
    children=[
        offcanvas,
        storage,
        dbc.Row(
            children=[dbc.Col(title_div, align="center", width=9, className="g-0")],
            justify="center",
            style={"height": "20vh"},
        ),
        dbc.Row(
            children=[dbc.Col(map_div, id=MAP_ROW, align="center", className="g-0")],
            justify="center",
            style={"height": "80vh"},
        ),
        dbc.Row(
            children=[dbc.Col(sub_title_div, align="center", className="g-0")],
            justify="center",
            style={"height": "20vh"},
        ),
        dbc.Row(id=CONTENT_ROW, children=[charts_div], justify="center"),
    ],
    id=MAIN_LAYOUT,
    fluid=True,
    style={"backgroundColor": "#FAFAFA"},
)

app.layout = main_layout

if __name__ == "__main__":
    app.run_server(debug=True)
