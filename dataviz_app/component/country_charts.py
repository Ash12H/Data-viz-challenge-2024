import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import html, dcc, callback, Output, Input
import pandas as pd
import dash_bootstrap_components as dbc


def _helper_section_title() -> html.H2:
    return html.H2(
        "Informations sur le pays sélectionné", style={"textAlign": "center"}
    )


def _helper_empty():
    return dbc.Alert(
        children=[
            html.H4("Info"),
            html.P("Click or select multiple countries to get more information."),
        ],
        color="info",
        style={
            "textAlign": "center",
            "margin": "auto",
            "width": "50%",
            "marginTop": "4%",
        },
    )


def __helper_chart_by_country_alphabetisation(
    country: str, alphabetisation: pd.DataFrame
) -> dcc.Graph:
    alph_sel = alphabetisation[
        alphabetisation["Pays et territoires insulaires du Pacifique"] == country
    ]

    if alph_sel.empty:
        data = {"Femme": 0, "Homme": 0}
    else:
        data = {
            "Femme": alph_sel["Femme"].values[0],
            "Homme": alph_sel["Homme"].values[0],
        }

    femme = go.Indicator(
        mode="number+delta",
        value=data["Femme"],
        delta={
            "reference": data["Homme"],
            "relative": True,
            "valueformat": ".1%",
        },
        title={"text": "Femme"},
    )
    homme = go.Indicator(
        mode="number+delta",
        value=data["Homme"],
        delta={
            "reference": data["Femme"],
            "relative": True,
            "valueformat": ".1%",
        },
        title={"text": "Homme"},
    )
    figure = make_subplots(
        rows=1, cols=2, specs=[[{"type": "indicator"}, {"type": "indicator"}]]
    )
    figure.add_trace(femme, row=1, col=1)
    figure.add_trace(homme, row=1, col=2)
    return dcc.Graph(figure=figure)


def __helper_chart_by_country_education(
    country: str, education: pd.DataFrame
) -> dcc.Graph:
    education_slice = education[
        education["Pays et territoires insulaires du Pacifique"] == country
    ]

    figure = px.bar(
        education_slice,
        x="Niveau d'éducation",
        y="Ratio",
        color="Genre",
        barmode="stack",
        labels={"Value": "Total population"},
        range_y=[0, 100],
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
    return dcc.Graph(figure=figure)


def __helper_chart_by_country_unemployed(
    country: str, unemployed: pd.DataFrame
) -> tuple[go.Pie, go.Pie]:
    unemp_sel = unemployed[
        unemployed["Pays et territoires insulaires du Pacifique"] == country
    ]

    if unemp_sel.empty:
        return dbc.Alert(
            children=[
                html.H4(
                    "No data available for this country.",
                    style={
                        # center the title in the alert
                        "textAlign": "center",
                        "margin": "auto",
                        "backgroundColor": "red",
                        # 40% padding top
                        "paddingTop": "40%",
                    },
                ),
            ],
            color="warning",
            style={"width": "100%", "height": "100%"},
        )
    unemployed_pie = px.pie(unemp_sel, names="Sexe", values="Pourcentage")

    return dcc.Graph(figure=unemployed_pie)


def _helper_chart_by_country(
    country: str,
    unemployed: pd.DataFrame,
    education: pd.DataFrame,
    alphabetisation: pd.DataFrame,
) -> html.Div:
    # INDICATOR
    alph_indicators = __helper_chart_by_country_alphabetisation(
        country, alphabetisation
    )

    # PIE
    unemployed_pie = __helper_chart_by_country_unemployed(country, unemployed)

    # BAR

    education = __helper_chart_by_country_education(country, education)

    return html.Div(
        children=[
            dbc.Row(html.H3(f"Indicateurs pour {country}")),
            dbc.Row(
                [
                    dbc.Col(alph_indicators),
                    dbc.Col(unemployed_pie),
                    dbc.Col(education),
                ]
            ),
        ],
        style={"backgroundColor": "blue"},
    )


def country_charts(
    unemployed: pd.DataFrame,
    education: pd.DataFrame,
    alphabetisation: pd.DataFrame,
    id_out: str,
    id_in: str,
) -> html.Div:
    charts_div = html.Div(id=id_out, style={"backgroundColor": "purple"})

    @callback(
        Output(id_out, "children"),
        Input(id_in, "clickData"),
        Input(id_in, "selectedData"),
    )
    def update_charts_by_country(clickData, selectedData):
        section_title = _helper_section_title()

        if selectedData is None and clickData is None:
            return section_title, _helper_empty()

        if selectedData is not None:
            countries = [i["location"] for i in selectedData["points"]]
        elif clickData is not None:
            countries = [clickData["points"][0]["location"]]

        unemployed_slice = unemployed[
            unemployed["Pays et territoires insulaires du Pacifique"].isin(countries)
        ]
        education_slice = education[
            education["Pays et territoires insulaires du Pacifique"].isin(countries)
        ]
        alphabetisation_slice = alphabetisation[
            alphabetisation["Pays et territoires insulaires du Pacifique"].isin(
                countries
            )
        ]

        charts_children = [
            _helper_chart_by_country(
                country, unemployed_slice, education_slice, alphabetisation_slice
            )
            for country in countries
        ]
        return section_title, html.Div(charts_children)

    return charts_div
