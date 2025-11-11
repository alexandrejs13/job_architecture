import streamlit as st
from utils.ui import sidebar_logo_and_title
from pathlib import Path

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. ESTILOS E ESTRUTURA PADRÃO
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===========================================================
# 3. CABEÇALHO E SIDEBAR
# ===========================================================
sidebar_logo_and_title()

# ===========================================================
# 4. HEADER PADRÃO
# ===========================================================
st.markdown("""
<style>
.page-header {
    background-color: #145efc;
    color: white;
    font-weight: 750;
    font-size: 1.35rem;
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
    width: 48px;
    height: 48px;
}

/* Centralização e espaçamento geral */
.block-container {
    max-width: 1000px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}

/* Cards dos Pilares Estruturantes */
.pillar-container {
    display: flex;
    gap: 20px;
    justify-content: space-between;
    align-items: stretch;  /* garante mesma altura */
    margin-top: 30px;
}

.pillar-card {
    background: #ffffff;
    border-radius: 10px;
    border-left: 5px solid #145efc;
    padding: 20px;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;  /* garante alinhamento */
    box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    min-height: 220px; /* força altura uniforme */
    transition: all 0.2s ease-in-out;
}
.pillar-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.1);
}

.pillar-title {
    font-weight: 750;
    font-size: 1.05rem;
    color: #145efc;
    margin-bottom: 8px;
}
.pillar-text {
    color: #333333;
    font-size: 0.95rem;
    line-height: 1.55;
    flex-grow: 1;
}

/* Fundo da página */
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png" alt="icon">
    Job Architecture
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 5. CONTEÚDO PRINCIPAL
# ===========================================================
st.markdown("""
A **Job Architecture (JA)** é a estrutura que organiza e padroniza os cargos na SIG, promovendo clareza, consistência e equidade global.

## Pilares Estruturantes
""", unsafe_allow_html=True)

# ===========================================================
# 6. CARDS DOS PILARES (ALTURA IGUAL)
# ===========================================================
st.markdown("""
<div class="pillar-container">

    <div class="pillar-card">
        <div class="pillar-title">Governança Global</div>
        <div class="pillar-text">
            Define princípios corporativos e metodologias comuns para classificação, avaliação e manutenção de cargos. 
            Garante consistência e integridade das informações em todos os níveis da organização.
        </div>
    </div>

    <div class="pillar-card">
        <div class="pillar-title">Clareza de Carreira</div>
        <div class="pillar-text">
            Proporciona visibilidade sobre caminhos de crescimento e evolução profissional, 
            facilitando a mobilidade interna e o desenvolvimento de talentos.
        </div>
    </div>

    <div class="pillar-card">
        <div class="pillar-title">Integração de Sistemas</div>
        <div class="pillar-text">
            Alinha a estrutura de cargos aos sistemas corporativos de RH e gestão, 
            assegurando que os dados fluam de forma integrada e suportem decisões estratégicas.
        </div>
    </div>

</div>
""", unsafe_allow_html=True)

# ===========================================================
# 7. RODAPÉ OU OBSERVAÇÕES
# ===========================================================
st.info("""
A Job Architecture não substitui as descrições de cargo locais — ela fornece a referência corporativa
para estrutura e avaliação.
""")
