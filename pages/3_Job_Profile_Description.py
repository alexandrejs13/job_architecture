# -*- coding: utf-8 -*-
# pages/3_Job_Profile_Description.py

import streamlit as st
import pandas as pd
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Job Profile Description",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logo SIG no topo da sidebar
sidebar_logo_and_title("assets/SIG_Logo_RGB_Black.png")

# ==========================================================
# TÍTULO SIG
# ==========================================================

st.markdown("""
<div class="sig-title">
    <img src="assets/icons/business review clipboard.png">
    <span>Job Profile Description</span>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# CARREGAMENTO DO ARQUIVO
# ==========================================================

file_path = Path("data/Job Profile.xlsx")

if not file_path.exists():
    st.error("Arquivo 'Job Profile.xlsx' não encontrado na pasta data/")
    st.stop()

df = pd.read_excel(file_path)

# ==========================================================
# SELEÇÃO DO CARGO
# ==========================================================

st.markdown("""
<div class="sig-card">
    <h3>Selecione o Cargo</h3>
    <p>Escolha um cargo para visualizar sua descrição completa, incluindo:</p>
    <ul>
        <li>Missão do Cargo</li>
        <li>Principais Responsabilidades</li>
        <li>Requisitos e Competências</li>
        <li>Qualificações</li>
        <li>Interações internas e externas</li>
    </ul>
</div>
""", unsafe_allow_html=True)

job_list = df["Job Title"].dropna().unique()
selected_job = st.selectbox("Escolha o cargo:", job_list)

if selected_job:
    job_data = df[df["Job Title"] == selected_job].iloc[0]

    # ==========================================================
    # MISSÃO DO CARGO
    # ==========================================================

    st.markdown("""
    <div class="sig-card">
        <h3>Missão do Cargo</h3>
        <p>{}</p>
    </div>
    """.format(job_data.get("Job Mission", "Informação não cadastrada")), unsafe_allow_html=True)

    # ==========================================================
    # PRINCIPAIS RESPONSABILIDADES
    # ==========================================================

    st.markdown("""
    <div class="sig-card">
        <h3>Principais Responsabilidades</h3>
        <p>{}</p>
    </div>
    """.format(job_data.get("Key Responsibilities", "Informação não cadastrada")), unsafe_allow_html=True)

    # ==========================================================
    # QUALIFICAÇÕES / COMPETÊNCIAS
    # ==========================================================

    st.markdown("""
    <div class="sig-card">
        <h3>Competências e Requisitos</h3>
        <p>{}</p>
    </div>
    """.format(job_data.get("Qualifications", "Informação não cadastrada")), unsafe_allow_html=True)

    # ==========================================================
    # INTERAÇÕES
    # ==========================================================

    st.markdown("""
    <div class="sig-card">
        <h3>Interações Internas e Externas</h3>
        <p>{}</p>
    </div>
    """.format(job_data.get("Interactions", "Informação não cadastrada")), unsafe_allow_html=True)

# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("""
<div class="sig-card">
    <p style="font-size:14px; color:#666;">
        Continue navegando para visualizar Job Maps, Job Match (GGS)
        e a Estrutura de Níveis Organizacionais.
    </p>
</div>
""", unsafe_allow_html=True)
