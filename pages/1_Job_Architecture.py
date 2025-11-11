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

# Header azul padronizado
st.markdown("""
<style>
.page-header {
    background-color: #145efc;
    color: white;
    font-weight: 750;
    font-size: 1.4rem;
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
    max-width: 950px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}

/* ===== CARDS DE PILARES ===== */
.pillar-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
    gap: 25px;
    margin-top: 20px;
}
.pillar-card {
    background-color: #ffffff;
    border-left: 6px solid #145efc;
    border-radius: 12px;
    padding: 26px 28px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    height: 260px; /* altura fixa igual para todos */
}
.pillar-title {
    color: #145efc;
    font-weight: 800;
    font-size: 1.1rem;
    margin-bottom: 10px;
}
.pillar-text {
    color: #2e2e2e;
    font-size: 1rem;
    line-height: 1.55;
}

/* Ajuste de espaçamento entre seções */
section.main > div {
    padding-top: 10px !important;
    padding-left: 25px !important;
    padding-right: 25px !important;
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

# ===========================================================
# 5. PILARES EM CARDS
# ===========================================================
st.markdown("""
<div class="pillar-grid">
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
            Proporciona visibilidade sobre caminhos de crescimento profissional, 
            facilitando a mobilidade interna e o desenvolvimento de talentos com base em competências e níveis de responsabilidade.
        </div>
    </div>

    <div class="pillar-card">
        <div class="pillar-title">Integração de Sistemas</div>
        <div class="pillar-text">
            Alinha a estrutura de cargos aos sistemas de RH, remuneração e performance, 
            assegurando que os dados fluam de forma precisa e atualizada em toda a jornada do colaborador.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===========================================================
# 6. SEÇÃO EXPLICATIVA
# ===========================================================
st.markdown("""
### Estrutura da Job Architecture

A arquitetura é composta por quatro elementos interdependentes, que permitem uma visão completa da organização de cargos:

- **Job Families:** agrupam funções por áreas de especialização.
- **Sub-Job Families:** detalham as diferentes vertentes dentro de cada família.
- **Career Bands e Global Grades:** classificam níveis hierárquicos e complexidade das funções.
- **Generic Profiles:** fornecem descrições padrão para referência global.

Cada elemento contribui para a coerência e comparabilidade entre cargos, servindo de base para decisões estratégicas de remuneração, sucessão e mobilidade.
""")

st.markdown("""
### Benefícios de uma Arquitetura Estruturada

Uma Job Architecture robusta apoia o crescimento sustentável da organização, ao mesmo tempo em que promove:

- **Transparência e Equidade:** assegura critérios claros para avaliação e progressão de cargos.  
- **Alinhamento Estratégico:** conecta a estrutura de cargos aos objetivos do negócio.  
- **Eficiência Operacional:** simplifica processos e elimina redundâncias nas estruturas de funções.  
- **Engajamento e Retenção:** fornece um panorama de carreira claro e consistente para os colaboradores.
""")

st.markdown("""
### Conclusão

A Job Architecture é um instrumento essencial de governança organizacional.  
Ela harmoniza a gestão de cargos em escala global, sustenta políticas de remuneração coerentes e fortalece a experiência do colaborador por meio da clareza e do reconhecimento das trajetórias profissionais.
""")
