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

# Header azul com largura total do conteúdo, ícone maior e tipografia refinada
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
# 5. PILARES (CARDS ALINHADOS NA MESMA LINHA)
# ===========================================================
st.markdown("""
<style>
.pillar-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 24px;
    margin-top: 32px;
}

.pillar-card {
    background: #ffffff;
    border-radius: 14px;
    border-left: 6px solid #145efc;
    padding: 28px;
    flex: 1;
    min-width: 280px;
    max-width: 32%;
    box-shadow: 0 4px 10px rgba(0,0,0,0.06);
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
    text-align: left;
}

.pillar-text {
    color: #333333;
    font-size: 1.05rem;
    line-height: 1.55;
    text-align: justify;
    flex-grow: 1;
}

/* Mantém todos os cards com mesma altura */
.pillar-container > .pillar-card {
    display: flex;
    flex-direction: column;
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

# ===========================================================
# 6. AJUSTES VISUAIS GERAIS
# ===========================================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}

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

.stAlert {
    background-color: #eef3ff !important;
    border-left: 4px solid #145efc !important;
    color: #000 !important;
    border-radius: 6px;
}

section.main > div {
    padding-top: 10px !important;
    padding-left: 25px !important;
    padding-right: 25px !important;
}
</style>
""", unsafe_allow_html=True)
