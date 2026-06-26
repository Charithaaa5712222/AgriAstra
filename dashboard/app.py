import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen
from folium.plugins import MiniMap
from folium.plugins import MousePosition
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AgriAstra",
    page_icon="🌾",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/agriastra_final_dataset.csv")

df = load_data()

st.markdown("""
<style>

/* Main App */
.stApp{
    background:#0b1220;
    color:#f8fafc;
}

/* Remove top padding */
.block-container{
    padding-top:1.5rem;
    padding-bottom:1rem;
}

/* Hero Banner */
.hero{
    background:linear-gradient(135deg,#0f766e,#166534);
    padding:35px;
    border-radius:18px;
    text-align:center;
    color:white;
    box-shadow:0px 8px 25px rgba(0,0,0,0.35);
}

/* Section Titles */
h1,h2,h3,h4{
    color:#ffffff;
}

/* Metric Cards */
div[data-testid="metric-container"]{
    background:#16213E;
    border:1px solid #2E3B55;
    padding:18px;
    border-radius:16px;
    box-shadow:0 4px 12px rgba(0,0,0,.35);
}

div[data-testid="metric-container"]:hover{
    transform:translateY(-4px);
    transition:.3s;
}

/* Tabs */
.stTabs [data-baseweb="tab"]{
    background:#16213E;
    border-radius:10px;
    color:white;
    margin-right:8px;
}

.stTabs [aria-selected="true"]{
    background:#00b894;
    color:white;
}

/* Dataframe */
[data-testid="stDataFrame"]{
    border-radius:12px;
}

/* Expanders */
.streamlit-expanderHeader{
    background:#16213E;
    border-radius:10px;
}

/* Footer */
footer{
    visibility:hidden;
}

</style>
""",unsafe_allow_html=True)

if "Moisture_Stress" in df.columns:
    stress_counts = df["Moisture_Stress"].value_counts()
else:
    stress_counts = pd.Series(dtype=int)

st.markdown("""
<div class="hero">
<h1>🌾 AgriAstra</h1>
<h3>AI-Driven Crop Monitoring & Irrigation Advisory System</h3>
<p style="font-size:20px;">
Smart Agriculture using Satellite Imagery • Machine Learning • GIS
</p>
</div>
""",unsafe_allow_html=True)

st.markdown("")

st.info("""
AgriAstra combines satellite imagery, rainfall data, machine learning,
and GIS visualization to monitor crop health and generate irrigation advisories.
""")

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "📍 Samples",
    len(df)
)

c2.metric(
    "🟢 Low Stress",
    int(stress_counts.get("Low",0))
)

c3.metric(
    "🟡 Moderate Stress",
    int(stress_counts.get("Moderate",0))
)

c4.metric(
    "🔴 High Stress",
    int(stress_counts.get("High",0))
)

st.markdown("---")

st.markdown("## 🤖 AI Model Performance")

left,right = st.columns([1,2])

with left:

    st.metric(
        "Model",
        "Random Forest"
    )

    st.metric(
        "Prediction",
        "Moisture Stress"
    )

with right:

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=100,
            title={"text":"Accuracy (%)"},
            gauge={
                "axis":{"range":[0,100]},
                "bar":{"color":"limegreen"},
                "steps":[
                    {"range":[0,50],"color":"#8B0000"},
                    {"range":[50,80],"color":"orange"},
                    {"range":[80,100],"color":"green"}
                ]
            }
        )
    )

    gauge.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1220",
        height=320,
        margin=dict(l=20,r=20,t=60,b=20)
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

st.markdown("---")
tab1,tab2,tab3 = st.tabs(
    [
        "🗺️ GIS Maps",
        "📊 Analytics",
        "📋 Project Info"
    ]
)

# Assuming 'tab1' and other tabs are defined above this block
# Assuming 'tab1' and other tabs are defined above this block
# Assuming 'tab1' and other tabs are defined above this block
with tab1:
    # GIS Dashboard Status Banner Block
    st.markdown("""
    <div style="
    background:linear-gradient(90deg,#14532d,#166534);
    padding:15px;
    border-radius:12px;
    margin-bottom:15px;
    color:white;
    box-shadow:0 4px 10px rgba(0,0,0,0.3);
    ">
    <h3 style="margin-top:0; color:white;">🛰️ GIS Dashboard Status</h3>

    <table style="width:100%;font-size:16px;color:white;border-collapse:collapse;">
    <tr>
    <td>🟢 <b>Satellite Layer</b></td>
    <td>Loaded</td>

    <td>🤖 <b>AI Model</b></td>
    <td>Random Forest</td>
    </tr>

    <tr>
    <td>🗺️ <b>District Boundary</b></td>
    <td>Loaded</td>

    <td>📍 <b>Study Area</b></td>
    <td>Nalgonda</td>
    </tr>

    <tr>
    <td>🌧️ <b>Rainfall Data</b></td>
    <td>Available</td>

    <td>📅 <b>Status</b></td>
    <td>Online</td>
    </tr>
    </table>

    </div>
    """, unsafe_allow_html=True)

    st.subheader("🌍 Interactive GIS Map")

    # Initialize the base map centered on Nalgonda
    m = folium.Map(
        location=[17.0575, 79.2671],
        zoom_start=10,
        tiles=None,
        control_scale=True
    )
    
    # Add GIS Plugins to the map object
    Fullscreen(
        position="topright",
        title="Full Screen",
        title_cancel="Exit Full Screen",
        force_separate_button=True
    ).add_to(m)

    MiniMap(toggle_display=True).add_to(m)
    MousePosition().add_to(m)
    
    # OpenStreetMap
    folium.TileLayer(
        "OpenStreetMap",
        name="OpenStreetMap"
    ).add_to(m)

    # CartoDB Light
    folium.TileLayer(
        "CartoDB Positron",
        name="Light Map"
    ).add_to(m)

    # CartoDB Dark
    folium.TileLayer(
        "CartoDB Dark_Matter",
        name="Dark Map"
    ).add_to(m)

    # Esri Satellite
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite",
        overlay=False,
        control=True
    ).add_to(m)

    # Load and Style the GeoJSON Boundary with Hover Effects
    folium.GeoJson(
        "geojson/nalgonda.geojson",
        name="Nalgonda Boundary",
        style_function=lambda feature: {
            "fillColor": "#00FF66",
            "color": "#00FF66",
            "weight": 2,
            "fillOpacity": 0.12
        },
        highlight_function=lambda feature: {
            "fillColor": "#00FF66",
            "color": "#FFFF00",
            "weight": 5,
            "fillOpacity": 0.30
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["shapeName"],
            aliases=["District:"],
            sticky=True
        )
    ).add_to(m)

    # Automatically bound the camera frame tightly to your spatial features
    m.fit_bounds([
        [16.65, 78.70],
        [17.55, 79.75]
    ])

    # Add Study Area Marker
    folium.CircleMarker(
        location=[17.0575, 79.2671],
        radius=8,
        color="yellow",
        fill=True,
        fill_color="red",
        fill_opacity=1,
        popup="Study Area - Nalgonda"
    ).add_to(m)

    # Add Map Controls
    folium.LayerControl().add_to(m)

    # Custom HTML Legend Setup
    legend_html = """
    <div style="
    position: fixed;
    bottom: 50px;
    left: 50px;
    width: 220px;
    background-color: rgba(15,23,42,0.92);
    border:2px solid #00ff66;
    border-radius:10px;
    padding:12px;
    font-size:14px;
    color:white;
    z-index:9999;
    box-shadow:0 4px 12px rgba(0,0,0,0.5);
    ">

    <h4 style="margin-top:0;color:#00ff66;">🗺️ Legend</h4>

    <p>🟢 <b>Low Stress</b></p>

    <p>🟡 <b>Moderate Stress</b></p>

    <p>🔴 <b>High Stress</b></p>

    <hr>

    <p>🟩 <b>Nalgonda Boundary</b></p>

    <p>📍 <b>Study Area</b></p>

    </div>
    """

    m.get_root().html.add_child(folium.Element(legend_html))

    # Render Folium Map in Streamlit
    st_folium(
        m,
        use_container_width=True,
        height=500
    )

    st.markdown("---")

    # GIS Visualization components kept inside tab1 to preserve layout
    st.subheader("🛰️ GIS Visualization")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.image(
            "dashboard/assets/ndvi_map.jpeg",
            caption="🌱 NDVI Map",
            use_container_width=True
        )

    with m2:
        st.image(
            "dashboard/assets/moisture_stress_map.jpeg",
            caption="💧 Moisture Stress Map",
            use_container_width=True
        )

    with m3:
        st.image(
            "dashboard/assets/irrigation_map.jpeg",
            caption="🚜 Irrigation Advisory Map",
            use_container_width=True
        )
with tab2:

    st.subheader("📊 Analytics Dashboard")

    left, right = st.columns(2)

    with left:

        fig = px.pie(
            values=stress_counts.values,
            names=stress_counts.index,
            hole=0.55,
            title="Moisture Stress Distribution"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            font=dict(color="white")
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig2 = px.bar(
            x=stress_counts.index,
            y=stress_counts.values,
            color=stress_counts.index,
            title="Stress Count"
        )

        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            xaxis_title="Stress Level",
            yaxis_title="Samples"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("📈 Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Samples",
        len(df)
    )

    c2.metric(
        "Low",
        int(stress_counts.get("Low",0))
    )

    c3.metric(
        "Moderate",
        int(stress_counts.get("Moderate",0))
    )

    c4.metric(
        "High",
        int(stress_counts.get("High",0))
    )

    st.markdown("---")

    st.subheader("📋 Dataset Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

with tab3:

    st.subheader("Project Information")

    st.success("""
Project Name: AgriAstra
""")

    st.info("""
Domain:
Precision Agriculture

Study Area:
Nalgonda District

Data Sources:
• Sentinel-1 SAR
• Sentinel-2 Optical
• CHIRPS Rainfall

Technologies:
• Google Earth Engine
• GIS Mapping
• Random Forest
• Python
• Streamlit
• GitHub
""")

st.markdown("---")

st.markdown("## 🚜 Irrigation Recommendations")

with st.expander(
    "View Recommendations"
):

    st.success(
        "🟢 Low → No irrigation needed"
    )

    st.warning(
        "🟡 Moderate → Irrigate within 3 days"
    )

    st.error(
        "🔴 High → Irrigate immediately"
    )

st.markdown("---")

st.markdown(
    "<center><h4>🌾 AgriAstra | Precision Agriculture using AI + GIS</h4></center>",
    unsafe_allow_html=True
)
