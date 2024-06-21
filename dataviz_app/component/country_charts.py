import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import html, dcc, callback, Output, Input, no_update
import pandas as pd
import dash_bootstrap_components as dbc
from dataviz_app.component.separator_wave import separator_wave

SIZE_FONT = 20
BAR_WIDTH = 500
PIE_WIDTH = 300


def _main_title(title) -> html.Div:
    return html.H3(
        title,
        style={"--w": "0px", "--c": "#FAFAFA", "color": "#0F0A31", "font-size": "3em"},
        className="fancy all_text",
    )


def _helper_chart_title(title: str) -> html.H4:
    return html.H4(
        title,
        className="header_graph",
    )


def _helper_no_data() -> dbc.Alert:
    return html.Div(
        html.P(
            "No data",
            style={
                "textAlign": "center",
                "fontSize": "1.5em",
                "font-family": "Times New Roman",
                "background-color": "rgba(0,0,0,0.5)",
                "border-radius": "10px",
                "display": "inline-block",
                "padding": "10px",
            },
        ),
        style={
            # center content
            "display": "flex",
            "justify-content": "center",
            "align-items": "center",
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

    def _indicator_generator(value, reference, title):
        return go.Indicator(
            mode="number+delta",
            value=value,
            delta={
                "reference": reference,
                "relative": True,
                "valueformat": ".1%",
                "increasing": {"color": "#F6BA45"},
                "decreasing": {"color": "#4878AD"},
                "font": {"size": 30, "family": "Times New Roman"},
            },
            title={
                "text": title,
                "font": {"size": 40, "family": "Times New Roman"},
            },
            number={
                "suffix": "%",
                "valueformat": ".1f",
                "font": {"size": 60, "family": "Times New Roman"},
            },
        )

    femme = _indicator_generator(data["Femme"], data["Homme"], "Femme")
    homme = _indicator_generator(data["Homme"], data["Femme"], "Homme")
    figure = make_subplots(
        rows=2,
        cols=1,
        specs=[[{"type": "indicator"}], [{"type": "indicator"}]],
    )
    figure.update_layout(
        margin={"r": 0, "t": 75, "l": 0, "b": 75, "pad": 0},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    figure.layout.template = "plotly_dark"
    figure.add_trace(femme, row=1, col=1)
    figure.add_trace(homme, row=2, col=1)
    return dcc.Graph(figure=figure)


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
        range_y=[0, 100],
        template="plotly_dark",
        color_discrete_map={"Femme": "#F6BA45", "Homme": "#4878AD"},
        width=BAR_WIDTH,
    )
    figure.for_each_annotation(
        lambda a: a.update(
            text=a.text.split("=")[-1],
            font=dict(
                family="Times New Roman",
                size=14,
                color="rgb(50, 50, 50)",
            ),
        )
    )
    figure.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.25,
            orientation="h",
            font=dict(size=SIZE_FONT + 4, family="Times New Roman"),
            title=None,
        ),
        legend_xref="container",
        legend_yref="container",
        margin={"r": 0, "t": 0, "l": 0, "b": 0, "pad": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(
            gridcolor="#FAFAFA",
            gridwidth=1,
            tickvals=[0, 25, 50, 75, 100],
            ticktext=["0%", "25%", "50%", "75%", "100%"],
        ),
        font=dict(size=SIZE_FONT, family="Times New Roman"),
    )
    figure.update_xaxes(title=None)
    return dcc.Graph(figure=figure)


def __helper_chart_by_country_unemployed(
    country: str, unemployed: pd.DataFrame
) -> dcc.Graph:
    unemp_sel = unemployed[
        unemployed["Pays et territoires insulaires du Pacifique"] == country
    ]

    if unemp_sel.empty:
        return _helper_no_data()

    unemployed_pie = px.pie(
        unemp_sel,
        names="Sexe",
        values="Pourcentage",
        template="plotly_dark",
        # set color
        color_discrete_map={"Femme": "#F6BA45", "Homme": "#4878AD"},
        color="Sexe",
        width=PIE_WIDTH,
    )
    unemployed_pie.update_layout(
        legend=dict(
            yanchor="top",
            y=1.1,
            x=0.25,
            orientation="v",
            # title="Genre",
            font=dict(size=SIZE_FONT + 4, family="Times New Roman"),
        ),
        font=dict(size=SIZE_FONT, family="Times New Roman"),
        # legend_xref="container",
        # legend_yref="container",
        margin={"r": 20, "t": 20, "l": 20, "b": 20},
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return dcc.Graph(figure=unemployed_pie)


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

    # DIV
    title_div = _main_title(country.capitalize())

    def centered_row(children, **kwargs) -> dbc.Row:
        return dbc.Row(
            children,
            justify="center",
            align="center",
            style={**kwargs},
        )

    alph_div = dbc.Col(
        [dbc.Row(title_alph, justify="start"), centered_row(alph_indicators)],
        width="auto",
    )
    unemployed_div = dbc.Col(
        [dbc.Row(title_unemployed), centered_row(unemployed_pie)],
        width="auto",
    )
    education_div = dbc.Col(
        [dbc.Row(title_education), centered_row(education)],
        width="auto",
    )

    return dbc.Container(
        children=[
            separator_wave(),
            html.Div(
                [
                    dbc.Row(title_div),
                    dbc.Row(style={"height": "25px"}),
                    dbc.Row(
                        [alph_div, education_div, unemployed_div],
                        justify="evenly",
                        style={"width": "90vw", "margin": "auto"},
                        class_name="g-5",
                    ),
                    dbc.Row(style={"height": "100px"}),
                ],
                className="container_chart",
            ),
        ],
        fluid=True,
        className="g-0",
    )


def country_charts(
    unemployed: pd.DataFrame,
    education: pd.DataFrame,
    alphabetisation: pd.DataFrame,
    id_out: str,
    storage: str,
) -> dbc.Col:
    charts_div = dbc.Col(id=id_out, className="g-0")

    @callback(
        Output(id_out, "children"),
        Input(storage, "data"),
    )
    def update_charts_by_country(data: list) -> None | html.Div:
        print("Log : Callback update_charts_by_country")
        if not any(data.values()):
            return None

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

        return dbc.Col([html.Div(style={"height": "100px"}), *charts_children])

    return charts_div
