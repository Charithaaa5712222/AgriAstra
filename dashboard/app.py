import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AgriAstra",
    page_icon="🌾",
    layout="wide"
)

# Load dataset
df = pd.read_csv("data/processed/agriastra_final_dataset.csv")

st.title("🌾 AgriAstra")
st.subheader("AI-Driven Crop Monitoring & Irrigation Advisory System")

st.markdown("---")

# Stress counts from dataset
stress_counts = df["Moisture_Stress"].value_counts()

col1, col2, col3 = st.columns(3)

col1.metric(
    "🟢 Low Stress",
    int(stress_counts.get("Low", 0))
)

col2.metric(
    "🟡 Moderate Stress",
    int(stress_counts.get("Moderate", 0))
)

col3.metric(
    "🔴 High Stress",
    int(stress_counts.get("High", 0))
)

st.markdown("---")

st.header("🗺️ GIS Maps")

m1, m2, m3 = st.columns(3)

with m1:
    st.image(
        "assets/ndvi_map.png",
        caption="NDVI Map"
    )

with m2:
    st.image(
        "assets/moisture_stress_map.png",
        caption="Moisture Stress Map"
    )

with m3:
    st.image(
        "assets/irrigation_map.png",
        caption="Irrigation Advisory Map"
    )

st.markdown("---")

st.header("🚜 Irrigation Recommendations")

st.success("🟢 Low → No irrigation needed")

st.warning("🟡 Moderate → Irrigate within 3 days")

st.error("🔴 High → Irrigate immediately")

st.markdown("---")

st.header("🛰️ Technologies Used")

st.write("• Google Earth Engine")
st.write("• Sentinel-1")
st.write("• Sentinel-2")
st.write("• CHIRPS Rainfall")
st.write("• Random Forest")
st.write("• Streamlit")
