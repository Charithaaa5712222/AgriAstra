import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen, MiniMap, MousePosition

st.set_page_config(
    page_title="GIS Dashboard",
    page_icon="🗺️",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
    background:#0b1220;
    color:white;
}

.block-container{
    padding-top:1.5rem;
}

footer{
    visibility:hidden;
}

</style>
""",unsafe_allow_html=True)

st.title("🗺️ GIS Dashboard")

st.markdown("""
Explore satellite imagery, district boundaries, and irrigation layers
for the Nalgonda study area.
""")

# ----------------------------------------------------
# GIS STATUS
# ----------------------------------------------------

st.markdown("""
<div style="
background:linear-gradient(90deg,#14532d,#166534);
padding:18px;
border-radius:15px;
margin-bottom:20px;
color:white;
">

<h3>🛰️ GIS Dashboard Status</h3>

<table style="width:100%;font-size:16px;">

<tr>
<td>🛰️ Satellite Layer</td>
<td><b>Loaded</b></td>

<td>🤖 AI Model</td>
<td><b>Random Forest</b></td>
</tr>

<tr>
<td>🗺️ Boundary</td>
<td><b>Loaded</b></td>

<td>📍 Study Area</td>
<td><b>Nalgonda</b></td>
</tr>

<tr>
<td>🌧️ Rainfall</td>
<td><b>Available</b></td>

<td>📅 Status</td>
<td><b>Online</b></td>
</tr>

</table>

</div>
""",unsafe_allow_html=True)

# ----------------------------------------------------
# INTERACTIVE MAP
# ----------------------------------------------------

st.subheader("🌍 Interactive GIS Map")

m = folium.Map(
    location=[17.0575,79.2671],
    zoom_start=10,
    tiles=None,
    control_scale=True
)

Fullscreen().add_to(m)

MiniMap(toggle_display=True).add_to(m)

MousePosition().add_to(m)

folium.TileLayer(
    "OpenStreetMap",
    name="OpenStreetMap"
).add_to(m)

folium.TileLayer(
    "CartoDB Positron",
    name="Light Map"
).add_to(m)

folium.TileLayer(
    "CartoDB Dark_Matter",
    name="Dark Map"
).add_to(m)

folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Satellite"
).add_to(m)

folium.GeoJson(
    "geojson/nalgonda.geojson",
    name="Nalgonda Boundary",
    style_function=lambda feature:{
        "fillColor":"#00FF66",
        "color":"#00FF66",
        "weight":2,
        "fillOpacity":0.15
    },
    highlight_function=lambda feature:{
        "fillColor":"yellow",
        "color":"yellow",
        "weight":4
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["shapeName"],
        aliases=["District:"]
    )
).add_to(m)

folium.CircleMarker(
    location=[17.0575,79.2671],
    radius=8,
    color="yellow",
    fill=True,
    fill_color="red",
    popup="Nalgonda District"
).add_to(m)

m.fit_bounds([
    [16.65,78.70],
    [17.55,79.75]
])

folium.LayerControl().add_to(m)

legend = """
<div style="
position:fixed;
bottom:50px;
left:50px;
width:220px;
background:#111827;
padding:15px;
border-radius:12px;
border:2px solid #22c55e;
z-index:9999;
color:white;
">

<h4>🗺️ Legend</h4>

🟢 Low Stress<br><br>

🟡 Moderate Stress<br><br>

🔴 High Stress<br><br>

🟩 Nalgonda Boundary<br><br>

📍 Study Area

</div>
"""

m.get_root().html.add_child(
    folium.Element(legend)
)

st_folium(
    m,
    use_container_width=True,
    height=550
)

st.markdown("---")

# ----------------------------------------------------
# GIS MAPS
# ----------------------------------------------------

st.subheader("🛰️ Satellite Layers")

c1,c2,c3 = st.columns(3)

with c1:

    st.image(
        "dashboard/assets/ndvi_map.jpeg",
        caption="🌱 NDVI Map",
        use_container_width=True
    )

with c2:

    st.image(
        "dashboard/assets/moisture_stress_map.jpeg",
        caption="💧 Moisture Stress",
        use_container_width=True
    )

with c3:

    st.image(
        "dashboard/assets/irrigation_map.jpeg",
        caption="🚜 Irrigation Advisory",
        use_container_width=True
    )

st.markdown("---")

st.info("""
🛰️ Satellite Layers Available

• NDVI Vegetation Map

• Moisture Stress Map

• Irrigation Advisory Map

• Nalgonda District Boundary

• Interactive Satellite Basemap
""")

st.markdown(
"""
<center>

<h4>
🗺️ GIS Dashboard
</h4>

AgriAstra | Precision Agriculture

</center>
""",
unsafe_allow_html=True
)
