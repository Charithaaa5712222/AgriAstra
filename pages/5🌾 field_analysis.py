import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import json

st.set_page_config(page_title="Field Analysis – AgriAstra", page_icon="🌾", layout="wide")

st.markdown("""
<style>
.stApp { background:#0b1220; color:#f8fafc; }
.block-container { padding-top:1.5rem; padding-bottom:1rem; }
h1,h2,h3,h4 { color:#ffffff; }
footer { visibility:hidden; }
.field-card {
    background:#16213E;
    border-radius:14px;
    padding:20px;
    border-left:5px solid #00b894;
    box-shadow:0 4px 12px rgba(0,0,0,0.4);
    margin-bottom:12px;
}
.metric-pill {
    display:inline-block;
    padding:6px 14px;
    border-radius:20px;
    font-size:14px;
    font-weight:600;
    margin:4px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/agriastra_final_dataset.csv")

@st.cache_resource
def train_model(df):
    le = LabelEncoder()
    X = df[["NDVI", "NDWI", "VH", "VV", "Rainfall"]]
    y = le.fit_transform(df["Moisture_Stress"])
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, le

df = load_data()
model, le = train_model(df)

st.markdown("## 🌾 Field-wise Analysis")
st.caption("Analyze any field location in Nalgonda district using satellite-derived indices.")

# ── Field Selection ──────────────────────────────────────────────────────────
st.markdown("### 📍 Select Field Location")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("""
    <div class="field-card">
    <h4 style="color:#00b894;margin-top:0;">Option A: Enter Coordinates</h4>
    </div>
    """, unsafe_allow_html=True)
    lat = st.number_input("Latitude", value=17.0575, min_value=16.5, max_value=17.6, step=0.001, format="%.4f")
    lon = st.number_input("Longitude", value=79.2671, min_value=78.6, max_value=79.8, step=0.001, format="%.4f")

with col_right:
    st.markdown("""
    <div class="field-card">
    <h4 style="color:#38bdf8;margin-top:0;">Option B: Choose Preset Location</h4>
    </div>
    """, unsafe_allow_html=True)
    presets = {
        "Nalgonda Center": (17.0575, 79.2671),
        "Miryalaguda": (16.8726, 79.5697),
        "Bhongir": (17.5144, 78.8915),
        "Suryapet": (17.1399, 79.6215),
        "Devarakonda": (16.6889, 79.5369),
        "Nakrekal": (17.0500, 79.3200),
        "Huzurnagar": (16.8976, 79.8852),
    }
    selected_preset = st.selectbox("Select a mandal/town", list(presets.keys()))
    if st.button("📍 Use This Location", use_container_width=True):
        lat, lon = presets[selected_preset]
        st.success(f"Using coordinates: {lat:.4f}, {lon:.4f}")

st.markdown("---")

# ── Manual Parameter Input ────────────────────────────────────────────────────
st.markdown("### 🛰️ Satellite Parameters")
st.caption("These would come from Google Earth Engine in live mode. Adjust manually or use dataset-derived defaults.")

p1, p2, p3, p4, p5 = st.columns(5)
with p1:
    ndvi = st.slider("🌱 NDVI", -0.5, 1.0, 0.45, 0.01, help="Normalized Difference Vegetation Index")
with p2:
    ndwi = st.slider("💧 NDWI", -0.8, 0.7, -0.52, 0.01, help="Normalized Difference Water Index")
with p3:
    vh = st.slider("📡 VH (SAR)", -35.0, -10.0, -18.9, 0.1, help="Sentinel-1 VH backscatter (dB)")
with p4:
    vv = st.slider("📡 VV (SAR)", -27.0, -3.0, -11.5, 0.1, help="Sentinel-1 VV backscatter (dB)")
with p5:
    rainfall = st.slider("🌧️ Rainfall (mm)", 0.0, 100.0, 18.5, 0.5, help="CHIRPS monthly rainfall")

# ── Analyze Button ─────────────────────────────────────────────────────────────
st.markdown("")
analyze_btn = st.button("🔍 Analyze Field", type="primary", use_container_width=True)

if analyze_btn:
    X_input = np.array([[ndvi, ndwi, vh, vv, rainfall]])
    pred_encoded = model.predict(X_input)[0]
    pred_label = le.inverse_transform([pred_encoded])[0]
    pred_proba = model.predict_proba(X_input)[0]
    classes = le.inverse_transform(range(len(le.classes_)))
    proba_dict = dict(zip(classes, pred_proba))

    # Advisory mapping
    advisory_map = {
        "Low": ("No irrigation needed", "#22c55e", "🟢", "✅ Crop is healthy. Monitor weekly."),
        "Moderate": ("Irrigate within 3 days", "#facc15", "🟡", "⚠️ Moderate stress detected. Plan irrigation soon."),
        "High": ("Irrigate immediately", "#ef4444", "🔴", "🚨 Critical stress! Immediate irrigation required.")
    }
    advisory, color, emoji, action = advisory_map.get(pred_label, ("Unknown", "#94a3b8", "⚪", ""))

    st.markdown("---")
    st.markdown("## 📊 Analysis Results")

    # ── Result Header ────────────────────────────────────────────────────────
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f"""
        <div style="background:#16213E;border-radius:14px;padding:20px;text-align:center;border-left:6px solid {color};">
        <p style="color:#94a3b8;margin:0;font-size:14px;">MOISTURE STRESS</p>
        <p style="color:{color};font-size:36px;font-weight:700;margin:8px 0;">{emoji} {pred_label}</p>
        <p style="color:#cbd5e1;font-size:13px;">Confidence: {max(pred_proba)*100:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    with r2:
        st.markdown(f"""
        <div style="background:#16213E;border-radius:14px;padding:20px;text-align:center;border-left:6px solid #38bdf8;">
        <p style="color:#94a3b8;margin:0;font-size:14px;">IRRIGATION ADVISORY</p>
        <p style="color:#38bdf8;font-size:22px;font-weight:700;margin:8px 0;">🚜 {advisory}</p>
        <p style="color:#cbd5e1;font-size:13px;">{action}</p>
        </div>
        """, unsafe_allow_html=True)
    with r3:
        st.markdown(f"""
        <div style="background:#16213E;border-radius:14px;padding:20px;text-align:center;border-left:6px solid #a78bfa;">
        <p style="color:#94a3b8;margin:0;font-size:14px;">FIELD LOCATION</p>
        <p style="color:#a78bfa;font-size:22px;font-weight:700;margin:8px 0;">📍 {lat:.4f}°N</p>
        <p style="color:#cbd5e1;font-size:13px;">{lon:.4f}°E — Nalgonda District</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ── Charts Row ────────────────────────────────────────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        # Radar chart of parameters
        categories = ["NDVI", "NDWI\n(norm)", "VH\n(norm)", "VV\n(norm)", "Rainfall\n(norm)"]
        # Normalize values to 0-1 for radar
        ndvi_n = (ndvi + 0.5) / 1.5
        ndwi_n = (ndwi + 0.8) / 1.5
        vh_n   = (vh + 35) / 25
        vv_n   = (vv + 27) / 24
        rain_n = rainfall / 100
        vals = [ndvi_n, ndwi_n, vh_n, vv_n, rain_n]
        vals_closed = vals + [vals[0]]
        cats_closed = ["NDVI","NDWI","VH","VV","Rainfall","NDVI"]

        fig_radar = go.Figure(go.Scatterpolar(
            r=vals_closed,
            theta=cats_closed,
            fill='toself',
            fillcolor='rgba(0,184,148,0.25)',
            line=dict(color='#00b894', width=2),
            name="Field Parameters"
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor='#16213E',
                radialaxis=dict(visible=True, range=[0,1], color='#94a3b8'),
                angularaxis=dict(color='#f8fafc')
            ),
            template="plotly_dark",
            paper_bgcolor="#0b1220",
            title=dict(text="🛰️ Parameter Profile", font=dict(color='white')),
            height=320,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with c2:
        # Confidence bar chart
        fig_conf = go.Figure(go.Bar(
            x=list(proba_dict.keys()),
            y=[v*100 for v in proba_dict.values()],
            marker_color=["#22c55e" if k=="Low" else "#facc15" if k=="Moderate" else "#ef4444" for k in proba_dict.keys()],
            text=[f"{v*100:.1f}%" for v in proba_dict.values()],
            textposition='outside',
            textfont=dict(color='white')
        ))
        fig_conf.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            title=dict(text="🤖 Model Confidence", font=dict(color='white')),
            yaxis=dict(range=[0,110], title="Confidence (%)", color='#94a3b8'),
            xaxis=dict(color='#f8fafc'),
            height=320,
            margin=dict(l=20, r=20, t=50, b=40)
        )
        st.plotly_chart(fig_conf, use_container_width=True)

    # ── Parameter Summary Cards ───────────────────────────────────────────────
    st.markdown("### 📋 Parameter Summary")
    pc1, pc2, pc3, pc4, pc5 = st.columns(5)
    params = [
        ("🌱 NDVI", ndvi, -0.5, 1.0, "#00b894", "Vegetation health"),
        ("💧 NDWI", ndwi, -0.8, 0.7, "#38bdf8", "Water content"),
        ("📡 VH SAR", vh, -35, -10, "#a78bfa", "Soil backscatter"),
        ("📡 VV SAR", vv, -27, -3, "#fb923c", "Surface roughness"),
        ("🌧️ Rainfall", rainfall, 0, 100, "#60a5fa", "Monthly (mm)"),
    ]
    for col, (label, val, vmin, vmax, clr, desc) in zip([pc1,pc2,pc3,pc4,pc5], params):
        pct = (val - vmin) / (vmax - vmin) * 100
        with col:
            st.markdown(f"""
            <div style="background:#16213E;border-radius:12px;padding:14px;text-align:center;border-top:4px solid {clr};">
            <p style="color:#94a3b8;font-size:12px;margin:0;">{label}</p>
            <p style="color:{clr};font-size:26px;font-weight:700;margin:6px 0;">{val:.2f}</p>
            <p style="color:#64748b;font-size:11px;margin:0;">{desc}</p>
            <div style="background:#0f172a;border-radius:4px;height:6px;margin-top:8px;">
            <div style="background:{clr};width:{pct:.0f}%;height:6px;border-radius:4px;"></div>
            </div>
            </div>
            """, unsafe_allow_html=True)

    # Store results in session for PDF export
    st.session_state["field_result"] = {
        "lat": lat, "lon": lon,
        "ndvi": ndvi, "ndwi": ndwi, "vh": vh, "vv": vv, "rainfall": rainfall,
        "stress": pred_label, "advisory": advisory, "confidence": max(pred_proba)*100,
        "color": color, "action": action
    }

    st.markdown("---")
    st.success("✅ Analysis complete! Head to **📄 PDF Report** page to download a full report.")

st.markdown("---")
st.markdown("<center><h4>🌾 AgriAstra | Precision Agriculture using AI + GIS</h4></center>", unsafe_allow_html=True)
