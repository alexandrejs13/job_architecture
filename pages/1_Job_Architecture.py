# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# OCULTAR “streamlit app” DO MENU
st.markdown("""
<style>
[data-testid="stSidebarHeader"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# FIXAR LARGURA DA SIDEBAR E EVITAR REDIMENSIONAMENTO
st.markdown("""
<style>
/* Sidebar fixa */
[data-testid="stSidebar"] {
    min-width: 260px !important;
    max-width: 260px !important;
}

/* Área principal ocupa todo o resto */
.block-container {
    padding-left: 40px !important;
    padding-right: 40px !important;
    max-width: 1400px !important;
}

/* Fundo da página branco (correta) */
[data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
}

/* Sidebar SIG Sand 1 */
[data-testid="stSidebar"] {
    background-color: #f5f3f0 !important;
}

/* Ícones dos títulos */
.page-icon {
    width: 70px;
    height: 70px;
    margin-right: 12px;
}

/* Título principal */
.page-title {
    font-family: 'PPSIGFlow', sans-serif;
    font-weight: 600;
    font-size: 26px;
    margin: 0;
    padding: 0;
}

/* Subtítulos */
.section-title {
    font-family: 'PPSIGFlow', sans-serif;
    font-weight: 600;
    font-size: 18px;
    margin-top: 50px;
    margin-bottom: 12px;
}

/* Texto geral */
.section-text {
    font-family: 'PPSIGFlow', sans-serif;
    font-size: 16px;
    line-height: 1.55;
}

/* Cards originais (mantidos) */
.pillar-card {
    background-color: #f5f3f0;
    border-left: 5px solid #145efc;
    border-radius: 12px;
    padding: 22px;
    height: 100%;
}
.pillar-card-title {
    font-family: 'PPSIGFlow', sans-serif;
    font-weight: 600;
    font-size: 16px;
    color: #145efc;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# TÍTULO PRINCIPAL COM ÍCONE
# ============================================================
st.markdown("""
<div style="display:flex; align-items:center; gap:12px; margin-top:10px;">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png" class="page-icon">
    <h1 class="page-title">Job Architecture</h1>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TEXTO INTRODUTÓRIO (ORIGINAL PRESERVADO)
# ============================================================
st.markdown("""
<div class="section-text">
A <strong>Job Architecture (JA)</strong> é o modelo corporativo que organiza, de forma integrada, todas as posições da empresa — definindo 
agrupamentos de funções, níveis de responsabilidade, critérios de progressão e diferenciais de complexidade.
<br><br>
Baseada na metodologia global da <strong>Willis Towers Watson (WTW)</strong>, a JA garante <strong>equidade interna</strong>, 
<strong>consistência organizacional</strong> e <strong>comparabilidade externa</strong>, sustentando decisões estratégicas em remuneração, 
estrutura organizacional, carreiras e sucessão.
<br><br>
Mais do que um catálogo de cargos, trata-se de uma <strong>infraestrutura de governança</strong> que conecta desenho organizacional, 
pessoas e estratégia — garantindo clareza, coerência e sustentabilidade nas decisões da empresa.
</div>
""", unsafe_allow_html=True)

# ============================================================
# PILARES (ORIGINAIS, CARDS PRESERVADOS)
# ============================================================
st.markdown('<div class="section-title">Pilares Estruturantes</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="pillar-card">
        <div class="pillar-card-title">Governança Global</div>
        <div class="section-text">
            Princípios e regras universais que asseguram comparabilidade entre países, funções e níveis — garantindo integridade organizacional.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="pillar-card">
        <div class="pillar-card-title">Clareza de Carreira</div>
        <div class="section-text">
            Estrutura que define bandas, níveis e critérios de progressão, oferecendo transparência e mobilidade estruturada.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="pillar-card">
        <div class="pillar-card-title">Integração de Sistemas</div>
        <div class="section-text">
            Framework único para remuneração, avaliação de desempenho, sucessão e benchmarking global.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# ESTRUTURA DA ARQUITETURA – TABELA (FINALMENTE CORRIGIDA)
# ============================================================
st.markdown('<div class="section-title">Estrutura da Arquitetura</div>', unsafe_allow_html=True)

st.markdown("""
<table style="width:100%; border-collapse: collapse;">
<thead>
    <tr>
        <th style="border-bottom:2px solid #145efc; padding:8px; text-align:left;">Elemento</th>
        <th style="border-bottom:2px solid #145efc; padding:8px; text-align:left;">Propósito</th>
        <th style="border-bottom:2px solid #145efc; padding:8px; text-align:left;">Exemplo</th>
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
        <td>Descrição corporativa de referência para cada nível.</td>
        <td>“Finance Specialist”, “HR Manager”</td>
    </tr>
</tbody>
</table>
""", unsafe_allow_html=True)
