from dash import html, callback, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

from dataviz_app.component import charts
from dataviz_app import id


def _helper_chart_title(title: str, style: dict = None) -> html.H4:
    return html.H4(title, className="header_graph", style=style)


def __helper_chart_by_country_alphabetisation(
    alphabetisation: pd.DataFrame,
) -> dcc.Graph:
    if alphabetisation.empty:
        return charts.no_data()

    return charts.alphabetisation_indicators(
        men=alphabetisation["Homme"].mean(), women=alphabetisation["Femme"].mean()
    )


def __helper_chart_by_country_education(education: pd.DataFrame) -> dcc.Graph:
    education_slice = (
        education.drop(
            columns="Pays et territoires insulaires du Pacifique",
        )
        .groupby(["Niveau d'éducation", "Genre"])
        .mean()
        .reset_index()
    )
    if education_slice.empty:
        return charts.no_data()

    return charts.education_bar(education_slice)


def __helper_chart_by_country_unemployed(unemployed: pd.DataFrame) -> dcc.Graph:
    unemp_sel = (
        unemployed.drop(
            columns="Pays et territoires insulaires du Pacifique",
        )
        .groupby(["Sexe"])
        .mean()
        .reset_index()
    )
    print(unemp_sel)

    if unemp_sel.empty:
        return charts.no_data()

    return charts.unemployed_pie(unemp_sel)


def _helper_chart_by_country(
    unemployed: pd.DataFrame, education: pd.DataFrame, alphabetisation: pd.DataFrame
) -> html.Div:
    def centered_row(children, **kwargs) -> dbc.Row:
        return dbc.Row(children, justify="center", align="center", style={**kwargs})

    # INDICATOR
    title_alph = _helper_chart_title("Youth literacy rate")
    alph_indicators = __helper_chart_by_country_alphabetisation(alphabetisation)
    alph_div = dbc.Col(
        [dbc.Row(title_alph, justify="start"), centered_row(alph_indicators)],
        width="2",
    )

    # PIE
    title_unemployed = _helper_chart_title(
        "Youth not in education employment or training",
        style={"width": "400px"},
    )
    unemployed_pie = __helper_chart_by_country_unemployed(unemployed)
    unemployed_div = dbc.Col(
        [dbc.Row(title_unemployed), centered_row(unemployed_pie)], width="3"
    )

    # BAR
    title_education = _helper_chart_title("Education attainment")
    education = __helper_chart_by_country_education(education)
    education_div = dbc.Col(
        [dbc.Row(title_education), centered_row(education)], width="5"
    )

    return dbc.Container(
        children=[dbc.Row([alph_div, education_div, unemployed_div], justify="evenly")],
        fluid=True,
        className="g-0",
    )


def overall_view(
    unemployed: pd.DataFrame, education: pd.DataFrame, alphabetisation: pd.DataFrame
) -> html.Div:
    canvas_menu = html.Div(
        [
            dbc.Button(
                children=[html.Span("Overall", className="button-menu-content")],
                id="overall_button",
                n_clicks=0,
                style={"position": "fixed", "top": "90px", "left": "10px"},
                className="button-menu",
            ),
            dbc.Offcanvas(
                id=id.OVERALL_VIEW,
                title="Overall view",
                is_open=False,
                placement="top",
                style={
                    "height": "fit-content",
                    "width": "100vw",
                    "overflowY": "auto",
                    "minHeight": "15vh",
                },
            ),
        ]
    )

    @callback(
        Output(id.OVERALL_VIEW, "is_open"),
        Input("overall_button", "n_clicks"),
        [State(id.OVERALL_VIEW, "is_open")],
    )
    def toggle_offcanvas(n1, is_open):
        if n1:
            return not is_open
        return is_open

    @callback(
        Output(id.OVERALL_VIEW, "children"),
        Input(id.STORE, "data"),
    )
    def update_charts_by_country(data: list) -> None | html.Div:
        if not any(data.values()):
            return html.P("Select at least one country.")

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

        return _helper_chart_by_country(
            unemployed_slice, education_slice, alphabetisation_slice
        )

    return canvas_menu
