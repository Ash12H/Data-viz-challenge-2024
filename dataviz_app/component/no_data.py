import dash_bootstrap_components as dbc
import dash_html_components as html


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
        style={"display": "flex", "justify-content": "center", "align-items": "center"},
    )
