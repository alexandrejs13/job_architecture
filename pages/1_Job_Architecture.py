import streamlit as st
from utils.ui import sidebar_logo_and_title
from pathlib import Path

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Architecture",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. CSS GLOBAL E SIDEBAR
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
    max-width: 1100px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
/* ======== CARDS DE PILARES ======== */
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
    justify-content: flex-start;
    min-height: 230px;
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
h2 {
    font-weight: 750 !important;
    color: #000 !important;
    margin-top: 40px !important;
    margin-bottom: 10px !important;
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
A **Job Architecture (JA)** é a base que estrutura e nivela cargos na SIG, garantindo **clareza, consistência e equidade global**.  
Ela define a lógica que conecta funções, níveis, responsabilidades e remuneração em uma estrutura corporativa única.

---

## Pilares Estruturantes
""")

# ===========================================================
# 5. CARDS DOS PILARES
# ===========================================================
st.markdown("""
<div class="pillar-grid">

    <div class="pillar-card">
        <div class="pillar-title">Governança Global</div>
        <div class="pillar-text">
            Estrutura padronizada que garante coerência entre funções, níveis e critérios de decisão em toda a organização.
        </div>
    </div>

    <div class="pillar-card">
        <div class="pillar-title">Clareza de Carreira</div>
        <div class="pillar-text">
            Cada posição está vinculada a um Career Band e Global Grade, oferecendo visibilidade, mobilidade e previsibilidade de crescimento.
        </div>
    </div>

    <div class="pillar-card">
        <div class="pillar-title">Integração de Sistemas</div>
        <div class="pillar-text">
            A Job Architecture é a base para processos de remuneração, descrição de cargos, avaliação e benchmarking externo.
        </div>
    </div>

</div>
""", unsafe_allow_html=True)

# ===========================================================
# 6. SEÇÃO DE ESTRUTURA
# ===========================================================
st.markdown("""
## Estrutura da Arquitetura

A arquitetura é composta por quatro elementos principais:

1. **Job Families** — Grandes grupos funcionais que organizam áreas de conhecimento.  
2. **Sub-Job Families** — Especializações dentro das famílias.  
3. **Career Levels** — Diferenciação por senioridade, complexidade e escopo.  
4. **Generic Profiles** — Modelos de referência para descrições de cargos.

---

## Objetivo da Job Architecture
Garantir que todas as posições da SIG estejam classificadas de forma uniforme, servindo como base para:

- Estrutura e governança de cargos;  
- Políticas de remuneração e mobilidade;  
- Desenvolvimento e planejamento de carreira.  

""")
# ===========================================================
# 7. NOTA FINAL
# ===========================================================
st.info("""
**Importante:**  
A Job Architecture não substitui as descrições de cargo locais — ela fornece a referência corporativa
para estrutura, consistência e avaliação global.
""")
