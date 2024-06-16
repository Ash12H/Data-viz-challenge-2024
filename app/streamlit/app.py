import streamlit as st
import geopandas as gpd
from streamlit_folium import st_folium

file = gpd.read_file("data/shapes/2_clean/pacific_eez.geojson")

st.title("DataViz Challenge 2024")

returned_map = st_folium(
    file.explore(),
    use_container_width=True,
)

st.write(returned_map)
