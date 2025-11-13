# -*- coding: utf-8 -*-
# pages/5_Job_Match.py

import streamlit as st
import pandas as pd
from pathlib import Path
from utils.ui import sidebar_logo_and_title
import json

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Job Match (GGS)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar com logo SIG
sidebar_logo_and_title("assets/SIG_Logo_RGB_Black.png")

# ==========================================================
# TÍTULO SIG
# ==========================================================

st.markdown("""
<div class="sig-title">
    <img src="assets/icons/checkmark success.png">
    <span>Job Match (GGS)</span>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# EXPLICAÇÃO INICIAL
# ==========================================================

st.markdown("""
<div class="sig-card">
    <h3>Metodologia GGS (WTW)</h3>
    <p>
        O Job Match GGS permite identificar a descrição genérica do cargo de acordo
        com os fatores de complexidade (framework WTW). Cada fator determina o nível
        esperado de contribuição, escopo e requisitos do cargo.
    </p>
    <p>
        Basta selecionar os fatores abaixo e o sistema retornará automaticamente
        o Job Profile correspondente.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# CARREGAMENTO DAS REGRAS GGS
# ==========================================================

ggs_path = Path("data/wtw_ggs_factors.json")

if not ggs_path.exists():
    st.error("Arquivo 'wtw_ggs_factors.json' não encontrado na pasta data/")
    st.stop()

with open(ggs_path, "r", encoding="utf-8") as f:
    ggs_data = json.load(f)

# Cada fator está estruturado como dict:
# {
#   "Fator": {
#       "Níveis": { "1": "descrição", "2": "...", ... }
#   }
# }

# ==========================================================
# FORMULÁRIO GGS
# ==========================================================

st.markdown("""
<div class="sig-card">
    <h3>Selecione os Fatores de Complexidade</h3>
    <p>Cada bloco pode ser expandido para visualizar a explicação detalhada.</p>
</div>
""", unsafe_allow_html=True)

factor_selections = {}

for factor_name, factor_content in ggs_data.items():

    with st.expander(factor_name):
        st.markdown(f"<p>{factor_content.get('descricao', '')}</p>", unsafe_allow_html=True)

        levels = list(factor_content.get("niveis", {}).keys())
        labels = [
            f"Nível {lvl} – {factor_content['niveis'][lvl][:80]}..."
            for lvl in levels
        ]

        selection = st.selectbox(
            f"Selecione o nível para {factor_name}:",
            options=levels,
            format_func=lambda x: f"Nível {x} – {factor_content['niveis'][x][:80]}..."
        )

        factor_selections[factor_name] = selection

# ==========================================================
# BOTÃO DE MATCH
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

process = st.button("Buscar Job Match", type="primary")

# ==========================================================
# CÁLCULO SIMPLES DO MATCH
# ==========================================================

if process:

    st.markdown("""
    <div class="sig-card">
        <h3>Resultado do Job Match</h3>
        <p>Com base nos fatores selecionados, o sistema encontrou o Job Profile mais compatível.</p>
    </div>
    """, unsafe_allow_html=True)

    # Carregar Job Profiles
    file_path = Path("data/Job Profile.xlsx")
    if not file_path.exists():
        st.error("Arquivo 'Job Profile.xlsx' não encontrado.")
        st.stop()

    df = pd.read_excel(file_path)

    # Logika simples:
    # Somamos os níveis escolhidos → maior soma = maior complexidade → job mais alto
    soma = sum(int(v) for v in factor_selections.values())

    # Critério de exemplo (ajustável conforme necessidade)
    if soma <= 8:
        nivel = "Entry Level"
    elif soma <= 12:
        nivel = "Intermediate"
    elif soma <= 16:
        nivel = "Senior"
    else:
        nivel = "Expert"

    # Filtragem no Excel (garante compatibilidade com qualquer estrutura)
    match_df = df[df["Level"].str.contains(nivel, case=False, na=False)]

    if match_df.empty:
        st.warning("Nenhum Job Profile correspondente encontrado com base na soma dos fatores.")
    else:
        selected = match_df.iloc[0]

        st.markdown(f"""
        <div class="sig-card">
            <h3>{selected['Job Title']}</h3>
            <p><strong>Nível:</strong> {selected['Level']}</p>
        </div>
        """, unsafe_allow_html=True)

        # MOSTRAR DESCRIÇÃO COMPLETA
        st.markdown("""
        <div class="sig-card">
            <h3>Descrição Completa do Cargo</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sig-card">
            <h4>Missão</h4>
            <p>{selected.get('Job Mission', 'Não informado')}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sig-card">
            <h4>Principais Responsabilidades</h4>
            <p>{selected.get('Key Responsibilities', 'Não informado')}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sig-card">
            <h4>Competências e Requisitos</h4>
            <p>{selected.get('Qualifications', 'Não informado')}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sig-card">
            <h4>Interações</h4>
            <p>{selected.get('Interactions', 'Não informado')}</p>
        </div>
        """, unsafe_allow_html=True)
