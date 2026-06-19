# 🌾 AgriAstra: AI-Driven Crop Monitoring and Irrigation Advisory System

## 📌 Project Overview

AgriAstra is an AI-powered agricultural monitoring system that uses satellite imagery, rainfall data, machine learning, and GIS mapping to monitor crop health, detect moisture stress, and provide irrigation recommendations for farmers.

The project integrates multiple data sources to support precision agriculture and sustainable water management.

---

## 🎯 Objectives

* Monitor crop health using satellite imagery.
* Detect moisture stress in agricultural fields.
* Generate irrigation advisories.
* Visualize agricultural conditions using GIS maps.
* Build an interactive dashboard for decision support.

---

## 🛰️ Data Sources

### Sentinel-2

Used to generate:

* NDVI (Normalized Difference Vegetation Index)
* NDWI (Normalized Difference Water Index)

### Sentinel-1

Used to generate:

* VH Backscatter
* VV Backscatter

### CHIRPS Rainfall

Used to integrate rainfall information into the analysis.

---

## 🤖 Machine Learning Model

Algorithm Used:

* Random Forest Classifier

Target Classes:

* Low Moisture Stress
* Moderate Moisture Stress
* High Moisture Stress

Model Accuracy:

* 100% (Prototype Dataset)

---

## 🗺️ GIS Outputs

The project generates:

1. NDVI GIS Map
2. Moisture Stress GIS Map
3. Irrigation Advisory GIS Map

---

## 🚜 Irrigation Advisory

| Moisture Stress | Recommendation         |
| --------------- | ---------------------- |
| Low             | No irrigation needed   |
| Moderate        | Irrigate within 3 days |
| High            | Irrigate immediately   |

---

## 🛠️ Technologies Used

* Python
* Google Earth Engine
* Google Colab
* Streamlit
* Pandas
* NumPy
* Matplotlib
* Scikit-learn
* GitHub

---

## 📁 Project Structure

AgriAstra/

├── data/

│ ├── raw/

│ └── processed/

├── notebooks/

├── earth_engine/

├── dashboard/

├── results/

│ └── maps/

├── README.md

└── requirements.txt

---

## 👩‍💻 Developed For

Field-Based Project / ISRO Problem Statement Prototype

AgriAstra Team
