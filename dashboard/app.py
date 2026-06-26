import folium
from streamlit_folium import st_folium
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

with tab1:

    st.subheader("🌍 Interactive GIS Map")

    m = folium.Map(
        location=[17.0575, 79.2671],
        zoom_start=10,
        tiles=None
    )

    folium.TileLayer(
        tiles="Esri WorldImagery",
        attr="Esri",
        name="Satellite"
    ).add_to(m)

    folium.GeoJson(
    "geojson/nalgonda.geojson",
    name="Nalgonda Boundary",
    style_function=lambda feature: {
        "fillColor": "#00FF00",
        "color": "#00FF00",
        "weight": 3,
        "fillOpacity": 0.15
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["shapeName"],
        aliases=["District:"]
    )
).add_to(m)

    folium.Marker(
        [17.0575, 79.2671],
        popup="Nalgonda District",
        tooltip="Study Area"
    ).add_to(m)

    folium.LayerControl().add_to(m)

    st_folium(
        m,
        use_container_width=True,
        height=500
    )

    st.markdown("---")

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

    st.subheader("Moisture Stress Distribution")

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

    st.subheader("Dataset Preview")

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
