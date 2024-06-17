from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
from plotly.graph_objs._figure import Figure


def _chart_helper(ratio_country: pd.DataFrame, param: dict) -> Figure:
    figure = px.bar(
        ratio_country,
        x="Niveau d'éducation",
        y="Ratio",
        color="Genre",
        barmode="stack",
        labels={"Value": "Total population"},
        range_y=[0, 100],
        **param,
    )

    figure.for_each_annotation(
        lambda a: a.update(
            text=a.text.split("=")[-1],
            font=dict(family="Arial", size=14, color="rgb(50, 50, 50)", weight="bold"),
        )
    )

    figure.update_layout(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.1, orientation="h"),
        legend_xref="container",
        legend_yref="container",
    )

    figure.add_hline(
        y=50,
        line_dash="dot",
        line_color="black",
        annotation=dict(x=0.1, y=50, text="50%"),
    )
    return figure


def chart(ratio: pd.DataFrame, id_out: str, id_in: str) -> html.Div:
    chart_div = html.Div(children=[], id=id_out, style={"backgroundColor": "purple"})

    @callback(
        Output(id_out, "children"),
        Input(id_in, "clickData"),
        Input(id_in, "selectedData"),
    )
    def chart_by_country(
        clickData, selectedData
    ) -> tuple[html.H2, html.P] | tuple[html.H2, dcc.Graph]:
        title = html.H2(
            "Répartition des niveaux d'éducation atteints par genre et par territoire",
            style={"textAlign": "center"},
        )

        if selectedData is None and clickData is None:
            return title, html.P(
                "Click or select multiple countries to get more information.\n"
                "TODO : Créer un toast qui explique comment utiliser le graphique.\n"
                "Contour arrondis, pointillés, text en gris clair...",
                style={
                    "textAlign": "center",
                    "margin": "100px",
                    "padding": "20px",
                    "border": "5px dashed #ccc",
                    "border-radius": "10px",
                    "background-color": "#f6f6f6",
                },
            )

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
                "facet_col_spacing": 0.05,
                "facet_row_spacing": 0.04,
            }

        graph = dcc.Graph(figure=_chart_helper(ratio_country, param))

        return (title, graph)

    return chart_div
