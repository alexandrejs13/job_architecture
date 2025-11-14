# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path

# =================================================================
# CONFIGURAÇÃO DA PÁGINA
# =================================================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =================================================================
# CARREGAR CSS GLOBAL
# =================================================================
assets_path = Path(__file__).parents[1] / "assets"

for css_file in ["fonts.css", "theme.css", "layout.css"]:
    css_path = assets_path / css_file
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# =================================================================
# TÍTULO COM ICONE
# =================================================================

st.markdown("""
<div class="page-header-sig">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png">
    <span>Job Architecture — Fundamentos e Governança</span>
</div>
""", unsafe_allow_html=True)

# =================================================================
# DESCRIÇÃO INICIAL
# =================================================================

st.markdown("""
<div class="content-block">

A <strong>Job Architecture (JA)</strong> é o modelo corporativo que estrutura de forma integrada todas as posições da organização, 
definindo a lógica de agrupamento de funções, níveis de responsabilidade, critérios de progressão e diferenciais de complexidade.

Baseada na metodologia global da <strong>Willis Towers Watson (WTW)</strong>, a Job Architecture fornece um framework que garante 
<strong>equidade interna, consistência organizacional e comparabilidade externa</strong>, sustentando decisões estratégicas sobre 
estrutura, remuneração, carreira e sucessão.

Mais do que um catálogo de cargos, trata-se de uma <strong>infraestrutura de governança</strong> que conecta o desenho organizacional 
à gestão de talentos, assegurando que as práticas de gestão de pessoas sejam <strong>claras, coerentes e orientadas por propósito.</strong>

</div>
""", unsafe_allow_html=True)

# =================================================================
# PILARES ESTRUTURANTES (CARDS)
# =================================================================

st.markdown("""<h2 class="section-title">Pilares Estruturantes</h2>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="sig-card">
        <div class="sig-card-title">Governança Global</div>
        <div class="sig-card-text">
        Define princípios, critérios e regras universais para a criação, atualização e manutenção dos cargos, garantindo comparabilidade entre países, funções e níveis organizacionais.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="sig-card">
        <div class="sig-card-title">Clareza de Carreira</div>
        <div class="sig-card-text">
        Cada cargo é vinculado a um <strong>Career Band</strong> e <strong>Global Grade</strong>, oferecendo visibilidade sobre progressão, mobilidade e diferenciação de níveis.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="sig-card">
        <div class="sig-card-title">Integração de Sistemas</div>
        <div class="sig-card-text">
        Sustenta processos de Remuneração, Performance, Talent Review e Benchmarking. Garante consistência entre estruturas e governança global.
        </div>
    </div>
    """, unsafe_allow_html=True)

# =================================================================
# ESTRUTURA DA ARQUITETURA (TABELA)
# =================================================================

st.markdown("""<h2 class="section-title">Estrutura da Arquitetura</h2>""", unsafe_allow_html=True)

st.markdown("""
<div class="content-block">

A arquitetura é composta por cinco elementos integrados, formando um modelo organizacional padronizado e comparável globalmente.

<br><br>

<table class="sig-table">
    <tr>
        <th>Elemento</th>
        <th>Propósito</th>
        <th>Exemplo</th>
    </tr>

    <tr>
        <td><strong>Job Family</strong></td>
        <td>Agrupa funções com competências similares e natureza de trabalho comum.</td>
        <td>Finanças, Engenharia, RH</td>
    </tr>

    <tr>
        <td><strong>Sub-Job Family</strong></td>
        <td>Distingue especializações dentro de cada Job Family.</td>
        <td>Contabilidade, Engenharia de Processo</td>
    </tr>

    <tr>
        <td><strong>Career Band</strong></td>
        <td>Representa o nível hierárquico e escopo de influência.</td>
        <td>Profissional, Gerencial, Executivo</td>
    </tr>

    <tr>
        <td><strong>Global Grade</strong></td>
        <td>Diferencia complexidade e contribuição entre os níveis.</td>
        <td>GG07, GG09, GG12</td>
    </tr>

    <tr>
        <td><strong>Generic Profile</strong></td>
        <td>Descrição corporativa de referência do nível.</td>
        <td>“Finance Specialist”, “HR Manager”</td>
    </tr>
</table>

</div>
""", unsafe_allow_html=True)

# =================================================================
# IMPORTÂNCIA ESTRATÉGICA
# =================================================================

st.markdown("""<h2 class="section-title">Importância Estratégica</h2>""", unsafe_allow_html=True)

st.markdown("""
<div class="content-block">

<p>
A <strong>Job Architecture</strong> é o alicerce das práticas de <strong>Gestão de Pessoas e Governança Corporativa</strong>.  
Ela fornece uma linguagem comum para estruturar, comparar e avaliar cargos, promovendo decisões justas e sustentáveis.
</p>

<p>
Com base em critérios consistentes de complexidade e contribuição, o modelo da WTW permite <strong>equidade interna, benchmarking de mercado e mapeamento de carreiras</strong> de forma padronizada.
</p>

<p>
Ao integrar estrutura organizacional, remuneração e desenvolvimento, a Job Architecture fortalece a conexão entre <strong>estratégia de negócios, desempenho organizacional e evolução profissional</strong>, garantindo coerência global e meritocracia.
</p>

</div>
""", unsafe_allow_html=True)
