# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path

# ===========================================================
# CARREGAR CSS GLOBAL (fonts, theme, menu)
# ===========================================================
assets_path = Path(__file__).parents[1] / "assets"

# Carregamento de todos os arquivos CSS, assegurando que o fonts.css seja carregado
# no início (embora a ordem não seja estritamente necessária, é boa prática).
for css in ["fonts.css", "theme.css", "menu.css", "layout.css", "header.css", "styles.css"]:
    css_file = assets_path / css
    if css_file.exists():
        with open(css_file) as f:
            # O st.markdown é a maneira correta de injetar o CSS no Streamlit
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===========================================================
# TÍTULO PRINCIPAL — Job Architecture (USANDO CLASSES CORRETAS)
# ===========================================================
st.markdown("""
<div class="sig-title-wrapper">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png"
         class="sig-title-icon">

    <h1 class="sig-title">
        Job Architecture
    </h1>
</div>
""", unsafe_allow_html=True)

# ===========================================================
# INTRODUÇÃO
# ===========================================================
st.markdown("""
<div class="sig-text" style="margin-bottom:30px;">

A <strong>Job Architecture (JA)</strong> é o modelo corporativo que organiza, de forma integrada, todas as posições da empresa —
definindo agrupamentos de funções, níveis de responsabilidade, critérios de progressão e diferenciais de complexidade.

Baseada na metodologia global da <strong>Willis Towers Watson (WTW)</strong>, a JA garante
<strong>equidade interna, consistência organizacional e comparabilidade externa</strong>,
dando sustentação às decisões estratégicas relacionadas à estrutura organizacional, remuneração, carreira e sucessão.

Mais do que um catálogo de cargos, trata-se de uma <strong>infraestrutura de governança</strong> que conecta desenho organizacional,
pessoas e estratégia — garantindo clareza, coerência e sustentabilidade nas decisões da empresa.

</div>
""", unsafe_allow_html=True)

# ===========================================================
# SUBTÍTULO — PILARES
# ===========================================================
st.markdown("""
<h2 class="sig-subtitle" style="margin-top:35px;">
Pilares Estruturantes
</h2>
""", unsafe_allow_html=True)

# ===========================================================
# CARDS SIG — cor SIG Sand 1
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
        <div class="sig-subtitle" style="font-size:18px; color:#145efc; margin-bottom:8px;">
            Governança Global
        </div>
        <div class="sig-text" style="font-size:16px; color:#333;">
            Princípios e regras universais que asseguram comparabilidade entre países,
            funções e níveis — garantindo integridade organizacional.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="{card_style}">
        <div class="sig-subtitle" style="font-size:18px; color:#145efc; margin-bottom:8px;">
            Clareza de Carreira
        </div>
        <div class="sig-text" style="font-size:16px; color:#333;">
            Estrutura que define bandas, níveis e critérios de progressão,
            oferecendo transparência e mobilidade estruturada.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="{card_style}">
        <div class="sig-subtitle" style="font-size:18px; color:#145efc; margin-bottom:8px;">
            Integração de Sistemas
        </div>
        <div class="sig-text" style="font-size:16px; color:#333;">
            Base única para remuneração, avaliação de desempenho, sucessão,
            talent review e benchmarking global.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===========================================================
# SUBTÍTULO — ESTRUTURA
# ===========================================================
st.markdown("""
<h2 class="sig-subtitle" style="margin-top:50px;">
Estrutura da Arquitetura
</h2>
""", unsafe_allow_html=True)

# ===========================================================
# TABELA SIG FINAL
# ===========================================================
st.markdown("""
<table class="sig-table" style="
    font-family:'PPSIGFlow';
    font-size:16px;
    color:#333;
">

<thead>
<tr style="background:#145efc; color:white;">
    <th style="padding:12px; text-align:left;">Elemento</th>
    <th style="padding:12px; text-align:left;">Propósito</th>
    <th style="padding:12px; text-align:left;">Exemplo</th>
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
    <td>Representa o escopo hierárquico e amplitude de impacto.</td>
    <td>Profissional, Gerencial, Executivo</td>
</tr>

<tr>
    <td><strong>Global Grade</strong></td>
    <td>Nível de complexidade, contribuição e responsabilidade.</td>
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
<h2 class="sig-subtitle" style="margin-top:50px;">
Importância Estratégica
</h2>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sig-text" style="text-align:justify;">

<p>
A <strong>Job Architecture</strong> é o alicerce das práticas de <strong>Gestão de Pessoas</strong> e
<strong>Governança Corporativa</strong>, promovendo decisões alinhadas, justas e sustentáveis.
</p>

<p>
Com base em critérios consistentes, o modelo permite <strong>equidade interna</strong>,
<strong>benchmarking de mercado</strong> e <strong>mapeamento estruturado de carreiras</strong>.
</p>

<p>
Ao integrar estrutura organizacional, remuneração e desenvolvimento, a Job Architecture
fortalece a conexão entre <strong>estratégia de negócios</strong>, <strong>desempenho organizacional</strong>
e <strong>evolução profissional</strong>, assegurando coerência e meritocracia.
</p>

</div>
""", unsafe_allow_html=True)
