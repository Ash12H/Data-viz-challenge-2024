from dash import Dash, html, dcc, Input, Output
import geopandas as gpd
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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

# SETUP MAP -----------------------------------------------------------

fig = px.choropleth(
    df_pacific,
    locations="eez_id",
    geojson=pacific_eez,
    color="value",
    color_continuous_scale="Viridis",
)
# put the color scale below the map
# fig.update_layout(coloraxis_colorbar=dict(yanchor="bottom", y=0.1, x=0.85))
fig.update_coloraxes(
    colorbar_orientation="h",
    colorbar_x=0.5,
    colorbar_y=-0.2,
    colorbar_title="Value",
    # title above the color scale
    colorbar_title_side="top",
)
fig.update_geos(
    fitbounds="locations",
    projection_type="equirectangular",
)
fig.update_layout(margin={"r": 2, "t": 2, "l": 2, "b": 2, "pad": 10})
fig.update_traces(marker_opacity=0.5)


# SETUP LAYOUT -----------------------------------------------------------

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
        html.H2(
            "Répartition des niveaux d'éducation atteints par genre et par territoire"
        ),
        dcc.Graph(figure=fig, id="ezz_map"),
    ],
    style={
        "justifyContent": "center",
        "backgroundColor": "red",
        "margin": "auto",
        "width": "95%",
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
        # "justifyContent": "center",
        "backgroundColor": "purple",
        # "margin": "auto",
        # "width": "70%",
    },
)


# CALLBACKS ---------------------------------------------------------------


@app.callback(
    Output("ratio_div", "children"),
    Input("ezz_map", "clickData"),
    Input("ezz_map", "selectedData"),
)
def chart_by_country(clickData, selectedData):
    if selectedData is None and clickData is None:
        return

    if selectedData is not None:
        country = [i["location"] for i in selectedData["points"]]

    elif clickData is not None:
        country = [clickData["points"][0]["location"]]

    ratio_country = ratio[
        ratio["Pays et territoires insulaires du Pacifique"].isin(country)
    ]

    nb_country = len(
        ratio_country["Pays et territoires insulaires du Pacifique"].unique()
    )
    if nb_country < 3:
        param = {
            "height": max(500, 380 * nb_country),
            "facet_row": "Pays et territoires insulaires du Pacifique",
        }
    else:
        param = {
            "height": max(500, 380 * (nb_country // 2 + nb_country % 2)),
            "facet_col": "Pays et territoires insulaires du Pacifique",
            "facet_col_wrap": 2,
        }

    fig = px.bar(
        ratio_country,
        x="Niveau d'éducation",
        y="Ratio",
        color="Genre",
        barmode="stack",
        labels={"Value": "Total population"},
        range_y=[0, 100],
        **param,
    )
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    # put the legend above the graph
    fig.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.1, orientation="h"),
        legend_xref="container",
        legend_yref="container",
    )
    # trace une ligne pointillée à 50% qui apparait dans la légende
    fig.add_hline(
        y=50,
        line_dash="dot",
        line_color="black",
        annotation=dict(x=0.1, y=50, text="50%"),
    )

    title = html.H2(
        "Répartition des niveaux d'éducation atteints par genre et par territoire",
        style={"textAlign": "center"},
    )
    graph = dcc.Graph(figure=fig, style={"width": "100%"})

    return (title, graph)


# APP LAYOUT

main_layout = html.Div(
    children=[
        dbc.Row(id="title_row", children=[title_div], style={"height": "10vh"}),
        dbc.Row(
            id="content_row",
            children=[
                dbc.Col(children=[map_div, text_div]),
                dbc.Col(
                    children=[chart_div],
                    style={
                        "maxHeight": "90vh",
                        "overflow": "scroll",
                        "width": "50wh",
                        "margin": 0,
                        "padding": 0,
                        "backgroundColor": "green",
                    },
                ),
            ],
        ),
    ],
    id="main_layout",
)

app.layout = main_layout

if __name__ == "__main__":
    app.run_server(debug=True)
