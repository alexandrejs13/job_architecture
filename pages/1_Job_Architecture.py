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
# 2. CSS GLOBAL E HEADER
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

# ===========================================================
# 3. HEADER AZUL PADRONIZADO
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
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.page-header img {
    width: 54px;
    height: 54px;
}
.block-container {
    max-width: 900px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}

/* ====== CARDS ALINHADOS ====== */
.pillar-container {
    display: flex;
    gap: 24px;
    justify-content: space-between;
    align-items: stretch;
    margin-top: 20px;
}
.pillar-card {
    flex: 1;
    background-color: #ffffff;
    border-left: 5px solid #145efc;
    border-radius: 8px;
    padding: 22px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    height: 260px; /* iguala os tamanhos */
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
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
    flex-grow: 1;
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
A **Job Architecture (JA)** é a estrutura corporativa que organiza, nivela e conecta os cargos de forma consistente em toda a organização.  
Ela serve como base para decisões estratégicas de **remuneração, carreira, governança e mobilidade interna**, garantindo clareza e equidade global.  

A implementação de uma Job Architecture sólida oferece transparência sobre como cada função se relaciona com as demais, define responsabilidades com precisão e apoia a evolução profissional de forma estruturada.
""")

st.markdown("### Pilares Estruturantes da Arquitetura de Cargos")

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

st.divider()

# ===========================================================
# 5. ESTRUTURA DA JOB ARCHITECTURE
# ===========================================================
st.markdown("""
### Estrutura da Job Architecture  
A arquitetura é composta por quatro elementos interdependentes, que permitem uma visão completa da organização de cargos:

- **Job Families:** agrupam funções por áreas de especialização.  
- **Sub-Job Families:** detalham as diferentes vertentes dentro de cada família.  
- **Career Bands e Global Grades:** classificam níveis hierárquicos e a complexidade das funções.  
- **Generic Profiles:** fornecem descrições padrão para referência global.

Cada elemento contribui para a coerência e comparabilidade entre cargos, servindo de base para decisões estruturadas de carreira, remuneração e sucessão.
""")
