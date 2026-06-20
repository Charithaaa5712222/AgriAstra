import streamlit as st
import pandas as pd

st.set_page_config(page_title="AgriAstra",page_icon="🌾",layout="wide")

try:
    df=pd.read_csv("data/processed/agriastra_final_dataset.csv")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

st.markdown("""
# 🌾 AgriAstra
### AI-Driven Crop Monitoring & Irrigation Advisory System
##### Smart Agriculture using Satellite Imagery, AI and GIS
""")

st.info("""
AgriAstra combines satellite imagery, rainfall data,
machine learning, and GIS visualization to monitor
crop health and generate irrigation advisories.
""")

st.markdown("---")

if "Moisture_Stress" in df.columns:
    stress_counts=df["Moisture_Stress"].value_counts()

    col1,col2,col3,col4=st.columns(4)

    col1.metric("📍 Samples",len(df))
    col2.metric("🟢 Low Stress",int(stress_counts.get("Low",0)))
    col3.metric("🟡 Moderate Stress",int(stress_counts.get("Moderate",0)))
    col4.metric("🔴 High Stress",int(stress_counts.get("High",0)))
else:
    st.warning("Column 'Moisture_Stress' not found in dataset.")
    stress_counts=pd.Series()

st.markdown("---")

st.markdown("## 🤖 AI Model")

c1,c2=st.columns(2)

with c1:
    st.metric("Random Forest Accuracy","100%")

with c2:
    st.metric("Model Type","Random Forest")

st.markdown("---")

st.header("🗺️ GIS Maps")
st.caption("NDVI • Moisture Stress • Irrigation Advisory")

m1,m2,m3=st.columns(3)

with m1:
    try:
        st.image("dashboard/assets/ndvi_map.jpeg",caption="🌱 NDVI Map",use_container_width=True)
    except:
        st.warning("NDVI map not found.")

with m2:
    try:
        st.image("dashboard/assets/moisture_stress_map.jpeg",caption="💧 Moisture Stress Map",use_container_width=True)
    except:
        st.warning("Moisture Stress map not found.")

with m3:
    try:
        st.image("dashboard/assets/irrigation_map.jpeg",caption="🚜 Irrigation Advisory Map",use_container_width=True)
    except:
        st.warning("Irrigation map not found.")

st.markdown("---")

st.markdown("## 📊 Moisture Stress Distribution")

if not stress_counts.empty:
    st.bar_chart(stress_counts)

st.markdown("---")

st.markdown("## 🚜 Irrigation Recommendations")

with st.expander("View Recommendations"):
    st.success("🟢 Low → No irrigation needed")
    st.warning("🟡 Moderate → Irrigate within 3 days")
    st.error("🔴 High → Irrigate immediately")

st.markdown("---")

st.header("📊 Dataset Preview")
st.dataframe(df.head())

st.markdown("---")

st.markdown("## 👩‍💻 Project Information")

st.info("""
Project: AgriAstra

Domain: Precision Agriculture

Study Area: Nalgonda District

Data Sources:
• Sentinel-1
• Sentinel-2
• CHIRPS Rainfall

Tools:
• Google Earth Engine
• Python
• Streamlit
• GitHub
• Random Forest
""")

st.markdown("---")

st.header("🛰️ Technologies Used")

technologies=[
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
