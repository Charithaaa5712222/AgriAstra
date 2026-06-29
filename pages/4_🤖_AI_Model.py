import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (confusion_matrix, classification_report,
                             accuracy_score, f1_score)

st.set_page_config(page_title="AI Model – AgriAstra", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.stApp { background:#0b1220; color:#f8fafc; }
.block-container { padding-top:1.5rem; padding-bottom:1rem; }
h1,h2,h3,h4 { color:#ffffff; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/agriastra_final_dataset.csv")
    return df

@st.cache_data
def train_and_evaluate():
    df = load_data()
    le = LabelEncoder()
    X = df[["NDVI", "NDWI", "VH", "VV", "Rainfall"]]
    y = le.fit_transform(df["Moisture_Stress"])
    
    # Proper train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    model = RandomForestClassifier(n_estimators=200, max_depth=12, min_samples_leaf=2, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    # Cross-validation (more realistic)
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=le.classes_, output_dict=True)
    feat_imp = model.feature_importances_
    
    return {
        "model": model, "le": le,
        "acc": acc, "f1": f1, "cm": cm, "report": report,
        "cv_scores": cv_scores, "feat_imp": feat_imp,
        "X_train": X_train, "X_test": X_test,
        "y_train": y_train, "y_test": y_test, "y_pred": y_pred,
        "classes": le.classes_
    }

results = train_and_evaluate()

st.markdown("## 🤖 AI Model — Performance & Evaluation")

# ── Important Note about 100% accuracy ───────────────────────────────────────
with st.expander("⚠️ Important Note: About Model Accuracy", expanded=True):
    st.warning("""
    **Why does evaluating on the full dataset show 100% accuracy?**
    
    The original model evaluation was performed on the **training data itself** — which always gives 100% because the Random Forest perfectly memorizes training samples. This is a known pitfall called **data leakage**.
    
    AgriAstra now uses **proper evaluation methodology**:
    - ✅ **80/20 Train-Test Split** — model is tested on data it has never seen  
    - ✅ **5-Fold Cross-Validation** — more robust generalization estimate
    - ✅ **Stratified Split** — preserves class distribution across folds
    
    Note: High accuracy (~95%+) on this dataset is still expected because the Moisture_Stress labels were derived 
    from NDVI/NDWI thresholds (rule-based), so the relationship is deterministic by construction. 
    In a real deployment, you would use independent ground-truth labels validated by field surveys.
    """)

# ── Model Performance Cards ───────────────────────────────────────────────────
st.markdown("### 📊 Model Performance (Test Set — 20% Holdout)")

c1, c2, c3, c4 = st.columns(4)
cv_mean = results["cv_scores"].mean()
cv_std  = results["cv_scores"].std()

with c1:
    st.markdown(f"""
    <div style="background:#16213E;border-radius:14px;padding:20px;text-align:center;border-left:6px solid #22c55e;">
    <p style="color:#94a3b8;font-size:13px;margin:0;">Test Accuracy</p>
    <p style="color:#22c55e;font-size:40px;font-weight:700;margin:8px 0;">{results['acc']*100:.1f}%</p>
    <p style="color:#64748b;font-size:12px;">Holdout test set</p>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div style="background:#16213E;border-radius:14px;padding:20px;text-align:center;border-left:6px solid #38bdf8;">
    <p style="color:#94a3b8;font-size:13px;margin:0;">5-Fold CV Accuracy</p>
    <p style="color:#38bdf8;font-size:40px;font-weight:700;margin:8px 0;">{cv_mean*100:.1f}%</p>
    <p style="color:#64748b;font-size:12px;">±{cv_std*100:.1f}% std dev</p>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div style="background:#16213E;border-radius:14px;padding:20px;text-align:center;border-left:6px solid #a78bfa;">
    <p style="color:#94a3b8;font-size:13px;margin:0;">Weighted F1-Score</p>
    <p style="color:#a78bfa;font-size:40px;font-weight:700;margin:8px 0;">{results['f1']:.3f}</p>
    <p style="color:#64748b;font-size:12px;">Balanced metric</p>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div style="background:#16213E;border-radius:14px;padding:20px;text-align:center;border-left:6px solid #fb923c;">
    <p style="color:#94a3b8;font-size:13px;margin:0;">Test Samples</p>
    <p style="color:#fb923c;font-size:40px;font-weight:700;margin:8px 0;">{len(results['y_test'])}</p>
    <p style="color:#64748b;font-size:12px;">From 500 total records</p>
    </div>""", unsafe_allow_html=True)

st.markdown("")

# ── Confusion Matrix + CV Scores ──────────────────────────────────────────────
cm_col, cv_col = st.columns(2)

with cm_col:
    st.markdown("### 🔢 Confusion Matrix")
    cm = results["cm"]
    classes = results["classes"]

    # Normalize for percentage display
    cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True) * 100
    
    text_matrix = [[f"{cm[i][j]}<br>({cm_norm[i][j]:.0f}%)" for j in range(len(classes))] for i in range(len(classes))]
    
    fig_cm = go.Figure(go.Heatmap(
        z=cm_norm,
        x=[f"Pred: {c}" for c in classes],
        y=[f"True: {c}" for c in classes],
        colorscale=[[0,"#0f172a"],[0.5,"#1e3a5f"],[1,"#22c55e"]],
        text=text_matrix,
        texttemplate="%{text}",
        textfont=dict(size=14, color="white"),
        showscale=True,
        colorbar=dict(tickfont=dict(color='white'), title=dict(text="%", font=dict(color='white')))
    ))
    fig_cm.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        height=320,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(color='white', side='bottom'),
        yaxis=dict(color='white', autorange='reversed')
    )
    st.plotly_chart(fig_cm, use_container_width=True)

with cv_col:
    st.markdown("### 📈 Cross-Validation Scores (5-Fold)")
    cv_scores = results["cv_scores"]
    folds = [f"Fold {i+1}" for i in range(len(cv_scores))]
    
    fig_cv = go.Figure()
    fig_cv.add_trace(go.Bar(
        x=folds, y=cv_scores * 100,
        marker_color=["#22c55e" if s >= cv_mean else "#facc15" for s in cv_scores],
        text=[f"{s*100:.1f}%" for s in cv_scores],
        textposition="outside",
        textfont=dict(color="white")
    ))
    fig_cv.add_hline(
        y=cv_mean*100,
        line=dict(color="#38bdf8", dash="dash", width=2),
        annotation_text=f"Mean: {cv_mean*100:.1f}%",
        annotation_font_color="#38bdf8"
    )
    fig_cv.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        yaxis=dict(range=[85, 101], title="Accuracy (%)", color='#94a3b8'),
        xaxis=dict(color='white'),
        height=320,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_cv, use_container_width=True)

# ── Per-class metrics ─────────────────────────────────────────────────────────
st.markdown("### 📋 Per-Class Performance")
report = results["report"]
class_colors = {"Low": "#22c55e", "Moderate": "#facc15", "High": "#ef4444"}

cols = st.columns(len(results["classes"]))
for col, cls in zip(cols, results["classes"]):
    metrics = report.get(cls, {})
    clr = class_colors.get(cls, "#94a3b8")
    with col:
        st.markdown(f"""
        <div style="background:#16213E;border-radius:12px;padding:16px;border-left:5px solid {clr};text-align:center;">
        <h4 style="color:{clr};margin-top:0;">{cls} Stress</h4>
        <p style="color:#94a3b8;font-size:12px;margin:4px 0;">Precision</p>
        <p style="color:white;font-size:22px;font-weight:700;margin:0;">{metrics.get('precision',0)*100:.1f}%</p>
        <p style="color:#94a3b8;font-size:12px;margin:8px 0 4px 0;">Recall</p>
        <p style="color:white;font-size:22px;font-weight:700;margin:0;">{metrics.get('recall',0)*100:.1f}%</p>
        <p style="color:#94a3b8;font-size:12px;margin:8px 0 4px 0;">F1-Score</p>
        <p style="color:{clr};font-size:22px;font-weight:700;margin:0;">{metrics.get('f1-score',0)*100:.1f}%</p>
        <p style="color:#64748b;font-size:11px;margin:8px 0 0 0;">Support: {int(metrics.get('support',0))} samples</p>
        </div>
        """, unsafe_allow_html=True)

# ── Feature Importance ────────────────────────────────────────────────────────
st.markdown("### 🌐 Feature Importance")

features = ["NDVI", "NDWI", "VH", "VV", "Rainfall"]
importances = results["feat_imp"]
feat_colors = ["#00b894", "#38bdf8", "#a78bfa", "#fb923c", "#60a5fa"]

sorted_idx = np.argsort(importances)[::-1]

fig_imp = go.Figure(go.Bar(
    x=[importances[i]*100 for i in sorted_idx],
    y=[features[i] for i in sorted_idx],
    orientation='h',
    marker_color=[feat_colors[i] for i in sorted_idx],
    text=[f"{importances[i]*100:.1f}%" for i in sorted_idx],
    textposition='outside',
    textfont=dict(color='white', size=12)
))
fig_imp.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0b1220",
    plot_bgcolor="#0b1220",
    xaxis=dict(title="Importance (%)", color='#94a3b8', range=[0, max(importances)*130]),
    yaxis=dict(color='white', autorange='reversed'),
    height=280,
    margin=dict(l=10, r=70, t=20, b=30)
)
st.plotly_chart(fig_imp, use_container_width=True)

# ── Model Details ─────────────────────────────────────────────────────────────
st.markdown("### ⚙️ Model Configuration")
d1, d2, d3 = st.columns(3)

with d1:
    st.markdown("""
    <div style="background:#16213E;padding:18px;border-radius:12px;border-left:5px solid #38bdf8;">
    <h4 style="color:white;margin-top:0;">⚙️ Hyperparameters</h4>
    <p style="color:#cbd5e1;">• Algorithm: Random Forest</p>
    <p style="color:#cbd5e1;">• n_estimators: 200</p>
    <p style="color:#cbd5e1;">• max_depth: 12</p>
    <p style="color:#cbd5e1;">• min_samples_leaf: 2</p>
    <p style="color:#cbd5e1;">• criterion: gini</p>
    <p style="color:#cbd5e1;">• random_state: 42</p>
    </div>
    """, unsafe_allow_html=True)

with d2:
    st.markdown("""
    <div style="background:#16213E;padding:18px;border-radius:12px;border-left:5px solid #00b894;">
    <h4 style="color:white;margin-top:0;">📥 Input Features</h4>
    <p style="color:#cbd5e1;">• NDVI — Sentinel-2 (Band 8, 4)</p>
    <p style="color:#cbd5e1;">• NDWI — Sentinel-2 (Band 3, 8)</p>
    <p style="color:#cbd5e1;">• VH — Sentinel-1 SAR (dB)</p>
    <p style="color:#cbd5e1;">• VV — Sentinel-1 SAR (dB)</p>
    <p style="color:#cbd5e1;">• Rainfall — CHIRPS (mm/month)</p>
    </div>
    """, unsafe_allow_html=True)

with d3:
    st.markdown("""
    <div style="background:#16213E;padding:18px;border-radius:12px;border-left:5px solid #a78bfa;">
    <h4 style="color:white;margin-top:0;">🎯 Output Classes</h4>
    <p style="color:#22c55e;">🟢 Low Stress → No irrigation needed</p>
    <p style="color:#facc15;">🟡 Moderate Stress → Irrigate within 3 days</p>
    <p style="color:#ef4444;">🔴 High Stress → Irrigate immediately</p>
    <br>
    <p style="color:#64748b;font-size:12px;">Labels derived from NDVI/NDWI thresholds 
    applied to Sentinel-2 imagery over Nalgonda District</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<center><h4>🌾 AgriAstra | Precision Agriculture using AI + GIS</h4></center>", unsafe_allow_html=True)
