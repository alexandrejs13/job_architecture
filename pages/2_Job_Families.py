import streamlit as st
from utils.ui import sidebar_logo_and_title
from pathlib import Path

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(page_title="Job Families", layout="wide", initial_sidebar_state="expanded")

css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

# ===========================================================
# CABEÇALHO AZUL COM ÍCONE E TÍTULO
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
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
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
h2 {
    font-weight: 700 !important;
    color: #000 !important;
    font-size: 1.35rem !important;
    margin-top: 25px !important;
    margin-bottom: 12px !important;
}
h3 {
    font-weight: 700 !important;
    color: #000 !important;
    font-size: 1.15rem !important;
}
.stAlert {
    background-color: #eef3ff !important;
    border-left: 4px solid #145efc !important;
    color: #000 !important;
    border-radius: 6px;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/people%20employees.png" alt="icon">
    Job Families
</div>
""", unsafe_allow_html=True)

# ===========================================================
# CONTEÚDO
# ===========================================================
st.markdown("""
## Conceito  
As **Job Families** agrupam funções com propósito organizacional semelhante.  
Elas servem como base para análises de remuneração, benchmarking e gestão de carreira.

## Estrutura  
Cada família de cargos pode conter diversas **Sub-Job Families**, representando especializações dentro da área.

## Exemplo  
- Human Resources  
  - Total Rewards  
  - HR Operations  
  - Talent Acquisition  
- Finance  
  - Accounting  
  - FP&A  
  - Treasury
""")
