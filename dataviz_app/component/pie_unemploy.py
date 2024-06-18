from dash import html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from plotly.graph_objs._figure import Figure


def _pie_helper(unemployed_by_country: pd.DataFrame, param: dict) -> Figure:
    figure = px.pie(
        unemployed_by_country.sort_values(
            "Pays et territoires insulaires du Pacifique"
        ),
        names="Sexe",
        values="Pourcentage",
        **param,
    )
    return figure


def pie_unemploy(
    unemployed_by_country: pd.DataFrame, id_in: str, id_out: str
) -> Figure:
    pie_div = html.Div(id=id_out, style={"backgroundColor": "purple"})

    @callback(
        Output(id_out, "children"),
        Input(id_in, "clickData"),
        Input(id_in, "selectedData"),
    )
    def pie_by_country(
        clickData, selectedData
    ) -> tuple[html.H2, html.P] | tuple[html.H2, dcc.Graph]:
        title = html.H2(
            "Nombre de jeunes personnes sans études, emploi ni formation par sexe",
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
                    "min-height": "200px",
                    "min-width": "200px",
                    "border": "5px dashed #ccc",
                    "border-radius": "10px",
                    "background-color": "#f6f6f6",
                },
            )

        if selectedData is not None:
            country = [i["location"] for i in selectedData["points"]]

        elif clickData is not None:
            country = [clickData["points"][0]["location"]]

        unemployed_country_sel = unemployed_by_country[
            unemployed_by_country["Pays et territoires insulaires du Pacifique"].isin(
                country
            )
        ]

        nb_country = len(
            unemployed_country_sel[
                "Pays et territoires insulaires du Pacifique"
            ].unique()
        )
        param = {
            "height": max(500, 380 * nb_country),
            "facet_row": "Pays et territoires insulaires du Pacifique",
        }

        graph = dcc.Graph(figure=_pie_helper(unemployed_country_sel, param))

        return (title, graph)

    return pie_div
