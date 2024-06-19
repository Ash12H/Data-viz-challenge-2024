import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import html, dcc, callback, Output, Input, State
import pandas as pd
import dash_bootstrap_components as dbc
import dash_ag_grid


def _helper_chart_title(title: str) -> html.H4:
    return html.H4(title, style={"textAlign": "center"})


def _helper_no_data() -> dbc.Alert:
    return dbc.Alert(
        children=[
            html.H4("No data available for this country."),
        ],
        color="warning",
        style={"textAlign": "center", "margin": "auto", "width": "50%"},
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
        return _helper_no_data()

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
    figure.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0, "pad": 0})
    figure.add_trace(femme, row=1, col=1)
    figure.add_trace(homme, row=1, col=2)
    return dcc.Graph(
        figure=figure,
        style={
            "height": "20vh",
        },
    )


def __helper_chart_by_country_education(
    country: str, education: pd.DataFrame
) -> dcc.Graph:
    education_slice = education[
        education["Pays et territoires insulaires du Pacifique"] == country
    ]

    if education_slice.empty:
        return _helper_no_data()

    figure = px.bar(
        education_slice,
        x="Niveau d'éducation",
        y="Ratio",
        color="Genre",
        barmode="stack",
        labels={"Value": "Total population"},
        range_y=[0, 100],
    )
    figure.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0, "pad": 0})
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
    return dcc.Graph(
        figure=figure,
        style={
            "height": "35vh",
        },
    )


def __helper_chart_by_country_unemployed(
    country: str, unemployed: pd.DataFrame
) -> tuple[go.Pie, go.Pie]:
    unemp_sel = unemployed[
        unemployed["Pays et territoires insulaires du Pacifique"] == country
    ]

    if unemp_sel.empty:
        return _helper_no_data()

    unemployed_pie = px.pie(unemp_sel, names="Sexe", values="Pourcentage")
    unemployed_pie.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0, "pad": 0})
    return dcc.Graph(
        figure=unemployed_pie,
        style={
            "height": "20vh",
        },
    )


def _helper_chart_by_country(
    country: str,
    unemployed: pd.DataFrame,
    education: pd.DataFrame,
    alphabetisation: pd.DataFrame,
) -> html.Div:
    # INDICATOR
    title_alph = _helper_chart_title("Alphabétisation")
    alph_indicators = __helper_chart_by_country_alphabetisation(
        country, alphabetisation
    )

    # PIE
    title_unemployed = _helper_chart_title("Chômage")
    unemployed_pie = __helper_chart_by_country_unemployed(country, unemployed)

    # BAR
    title_education = _helper_chart_title("Éducation")
    education = __helper_chart_by_country_education(country, education)

    main_title = html.H3(
        f"{country.capitalize()}",
        style={"textAlign": "center"},
    )

    return dbc.Container(
        children=[
            dbc.Row(main_title),
            dbc.Row(
                [
                    dbc.Col([title_alph, alph_indicators], align="center", width=3),
                    dbc.Col(
                        [title_unemployed, unemployed_pie], align="center", width=4
                    ),
                    dbc.Col([title_education, education], align="center", width=5),
                ],
            ),
        ],
        fluid=True,
    )


def country_charts(
    unemployed: pd.DataFrame,
    education: pd.DataFrame,
    alphabetisation: pd.DataFrame,
    id_out: str,
    storage: str,
) -> html.Div:
    charts_div = dbc.Container(
        id=id_out, style={"backgroundColor": "purple"}, fluid=True
    )

    @callback(
        Output(id_out, "children"),
        Input(storage, "data"),
    )
    def update_charts_by_country(data: list):
        print("Log : Callback update_charts_by_country")
        if not any(data.values()):
            return _helper_empty()

        countries = [territory for territory, selected in data.items() if selected]

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
        # Same but with a Hr between each
        # charts_children = [
        #     html.Div(
        #         [
        #             _helper_chart_by_country(
        #                 country, unemployed_slice, education_slice, alphabetisation_slice
        #             ),
        #             html.Hr(),
        #         ]
        #     )
        #     for country in countries
        # ]

        return html.Div(charts_children)

    return charts_div
