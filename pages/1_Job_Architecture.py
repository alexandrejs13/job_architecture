# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path

# ------------------------------------------------------------
# CONFIG GLOBAL
# ------------------------------------------------------------
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# IMPORTA CSS GLOBAL
# ------------------------------------------------------------
assets_path = Path(__file__).parents[1] / "assets"

for css_file in ["fonts.css", "theme.css", "menu.css"]:
    css_path = assets_path / css_file
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ------------------------------------------------------------
# TÍTULO COM ÍCONE 2CM
# ------------------------------------------------------------
ICON_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png"

st.markdown(f"""
<div class="page-header">
    <img src="{ICON_URL}" class="page-icon">
    <span class="page-title">Job Architecture — Fundamentos e Governança</span>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# TEXTO INTrodutÓRIO
# ------------------------------------------------------------
st.markdown("""
<div class="section-text">

A <strong>Job Architecture (JA)</strong> é o modelo corporativo que estrutura de forma integrada todas as posições da organização, definindo agrupamento de funções, níveis de responsabilidade, critérios de progressão e diferenciais de complexidade.

Baseada na metodologia global da <strong>Willis Towers Watson (WTW)</strong>, a JA garante <strong>equidade interna, consistência organizacional e comparabilidade externa</strong>, sustentando decisões estratégicas sobre estrutura, remuneração, carreira e sucessão.

Mais do que um catálogo de cargos, trata-se de uma <strong>infraestrutura de governança</strong> que conecta o desenho organizacional à gestão de talentos, assegurando práticas claras, coerentes e orientadas por propósito.

</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# PILARES
# ------------------------------------------------------------

st.markdown('<h2 class="subsection-title">Pilares Estruturantes</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="pillar-card">
        <div class="pillar-title">Governança Global</div>
        <div class="pillar-text">
        Regras universais que asseguram comparabilidade entre países e funções, garantindo integridade organizacional.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="pillar-card">
        <div class="pillar-title">Clareza de Carreira</div>
        <div class="pillar-text">
        Estrutura que define bandas e grades, orientando diferenciação de níveis, progressão e mobilidade.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="pillar-card">
        <div class="pillar-title">Integração de Sistemas</div>
        <div class="pillar-text">
        Base estruturada para performance, remuneração, sucessão e benchmarking global.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
# ESTRUTURA DA ARQUITETURA – TABELA
# ------------------------------------------------------------

st.markdown("""
<h2 class="subsection-title">Estrutura da Arquitetura</h2>

<div class="section-text">
A arquitetura é composta por cinco elementos integrados, que formam um modelo padronizado e comparável globalmente.
</div>

<table class="sig-table">
    <thead>
        <tr>
            <th>Elemento</th>
            <th>Propósito</th>
            <th>Exemplo</th>
        </tr>
    </thead>

    <tbody>
        <tr>
            <td><strong>Job Family</strong></td>
            <td>Agrupa funções com competências similares.</td>
            <td>Finanças, Engenharia, RH</td>
        </tr>

        <tr>
            <td><strong>Sub-Job Family</strong></td>
            <td>Especializações dentro de cada Job Family.</td>
            <td>Contabilidade, Engenharia de Processo</td>
        </tr>

        <tr>
            <td><strong>Career Band</strong></td>
            <td>Nível hierárquico e escopo de influência.</td>
            <td>Profissional, Gerencial, Executivo</td>
        </tr>

        <tr>
            <td><strong>Global Grade</strong></td>
            <td>Diferencia complexidade entre níveis.</td>
            <td>GG07, GG09, GG12</td>
        </tr>

        <tr>
            <td><strong>Generic Profile</strong></td>
            <td>Descrição corporativa de referência por nível.</td>
            <td>“Finance Specialist”, “HR Manager”</td>
        </tr>

    </tbody>
</table>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# IMPORTÂNCIA ESTRATÉGICA
# ------------------------------------------------------------

st.markdown("""
<h2 class="subsection-title">Importância Estratégica</h2>

<div class="section-text">
A <strong>Job Architecture</strong> é o alicerce das práticas de <strong>Gestão de Pessoas e Governança Corporativa</strong>.
Fornece uma linguagem comum para estruturar, comparar e avaliar cargos, permitindo decisões justas e sustentáveis.
</div>

<div class="section-text">
O modelo WTW possibilita <strong>equidade interna</strong>, <strong>benchmarking externo</strong> e <strong>mapeamento estruturado de carreiras</strong>.
</div>

<div class="section-text">
Ao integrar estrutura, remuneração e desenvolvimento, fortalece a conexão entre <strong>estratégia de negócios</strong>,
<strong>desempenho organizacional</strong> e <strong>evolução profissional</strong>.
</div>
""", unsafe_allow_html=True)
