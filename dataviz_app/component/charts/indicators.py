from dash import dcc
from plotly.subplots import make_subplots
from plotly import graph_objects as go


def alphabetisation_indicators(men, women) -> dcc.Graph:
    def _indicator_generator(value, reference, title) -> go.Indicator:
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

    femme = _indicator_generator(women, men, "Women")
    homme = _indicator_generator(men, women, "Men")
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
