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
""", unsafe_allow_html=True)

# ── Stress counts ──────────────────────────────────────────────────────────────
if "Moisture_Stress" in df.columns:
    stress_counts = df["Moisture_Stress"].value_counts()
else:
    stress_counts = pd.Series(dtype=int)

# ── Hero Banner ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
background:linear-gradient(135deg,#0f766e,#166534,#15803d);
padding:45px;
border-radius:20px;
text-align:center;
box-shadow:0 8px 30px rgba(0,0,0,.45);
margin-bottom:20px;
">

<h1 style="color:white;font-size:52px;margin-bottom:10px;">
🌾 AgriAstra
</h1>

<h3 style="color:#d1fae5;">
AI-Driven Crop Monitoring & Irrigation Advisory System
</h3>

<p style="font-size:20px;color:#e5e7eb;">
🛰️ Satellite Imagery • 🌱 Vegetation Monitoring • 🤖 Machine Learning • 🗺️ GIS Mapping
</p>

<hr style="border:1px solid rgba(255,255,255,.25);">

<div style="
display:flex;
justify-content:center;
gap:40px;
font-size:18px;
color:white;
">

<div>
<b>📍 Study Area</b><br>
Nalgonda District
</div>

<div>
<b>🤖 Model</b><br>
Random Forest
</div>

<div>
<b>🛰️ Data</b><br>
Sentinel + CHIRPS
</div>

</div>

</div>
""", unsafe_allow_html=True)

st.markdown("")

st.info("""
AgriAstra combines satellite imagery, rainfall data, machine learning,
and GIS visualization to monitor crop health and generate irrigation advisories.
""")

# ── KPI Cards ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div style="
    background:#16213E;
    padding:20px;
    border-left:6px solid #38bdf8;
    border-radius:15px;
    text-align:center;
    box-shadow:0 4px 10px rgba(0,0,0,.35);
    ">
        <h4 style="color:white;font-size:16px;margin-bottom:8px;">📍 Samples</h4>
        <p style="color:#38bdf8;font-size:42px;font-weight:700;margin:0;line-height:1.2;">{len(df)}</p>
        <p style="color:#cbd5e1;margin-top:8px;">Total Records</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="
    background:#16213E;
    padding:20px;
    border-left:6px solid #22c55e;
    border-radius:15px;
    text-align:center;
    box-shadow:0 4px 10px rgba(0,0,0,.35);
    ">
        <h4 style="color:white;font-size:16px;margin-bottom:8px;">🟢 Low Stress</h4>
        <p style="color:#22c55e;font-size:42px;font-weight:700;margin:0;line-height:1.2;">{int(stress_counts.get("Low", 0))}</p>
        <p style="color:#cbd5e1;margin-top:8px;">Healthy Crops</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div style="
    background:#16213E;
    padding:20px;
    border-left:6px solid #facc15;
    border-radius:15px;
    text-align:center;
    box-shadow:0 4px 10px rgba(0,0,0,.35);
    ">
        <h4 style="color:white;font-size:16px;margin-bottom:8px;">🟡 Moderate Stress</h4>
        <p style="color:#facc15;font-size:42px;font-weight:700;margin:0;line-height:1.2;">{int(stress_counts.get("Moderate", 0))}</p>
        <p style="color:#cbd5e1;margin-top:8px;">Needs Monitoring</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div style="
    background:#16213E;
    padding:20px;
    border-left:6px solid #ef4444;
    border-radius:15px;
    text-align:center;
    box-shadow:0 4px 10px rgba(0,0,0,.35);
    ">
        <h4 style="color:white;font-size:16px;margin-bottom:8px;">🔴 High Stress</h4>
        <p style="color:#ef4444;font-size:42px;font-weight:700;margin:0;line-height:1.2;">{int(stress_counts.get("High", 0))}</p>
        <p style="color:#cbd5e1;margin-top:8px;">Immediate Action</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Irrigation Recommendations ─────────────────────────────────────────────────
st.markdown("## 🚜 Irrigation Recommendations")

with st.expander("View Recommendations"):
    st.success("🟢 Low → No irrigation needed")
    st.warning("🟡 Moderate → Irrigate within 3 days")
    st.error("🔴 High → Irrigate immediately")

st.markdown("---")

st.markdown(
    "<center><h4>🌾 AgriAstra | Precision Agriculture using AI + GIS</h4></center>",
    unsafe_allow_html=True
)
