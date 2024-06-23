from dash import dcc
import plotly.express as px
import pandas as pd

BAR_WIDTH = 500
SIZE_FONT = 20


def education_bar(education: pd.DataFrame) -> dcc.Graph:
    education_slice = education.rename(
        columns={"Genre": "Gender", "Niveau d'éducation": "Education level"}
    ).replace({"Femme": "Women", "Homme": "Men"})

    education_slice["Education level"] = education_slice[
        "Education level"
    ].cat.rename_categories(
        {
            "Petite enfance": "Kindergarten",
            "Primaire": "Primary",
            "Secondaire inf.": "Lower secondary",
            "Secondaire sup.": "Upper secondary",
            "Post-sec. non sup.": "Post-sec non-tertiary",
            "Tertiaire": "Tertiary",
            "Non indiqué": "Not specified",
            "Total": "Total",
        }
    )

    figure = px.bar(
        education_slice,
        x="Education level",
        y="Ratio",
        color="Gender",
        barmode="stack",
        range_y=[0, 100],
        template="plotly_dark",
        color_discrete_map={"Women": "#F6BA45", "Men": "#4878AD"},
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
