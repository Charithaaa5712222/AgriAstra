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
.main{
    padding-top:1rem;
}
.metric-card{
    background-color:#f8f9fa;
    padding:20px;
    border-radius:15px;
    border:1px solid #e6e6e6;
}
.hero{
    padding:20px;
    border-radius:15px;
    background:linear-gradient(90deg,#1b5e20,#43a047);
    color:white;
    text-align:center;
}
</style>
""",unsafe_allow_html=True)

st.sidebar.image(
    "dashboard/assets/ndvi_map.jpeg",
    use_container_width=True
)

st.sidebar.title("🌾 AgriAstra")

st.sidebar.markdown("---")

if "Moisture_Stress" in df.columns:

    selected_stress = st.sidebar.multiselect(
        "Filter Stress Level",
        df["Moisture_Stress"].unique(),
        default=df["Moisture_Stress"].unique()
    )

    df = df[
        df["Moisture_Stress"].isin(selected_stress)
    ]

st.markdown("""
<div class="hero">
<h1>🌾 AgriAstra</h1>
<h3>AI-Driven Crop Monitoring & Irrigation Advisory System</h3>
<h4>Smart Agriculture using Satellite Imagery, AI and GIS</h4>
</div>
""",unsafe_allow_html=True)

st.markdown("")

st.info("""
AgriAstra combines satellite imagery, rainfall data, machine learning,
and GIS visualization to monitor crop health and generate irrigation advisories.
""")

stress_counts = df["Moisture_Stress"].value_counts()

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

a1,a2,a3 = st.columns(3)

a1.metric(
    "Accuracy",
    "100%"
)

a2.metric(
    "Model",
    "Random Forest"
)

a3.metric(
    "Prediction Target",
    "Moisture Stress"
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

    st.subheader("GIS Visualization")

    m1,m2,m3 = st.columns(3)

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

    st.bar_chart(stress_counts)

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
