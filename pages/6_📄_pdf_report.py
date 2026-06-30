import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF
from datetime import datetime
import io
import os

st.set_page_config(page_title="PDF Report – AgriAstra", page_icon="📄", layout="wide")

st.markdown("""
<style>
.stApp { background:#0b1220; color:#f8fafc; }
.block-container { padding-top:1.5rem; padding-bottom:1rem; }
h1,h2,h3,h4 { color:#ffffff; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 📄 Downloadable PDF Report")
st.caption("Generate a professional field report with AI predictions, charts, and irrigation recommendations.")

# ── Check if field analysis was done ─────────────────────────────────────────
has_result = "field_result" in st.session_state

if not has_result:
    st.info("💡 Run a **Field Analysis** first to auto-populate the report. Or fill in details manually below.")

# ── Report Form ───────────────────────────────────────────────────────────────
st.markdown("### 📝 Report Details")

col1, col2 = st.columns(2)

if has_result:
    r = st.session_state["field_result"]
    default_lat = str(round(r["lat"], 4))
    default_lon = str(round(r["lon"], 4))
    default_ndvi = round(r["ndvi"], 3)
    default_ndwi = round(r["ndwi"], 3)
    default_rainfall = round(r["rainfall"], 2)
    default_stress = r["stress"]
    default_advisory = r["advisory"]
    default_conf = round(r["confidence"], 1)
else:
    default_lat = "17.0575"
    default_lon = "79.2671"
    default_ndvi = 0.45
    default_ndwi = -0.52
    default_rainfall = 18.5
    default_stress = "Moderate"
    default_advisory = "Irrigate within 3 days"
    default_conf = 87.5

with col1:
    farmer_name = st.text_input("👨‍🌾 Farmer / Field Owner Name", value="Farmer Name")
    field_id = st.text_input("🏷️ Field ID / Survey Number", value="FLD-2025-001")
    mandal = st.text_input("📍 Mandal / Village", value="Nalgonda")
    district = st.text_input("🗺️ District", value="Nalgonda, Telangana")

with col2:
    lat_str = st.text_input("🌐 Latitude", value=default_lat)
    lon_str = st.text_input("🌐 Longitude", value=default_lon)
    season = st.selectbox("🌾 Season", ["Kharif 2025", "Rabi 2025-26", "Zaid 2026", "Kharif 2024"])
    crop = st.selectbox("🌱 Crop Type", ["Paddy", "Cotton", "Maize", "Groundnut", "Soybean", "Jowar", "Sugarcane"])

st.markdown("### 🤖 AI Prediction Summary")
m1, m2, m3 = st.columns(3)
with m1:
    ndvi_val = st.number_input("NDVI", value=default_ndvi, min_value=-1.0, max_value=1.0, step=0.001)
with m2:
    ndwi_val = st.number_input("NDWI", value=default_ndwi, min_value=-1.0, max_value=1.0, step=0.001)
with m3:
    rainfall_val = st.number_input("Rainfall (mm)", value=default_rainfall)

stress_level = st.selectbox("Moisture Stress Level", ["Low", "Moderate", "High"], index=["Low","Moderate","High"].index(default_stress))
advisory_text = st.text_input("Irrigation Advisory", value=default_advisory)
confidence_val = st.number_input("Model Confidence (%)", value=default_conf, min_value=0.0, max_value=100.0)

additional_notes = st.text_area("📋 Additional Notes / Observations", 
    placeholder="Add any field observations, soil type, crop growth stage, etc.", height=100)

# ── Generate PDF ──────────────────────────────────────────────────────────────
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()

    # Color scheme
    dark_bg = (11, 18, 32)
    green_accent = (0, 184, 148)
    header_green = (15, 118, 110)
    text_light = (248, 250, 252)
    card_bg = (22, 33, 62)
    muted = (148, 163, 184)

    stress_colors = {
        "Low": (34, 197, 94),
        "Moderate": (250, 204, 21),
        "High": (239, 68, 68)
    }

    # ── Header Banner ──────────────────────────────────────────────────────────
    pdf.set_fill_color(*header_green)
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_xy(10, 8)
    pdf.cell(0, 10, "AgriAstra", ln=True)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_xy(10, 21)
    pdf.cell(0, 7, "AI-Driven Crop Monitoring & Irrigation Advisory System", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(209, 250, 229)
    pdf.set_xy(10, 31)
    pdf.cell(0, 6, "Satellite Imagery | GIS Analysis | Machine Learning | Nalgonda District", ln=True)

    # Report title
    pdf.set_fill_color(11, 18, 32)
    pdf.rect(0, 45, 210, 297, 'F')
    pdf.set_xy(10, 52)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, "Field Irrigation Advisory Report", ln=True)

    now = datetime.now()
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*muted)
    pdf.set_x(10)
    pdf.cell(0, 6, f"Generated: {now.strftime('%d %B %Y, %I:%M %p')}  |  Season: {season}  |  Crop: {crop}", ln=True)
    pdf.ln(3)

    # ── Field Information ──────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*green_accent)
    pdf.set_x(10)
    pdf.cell(0, 8, "FIELD INFORMATION", ln=True)

    # Card background
    pdf.set_fill_color(*card_bg)
    pdf.rect(10, pdf.get_y(), 190, 36, 'F')
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(255, 255, 255)
    y = pdf.get_y() + 4
    
    fields_info = [
        ("Farmer Name", farmer_name, "Field ID", field_id),
        ("Mandal/Village", mandal, "District", district),
        ("Latitude", lat_str, "Longitude", lon_str),
    ]
    for row in fields_info:
        pdf.set_xy(14, y)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*muted)
        pdf.cell(25, 5, row[0] + ":", ln=False)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(65, 5, str(row[1]), ln=False)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*muted)
        pdf.cell(25, 5, row[2] + ":", ln=False)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(65, 5, str(row[3]), ln=True)
        y += 8
    pdf.set_y(y + 5)

    # ── AI Prediction ─────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*green_accent)
    pdf.set_x(10)
    pdf.cell(0, 8, "AI PREDICTION RESULTS", ln=True)

    sc = stress_colors.get(stress_level, (148, 163, 184))
    
    # Stress level card
    pdf.set_fill_color(*card_bg)
    pdf.rect(10, pdf.get_y(), 90, 30, 'F')
    pdf.set_fill_color(*sc)
    pdf.rect(10, pdf.get_y(), 5, 30, 'F')
    y_card = pdf.get_y()
    pdf.set_xy(18, y_card + 4)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*muted)
    pdf.cell(0, 5, "MOISTURE STRESS LEVEL", ln=True)
    pdf.set_xy(18, y_card + 12)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*sc)
    pdf.cell(0, 10, stress_level.upper(), ln=True)
    pdf.set_xy(18, y_card + 24)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*muted)
    pdf.cell(0, 5, f"Model Confidence: {confidence_val:.1f}%", ln=True)

    # Advisory card
    pdf.set_fill_color(*card_bg)
    pdf.rect(105, y_card, 95, 30, 'F')
    pdf.set_fill_color(56, 189, 248)
    pdf.rect(105, y_card, 5, 30, 'F')
    pdf.set_xy(113, y_card + 4)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*muted)
    pdf.cell(0, 5, "IRRIGATION ADVISORY", ln=True)
    pdf.set_xy(113, y_card + 12)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(56, 189, 248)
    pdf.cell(0, 6, advisory_text, ln=True)
    pdf.set_y(y_card + 36)
    pdf.ln(4)

    # ── Satellite Parameters ───────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*green_accent)
    pdf.set_x(10)
    pdf.cell(0, 8, "SATELLITE-DERIVED PARAMETERS", ln=True)

    pdf.set_fill_color(*card_bg)
    pdf.rect(10, pdf.get_y(), 190, 28, 'F')
    y_params = pdf.get_y() + 4

    params = [
        ("NDVI", f"{ndvi_val:.3f}", "Vegetation Index", (0, 184, 148)),
        ("NDWI", f"{ndwi_val:.3f}", "Water Index", (56, 189, 248)),
        ("VH SAR", "Sentinel-1", "Backscatter", (167, 139, 250)),
        ("Rainfall", f"{rainfall_val:.1f} mm", "CHIRPS Data", (96, 165, 250)),
    ]
    x_offset = 14
    for param_name, param_val, param_desc, pclr in params:
        pdf.set_fill_color(*pclr)
        pdf.rect(x_offset, y_params, 2, 20, 'F')
        pdf.set_xy(x_offset + 4, y_params + 2)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*muted)
        pdf.cell(35, 4, param_name, ln=True)
        pdf.set_xy(x_offset + 4, y_params + 8)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*pclr)
        pdf.cell(35, 6, param_val, ln=True)
        pdf.set_xy(x_offset + 4, y_params + 16)
        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(*muted)
        pdf.cell(35, 4, param_desc, ln=True)
        x_offset += 48

    pdf.set_y(y_params + 32)

    # ── Recommendations ────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*green_accent)
    pdf.set_x(10)
    pdf.cell(0, 8, "IRRIGATION RECOMMENDATIONS", ln=True)

    rec_map = {
        "Low": [
            "No irrigation required at this time.",
            "Continue monitoring NDVI weekly via satellite data.",
            "Maintain current crop management practices.",
            "Next assessment recommended in 7 days."
        ],
        "Moderate": [
            "Irrigate within the next 2-3 days to prevent yield loss.",
            "Apply 40-60mm of water depending on soil type.",
            "Monitor soil moisture levels after irrigation.",
            "Check NDWI values post-irrigation to confirm recovery."
        ],
        "High": [
            "CRITICAL: Irrigate immediately to prevent crop damage.",
            "Apply 60-80mm water urgently — crop stress is severe.",
            "Consider foliar spray as immediate relief measure.",
            "Reassess satellite indices within 48 hours post-irrigation."
        ]
    }
    recs = rec_map.get(stress_level, [])
    
    pdf.set_fill_color(*card_bg)
    y_rec = pdf.get_y()
    pdf.rect(10, y_rec, 190, len(recs)*10 + 8, 'F')
    
    for i, rec in enumerate(recs):
        pdf.set_xy(16, y_rec + 4 + i*10)
        pdf.set_fill_color(*sc)
        pdf.rect(14, y_rec + 6 + i*10, 3, 3, 'F')
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 8, rec, ln=True)

    pdf.set_y(y_rec + len(recs)*10 + 12)

    # ── Additional Notes ───────────────────────────────────────────────────────
    if additional_notes.strip():
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(*green_accent)
        pdf.set_x(10)
        pdf.cell(0, 8, "FIELD OBSERVATIONS & NOTES", ln=True)
        pdf.set_fill_color(*card_bg)
        y_note = pdf.get_y()
        pdf.rect(10, y_note, 190, 30, 'F')
        pdf.set_xy(14, y_note + 5)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(255, 255, 255)
        pdf.multi_cell(182, 6, additional_notes)
        pdf.ln(5)

    # ── Footer ─────────────────────────────────────────────────────────────────
    pdf.set_fill_color(*header_green)
    pdf.rect(0, 277, 210, 20, 'F')
    pdf.set_xy(10, 281)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(209, 250, 229)
    pdf.cell(100, 6, "AgriAstra | AI-Driven Crop Monitoring | ISRO Hackathon 2025", ln=False)
    pdf.set_x(130)
    pdf.cell(0, 6, f"Page 1  |  {now.strftime('%d/%m/%Y')}", ln=True)
    pdf.set_xy(10, 288)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*muted)
    pdf.cell(0, 5, "Powered by Sentinel-1/2 Satellite Data, CHIRPS Rainfall, Random Forest ML | Study Area: Nalgonda, Telangana", ln=True)

    return bytes(pdf.output())


st.markdown("---")

if st.button("📄 Generate & Download PDF Report", type="primary", use_container_width=True):
    with st.spinner("Generating professional PDF report..."):
        try:
            pdf_bytes = generate_pdf()
            filename = f"AgriAstra_Report_{farmer_name.replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            
            st.success("✅ PDF Report generated successfully!")
            
            # Preview
            sc_map = {"Low": "#22c55e", "Moderate": "#facc15", "High": "#ef4444"}
            sc_color = sc_map.get(stress_level, "#94a3b8")
            
            st.markdown(f"""
            <div style="background:#16213E;border-radius:14px;padding:20px;border-left:5px solid #00b894;margin-bottom:16px;">
            <h4 style="color:#00b894;margin-top:0;">📄 Report Preview</h4>
            <table style="color:white;font-size:14px;width:100%;">
            <tr><td style="color:#94a3b8;width:160px;">Farmer:</td><td><b>{farmer_name}</b></td><td style="color:#94a3b8;width:160px;">Field ID:</td><td><b>{field_id}</b></td></tr>
            <tr><td style="color:#94a3b8;">Location:</td><td>{mandal}, {district}</td><td style="color:#94a3b8;">Season:</td><td>{season}</td></tr>
            <tr><td style="color:#94a3b8;">Stress Level:</td><td><b style="color:{sc_color};">{stress_level}</b></td><td style="color:#94a3b8;">Advisory:</td><td>{advisory_text}</td></tr>
            <tr><td style="color:#94a3b8;">Confidence:</td><td>{confidence_val:.1f}%</td><td style="color:#94a3b8;">Generated:</td><td>{datetime.now().strftime('%d %b %Y %I:%M %p')}</td></tr>
            </table>
            </div>
            """, unsafe_allow_html=True)
            
            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
            st.info("Make sure you have fpdf2 installed: `pip install fpdf2`")

st.markdown("---")
st.markdown("<center><h4>🌾 AgriAstra | Precision Agriculture using AI + GIS</h4></center>", unsafe_allow_html=True)
