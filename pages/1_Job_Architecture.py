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
<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png" alt="icon">
  Job Architecture
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. PILARES (AQUI VEM SEU BLOCO)
# ===========================================================
st.markdown("""
<style>
.pillar-container {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    justify-content: space-between;
    align-items: stretch;
    margin-top: 20px;
}
.pillar-card {
    background: #ffffff;
    border-radius: 14px;
    border-left: 6px solid #145efc;
    padding: 26px 28px;
    flex: 1;
    min-width: 280px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
}
.pillar-title {
    font-weight: 800;
    font-size: 1.25rem;
    color: #145efc;
    margin-bottom: 12px;
}
.pillar-text {
    color: #333333;
    font-size: 1.05rem;
    line-height: 1.55;
    flex-grow: 1;
}
</style>

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
