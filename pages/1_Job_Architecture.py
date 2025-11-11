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
# 2. CSS GLOBAL E ESTRUTURA PADRÃO
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===========================================================
# 3. CABEÇALHO E SIDEBAR
# ===========================================================
sidebar_logo_and_title()

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
.block-container {
    max-width: 900px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}

/* ===== VISUAL GLOBAL ===== */
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}

/* ===== CARDS DE PILARES - ALTURA UNIFORME ===== */
.pillar-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
    gap: 25px;
    margin-top: 20px;
}
.pillar-card {
    background: #ffffff;
    border-left: 6px solid #145efc;
    border-radius: 12px;
    padding: 26px 28px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 250px; /* altura fixa uniforme */
}
.pillar-title {
    color: #145efc;
    font-weight: 800;
    font-size: 1.15rem;
    margin-bottom: 12px;
}
.pillar-text {
    color: #2e2e2e;
    font-size: 1rem;
    line-height: 1.55;
}

/* ===== ESTILO DOS TÍTULOS ===== */
h2 {
    font-weight: 700 !important;
    color: #000000 !important;
    font-size: 1.35rem !important;
    margin-top: 25px !important;
    margin-bottom: 12px !important;
}
h3 {
    font-weight: 700 !important;
    color: #000000 !important;
    font-size: 1.15rem !important;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png" alt="icon">
    Job Architecture
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. CONTEÚDO PRINCIPAL
# ===========================================================
st.markdown("""
A **Job Architecture (JA)** é a estrutura que organiza todos os cargos e posições dentro da SIG, 
definindo critérios consistentes para **classificação, progressão, remuneração e governança global**.

Sua aplicação garante alinhamento entre funções similares, transparência nos critérios de carreira 
e coerência na estrutura organizacional em todos os países onde atuamos.
""")

st.markdown("""
## Estrutura da Arquitetura de Cargos

A Job Architecture é composta por quatro elementos integrados que permitem a padronização global:
1. **Job Families** – agrupamentos amplos de funções com propósito e expertise semelhantes.  
2. **Sub Job Families** – especializações específicas dentro de cada família.  
3. **Career Levels** – níveis que refletem o escopo de responsabilidade e maturidade do papel.  
4. **Generic Profiles** – descrições corporativas de referência utilizadas globalmente.
""")

st.markdown("""
## Pilares Estruturantes
""")

st.markdown("""
<div class="pillar-grid">
    <div class="pillar-card">
        <div class="pillar-title">Governança Global</div>
        <div class="pillar-text">
            Define políticas, critérios e princípios que asseguram coerência e equidade na avaliação de cargos e níveis,
            fortalecendo a consistência da estrutura corporativa em escala global.
        </div>
    </div>
    <div class="pillar-card">
        <div class="pillar-title">Clareza de Carreira</div>
        <div class="pillar-text">
            Oferece transparência sobre trajetórias, movimentações e expectativas de desenvolvimento, 
            facilitando o entendimento sobre oportunidades e evolução profissional.
        </div>
    </div>
    <div class="pillar-card">
        <div class="pillar-title">Integração de Sistemas</div>
        <div class="pillar-text">
            Conecta os elementos de arquitetura a processos de remuneração, sucessão e desempenho, 
            promovendo sinergia entre as ferramentas e práticas de gestão de pessoas.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
## Objetivo
A Job Architecture serve como base corporativa para **remuneração, carreira e governança**.  
Seu objetivo é garantir que todas as posições SIG estejam classificadas de forma uniforme, 
promovendo decisões mais estratégicas, justas e sustentáveis.
""")

st.info("""
**Nota:**  
A Job Architecture não substitui as descrições de cargo locais — 
ela oferece uma referência global que orienta o design organizacional e a consistência entre funções.
""")
