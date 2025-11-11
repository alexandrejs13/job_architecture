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
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}

/* ===== Pilares ===== */
.pillar-container {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    align-items: stretch; /* 🔹 garante altura igual */
    flex-wrap: wrap;
    margin-top: 30px;
}

.pillar-card {
    background: #ffffff;
    border-radius: 12px;
    border-left: 6px solid #145efc;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
    flex: 1;
    min-width: 260px;
    padding: 24px 28px;
    display: flex;
    flex-direction: column;
    justify-content: space-between; /* 🔹 força uniformidade */
    height: 100%;
}

.pillar-title {
    font-weight: 800;
    font-size: 1.2rem;
    color: #145efc;
    margin-bottom: 10px;
}

.pillar-text {
    color: #333333;
    font-size: 1.05rem;
    line-height: 1.55;
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
## Introdução  
A **Job Architecture (JA)** é a base que estrutura e nivela cargos na SIG, promovendo clareza, consistência e equidade global.
""")

st.markdown("""
## Estrutura  
A arquitetura é composta por quatro elementos principais:

1. **Job Families:** grandes grupos funcionais.  
2. **Sub-Job Families:** especializações dentro das famílias.  
3. **Career Levels:** níveis de senioridade e foco do papel.  
4. **Generic Profiles:** descrições padronizadas usadas em todo o mundo.
""")

st.markdown("""
## Objetivo  
Garantir que todas as posições SIG estejam classificadas de forma uniforme, servindo de base para remuneração, carreira e governança.
""")

st.info("""
**Importante:**  
A Job Architecture não substitui as descrições de cargo locais — ela fornece a referência corporativa para estrutura e avaliação.
""")

# ===========================================================
# 5. PILARES ESTRUTURANTES
# ===========================================================
st.markdown("""
## Pilares Estruturantes

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
