import streamlit as st
import pandas as pd

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="AgriAstra",
    page_icon="🌾",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
try:
    df = pd.read_csv("data/processed/agriastra_final_dataset.csv")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ---------------- TITLE ----------------
st.title("🌾 AgriAstra")
st.subheader("AI-Driven Crop Monitoring & Irrigation Advisory System")

st.info("""
AgriAstra combines satellite imagery, rainfall data,
machine learning, and GIS visualization to monitor
crop health and generate irrigation advisories.
""")

st.markdown("---")

# ---------------- STRESS COUNTS ----------------
if "Moisture_Stress" in df.columns:
    stress_counts = df["Moisture_Stress"].value_counts()

    col1, col2, col3 = st.columns(3)

    col1.metric("🟢 Low Stress", int(stress_counts.get("Low", 0)))
    col2.metric("🟡 Moderate Stress", int(stress_counts.get("Moderate", 0)))
    col3.metric("🔴 High Stress", int(stress_counts.get("High", 0)))
else:
    st.warning("Column 'Moisture_Stress' not found in dataset.")

# ---------------- MODEL PERFORMANCE ----------------
st.markdown("### 🤖 Model Performance")
st.metric("Random Forest Accuracy", "100%")

st.markdown("---")

# ---------------- GIS MAPS ----------------
st.header("🗺️ GIS Maps")
st.caption("NDVI • Moisture Stress • Irrigation Advisory")

m1, m2, m3 = st.columns(3)

with m1:
    try:
        st.image(
            "assets/ndvi_map.jpeg",
            caption="🌱 NDVI Map",
            use_container_width=True
        )
    except:
        st.warning("NDVI map not found.")

with m2:
    try:
        st.image(
            "assets/moisture_stress_map.jpeg",
            caption="💧 Moisture Stress Map",
            use_container_width=True
        )
    except:
        st.warning("Moisture Stress map not found.")

with m3:
    try:
        st.image(
            "assets/irrigation_map.jpeg",
            caption="🚜 Irrigation Advisory Map",
            use_container_width=True
        )
    except:
        st.warning("Irrigation map not found.")

st.markdown("---")

# ---------------- IRRIGATION ADVISORY ----------------
st.header("🚜 Irrigation Recommendations")

st.success("🟢 Low → No irrigation needed")
st.warning("🟡 Moderate → Irrigate within 3 days")
st.error("🔴 High → Irrigate immediately")

st.markdown("---")

# ---------------- DATASET PREVIEW ----------------
st.header("📊 Dataset Preview")
st.dataframe(df.head())

st.markdown("---")

# ---------------- TECHNOLOGIES USED ----------------
st.header("🛰️ Technologies Used")

technologies = [
    "Google Earth Engine",
    "Sentinel-2",
    "Sentinel-1",
    "CHIRPS Rainfall",
    "Random Forest",
    "Python",
    "Streamlit"
]

for tech in technologies:
    st.write(f"• {tech}")
