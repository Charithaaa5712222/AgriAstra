import folium
from streamlit_folium import st_folium
from folium.plugins import Fullscreen, MiniMap, MousePosition
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

# Convert dataframe to CSV format in memory for the download button feature
@st.cache_data
def convert_df(dataframe):
    return dataframe.to_csv(index=False).encode('utf-8')

csv_data = convert_df(df)

# Custom styles, chart styling consistency, and subtle side branding
st.markdown("""
<style>

/* Main App Layout Background Tweak */
.stApp {
    background: #0b1220;
    color: #f8fafc;
}

/* Sidebar Branding Subtle Tweak */
[data-testid="stSidebar"] {
    background-color: #0f172a;
    border-right: 1px solid #1e293b;
}

/* Remove top padding */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
}

/* Hero Banner */
.hero {
    background: linear-gradient(135deg, #0f766e, #166534);
    padding: 35px;
    border-radius: 18px;
    text-align: center;
    color: white;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.35);
}

/* Section Titles */
h1, h2, h3, h4 {
    color: #ffffff;
}

/* Metric Cards */
div[data-testid="metric-container"] {
    background: #16213E;
    border: 1px solid #2E3B55;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,.35);
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
    transition: .3s;
}

/* Tabs UI styling */
.stTabs [data-baseweb="tab"] {
    background: #16213E;
    border-radius: 10px;
    color: white;
    margin-right: 8px;
}

.stTabs [aria-selected="true"] {
    background: #00b894;
    color: white;
}

/* Dataframe styling overrides */
[data-testid="stDataFrame"] {
    border-radius: 12px;
}

/* Expanders custom color matching design system */
.streamlit-expanderHeader {
    background: #16213E;
    border-radius: 10px;
}

/* Hide default streamlit standard footer footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# Subtle Branding elements over sidebar layout
st.sidebar.markdown("<h2 style='color:#00ff66; text-align:center;'>🛰️ AgroGIS</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align:center; color:#94a3b8;'>v2.4.0 • Active Operational Mode</p>", unsafe_allow_html=True)

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
""", unsafe_allow_html=True)

st.markdown("")

st.info("""
AgriAstra combines satellite imagery, rainfall data, machine learning,
and GIS visualization to monitor crop health and generate irrigation advisories.
""")

c1, c2, c3, c4 = st.columns(4)

c1.metric("📍 Samples", len(df))
c2.metric("🟢 Low Stress", int(stress_counts.get("Low", 0)))
c3.metric("🟡 Moderate Stress", int(stress_counts.get("Moderate", 0)))
c4.metric("🔴 High Stress", int(stress_counts.get("High", 0)))

st.markdown("---")

st.markdown("## 🤖 AI Model Performance & Advisory Index")

# Layout expanded to hold your charts side-by-side cleanly
gauge_col1, gauge_col2 = st.columns(2)

with gauge_col1:
    # Single Donut Chart displaying Moisture Stress Distribution with consistent styling
    fig_donut = px.pie(
        values=stress_counts.values,
        names=stress_counts.index,
        hole=0.6,
        title="Moisture Stress Distribution Profile",
        color=stress_counts.index,
        color_discrete_map={"Low": "#166534", "Moderate": "#EA580C", "High": "#DC2626"}
    )
    fig_donut.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        font=dict(color="white"),
        height=280,
        margin=dict(l=30, r=30, t=50, b=20)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with gauge_col2:
    # Second Gauge mapping Critical Irrigation demand index
    high_stress_rate = (int(stress_counts.get("High", 0)) / len(df) * 100) if len(df) > 0 else 0
    
    irrigation_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=high_stress_rate,
            title={"text": "🚜 Immediate Irrigation Demand (% Area)", "font": {"color": "white"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "white"},
                "bar": {"color": "#38BDF8"},
                "bgcolor": "rgba(30, 41, 59, 0.5)",
                "steps": [
                    {"range": [0, 30], "color": "rgba(22, 101, 52, 0.4)"},
                    {"range": [30, 70], "color": "rgba(234, 88, 12, 0.4)"},
                    {"range": [70, 100], "color": "rgba(220, 38, 38, 0.4)"}
                ]
            }
        )
    )
    irrigation_gauge.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1220",
        height=280,
        margin=dict(l=30, r=30, t=50, b=20)
    )
    st.plotly_chart(irrigation_gauge, use_container_width=True)

st.markdown("---")
tab1, tab2, tab3 = st.tabs(
    [
        "🗺️ GIS Maps",
        "📊 Analytics",
        "📋 Project Info"
    ]
)

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

    m = folium.Map(
        location=[17.0575, 79.2671],
        zoom_start=10,
        tiles=None,
        control_scale=True
    )
    
    Fullscreen(
        position="topright",
        title="Full Screen",
        title_cancel="Exit Full Screen",
        force_separate_button=True
    ).add_to(m)

    MiniMap(toggle_display=True).add_to(m)
    MousePosition().add_to(m)
    
    folium.TileLayer("OpenStreetMap", name="OpenStreetMap").add_to(m)
    folium.TileLayer("CartoDB Positron", name="Light Map").add_to(m)
    folium.TileLayer("CartoDB Dark_Matter", name="Dark Map").add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite",
        overlay=False,
        control=True
    ).add_to(m)

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

    m.fit_bounds([
        [16.65, 78.70],
        [17.55, 79.75]
    ])

    folium.CircleMarker(
        location=[17.0575, 79.2671],
        radius=8,
        color="yellow",
        fill=True,
        fill_color="red",
        fill_opacity=1,
        popup="Study Area - Nalgonda"
    ).add_to(m)

    folium.LayerControl().add_to(m)

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
    <hr style="border: 0; border-top: 1px solid #2E3B55;">
    <p>🟩 <b>Nalgonda Boundary</b></p>
    <p>📍 <b>Study Area</b></p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    st_folium(m, use_container_width=True, height=500)

    st.markdown("---")

    st.subheader("🛰️ GIS Visualization Layers")
    m1, m2, m3 = st.columns(3)

    with m1:
        st.image("dashboard/assets/ndvi_map.jpeg", caption="🌱 NDVI Map", use_container_width=True)
    with m2:
        st.image("dashboard/assets/moisture_stress_map.jpeg", caption="💧 Moisture Stress Map", use_container_width=True)
    with m3:
        st.image("dashboard/assets/irrigation_map.jpeg", caption="🚜 Irrigation Advisory Map", use_container_width=True)

with tab2:
    st.subheader("📊 Analytics Dashboard")
    left, right = st.columns(2)

    with left:
        # Repurposed the single distribution display here cleanly 
        fig_analytics = px.pie(
            values=stress_counts.values,
            names=stress_counts.index,
            hole=0.55,
            title="Relative Moisture Stress Share Breakdown",
            color=stress_counts.index,
            color_discrete_map={"Low": "#166534", "Moderate": "#EA580C", "High": "#DC2626"}
        )
        fig_analytics.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            font=dict(color="white")
        )
        st.plotly_chart(fig_analytics, use_container_width=True)

    with right:
        fig2 = px.bar(
            x=stress_counts.index,
            y=stress_counts.values,
            color=stress_counts.index,
            title="Stress Stratification Frequency Counts",
            color_discrete_map={"Low": "#166534", "Moderate": "#EA580C", "High": "#DC2626"}
        )
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            xaxis_title="Stress Level Classification",
            yaxis_title="Total Surveyed Samples"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("📈 Spatial Coverage Summary Metrics")
    
    analytics_c1, analytics_c2, analytics_c3, analytics_c4 = st.columns(4)
    analytics_c1.metric("Total Samples Tracked", len(df))
    analytics_c2.metric("Low Risk Area", int(stress_counts.get("Low", 0)))
    analytics_c3.metric("Moderate Risk Area", int(stress_counts.get("Moderate", 0)))
    analytics_c4.metric("High Emergency Area", int(stress_counts.get("High", 0)))

    st.markdown("---")
    
    # Download button integration for the dataset
    dl_col1, dl_col2 = st.columns([3, 1])
    with dl_col1:
        st.subheader("📋 Core GIS Vector Point Records")
    with dl_col2:
        st.download_button(
            label="📥 Export Dataset (CSV)",
            data=csv_data,
            file_name='agriastra_gis_metrics.csv',
            mime='text/csv',
            use_container_width=True
        )

    st.dataframe(df.head(20), use_container_width=True)

with tab3:
    st.subheader("Project Information")
    st.success("Project Name: AgriAstra Dashboard Environment")
    st.info("""
    **Domain Focus:** Precision Hydro-Agriculture Mapping  

    **Geographical Focus Bounds:** Nalgonda District, State Boundary Infrastructure  

    **Remote Sensing Data Sources:** • Sentinel-1 SAR Micro-wave Backscatter  
    • Sentinel-2 Optical Multi-Spectral Radiometry  
    • CHIRPS High-Resolution Daily Precipitation Estimates  

    **Software Architecture Engine:** • Google Earth Engine API Ecosystem  
    • GIS Vectorization and Spatial Boundary Processing  
    • Random Forest Classification Machine Learning Core  
    """)

st.markdown("---")
st.markdown("## 🚜 Automatic Spatial Irrigation Advisories")

with st.expander("View Active Algorithmic Recommendations", expanded=True):
    st.success("🟢 Low Stress Registered Status → Normal capillary saturation. No active supplementary irrigation required.")
    st.warning("🟡 Moderate Stress Registered Status → Moisture deficit tracked. Schedule regular distribution systems cycle within 72 hours.")
    st.error("🔴 High Stress Registered Status → Critical wilting baseline risk. Initialize priority corrective localized flow lines immediately.")

# A clean footer containing project and team information
st.markdown("""
<div style="
    text-align: center;
    padding: 20px;
    margin-top: 30px;
    background-color: #16213E;
    border-top: 2px solid #2E3B55;
    border-radius: 12px;
    color: #94a3b8;
    font-size: 14px;
">
    <p style="margin: 0; color: #00ff66; font-weight: bold; font-size:16px;">🌾 AgriAstra Smart Precision Farming Platform</p>
    <p style="margin: 5px 0 12px 0;">Machine Learning Framework for Scalable Water Resource Management & Stress Diagnostics</p>
    <p style="margin: 0; font-size: 13px;">
        👥 <b>Project Team:</b> GIS Research & Analytics Group | 🛠️ <b>Technology Stack:</b> Python, Streamlit, Folium, Plotly Engine
    </p>
    <p style="margin-top: 10px; font-size: 11px; color: #64748b;">© 2026 AgriAstra Spatial Systems. Protected under Open Data Open-source Attribution standards.</p>
</div>
""", unsafe_allow_html=True)
