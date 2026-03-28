# ============================================================
#  dashboard/app.py  — Streamlit Main Entry Point
# ============================================================

import streamlit as st

st.set_page_config(
    page_title="ENAP — Tableau de Bord",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Header ───────────────────────────────────────────────────
st.title("📊 ENAP — Projet Pluridisciplinaire")
st.markdown("### Tableau de bord d'analyse et de prévision")
st.divider()

# ── Navigation Info ──────────────────────────────────────────
st.info("👈 Use the sidebar to navigate between analysis pages.")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Module", value="Ventes & Prévisions", delta="Actif")

with col2:
    st.metric(label="Module", value="Clients & Churn", delta="Actif")

with col3:
    st.metric(label="Module", value="Stock & Anomalies", delta="Actif")
