# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path

# ===========================================================
# CONFIGURAÇÃO GLOBAL
# ===========================================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CARREGAR CSS
assets = Path(__file__).parents[1] / "assets"

for css_file in ["fonts.css", "menu.css", "theme.css"]:
    path = assets / css_file
    if path.exists():
        with open(path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===========================================================
# 1) TÍTULO PRINCIPAL COM ÍCONE — FORMATO SIG
# ===========================================================

st.markdown(f"""
<div style="
    display:flex;
    align-items:center;
    gap:20px;
    margin-top:10px;
    margin-bottom:30px;
">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png"
         style="width:75px; height:75px; opacity:0.90;">

    <h1 style="
        font-family:'PPSIGFlow';
        font-weight:600;
        font-size:26px;
        margin:0;
        padding:0;
        color:#000000;
    ">
        Job Architecture — Fundamentos e Governança
    </h1>
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 2) DESCRIÇÃO INICIAL
# ===========================================================
st.markdown("""
<div style="
    font-family:'PPSIGFlow';
    font-size:16px;
    line-height:1.55;
    color:#333;
">
A <strong>Job Architecture (JA)</strong> é o modelo corporativo que estrutura de forma integrada todas as posições da organização,
definindo agrupamento de funções, níveis de responsabilidade, critérios de progressão e diferenciais de complexidade.

Baseada na metodologia global da <strong>Willis Towers Watson (WTW)</strong>, a JA garante 
<strong>equidade interna, consistência organizacional e comparabilidade externa</strong>, 
sustentando decisões estratégicas sobre estrutura, remuneração, carreira e sucessão.

Mais do que um catálogo de cargos, trata-se de uma <strong>infraestrutura de governança</strong> que conecta o desenho organizacional à gestão de talentos,
assegurando práticas claras, coerentes e orientadas por propósito.
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 3) SUBTÍTULO: PILARES ESTRUTURANTES
# ===========================================================
st.markdown("""
<h2 style="
    font-family:'PPSIGFlow';
    font-size:21px;
    font-weight:600;
    margin-top:45px;
    color:#000;
">Pilares Estruturantes</h2>
""", unsafe_allow_html=True)

# ===========================================================
# 4) CARDS (3 COLUNAS) — SIG SAND 1
# ===========================================================
card_style = """
background-color:#f2f0ed;
padding:22px;
border-radius:18px;
height:100%;
border-left:5px solid #145efc;
"""

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="{card_style}">
        <h3 style="font-family:'PPSIGFlow'; font-size:18px; font-weight:600; color:#145efc;">
            Governança Global
        </h3>
        <p style="font-family:'PPSIGFlow'; font-size:16px; color:#333;">
            Regras universais que asseguram comparabilidade entre países e funções,
            garantindo integridade organizacional.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="{card_style}">
        <h3 style="font-family:'PPSIGFlow'; font-size:18px; font-weight:600; color:#145efc;">
            Clareza de Carreira
        </h3>
        <p style="font-family:'PPSIGFlow'; font-size:16px; color:#333;">
            Estrutura que define bandas e grades, orientando diferenciação de níveis,
            progressão e mobilidade.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="{card_style}">
        <h3 style="font-family:'PPSIGFlow'; font-size:18px; font-weight:600; color:#145efc;">
            Integração de Sistemas
        </h3>
        <p style="font-family:'PPSIGFlow'; font-size:16px; color:#333;">
            Base estruturada para performance, remuneração, sucessão e benchmarking global.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===========================================================
# 5) SUBTÍTULO: ESTRUTURA DA ARQUITETURA
# ===========================================================
st.markdown("""
<h2 style="
    font-family:'PPSIGFlow';
    font-size:21px;
    font-weight:600;
    margin-top:55px;
    color:#000;
">Estrutura da Arquitetura</h2>
""", unsafe_allow_html=True)

# ===========================================================
# 6) TABELA CORRIGIDA (AGORA FUNCIONA)
# ===========================================================

st.markdown("""
<table style="width:100%; border-collapse:collapse; margin-top:20px;">

<tr style="background:#145efc; color:white;">
    <th style="padding:12px; text-align:left; font-family:'PPSIGFlow'; font-size:18px;">Elemento</th>
    <th style="padding:12px; text-align:left; font-family:'PPSIGFlow'; font-size:18px;">Propósito</th>
    <th style="padding:12px; text-align:left; font-family:'PPSIGFlow'; font-size:18px;">Exemplo</th>
</tr>

<tr><td><strong>Job Family</strong></td>
<td>Agrupa funções com competências semelhantes.</td>
<td>Finanças, Engenharia, RH</td>
</tr>

<tr><td><strong>Sub-Job Family</strong></td>
<td>Diferencia especializações dentro de cada Job Family.</td>
<td>Contabilidade, Engenharia de Processo</td>
</tr>

<tr><td><strong>Career Band</strong></td>
<td>Representa hierarquia e escopo de influência.</td>
<td>Profissional, Gerencial, Executivo</td>
</tr>

<tr><td><strong>Global Grade</strong></td>
<td>Diferencia complexidade e contribuição.</td>
<td>GG07, GG09, GG12</td>
</tr>

<tr><td><strong>Generic Profile</strong></td>
<td>Descrição corporativa essencial.</td>
<td>“Finance Specialist”, “HR Manager”</td>
</tr>

</table>
""", unsafe_allow_html=True)
