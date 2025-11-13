# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from pathlib import Path
from job_architecture.utils.ui import sidebar_logo_and_title
from job_architecture.utils.ggs_factors import load_factors, get_applicable_factors
from job_architecture.utils.job_match_engine import (
    infer_job_level_from_factors,
    find_matching_job_profile,
    load_job_profile_dataset,
)

# ============================================
# CONFIG DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Job Match",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS global do header (mesmo padrão das outras páginas)
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar padrão SIG
sidebar_logo_and_title()

# Pequeno ajuste de padding
st.markdown(
    """
    <style>
        .block-container {padding-top: 2rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================
# PATHS DOS ARQUIVOS DE DADOS
# __file__ = job_architecture/pages/5_Job_Match.py
# parents[1] = job_architecture/
# ============================================
ROOT_DIR = Path(__file__).parents[1]
DATA_DIR = ROOT_DIR / "data"

JOB_PROFILE_XLSX = DATA_DIR / "Job Profile.xlsx"
GG_FACTORS_JSON = DATA_DIR / "wtw_ggs_factors.json"

# ============================================
# CARREGAR DADOS
# ============================================
job_profiles = load_job_profile_dataset(JOB_PROFILE_XLSX)
ggs_factors = load_factors(GG_FACTORS_JSON)

# ============================================
# CABEÇALHO DA PÁGINA
# ============================================
st.title("🔍 Job Match")
st.write(
    "Defina a **Família**, **Subfamília**, o **cargo ao qual reporta** "
    "e os **Fatores GGS**. O sistema irá sugerir o cargo global mais aderente."
)

st.markdown("---")

# ============================================
# PARÂMETROS HIERÁRQUICOS
# ============================================
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
    "Presidente / CEO",
]

with col1:
    selected_family = st.selectbox("Família (Função)", familias)

with col2:
    selected_subfamily = st.selectbox("Subfamília (Disciplina)", subfamilias)

with col3:
    selected_reporting = st.selectbox(
        "Cargo ao qual reporta (Filtro Rígido)", reporting_options
    )

st.markdown("### 🧠 Fatores de Complexidade do Cargo (GGS)")
st.caption(
    "Abra cada accordion e selecione o nível que melhor descreve o cargo. "
    "Os textos foram resumidos com base no guia oficial WTW."
)

# ============================================
# FATORES GGS EM ACCORDION
# ============================================
applicable_factors = get_applicable_factors(ggs_factors, selected_reporting)
user_factor_choices = {}

for factor_key, factor_obj in applicable_factors.items():
    with st.expander(f"**{factor_obj['label']}** — {factor_obj['short_desc']}"):
        st.caption(factor_obj["short_desc"])

        # Monta as opções com título + descrição resumida
        level_options = []
        level_map = {}
        for level_key, level_data in factor_obj["levels"].items():
            label = f"{level_data['title']} — {level_data['description']}"
            level_options.append(label)
            level_map[label] = level_key

        escolha = st.selectbox(
            f"Selecione o nível de **{factor_obj['label']}**",
            level_options,
            key=f"factor_{factor_key}",
        )

        user_factor_choices[factor_key] = level_map[escolha]

st.markdown("---")

# ============================================
# BOTÃO DE AÇÃO
# ============================================
if st.button("Buscar Job Match", use_container_width=True):

    with st.spinner("Calculando o nível GGS e procurando o melhor cargo..."):

        # 1) Inferir Career Band / Level / Survey Grade (GG)
        inferred_level = infer_job_level_from_factors(user_factor_choices, ggs_factors)

        # 2) Encontrar o cargo mais compatível
        resultado = find_matching_job_profile(
            job_profiles,
            selected_family,
            selected_subfamily,
            inferred_level,
        )

    st.markdown("## 🎯 Resultado do Job Match")

    if resultado is None:
        st.error(
            "Nenhum cargo compatível foi encontrado com base nas seleções. "
            "Tente ajustar alguns fatores de complexidade ou a combinação Família/Subfamília."
        )
    else:
        job = resultado

        # Título + nível
        st.markdown(f"### **{job['Job Title']}**")
        st.markdown(
            f"**Survey Grade (GG):** {job.get('Survey Grade', 'N/A')}  \n"
            f"**Career Band:** {job.get('Career Band', 'N/A')}  \n"
            f"**Família:** {job.get('Family', 'N/A')} — "
            f"**Subfamília:** {job.get('Subfamily', 'N/A')}"
        )

        st.markdown("---")

        # BLOCO 1 — Job Profile Description
        st.markdown("### 📌 Job Profile Description")
        st.write(job.get("Job Profile Description", "—"))

        # BLOCO 2 — Career Band Description
        st.markdown("### 🧱 Career Band Description")
        st.write(job.get("Career Band Description", "—"))

        # BLOCO 3 — Main Description
        st.markdown("### 📝 Main Description")
        st.write(job.get("Main Description", "—"))

        # BLOCO 4 — Grade Differentiator
        st.markdown("### 🟦 Grade Differentiator")
        st.write(job.get("Grade Differentiator", "—"))

        # BLOCO 5 — Qualifications
        st.markdown("### 🎓 Qualifications")
        st.write(job.get("Qualifications", "—"))

        # BLOCO 6 — Specific Parameters / KPIs
        st.markdown("### 🧩 Specific Parameters / KPIs")
        st.write(job.get("Specific Parameters", "—"))

        # BLOCO 7 — Competencies
        st.markdown("### 💡 Competencies")
        st.write(job.get("Competencies", "—"))
