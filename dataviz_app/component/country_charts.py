from dash import html, dcc, callback, Output, Input
import pandas as pd
import dash_bootstrap_components as dbc
from dataviz_app.component.separator_wave import separator_wave
from dataviz_app.component import charts

SIZE_FONT = 20
BAR_WIDTH = 500
PIE_WIDTH = 300
PIE_HEIGHT = 300


def _main_title(title) -> html.Div:
    return html.H3(
        title,
        style={"--w": "0px", "--c": "#FAFAFA", "color": "#0F0A31", "font-size": "3em"},
        className="fancy all_text",
    )


def _helper_chart_title(title: str, style: dict = None) -> html.H4:
    return html.H4(title, className="header_graph", style=style)


def __helper_chart_by_country_alphabetisation(
    country: str, alphabetisation: pd.DataFrame
) -> dcc.Graph:
    alph_sel = alphabetisation[
        alphabetisation["Pays et territoires insulaires du Pacifique"] == country
    ]

    if alph_sel.empty:
        return charts.no_data()

    return charts.alphabetisation_indicators(
        men=alph_sel["Homme"].values[0], women=alph_sel["Femme"].values[0]
    )


def __helper_chart_by_country_education(
    country: str, education: pd.DataFrame
) -> dcc.Graph:
    education_slice = education[
        education["Pays et territoires insulaires du Pacifique"] == country
    ]
    if education_slice.empty:
        return charts.no_data()

    return charts.education_bar(education_slice)


def __helper_chart_by_country_unemployed(
    country: str, unemployed: pd.DataFrame
) -> dcc.Graph:
    unemp_sel = unemployed[
        unemployed["Pays et territoires insulaires du Pacifique"] == country
    ]

    if unemp_sel.empty:
        return charts.no_data()

    return charts.unemployed_pie(unemp_sel)


def _helper_chart_by_country(
    country: str,
    unemployed: pd.DataFrame,
    education: pd.DataFrame,
    alphabetisation: pd.DataFrame,
) -> html.Div:
    def centered_row(children, **kwargs) -> dbc.Row:
        return dbc.Row(
            children,
            justify="center",
            align="center",
            style={**kwargs},
        )

    # INDICATOR
    title_alph = _helper_chart_title("Youth literacy rate")
    alph_indicators = __helper_chart_by_country_alphabetisation(
        country, alphabetisation
    )
    alph_div = dbc.Col(
        [dbc.Row(title_alph, justify="start"), centered_row(alph_indicators)],
        width="auto",
    )

    # PIE
    title_unemployed = _helper_chart_title(
        "Youth not in education employment or training",
        style={"width": "400px"},
    )
    unemployed_pie = __helper_chart_by_country_unemployed(country, unemployed)
    unemployed_div = dbc.Col(
        [dbc.Row(title_unemployed), centered_row(unemployed_pie)],
        width="auto",
    )

    # BAR
    title_education = _helper_chart_title("Education attainment")
    education = __helper_chart_by_country_education(country, education)
    education_div = dbc.Col(
        [dbc.Row(title_education), centered_row(education)],
        width="auto",
    )

    # MAIN DIV
    content = html.Div(
        [
            dbc.Row(_main_title(country.capitalize())),
            dbc.Row(style={"height": "25px"}),
            dbc.Row([alph_div, education_div, unemployed_div], justify="evenly"),
            dbc.Row(style={"height": "100px"}),
        ],
        className="container_chart",
    )
    return dbc.Container(
        children=[html.Div(separator_wave()), content], fluid=True, className="g-0"
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
