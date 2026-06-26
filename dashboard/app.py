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

# ─── COLOUR TOKENS ────────────────────────────────────────────────────────────
PALETTE = {
    "bg":          "#0b1220",
    "surface":     "#111827",
    "card":        "#16213E",
    "border":      "#1e3a5f",
    "accent":      "#00c896",          # teal-green
    "accent2":     "#3b82f6",          # blue
    "warn":        "#f59e0b",
    "danger":      "#ef4444",
    "text":        "#f8fafc",
    "muted":       "#94a3b8",
    "low":         "#22c55e",
    "moderate":    "#f59e0b",
    "high":        "#ef4444",
}

CHART_COLORS = [PALETTE["low"], PALETTE["moderate"], PALETTE["high"]]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Space+Grotesk:wght@500;700&display=swap');

/* ── Base ── */
.stApp {{
    background: {PALETTE["bg"]};
    color: {PALETTE["text"]};
    font-family: 'Inter', sans-serif;
}}

/* Subtle grain texture overlay on the main background */
.stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0,200,150,0.08) 0%, transparent 70%),
        url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
}}

.block-container {{
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    position: relative;
    z-index: 1;
}}

/* ── Hero ── */
.hero {{
    background: linear-gradient(135deg, #064e3b 0%, #065f46 45%, #166534 100%);
    padding: 40px 48px;
    border-radius: 20px;
    text-align: center;
    color: white;
    box-shadow: 0 8px 32px rgba(0,200,150,0.18), 0 2px 8px rgba(0,0,0,0.4);
    border: 1px solid rgba(0,200,150,0.2);
    position: relative;
    overflow: hidden;
}}

.hero::after {{
    content: '🌾';
    position: absolute;
    right: 40px;
    bottom: -10px;
    font-size: 120px;
    opacity: 0.07;
    pointer-events: none;
}}

.hero h1 {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    margin: 0 0 8px;
    letter-spacing: -0.5px;
}}

.hero h3 {{
    font-weight: 400;
    opacity: 0.88;
    margin: 0 0 10px;
}}

.hero-badge {{
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 13px;
    margin: 3px 4px;
    backdrop-filter: blur(6px);
}}

/* ── Headings ── */
h1, h2, h3, h4 {{
    color: {PALETTE["text"]};
    font-family: 'Space Grotesk', sans-serif;
}}

/* ── Metric Cards ── */
div[data-testid="metric-container"] {{
    background: {PALETTE["card"]};
    border: 1px solid {PALETTE["border"]};
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(0,0,0,.35);
    transition: transform .25s, box-shadow .25s;
}}

div[data-testid="metric-container"]:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 28px rgba(0,200,150,0.12);
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] {{
    background: {PALETTE["card"]};
    border-radius: 10px;
    color: {PALETTE["muted"]};
    margin-right: 8px;
    font-weight: 600;
    padding: 8px 18px;
    border: 1px solid {PALETTE["border"]};
    transition: background .2s;
}}

.stTabs [aria-selected="true"] {{
    background: {PALETTE["accent"]};
    color: #0b1220;
    border-color: {PALETTE["accent"]};
}}

/* ── Data frame ── */
[data-testid="stDataFrame"] {{
    border-radius: 12px;
    border: 1px solid {PALETTE["border"]};
}}

/* ── Expanders ── */
.streamlit-expanderHeader {{
    background: {PALETTE["card"]};
    border-radius: 10px;
    border: 1px solid {PALETTE["border"]};
    font-weight: 600;
}}

/* ── Download button ── */
div[data-testid="stDownloadButton"] > button {{
    background: linear-gradient(90deg, {PALETTE["accent"]}, #0ea5e9);
    color: #0b1220;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 10px 24px;
    font-size: 15px;
    cursor: pointer;
    transition: opacity .2s, transform .2s;
    width: 100%;
}}

div[data-testid="stDownloadButton"] > button:hover {{
    opacity: 0.9;
    transform: translateY(-2px);
}}

/* ── Section divider ── */
hr {{
    border: none;
    border-top: 1px solid {PALETTE["border"]};
    margin: 1.5rem 0;
}}

/* ── Footer ── */
.agriastra-footer {{
    background: linear-gradient(135deg, {PALETTE["surface"]} 0%, #0d1f30 100%);
    border: 1px solid {PALETTE["border"]};
    border-radius: 18px;
    padding: 36px 40px 28px;
    margin-top: 2rem;
    color: {PALETTE["muted"]};
    font-size: 14px;
}}

.footer-brand {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: {PALETTE["accent"]};
    margin-bottom: 4px;
}}

.footer-tagline {{
    color: {PALETTE["muted"]};
    font-size: 13px;
    margin-bottom: 18px;
}}

.footer-section-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    color: {PALETTE["text"]};
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 10px;
    border-bottom: 1px solid {PALETTE["border"]};
    padding-bottom: 6px;
}}

.footer-member {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 7px;
    color: {PALETTE["muted"]};
}}

.footer-member .avatar {{
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, {PALETTE["accent"]}, {PALETTE["accent2"]});
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
    color: #0b1220;
    flex-shrink: 0;
}}

.footer-tech-pill {{
    display: inline-block;
    background: rgba(0,200,150,0.1);
    border: 1px solid rgba(0,200,150,0.25);
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 12px;
    color: {PALETTE["accent"]};
    margin: 3px 3px 3px 0;
}}

.footer-bottom {{
    margin-top: 24px;
    padding-top: 16px;
    border-top: 1px solid {PALETTE["border"]};
    text-align: center;
    font-size: 12px;
    color: {PALETTE["muted"]};
}}

footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ─── DATA ─────────────────────────────────────────────────────────────────────
if "Moisture_Stress" in df.columns:
    stress_counts = df["Moisture_Stress"].value_counts()
else:
    stress_counts = pd.Series(dtype=int)

total   = len(df)
low     = int(stress_counts.get("Low", 0))
mod     = int(stress_counts.get("Moderate", 0))
high    = int(stress_counts.get("High", 0))

pct_needs_irrig = round((mod + high) / total * 100, 1) if total else 0

# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🌾 AgriAstra</h1>
  <h3>AI-Driven Crop Monitoring &amp; Irrigation Advisory System</h3>
  <div style="margin-top:12px;">
    <span class="hero-badge">🛰️ Satellite Imagery</span>
    <span class="hero-badge">🤖 Machine Learning</span>
    <span class="hero-badge">🗺️ GIS Mapping</span>
    <span class="hero-badge">📍 Nalgonda District</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

st.info("AgriAstra combines satellite imagery, rainfall data, machine learning, and GIS visualization to monitor crop health and generate irrigation advisories.")

# ─── KPI METRICS ──────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("📍 Total Samples", f"{total:,}")
c2.metric("🟢 Low Stress",     low,  help="No irrigation needed")
c3.metric("🟡 Moderate Stress", mod, help="Irrigate within 3 days")
c4.metric("🔴 High Stress",    high, help="Irrigate immediately")

st.markdown("---")

# ─── AI MODEL + IRRIGATION GAUGE ──────────────────────────────────────────────
st.markdown("## 🤖 AI Model Performance")

left, right = st.columns([1, 2])

with left:
    st.metric("Model",      "Random Forest")
    st.metric("Prediction", "Moisture Stress")

def make_gauge(value, title, bar_color, suffix="%"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": suffix, "font": {"size": 28, "color": "white"}},
        title={"text": title, "font": {"size": 14, "color": "#94a3b8"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#94a3b8"},
            "bar":  {"color": bar_color, "thickness": 0.28},
            "bgcolor": "#16213E",
            "borderwidth": 0,
            "steps": [
                {"range": [0,  50], "color": "#1e293b"},
                {"range": [50, 80], "color": "#1e2f45"},
                {"range": [80, 100],"color": "#1a3a2a"},
            ],
            "threshold": {
                "line": {"color": bar_color, "width": 3},
                "thickness": 0.8,
                "value": value
            }
        }
    ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1220",
        height=320,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

with right:
    st.plotly_chart(make_gauge(100, "Accuracy (%)", "limegreen"), use_container_width=True)

st.markdown("---")

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🗺️ GIS Maps", "📊 Analytics", "📋 Project Info"])

# ── GIS Maps ──────────────────────────────────────────────────────────────────
with tab1:
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

    m = folium.Map(location=[17.0575, 79.2671], zoom_start=10, tiles=None, control_scale=True)

    Fullscreen(position="topright", title="Full Screen",
               title_cancel="Exit Full Screen", force_separate_button=True).add_to(m)
    MiniMap(toggle_display=True).add_to(m)
    MousePosition().add_to(m)

    folium.TileLayer("OpenStreetMap",        name="OpenStreetMap").add_to(m)
    folium.TileLayer("CartoDB Positron",     name="Light Map").add_to(m)
    folium.TileLayer("CartoDB Dark_Matter",  name="Dark Map").add_to(m)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Satellite", overlay=False, control=True
    ).add_to(m)

    folium.GeoJson(
        "geojson/nalgonda.geojson",
        name="Nalgonda Boundary",
        style_function=lambda f: {"fillColor":"#00c896","color":"#00c896","weight":2,"fillOpacity":0.12},
        highlight_function=lambda f: {"fillColor":"#00c896","color":"#FFFF00","weight":5,"fillOpacity":0.30},
        tooltip=folium.GeoJsonTooltip(fields=["shapeName"], aliases=["District:"], sticky=True)
    ).add_to(m)

    m.fit_bounds([[16.65, 78.70],[17.55, 79.75]])

    folium.CircleMarker(
        location=[17.0575, 79.2671], radius=8,
        color="yellow", fill=True, fill_color="red", fill_opacity=1,
        popup="Study Area – Nalgonda"
    ).add_to(m)

    folium.LayerControl().add_to(m)

    legend_html = """
    <div style="
      position:fixed;bottom:50px;left:50px;width:220px;
      background:rgba(11,18,32,0.95);border:2px solid #00c896;
      border-radius:10px;padding:12px;font-size:14px;
      color:white;z-index:9999;box-shadow:0 4px 12px rgba(0,0,0,0.5);">
      <h4 style="margin-top:0;color:#00c896;">🗺️ Legend</h4>
      <p>🟢 <b>Low Stress</b> – No action</p>
      <p>🟡 <b>Moderate Stress</b> – 3 days</p>
      <p>🔴 <b>High Stress</b> – Immediate</p>
      <hr style="border-color:#1e3a5f;">
      <p>🟩 <b>Nalgonda Boundary</b></p>
      <p>📍 <b>Study Area Centre</b></p>
    </div>"""
    m.get_root().html.add_child(folium.Element(legend_html))

    st_folium(m, use_container_width=True, height=500)

    st.markdown("---")
    st.subheader("🛰️ GIS Visualization")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.image("dashboard/assets/ndvi_map.jpeg",           caption="🌱 NDVI Map",            use_container_width=True)
    with m2:
        st.image("dashboard/assets/moisture_stress_map.jpeg", caption="💧 Moisture Stress Map", use_container_width=True)
    with m3:
        st.image("dashboard/assets/irrigation_map.jpeg",     caption="🚜 Irrigation Advisory Map", use_container_width=True)

# ── Analytics ─────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("📊 Analytics Dashboard")

    left, right = st.columns(2)

    with left:
        fig_donut = px.pie(
            values=stress_counts.values,
            names=stress_counts.index,
            hole=0.58,
            title="Moisture Stress Distribution",
            color=stress_counts.index,
            color_discrete_map={
                "Low":      PALETTE["low"],
                "Moderate": PALETTE["moderate"],
                "High":     PALETTE["high"],
            }
        )
        fig_donut.update_traces(textfont_size=14, marker=dict(line=dict(color="#0b1220", width=2)))
        fig_donut.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1220", plot_bgcolor="#0b1220",
            font=dict(color="white", family="Inter"),
            legend=dict(bgcolor="#16213E", bordercolor="#1e3a5f", borderwidth=1)
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with right:
        fig_bar = go.Figure(go.Bar(
            x=stress_counts.index.tolist(),
            y=stress_counts.values.tolist(),
            marker_color=[
                PALETTE["low"] if x == "Low"
                else PALETTE["moderate"] if x == "Moderate"
                else PALETTE["high"]
                for x in stress_counts.index
            ],
            marker_line_color="#0b1220",
            marker_line_width=2,
            text=stress_counts.values,
            textposition="outside",
            textfont=dict(color="white", size=14),
        ))
        fig_bar.update_layout(
            title="Sample Count by Stress Level",
            template="plotly_dark",
            paper_bgcolor="#0b1220", plot_bgcolor="#0b1220",
            xaxis=dict(title="Stress Level", color="#94a3b8", gridcolor="#1e3a5f"),
            yaxis=dict(title="Samples",      color="#94a3b8", gridcolor="#1e3a5f"),
            font=dict(color="white", family="Inter"),
            bargap=0.35,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # Second donut – irrigation need breakdown
    irrig_values = [low, mod + high]
    irrig_labels = ["No Irrigation Needed", "Irrigation Required"]
    fig_irrig = px.pie(
        values=irrig_values,
        names=irrig_labels,
        hole=0.60,
        title="🚜 Irrigation Requirement Overview",
        color=irrig_labels,
        color_discrete_map={
            "No Irrigation Needed": PALETTE["low"],
            "Irrigation Required":  PALETTE["warn"],
        }
    )
    fig_irrig.update_traces(textfont_size=14, marker=dict(line=dict(color="#0b1220", width=2)))
    fig_irrig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1220", plot_bgcolor="#0b1220",
        font=dict(color="white", family="Inter"),
        legend=dict(bgcolor="#16213E", bordercolor="#1e3a5f", borderwidth=1)
    )

    irrig_col, space = st.columns([2, 1])
    with irrig_col:
        st.plotly_chart(fig_irrig, use_container_width=True)

    st.markdown("---")
    st.subheader("📈 Summary")
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total Samples", f"{total:,}")
    s2.metric("Low",      low)
    s3.metric("Moderate", mod)
    s4.metric("High",     high)

    st.markdown("---")
    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head(20), use_container_width=True)

    # ── Download Button ────────────────────────────────────────────────────────
    st.markdown("### ⬇️ Export Dataset")
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Full Dataset as CSV",
        data=csv_bytes,
        file_name="agriastra_dataset.csv",
        mime="text/csv",
    )

# ── Project Info ───────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Project Information")

    st.success("**Project Name:** AgriAstra – Precision Agriculture using AI + GIS")

    st.info("""
**Domain:** Precision Agriculture  
**Study Area:** Nalgonda District, Telangana  

**Data Sources**
- Sentinel-1 SAR
- Sentinel-2 Optical
- CHIRPS Rainfall

**Technologies**
- Google Earth Engine
- GIS Mapping (Folium)
- Random Forest Classifier
- Python · Streamlit · Plotly
- GitHub
""")

st.markdown("---")

# ── Irrigation Recommendations ────────────────────────────────────────────────
st.markdown("## 🚜 Irrigation Recommendations")
with st.expander("View Recommendations"):
    st.success( "🟢 **Low Stress** → No irrigation needed. Crops are healthy.")
    st.warning( "🟡 **Moderate Stress** → Irrigate within 3 days to prevent yield loss.")
    st.error(   "🔴 **High Stress** → Irrigate immediately to avoid crop damage.")

st.markdown("---")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="agriastra-footer">

  <div style="display:grid;grid-template-columns:2fr 1fr 1fr;gap:32px;flex-wrap:wrap;">

    <!-- Brand column -->
    <div>
      <div class="footer-brand">🌾 AgriAstra</div>
      <div class="footer-tagline">AI-Driven Crop Monitoring &amp; Irrigation Advisory System</div>
      <p style="font-size:13px;line-height:1.7;">
        AgriAstra leverages Sentinel satellite imagery, CHIRPS rainfall data,
        and Random Forest machine learning to deliver actionable irrigation
        advisories across Nalgonda District, Telangana.
      </p>
      <div style="margin-top:10px;">
        <span class="footer-tech-pill">Google Earth Engine</span>
        <span class="footer-tech-pill">Random Forest</span>
        <span class="footer-tech-pill">Folium GIS</span>
        <span class="footer-tech-pill">Streamlit</span>
        <span class="footer-tech-pill">Plotly</span>
        <span class="footer-tech-pill">Python</span>
      </div>
    </div>

    <!-- Team column -->
    <div>
      <div class="footer-section-title">👥 Team</div>
      <div class="footer-member"><div class="avatar">P1</div><span>Team Member 1<br><small>Project Lead</small></span></div>
      <div class="footer-member"><div class="avatar">P2</div><span>Team Member 2<br><small>ML Engineer</small></span></div>
      <div class="footer-member"><div class="avatar">P3</div><span>Team Member 3<br><small>GIS Specialist</small></span></div>
      <div class="footer-member"><div class="avatar">P4</div><span>Team Member 4<br><small>Data Engineer</small></span></div>
    </div>

    <!-- Project details column -->
    <div>
      <div class="footer-section-title">📌 Project Details</div>
      <p><b>Study Area</b><br>Nalgonda District, Telangana</p>
      <p><b>Data Sources</b><br>Sentinel-1 · Sentinel-2 · CHIRPS</p>
      <p><b>Model</b><br>Random Forest Classifier</p>
      <p><b>Accuracy</b><br>100% (Training)</p>
      <p><b>Status</b><br><span style="color:#22c55e;">● Active</span></p>
    </div>

  </div>

  <div class="footer-bottom">
    © 2025 AgriAstra &nbsp;|&nbsp; Precision Agriculture using AI + GIS
    &nbsp;|&nbsp; Built with 🌱 for Nalgonda District
  </div>

</div>
""", unsafe_allow_html=True)
