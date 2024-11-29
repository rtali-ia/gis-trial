# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# from datetime import datetime

# # Coordinates for Ames, IA
# AMES_COORDINATES = [42.0308, -93.6319]

# # Sidebar inputs
# st.sidebar.title("NASA GIBS Viewer")
# layer = st.sidebar.selectbox(
#     "Select a GIBS Layer",
#     [
#         "MODIS_Terra_CorrectedReflectance_TrueColor",  # True Color
#         "VIIRS_SNPP_CorrectedReflectance_TrueColor",  # True Color
#         "MODIS_Terra_Land_Surface_Temp_Day",  # True Color
#         "Aquarius_Soil_Mositure_Daily",  # Soil Moisture
#         "AIRS_L2_Surface_Skin_Temperature_Day",  # Soil Temperature
#         "MODIS_Terra_CorrectedReflectance_Bands721",  # Infrared
#         "MODIS_Terra_NDVI_8Day",  # Surface Temperature
#         "OCO-2_Solar_Induced_Fluorescence_Blended",  # Solar Induced Fluorescence
#         "AIRS_L3_All_Sky_Outgoing_Longwave_Radiation_Daily_Day",  # Outgoing Longwave Radiation
#     ],
# )
# date = st.sidebar.date_input("Select Date", datetime.today())
# zoom = st.sidebar.slider("Zoom Level", min_value=1, max_value=12, value=8)

# # Initialize Folium map centered on Ames, IA
# m = folium.Map(location=AMES_COORDINATES, zoom_start=zoom)

# # NASA GIBS WMTS layer URL
# wmts_url = f"https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/{layer}/default/{date.strftime('%Y-%m-%d')}/250m/{{z}}/{{y}}/{{x}}.jpg"

# # Add the NASA GIBS layer
# folium.TileLayer(
#     tiles=wmts_url,
#     attr="Imagery courtesy of NASA GIBS",
#     name="NASA GIBS",
#     overlay=True,
#     control=True,
# ).add_to(m)

# # Add a layer control panel
# folium.LayerControl().add_to(m)

# # Display map in Streamlit
# st.title("NASA GIBS Data Viewer: Ames, Iowa")
# st_folium(m, width=700, height=500)



import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime

# Coordinates for Ames, IA
AMES_COORDINATES = [42.0308, -93.6319]

# Sidebar inputs
st.sidebar.title("NASA GIBS Viewer")
layer = st.sidebar.selectbox(
    "Select a GIBS Layer",
    [
        "MODIS_Terra_CorrectedReflectance_TrueColor",  # True Color
        "VIIRS_SNPP_CorrectedReflectance_TrueColor",  # True Color
        "MODIS_Aqua_CorrectedReflectance_TrueColor",  # True Color
        "SMAP_L3_Active_Soil_Moisture",  # Soil Moisture
        "MODIS_Terra_Land_Surface_Temp_Day",  # Soil Temperature
        "MODIS_Terra_CorrectedReflectance_Bands721",  # Infrared
        "CERES_NETFLUX_Outgoing_Longwave_Radiation_Day",  # Correct CERES Layer Name
    ],
)
date = st.sidebar.date_input("Select Date", datetime.today())
zoom = st.sidebar.slider("Zoom Level", min_value=1, max_value=12, value=8)

# Resolution and format mapping
layer_resolution = {
    "MODIS_Terra_CorrectedReflectance_TrueColor": "250m",
    "VIIRS_SNPP_CorrectedReflectance_TrueColor": "250m",
    "MODIS_Aqua_CorrectedReflectance_TrueColor": "250m",
    "SMAP_L3_Active_Soil_Moisture": "2km",
    "MODIS_Terra_Land_Surface_Temp_Day": "1km",
    "MODIS_Terra_CorrectedReflectance_Bands721": "250m",
    "CERES_NETFLUX_Outgoing_Longwave_Radiation_Day": "2km",
}

resolution = layer_resolution.get(layer, "250m")

# NASA GIBS WMTS layer URL
wmts_url = f"https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/{layer}/default/{date.strftime('%Y-%m-%d')}/{resolution}/{{z}}/{{y}}/{{x}}.png"

# Initialize Folium map centered on Ames, IA
m = folium.Map(location=AMES_COORDINATES, zoom_start=zoom)

# Add the NASA GIBS layer
folium.TileLayer(
    tiles=wmts_url,
    attr="Imagery courtesy of NASA GIBS",
    name="NASA GIBS",
    overlay=True,
    control=True,
).add_to(m)

# Add a layer control panel
folium.LayerControl().add_to(m)

# Display map in Streamlit
st.title("NASA GIBS Data Viewer: Ames, Iowa")
st_folium(m, width=700, height=500)
