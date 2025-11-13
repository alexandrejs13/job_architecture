# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from pathlib import Path

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

# Oculta header / footer do Streamlit
st.markdown("""
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# =========================================================
# CARREGAR BASES E FATORES
# =========================================================
DATA_DIR = Path(__file__).parents[1] / "data"
JOB_PROFILE_XLSX = DATA_DIR / "Job Profile.xlsx"
GG_FACTORS_JSON = DATA_DIR / "wtw_ggs_factors.json"

job_profiles = load_job_profile_dataset(JOB_PROFILE_XLSX)
ggs_factors = load_factors(GG_FACTORS_JSON)

# =========================================================
# LAYOUT
# =========================================================
st.title("🔍 Job Match")
st.write("Selecione os parâmetros e fatores GGS para encontrar o cargo mais compatível.")

st.markdown("---")

col1, col2, col3 = st.columns(3)

# IMPORTANTE: Carregar famílias e subfamílias da Job Profile.xlsx
familias = sorted(job_profiles["Family"].dropna().unique())
subfamilias = sorted(job_profiles["Subfamily"].dropna().unique())
reporting_options = ["Aprendiz / Estágio", "Assistente", "Analista", "Especialista",
                     "Supervisor", "Coordenador", "Gerente", "Diretor", "VP", "Presidente / CEO"]

with col1:
    selected_family = st.selectbox("Família", familias)

with col2:
    selected_subfamily = st.selectbox("Subfamília", subfamilias)

with col3:
    selected_reporting = st.selectbox("Cargo ao qual reporta (Filtro Rígido)", reporting_options)

st.markdown("### 🧠 Fatores de Complexidade (GGS)")
st.caption("Use os accordions para escolher o nível de cada fator.")

# =========================================================
# RENDERIZAR FATORES GGS COM FILTRO AUTOMÁTICO
# =========================================================
applicable_factors = get_applicable_factors(ggs_factors, selected_reporting)

user_factor_choices = {}

for factor_key, factor_obj in applicable_factors.items():

    with st.expander(f"**{factor_obj['label']}** — {factor_obj['short_desc']}"):
        st.markdown(f"_{factor_obj['short_desc']}_")

        # níveis
        level_options = []
        level_map = {}

        for level_key, level_data in factor_obj["levels"].items():
            option_label = f"{level_data['title']} — {level_data['description']}"
            level_options.append(option_label)
            level_map[option_label] = level_key

        chosen = st.selectbox(
            f"Selecione o nível de **{factor_obj['label']}**",
            level_options,
            key=factor_key
        )

        user_factor_choices[factor_key] = level_map[chosen]

st.markdown("---")

# =========================================================
# BOTÃO DE MATCH
# =========================================================
if st.button("Buscar Job Match", use_container_width=True):

    with st.spinner("Analisando fatores, níveis e estruturas..."):

        # 1 — Inferir Level / Career Band / Survey Grade
        inferred_level = infer_job_level_from_factors(user_factor_choices, ggs_factors)

        # 2 — Encontrar o cargo correspondente
        match_result = find_matching_job_profile(
            job_profiles,
            selected_family,
            selected_subfamily,
            inferred_level
        )

    st.markdown("## 🎯 Resultado do Job Match")

    if match_result is None:
        st.error("Nenhum cargo correspondente encontrado com base nos fatores selecionados.")
    else:
        job = match_result

        st.markdown(f"### **{job['Job Title']}**")
        st.markdown(f"**GG:** {job.get('Survey Grade','N/A')} — **Career Band:** {job.get('Career Band','N/A')}")

        st.markdown("---")
        st.markdown("### 📌 Job Profile Description")
        st.write(job.get("Job Profile Description","—"))

        st.markdown("### 🧱 Career Band Description")
        st.write(job.get("Career Band Description","—"))

        st.markdown("### 📝 Main Description")
        st.write(job.get("Main Description","—"))

        st.markdown("### 🟦 Grade Differentiator")
        st.write(job.get("Grade Differentiator","—"))

        st.markdown("### 🎓 Qualifications")
        st.write(job.get("Qualifications","—"))

        st.markdown("### 🧩 Specific Parameters / KPIs")
        st.write(job.get("Specific Parameters","—"))

        st.markdown("### 💡 Competencies")
        st.write(job.get("Competencies","—"))
