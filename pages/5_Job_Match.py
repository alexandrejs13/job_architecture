# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from pathlib import Path

# === IMPORTAÇÕES DOS MÓDULOS ===
from utils.ggs_factors import load_factors, get_applicable_factors
from utils.job_match_engine import (
    infer_job_level_from_factors,
    find_matching_job_profile,
    load_job_profile_dataset
)

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Job Match",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ocultar header e footer
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding-top: 20px;}
    </style>
""", unsafe_allow_html=True)

# =========================================================
# LOCALIZAÇÃO DAS BASES
# =========================================================

# __file__ está em: job_architecture/pages/5_Job_Match.py
# parents[1] = job_architecture/
DATA_DIR = Path(__file__).parents[1] / "data"

JOB_PROFILE_XLSX = DATA_DIR / "Job Profile.xlsx"
GG_FACTORS_JSON = DATA_DIR / "wtw_ggs_factors.json"

# =========================================================
# CARREGAR BASES
# =========================================================
job_profiles = load_job_profile_dataset(JOB_PROFILE_XLSX)
ggs_factors = load_factors(GG_FACTORS_JSON)

# =========================================================
# INTERFACE
# =========================================================
st.title("🔍 Job Match")
st.write("Selecione família, subfamília e fatores GGS para encontrar o cargo ideal.")

st.markdown("---")

# CAMPOS PRINCIPAIS
col1, col2, col3 = st.columns(3)

familias = sorted(job_profiles["Family"].dropna().unique())
subfamilias = sorted(job_profiles["Subfamily"].dropna().unique())

reporting_options = [
    "Aprendiz / Estágio",
    "Assistente",
    "Analista",
    "Especialista",
    "Supervisor",
    "Coordenador",
    "Gerente",
    "Diretor",
    "VP",
    "Presidente / CEO"
]

with col1:
    selected_family = st.selectbox("Família", familias)

with col2:
    selected_subfamily = st.selectbox("Subfamília", subfamilias)

with col3:
    selected_reporting = st.selectbox("Cargo ao qual reporta (Filtro Rígido)", reporting_options)

st.markdown("### 🧠 Fatores de Complexidade (GGS)")

applicable_factors = get_applicable_factors(ggs_factors, selected_reporting)

user_factor_choices = {}

# =========================================================
# ACCORDIONS DOS FATORES
# =========================================================
for factor_key, factor_obj in applicable_factors.items():

    with st.expander(f"**{factor_obj['label']}** — {factor_obj['short_desc']}"):
        st.caption(factor_obj["short_desc"])

        level_options = []
        level_map = {}

        for level_key, level_data in factor_obj["levels"].items():
            text = f"{level_data['title']} — {level_data['description']}"
            level_options.append(text)
            level_map[text] = level_key

        escolha = st.selectbox(
            f"Selecione o nível de **{factor_obj['label']}**",
            level_options,
            key=factor_key
        )

        user_factor_choices[factor_key] = level_map[escolha]

st.markdown("---")

# =========================================================
# BOTÃO
# =========================================================
if st.button("Buscar Job Match", use_container_width=True):

    with st.spinner("Processando fatores e identificando o cargo ideal..."):

        inferred_level = infer_job_level_from_factors(
            user_factor_choices,
            ggs_factors
        )

        resultado = find_matching_job_profile(
            job_profiles,
            selected_family,
            selected_subfamily,
            inferred_level
        )

    # =====================================================
    # RESULTADO
    # =====================================================
    st.markdown("## 🎯 Resultado do Job Match")

    if resultado is None:
        st.error("Nenhum cargo compatível encontrado com os fatores selecionados.")
    else:
        job = resultado

        st.markdown(f"### **{job['Job Title']}**")
        st.markdown(
            f"**Survey Grade (GG):** {job.get('Survey Grade', 'N/A')} — "
            f"**Career Band:** {job.get('Career Band', 'N/A')}"
        )

        st.markdown("---")

        # BLOCO 1 — SUMÁRIO / DESCRIÇÃO PRINCIPAL
        st.markdown("### 📌 Job Profile Description")
        st.write(job.get("Job Profile Description", "—"))

        # BLOCO 2 — CAREER BAND
        st.markdown("### 🧱 Career Band Description")
        st.write(job.get("Career Band Description", "—"))

        # BLOCO 3 — MAIN DESCRIPTION
        st.markdown("### 📝 Main Description")
        st.write(job.get("Main Description", "—"))

        # BLOCO 4 — GRADE DIFFERENTIATOR
        st.markdown("### 🟦 Grade Differentiator")
        st.write(job.get("Grade Differentiator", "—"))

        # BLOCO 5 — QUALIFICAÇÕES
        st.markdown("### 🎓 Qualifications")
        st.write(job.get("Qualifications", "—"))

        # BLOCO 6 — KPIs
        st.markdown("### 🧩 Specific Parameters / KPIs")
        st.write(job.get("Specific Parameters", "—"))

        # BLOCO 7 — COMPETÊNCIAS
        st.markdown("### 💡 Competencies")
        st.write(job.get("Competencies", "—"))
