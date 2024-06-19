import dash_ag_grid
import pandas as pd
from dash import callback, Output, Input


def agrid_territory(data: pd.DataFrame, id_out: str, id_in: str):
    agrid_div = dash_ag_grid.AgGrid(
        id=id_out,
        columnDefs=[
            {
                "headerName": "Territory",
                "field": "Territory",
                "sortable": False,
                "rowDrag": True,
            },
        ],
        rowData=pd.DataFrame({"Territory": data["pacific_island"]}).to_dict("records"),
        dashGridOptions={
            "animateRows": "animate",
            "rowDragManaged": True,
            "domLayout": "autoHeight",
        },
    )

    @callback(
        Output(id_out, "rowData"),
        Input(id_in, "data"),
    )
    def update_content(storage):
        countries = [territory for territory, selected in storage.items() if selected]
        return pd.DataFrame({"Territory": countries}).to_dict("records")

    return agrid_div
