import streamlit as st
from utils.ui import sidebar_logo_and_title, header
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

# Container azul do tamanho do texto e ícone ampliado
st.markdown("""
<style>
    .page-header {
        background-color: #145efc;
        color: white;
        font-weight: 700;
        font-size: 1.2rem;
        border-radius: 12px;
        padding: 18px 36px;
        display: flex;
        align-items: center;
        gap: 14px;
        width: fit-content; /* largura ajusta ao conteúdo */
        margin-bottom: 35px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .page-header img {
        width: 38px;  /* ícone maior */
        height: 38px;
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
# 5. AJUSTES VISUAIS GERAIS
# ===========================================================
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #f5f3f0;
        color: #202020;
        font-family: "Source Sans Pro", "Helvetica", sans-serif;
    }

    /* Títulos menores e mais elegantes */
    h2 {
        font-weight: 700 !important;
        color: #000000 !important;
        font-size: 1.4rem !important;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
    }
    h3 {
        font-weight: 700 !important;
        color: #000000 !important;
        font-size: 1.2rem !important;
    }

    /* Caixa informativa refinada */
    .stAlert {
        background-color: #eef3ff !important;
        border-left: 4px solid #145efc !important;
        color: #000 !important;
        border-radius: 6px;
    }

    /* Ajuste de margens e alinhamento */
    section.main > div {
        padding-top: 10px !important;
        padding-left: 25px !important;
        padding-right: 25px !important;
    }
</style>
""", unsafe_allow_html=True)
