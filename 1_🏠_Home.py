import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="AgriAstra",
    page_icon="🌾",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/agriastra_final_dataset.csv")

df = load_data()

if "Moisture_Stress" in df.columns:
    stress_counts = df["Moisture_Stress"].value_counts()
else:
    stress_counts = pd.Series(dtype=int)

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

footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------

st.markdown("""
<div style="
background:linear-gradient(135deg,#0f766e,#166534,#15803d);
padding:45px;
border-radius:20px;
text-align:center;
box-shadow:0 8px 30px rgba(0,0,0,.45);
margin-bottom:20px;
">

<h1 style="color:white;font-size:52px;">
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
Sentinel-1 • Sentinel-2 • CHIRPS
</div>

</div>

</div>
""", unsafe_allow_html=True)

# ---------------- INTRO ----------------

st.info("""
AgriAstra combines satellite imagery, rainfall data, machine learning, and GIS visualization to monitor crop health and generate intelligent irrigation advisories for precision agriculture.
""")

# ---------------- KPI CARDS ----------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "📍 Samples",
        len(df)
    )

with c2:
    st.metric(
        "🟢 Low Stress",
        int(stress_counts.get("Low",0))
    )

with c3:
    st.metric(
        "🟡 Moderate Stress",
        int(stress_counts.get("Moderate",0))
    )

with c4:
    st.metric(
        "🔴 High Stress",
        int(stress_counts.get("High",0))
    )

st.markdown("---")

# ---------------- AI MODEL ----------------

left, right = st.columns([1,2])

with left:

    st.markdown("""
<div style="
background:#16213E;
padding:20px;
border-radius:15px;
border-left:5px solid #22c55e;
">

<h3 style="color:white;">
🤖 AI Model Summary
</h3>

<hr>

<p style="color:white;">
🌲 <b>Model:</b> Random Forest
</p>

<p style="color:white;">
💧 <b>Prediction:</b> Moisture Stress
</p>

<p style="color:white;">
🎯 <b>Accuracy:</b> 100%
</p>

<p style="color:white;">
🟢 <b>Status:</b> Production Ready
</p>

</div>
""", unsafe_allow_html=True)

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
        height=320
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

st.markdown("---")

# ---------------- FEATURES ----------------

st.markdown("## ⭐ Key Features")

f1, f2, f3 = st.columns(3)

with f1:
    st.success("""
### 🛰️ Satellite Monitoring

Monitor crop health using Sentinel-1 and Sentinel-2 imagery.
""")

with f2:
    st.info("""
### 🤖 AI Prediction

Random Forest model predicts crop moisture stress with high accuracy.
""")

with f3:
    st.warning("""
### 🚜 Smart Irrigation

Generate irrigation recommendations based on crop stress levels.
""")

st.markdown("---")

# ---------------- QUICK OVERVIEW ----------------

st.markdown("## 🚜 System Quick Overview")

with st.expander(
    "View Crop Status",
    expanded=True
):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success("""
🟢 **Low Stress**

Healthy vegetation.

No irrigation required.
""")

    with col2:
        st.warning("""
🟡 **Moderate Stress**

Requires monitoring.

Irrigate within 3 days.
""")

    with col3:
        st.error("""
🔴 **High Stress**

Critical moisture stress.

Immediate irrigation required.
""")

st.markdown("---")

# ---------------- NAVIGATION ----------------

st.markdown("## 🚀 Explore AgriAstra")

c1, c2, c3 = st.columns(3)

with c1:
    st.page_link(
        "pages/1_🗺️_GIS_Dashboard.py",
        label="🗺️ Open GIS Dashboard"
    )

with c2:
    st.page_link(
        "pages/2_📊_Analytics.py",
        label="📊 View Analytics"
    )

with c3:
    st.page_link(
        "pages/3_🤖_AI_Model.py",
        label="🤖 AI Model"
    )

st.markdown("---")

st.markdown(
"""
<center>

<h4 style="color:white;">
🌾 AgriAstra
</h4>

Precision Agriculture using AI • GIS • Remote Sensing

</center>
""",
unsafe_allow_html=True
)
