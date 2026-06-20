```python
import streamlit as st
import pandas as pd

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="AgriAstra",
    page_icon="🌾",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

df = pd.read_csv(
    "data/processed/agriastra_final_dataset.csv"
)

# ---------------- TITLE ----------------

st.title("🌾 AgriAstra")

st.subheader(
    "AI-Driven Crop Monitoring & Irrigation Advisory System"
)

st.info(
"""
AgriAstra combines satellite imagery, rainfall data,
machine learning, and GIS visualization to monitor
crop health and generate irrigation advisories.
"""
)

st.markdown("---")

# ---------------- STRESS COUNTS ----------------

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

# ---------------- MODEL PERFORMANCE ----------------

st.markdown("### 🤖 Model Performance")

st.metric(
    "Random Forest Accuracy",
    "100%"
)

st.markdown("---")

# ---------------- GIS MAPS ----------------

st.header("🗺️ GIS Maps")

st.caption(
    "NDVI • Moisture Stress • Irrigation Advisory"
)

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

st.markdown("---")

# ---------------- IRRIGATION ADVISORY ----------------

st.header("🚜 Irrigation Recommendations")

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

# ---------------- DATASET PREVIEW ----------------

st.header("📊 Dataset Preview")

st.dataframe(
    df.head()
)

st.markdown("---")

# ---------------- TECHNOLOGIES USED ----------------

st.header("🛰️ Technologies Used")

st.write("• Google Earth Engine")

st.write("• Sentinel-2")

st.write("• Sentinel-1")

st.write("• CHIRPS Rainfall")

st.write("• Random Forest")

st.write("• Python")

st.write("• Streamlit")
```
