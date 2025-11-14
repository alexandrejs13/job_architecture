# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path

# ===========================================================
# CARREGAR CSS GLOBAL
# ===========================================================
assets_path = Path(__file__).parents[1] / "assets"

for css in ["fonts.css", "theme.css", "menu.css"]:
    css_file = assets_path / css
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===========================================================
# TÍTULO PRINCIPAL DA PÁGINA
# ===========================================================
st.markdown("""
<div class="page-main-title" style="
    display:flex;
    align-items:center;
    gap:18px;
    margin-top:15px;
">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png"
         style="width:75px; height:75px;">

    <h1 style="
        font-family:'PPSIGFlow';
        font-weight:600;
        font-size:26px;
        margin:0;
        padding:0;
        color:#000000;
    ">
        Job Architecture
    </h1>
</div>
""", unsafe_allow_html=True)

# ===========================================================
# INTRODUÇÃO
# ===========================================================
st.markdown("""
<div style="
    font-family:'PPSIGFlow';
    font-size:16px;
    color:#333;
    line-height:1.55;
">

A <strong>Job Architecture (JA)</strong> é o modelo corporativo que estrutura de forma integrada todas as posições da organização,
definindo agrupamento de funções, níveis de responsabilidade, critérios de progressão e diferenciais de complexidade.

Baseada na metodologia global da <strong>Willis Towers Watson (WTW)</strong>, a JA garante 
<strong>equidade interna, consistência organizacional e comparabilidade externa</strong>,
sustentando decisões estratégicas sobre estrutura, remuneração, carreira e sucessão.

Mais do que um catálogo de cargos, trata-se de uma <strong>infraestrutura de governança</strong> que conecta o desenho organizacional
à gestão de talentos, assegurando práticas claras, coerentes e orientadas por propósito.

</div>
""", unsafe_allow_html=True)

# ===========================================================
# SUBTÍTULO: PILARES
# ===========================================================
st.markdown("""
<h2 style="
    font-family:'PPSIGFlow';
    font-size:18px;
    font-weight:600;
    color:#000000;
    margin-top:40px;
">
Pilares Estruturantes
</h2>
""", unsafe_allow_html=True)

# ===========================================================
# CARDS SIG
# ===========================================================

card_style = """
background-color:#f2efeb;
padding:22px;
border-radius:18px;
border:1px solid #e5e3df;
height:100%;
"""

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="font-family:'PPSIGFlow'; font-size:18px; font-weight:600; color:#145efc;">
            Governança Global
        </div>
        <div style="font-family:'PPSIGFlow'; font-size:16px; color:#333;">
            Regras universais que asseguram comparabilidade entre países e funções,
            garantindo integridade organizacional.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="font-family:'PPSIGFlow'; font-size:18px; font-weight:600; color:#145efc;">
            Clareza de Carreira
        </div>
        <div style="font-family:'PPSIGFlow'; font-size:16px; color:#333;">
            Estrutura que define bandas e grades, orientando diferenciação de níveis,
            progressão e mobilidade.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="{card_style}">
        <div style="font-family:'PPSIGFlow'; font-size:18px; font-weight:600; color:#145efc;">
            Integração de Sistemas
        </div>
        <div style="font-family:'PPSIGFlow'; font-size:16px; color:#333;">
            Base estruturada para performance, remuneração, sucessão e benchmarking global.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===========================================================
# SUBTÍTULO: ESTRUTURA DA ARQUITETURA
# ===========================================================
st.markdown("""
<h2 style="
    font-family:'PPSIGFlow';
    font-size:18px;
    font-weight:600;
    color:#000000;
    margin-top:50px;
">
Estrutura da Arquitetura
</h2>
""", unsafe_allow_html=True)

# ===========================================================
# TABELA SIG
# ===========================================================
st.markdown("""
<table style="
    width:100%;
    border-collapse:collapse;
    margin-top:16px;
    font-family:'PPSIGFlow';
    font-size:16px;
">

<thead>
<tr style="background:#145efc; color:white;">
    <th style="padding:12px; text-align:left;">Elemento</th>
    <th style="padding:12px; text-align:left;">Propósito</th>
    <th style="padding:12px; text-align:left;">Exemplo</th>
</tr>
</thead>

<tbody style="color:#333;">

<tr>
    <td><strong>Job Family</strong></td>
    <td>Agrupa funções com competências similares.</td>
    <td>Finanças, Engenharia, RH</td>
</tr>

<tr>
    <td><strong>Sub-Job Family</strong></td>
    <td>Diferencia especializações dentro da Job Family.</td>
    <td>Contabilidade, Engenharia de Processo</td>
</tr>

<tr>
    <td><strong>Career Band</strong></td>
    <td>Nível hierárquico e escopo de influência.</td>
    <td>Profissional, Gerencial, Executivo</td>
</tr>

<tr>
    <td><strong>Global Grade</strong></td>
    <td>Diferencia complexidade e contribuição entre níveis.</td>
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

# ===========================================================
# IMPORTÂNCIA ESTRATÉGICA
# ===========================================================
st.markdown("""
<h2 style="
    font-family:'PPSIGFlow';
    font-size:18px;
    font-weight:600;
    margin-top:50px;
    color:#000000;
">
Importância Estratégica
</h2>
""", unsafe_allow_html=True)

st.markdown("""
<div style="font-family:'PPSIGFlow'; font-size:16px; line-height:1.55; color:#333; text-align:justify;">

<p>
A <strong>Job Architecture</strong> é o alicerce das práticas de <strong>Gestão de Pessoas e Governança Corporativa</strong>.
Ela fornece uma linguagem comum para estruturar, comparar e avaliar cargos, promovendo decisões justas e sustentáveis.
</p>

<p>
Com base em critérios consistentes de complexidade e contribuição, o modelo da WTW permite 
<strong>equidade interna</strong>, <strong>benchmarking de mercado</strong> e <strong>mapeamento de carreiras</strong>
de forma padronizada.
</p>

<p>
Ao integrar estrutura, remuneração e desenvolvimento, a Job Architecture fortalece a conexão entre
<strong>estratégia de negócios</strong>, <strong>desempenho organizacional</strong> e <strong>evolução profissional</strong>,
garantindo coerência global e meritocracia.
</p>

</div>
""", unsafe_allow_html=True)
