from dash import html, callback, Input, Output
from dataviz_app import id


def animated_arrow(right: bool) -> html.Div:
    position = "right" if right else "left"
    arrow_id = f"{id.ARROW}_{position}"
    arrow = html.Div(
        className="arrow-container",
        children=[
            html.I(
                id=arrow_id,
                className="bi bi-chevron-double-down arrow",
                style={
                    "visibility": "hidden",
                },
            )
        ],
        style={position: "50px"},
    )

    @callback(
        Output(arrow_id, "style"),
        Input(id.STORE, "data"),
    )
    def show_arrow(data: dict) -> bool:
        if not any(data.values()):
            return {"visibility": "hidden"}
        return {}

    return arrow
