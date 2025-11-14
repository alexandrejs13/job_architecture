# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# CARREGAR CSS GLOBAL (fonts, theme, menu)
# ===========================================================
assets_path = Path(__file__).parents[1] / "assets"
css_files = ["fonts.css", "theme.css", "menu.css"]

for css_name in css_files:
    css_path = assets_path / css_name
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===========================================================
# TÍTULO PRINCIPAL — ÍCONE 2×2 cm + 26px
# ===========================================================
st.markdown("""
<div class="sig-title-wrapper">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png"
         class="sig-title-icon">
    <h1 class="sig-title">Job Architecture</h1>
</div>
""", unsafe_allow_html=True)

# ===========================================================
# INTRODUÇÃO
# ===========================================================
st.markdown("""
<p class="sig-text">
A <strong>Job Architecture (JA)</strong> é o modelo corporativo que organiza,
de forma integrada, todas as posições da empresa — definindo agrupamentos de funções,
níveis de responsabilidade, critérios de progressão e diferenciais de complexidade.
</p>

<p class="sig-text">
Baseada na metodologia global da <strong>Willis Towers Watson (WTW)</strong>,
a JA garante <strong>equidade interna</strong>, <strong>consistência organizacional</strong>
e <strong>comparabilidade externa</strong>, sustentando decisões estratégicas em remuneração,
estrutura organizacional, carreiras e sucessão.
</p>

<p class="sig-text">
Mais do que um catálogo de cargos, trata-se de uma <strong>infraestrutura de governança</strong>,
que conecta desenho organizacional, pessoas e estratégia — garantindo clareza,
coerência e sustentabilidade nas decisões da empresa.
</p>
""", unsafe_allow_html=True)

# ===========================================================
# PILARES ESTRUTURANTES (3 CARDS)
# ===========================================================
st.markdown('<div class="sig-subtitle">Pilares Estruturantes</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="sig-card">
        <div class="sig-card-title">Governança Global</div>
        <p class="sig-text" style="margin-bottom:0;">
            Princípios e regras universais que asseguram comparabilidade
            entre países, funções e níveis — garantindo integridade organizacional.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="sig-card">
        <div class="sig-card-title">Clareza de Carreira</div>
        <p class="sig-text" style="margin-bottom:0;">
            Estrutura que define bandas, níveis e critérios de progressão,
            oferecendo transparência e mobilidade estruturada para colaboradores.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="sig-card">
        <div class="sig-card-title">Integração de Sistemas</div>
        <p class="sig-text" style="margin-bottom:0;">
            Framework único para remuneração, avaliação de desempenho,
            sucessão, talent review e benchmarking global.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===========================================================
# ESTRUTURA DA ARQUITETURA — TABELA SIG
# ===========================================================
st.markdown('<div class="sig-subtitle">Estrutura da Arquitetura</div>', unsafe_allow_html=True)

st.markdown("""
<p class="sig-text">
A arquitetura é composta por cinco elementos integrados,
definindo uma estrutura organizacional padronizada e comparável globalmente:
</p>
""", unsafe_allow_html=True)

st.markdown("""
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
            <td>Agrupa funções com competências similares e natureza comum.</td>
            <td>Finanças, Engenharia, RH</td>
        </tr>

        <tr>
            <td><strong>Sub-Job Family</strong></td>
            <td>Especializações específicas dentro de cada Job Family.</td>
            <td>Contabilidade, Engenharia de Processo</td>
        </tr>

        <tr>
            <td><strong>Career Band</strong></td>
            <td>Representa o escopo hierárquico e a amplitude de impacto.</td>
            <td>Profissional, Gerencial, Executivo</td>
        </tr>

        <tr>
            <td><strong>Global Grade</strong></td>
            <td>Nível de complexidade, contribuição e responsabilidade.</td>
            <td>GG07, GG09, GG12</td>
        </tr>

        <tr>
            <td><strong>Generic Profile</strong></td>
            <td>Descrição corporativa de referência para cada nível.</td>
            <td>“Finance Specialist”, “HR Manager”</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

# ===========================================================
# IMPORTÂNCIA ESTRATÉGICA
# ===========================================================
st.markdown('<div class="sig-subtitle">Importância Estratégica</div>', unsafe_allow_html=True)

st.markdown("""
<p class="sig-text">
A <strong>Job Architecture</strong> é o alicerce da governança de pessoas, sustentando práticas
de remuneração, carreira, estrutura organizacional e processos globais de talento.
</p>

<p class="sig-text">
Ela permite análises de equidade interna, benchmarking de mercado e evolução profissional,
garantindo que as decisões sejam consistentes, imparciais e alinhadas à estratégia da empresa.
</p>

<p class="sig-text">
Ao integrar desenho organizacional, remuneração e desenvolvimento, a JA fortalece
a conexão entre <strong>estratégia de negócios</strong> e <strong>desempenho organizacional</strong>,
promovendo meritocracia e sustentabilidade.
</p>
""", unsafe_allow_html=True)
