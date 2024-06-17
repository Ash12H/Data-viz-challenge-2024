import plotly.express as px
import pandas as pd
import geopandas as gpd
from plotly.graph_objs._figure import Figure


def pacific_map(data: pd.DataFrame, pacific_eez: gpd.GeoDataFrame) -> Figure:
    figure = px.choropleth(
        data,
        locations="eez_id",
        geojson=pacific_eez,
        color="value",
        color_continuous_scale="Viridis",
    )
    figure.update_coloraxes(
        colorbar_orientation="h",
        colorbar_x=0.5,
        colorbar_y=-0.2,
        colorbar_title="Value",
        colorbar_title_side="top",
    )
    figure.update_geos(
        fitbounds="locations",
        projection_type="equirectangular",
    )
    figure.update_layout(margin={"r": 10, "t": 0, "l": 10, "b": 0, "pad": 0})
    figure.update_traces(marker_opacity=0.5)
    return figure
