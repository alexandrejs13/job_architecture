# -*- coding: utf-8 -*-
# pages/5_Job_Match.py

import streamlit as st
from pathlib import Path
import json

# IMPORTS CORRETOS (OPÇÃO A)
from utils.ui import sidebar_logo_and_title
from utils.ggs_factors import load_factors, get_applicable_factors
from utils.job_match_engine import find_best_match

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Job Match (GGS)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# SIDEBAR SIG UNIFICADA
# =============================================================================
sidebar_logo_and_title(
    logo_path="assets/SIG_Logo_RGB_Black.png",
    active_page="Job Match (GGS)",
    menu_items=[
        ("Job Architecture", "governance.png", "1_Job_Architecture.py"),
        ("Job Families", "people employees.png", "2_Job_Families.py"),
        ("Job Profile Description", "business review clipboard.png", "3_Job_Profile_Description.py"),
        ("Job Maps", "globe trade.png", "4_Job_Maps.py"),
        ("Job Match (GGS)", "checkmark success.png", "5_Job_Match.py"),
        ("Structure Level", "process.png", "6_Structure_Level.py"),
        ("Dashboard", "data 2 performance.png", "7_Dashboard.py"),
    ],
    icons_path="assets/icons",
    pilula_color="#145efc",
    sidebar_bg="#f2efeb",
    text_color="#000000",
)

# =============================================================================
# CSS SIG UNIFICADO
# =============================================================================
st.markdown("""
<style>

    body, .main {
        background-color: #ffffff !important;
    }

    .sig-title {
        background-color: #145efc;
        color: white;
        padding: 14px 20px;
        border-radius: 6px;
        font-size: 22px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 18px;
        margin-top: 8px;
    }

    .sig-container {
        background-color: #ffffff;
        border: 1px solid #e5dfd9;
        padding: 18px 22px;
        border-radius: 6px;
        margin-bottom: 20px;
    }

    .accordion-header {
        background-color: #f2efeb;
        padding: 10px 14px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        border: 1px solid #dcd6d0;
    }

    .accordion-body {
        background-color: white;
        border-left: 2px solid #145efc;
        padding: 14px 16px;
        margin-top: 4px;
        border-radius: 6px;
    }

    .stButton>button {
        background-color: #145efc !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 10px 18px !important;
        font-weight: 600 !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #0f4cd4 !important;
    }

</style>
""", unsafe_allow_html=True)

# =============================================================================
# TÍTULO DA PÁGINA
# =============================================================================
icon_path = Path("assets/icons/checkmark success.png")

st.markdown(
    f"""
    <div class="sig-title">
        <img src="{icon_path.as_posix()}" width="22px">
        Job Match (GGS)
    </div>
    """,
    unsafe_allow_html=True
)

# =============================================================================
# CARREGAR FATORES WTW GGS
# =============================================================================
factors = load_factors("data/wtw_ggs_factors.json")

if not factors:
    st.error("Erro ao carregar os fatores GGS (wtw_ggs_factors.json).")
    st.stop()

# =============================================================================
# SELEÇÃO DO CARGO SUPERIOR (FILTRO RÍGIDO)
# =============================================================================
st.markdown("""
<div class="sig-container">
<h3>1. Cargo ao qual esta posição reporta</h3>
Selecione o nível hierárquico que limita automaticamente quais cargos podem ser retornados.
</div>
""", unsafe_allow_html=True)

report_to_options = [
    "Apprentice",
    "Intern",
    "Assistant",
    "Analyst",
    "Senior Analyst",
    "Coordinator",
    "Supervisor",
    "Manager",
    "Senior Manager",
    "Director",
    "Senior Director",
    "VP",
    "SVP",
    "C-Level"
]

report_to = st.selectbox("Selecione o nível hierárquico superior", report_to_options)

# Carrega fatores válidos de acordo com o supervisor
applicable_factors = get_applicable_factors(factors, report_to)

# =============================================================================
# FORMULÁRIO DOS FATORES GGS (ACCORDION)
# =============================================================================
st.markdown("""
<div class="sig-container">
<h3>2. Selecione os fatores GGS aplicáveis</h3>
Escolha um nível para cada fator conforme a realidade do cargo.
</div>
""", unsafe_allow_html=True)

selected_levels = {}

for factor_name, factor_data in applicable_factors.items():
    with st.expander(f"📌 {factor_name}"):
        st.markdown(f"<div class='accordion-body'>{factor_data['description']}</div>", unsafe_allow_html=True)
        level = st.selectbox(
            f"Selecione o nível para: {factor_name}",
            factor_data["levels"],
            key=factor_name
        )
        selected_levels[factor_name] = level

# =============================================================================
# BOTÃO — EXECUTAR MATCH
# =============================================================================
st.markdown("<br>", unsafe_allow_html=True)
execute = st.button("🔍 Buscar Job Match")

if not execute:
    st.stop()

# =============================================================================
# EXECUTA MATCH
# =============================================================================
with st.spinner("Calculando aderência ao catálogo global SIG..."):
    match = find_best_match(selected_levels, report_to)

if not match:
    st.error("Nenhum match encontrado. Ajuste os fatores.")
    st.stop()

# =============================================================================
# RESULTADO — MOSTRAR CARGO E DESCRIÇÃO COMPLETA
# =============================================================================
matched_title = match["job_title"]
matched_description = match["description"]

st.markdown(f"""
<div class="sig-title">
    <img src="{icon_path.as_posix()}" width="22px">
    Cargo Encontrado: {matched_title}
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="sig-container">
    <h4>Descrição Completa</h4>
    <p>{matched_description}</p>
</div>
""", unsafe_allow_html=True)
