import plotly.express as px
import pandas as pd
from dash import dcc

SIZE_FONT = 20
PIE_WIDTH = 300
PIE_HEIGHT = 300


def unemployed_pie(unemployed: pd.DataFrame) -> dcc.Graph:
    unemp_sel = unemployed.rename(columns={"Sexe": "Gender"}).replace(
        {"Femme": "Women", "Homme": "Men"}
    )

    unemployed_pie = px.pie(
        unemp_sel,
        names="Gender",
        values="Pourcentage",
        template="plotly_dark",
        color_discrete_map={"Women": "#F6BA45", "Men": "#4878AD"},
        color="Gender",
        width=PIE_WIDTH,
        height=PIE_HEIGHT,
    )
    unemployed_pie.update_layout(
        legend=dict(
            yanchor="top",
            y=0,
            x=0.15,
            orientation="h",
            font=dict(size=SIZE_FONT + 4, family="Times New Roman"),
        ),
        font=dict(size=SIZE_FONT, family="Times New Roman"),
        margin={"t": 20, "r": 0, "b": 0, "l": 0, "pad": 0},
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return dcc.Graph(
        figure=unemployed_pie,
        style={
            "padding": "0px",
            "margin": "0px",
            "width": "fit-content",
            "height": "fit-content",
        },
    )
