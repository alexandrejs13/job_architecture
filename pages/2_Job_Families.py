import streamlit as st
from utils.ui import sidebar_logo_and_title
from pathlib import Path

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Families",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# ESTILOS ESTRUTURAIS PADRÕES
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===========================================================
# SIDEBAR LIMPA E CENTRALIZADA
# ===========================================================
sidebar_logo_and_title()

# ===========================================================
# CABEÇALHO AZUL PADRONIZADO (ALINHADO AO CONTEÚDO)
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
    max-width: 900px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
/* Títulos refinados */
h2 {
    font-weight: 700 !important;
    color: #000000 !important;
    font-size: 1.32rem !important;
    margin-top: 25px !important;
    margin-bottom: 12px !important;
}
h3 {
    font-weight: 700 !important;
    color: #000000 !important;
    font-size: 1.15rem !important;
}
/* Caixa informativa refinada */
.stAlert {
    background-color: #eef3ff !important;
    border-left: 4px solid #145efc !important;
    color: #000 !important;
    border-radius: 6px;
}
/* Suaviza espaçamento interno */
section.main > div {
    padding-top: 10px !important;
    padding-left: 25px !important;
    padding-right: 25px !important;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/people%20employees.png" alt="icon">
    Job Families
</div>
""", unsafe_allow_html=True)

# ===========================================================
# CONTEÚDO ORIGINAL (MANTIDO NA ÍNTEGRA)
# ===========================================================
st.markdown("""
## Conceito  
As **Job Families** agrupam funções com propósito organizacional semelhante.  
Elas servem como base para análises de remuneração, benchmarking e gestão de carreira.
""")

st.markdown("""
## Estrutura  
Cada família de cargos pode conter diversas **Sub-Job Families**, representando especializações dentro da área.
""")

st.markdown("""
## Exemplo  
- **Human Resources**  
  - Total Rewards  
  - HR Operations  
  - Talent Acquisition  
- **Finance**  
  - Accounting  
  - FP&A  
  - Treasury
""")

st.info("""
**Importante:**  
Cada Job Family reflete uma função corporativa, mas pode abranger múltiplas especializações, conforme a complexidade da operação local ou global.
""")
