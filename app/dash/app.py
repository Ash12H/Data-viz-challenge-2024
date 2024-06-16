from dash import Dash, html, dcc, Input, Output
import geopandas as gpd
import pandas as pd
import numpy as np
import plotly.express as px

app = Dash()

# LOAD DATA

pacific_eez = gpd.read_file(
    "/Users/ash/Documents/Workspaces/Python/Data-viz-challenge-2024/data/shapes/2_clean/pacific_eez.geojson"
)
pacific_eez = pacific_eez.drop(columns=["index"]).set_index("pacific_island")
df_pacific = pd.DataFrame(
    {"eez_id": pacific_eez.index, "value": np.random.rand(13) * 10}
)

ratio = pd.read_parquet(
    "/Users/ash/Documents/Workspaces/Python/Data-viz-challenge-2024/data/3_product/education_attainment_ratio.parquet"
)

# SETUP MAP

fig = px.choropleth(
    df_pacific,
    locations="eez_id",
    geojson=pacific_eez,
    color="value",
    color_continuous_scale="Viridis",
)
fig.update_geos(
    fitbounds="locations",
    # projection en oval pour la carte du pacifique
    projection_type="equirectangular",
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_traces(marker_opacity=0.5)


# SETUP LAYOUT

title_div = html.Div(
    children=[
        html.H1(children="DataViz Challenge 2024"),
    ],
    style={
        "textAlign": "center",
        "backgroundColor": "blue",
    },
)

map_div = html.Div(
    children=[
        dcc.Graph(figure=fig, id="ezz_map"),
    ],
    style={
        "justifyContent": "center",
        "backgroundColor": "red",
        "margin": "auto",
        "width": "70%",
    },
)

text_div = html.Div(
    children=[
        html.P(
            "Click or select multiple countries to get more information (double click to reset)."
        ),
        html.P(id="clicked_country"),
    ],
    style={
        "textAlign": "center",
    },
)

chart_div = html.Div(
    children=[],
    id="ratio_div",
    style={
        "justifyContent": "center",
        "backgroundColor": "red",
        "margin": "auto",
        "width": "70%",
    },
)

# CALLBACKS


@app.callback(
    Output("clicked_country", "children"),
    Input("ezz_map", "clickData"),
    Input("ezz_map", "selectedData"),
)
def display_click_data(clickData, selectedData):
    if selectedData is None and clickData is None:
        return "None"

    if selectedData is not None:
        country = [i["location"] for i in selectedData["points"]]

    elif clickData is not None:
        country = [clickData["points"][0]["location"]]

    return f"Country: {country}"


@app.callback(
    Output("ratio_div", "children"),
    Input("ezz_map", "clickData"),
    Input("ezz_map", "selectedData"),
)
def chart_by_country(clickData, selectedData):
    if selectedData is None and clickData is None:
        return "None"

    if selectedData is not None:
        country = [i["location"] for i in selectedData["points"]]

    elif clickData is not None:
        country = [clickData["points"][0]["location"]]

    ratio_country = ratio[
        ratio["Pays et territoires insulaires du Pacifique"].isin(country)
    ]

    fig = px.bar(
        ratio_country,
        x="Niveau d'éducation",
        y="Ratio",
        color="Genre",
        facet_row="Pays et territoires insulaires du Pacifique",
        barmode="stack",
        title="Répartition des niveaux d'éducation par genre et par territoire",
        labels={"Value": "Total population"},
        range_y=[0, 100],
        height=200 + (200 * len(country)),
        width=800,
    )
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return dcc.Graph(figure=fig)


# APP LAYOUT

app.layout = html.Div(children=[title_div, map_div, text_div, chart_div])

if __name__ == "__main__":
    app.run_server(debug=True)
