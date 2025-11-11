import streamlit as st
from utils.ui import sidebar_logo_and_title
from pathlib import Path

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Architecture",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. CSS GLOBAL E SIDEBAR UNIFICADA
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

# ===========================================================
# 3. CABEÇALHO AZUL PADRONIZADO
# ===========================================================
st.markdown("""
<style>
.page-header {
    background-color: #145efc;
    color: white;
    font-weight: 750;
    font-size: 1.45rem;
    border-radius: 12px;
    padding: 22px 36px;
    display: flex;
    align-items: center;
    gap: 18px;
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.page-header img {
    width: 54px;
    height: 54px;
}
.block-container {
    max-width: 1000px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}

/* ===== CORREÇÃO PARA CARTÕES DE MESMA ALTURA ===== */
/* Aplica Flexbox nas colunas do Streamlit para que os filhos (os cards) preencham 100% da altura */
[data-testid="stColumn"] {
    display: flex;
    flex-direction: column;
}
/* ================================================ */

/* ===== CARDS ===== */
.pillar-card {
    background-color: #ffffff;
    border-left: 5px solid #145efc;
    border-radius: 8px;
    padding: 22px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    height: 100%; /* Mantido para garantir que o card preencha a altura da coluna */
}
.pillar-title {
    font-weight: 700;
    color: #145efc;
    font-size: 1.05rem;
    margin-bottom: 6px;
}
.pillar-text {
    color: #333333;
    font-size: 0.98rem;
    line-height: 1.6;
}
.section-title {
    font-weight: 700;
    font-size: 1.2rem;
    color: #000000;
    margin-top: 35px;
    margin-bottom: 10px;
}
.section-text {
    font-size: 1rem;
    color: #202020;
    line-height: 1.65;
    text-align: justify;
}
.job-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}
.job-table th {
    text-align: left;
    padding: 10px;
    border-bottom: 2px solid #145efc;
    font-weight: 700;
    color: #145efc;
}
.job-table td {
    padding: 10px;
    border-bottom: 1px solid #e6e6e6;
    vertical-align: top;
    color: #333;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png" alt="icon">
    Job Architecture — Fundamentos e Governança
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. CONCEITO CENTRAL
# ===========================================================
st.markdown("""
<div class="section-text">
A <strong>Job Architecture (JA)</strong> é o sistema que organiza e estrutura todas as posições da SIG, 
definindo como agrupamos funções, níveis de responsabilidade e critérios de progressão. 
Seu propósito é garantir <strong>transparência, consistência e alinhamento global</strong> entre 
remuneração, desenvolvimento e governança organizacional.

Mais do que um catálogo de cargos, a Job Architecture é uma <strong>estrutura viva</strong> que conecta 
o desenho organizacional à estratégia de talentos, assegurando que decisões sobre estrutura e carreira 
sejam tomadas com base em princípios comuns e comparáveis.
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 5. PILARES DA ARQUITETURA
# ===========================================================
st.markdown('<div class="section-title">Pilares Estruturantes</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="pillar-card">
        <div class="pillar-title">Governança Global</div>
        <div class="pillar-text">
        Estrutura padronizada que garante coerência entre funções, níveis e critérios de decisão em toda a organização.
        </div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="pillar-card">
        <div class="pillar-title">Clareza de Carreira</div>
        <div class="pillar-text">
        Cada posição está vinculada a um Career Band e Global Grade, oferecendo visibilidade, mobilidade e previsibilidade de crescimento.
        </div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="pillar-card">
        <div class="pillar-title">Integração de Sistemas</div>
        <div class="pillar-text">
        A Job Architecture é a base para processos de remuneração, descrição de cargos, avaliação e benchmarking externo.
        </div>
    </div>
    """, unsafe_allow_html=True)

# (Restante do seu código...)
