from dash import html, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

MENU_CONTENT = dbc.Container(
    children=[
        dbc.Row(html.H2("Map")),
        dbc.Row(html.P("Map of the Pacific Ocean...")),
        dbc.Row(html.H2("Charts")),
        dbc.Row(html.H3("Alphabetisation")),
        dbc.Row(html.P("Indicator...")),
        dbc.Row(html.H3("Education")),
        dbc.Row(html.P("Bar...")),
        dbc.Row(html.H3("Unemployment")),
        dbc.Row(html.P("Pie chart...")),
    ]
)


def menu(id_out: str) -> html.Div:
    canvas_menu = html.Div(
        [
            dbc.Button(
                children=html.I(
                    className="bi bi-list",
                    style={
                        "fontSize": "3em",
                        # no space around the icon
                        "margin": "0px",
                        "padding": "0px",
                        # remonte le texte d'un certain nombre de pixels
                        "position": "relative",
                        "top": "-11px",
                    },
                ),
                id="button_menu",
                n_clicks=0,
                style={
                    "position": "fixed",
                    "top": "10px",
                    "left": "10px",
                    "border": "none",
                    # same size as the icon inside
                    "height": "50px",
                    "width": "50px",
                    "borderRadius": "50%",
                    "margin": "0px",
                    "padding": "0px",
                    # in foreground
                    "zIndex": "999",
                },
            ),
            dbc.Offcanvas(
                MENU_CONTENT,
                id=id_out,
                title="DataViz Challenge 2024",
                is_open=False,
                placement="top",
                style={"height": "100vh", "width": "50vw", "overflowY": "auto"},
            ),
        ]
    )

    @callback(
        Output(id_out, "is_open"),
        Input("button_menu", "n_clicks"),
        [State(id_out, "is_open")],
    )
    def toggle_offcanvas(n1, is_open):
        if n1:
            return not is_open
        return is_open

    return canvas_menu
