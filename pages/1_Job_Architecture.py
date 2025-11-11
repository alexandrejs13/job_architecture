# ===========================================================
# 1_JOB_ARCHITECTURE.PY — VISÃO GERAL CORPORATIVA
# ===========================================================

import streamlit as st
from utils.ui import sidebar_logo_and_title
from pathlib import Path

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Architecture Overview",
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
.section {
    background-color: #ffffff;
    border-left: 5px solid #145efc;
    border-radius: 10px;
    padding: 24px 30px;
    margin-bottom: 25px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}
.section h3 {
    color: #145efc;
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 10px;
}
.section p {
    font-size: 1.05rem;
    line-height: 1.6;
    color: #333333;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png" alt="icon">
    Estrutura Global de Cargos — Job Architecture
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. CONTEÚDO PRINCIPAL
# ===========================================================
st.markdown("""
A **Job Architecture (JA)** é o sistema estruturante que organiza todos os cargos e posições dentro da SIG, permitindo **clareza organizacional**, **equidade interna** e **padronização global** das funções.

Essa arquitetura é a base de referência para remuneração, desenvolvimento de carreira e gestão de talentos — garantindo que cada posição esteja alinhada à sua **contribuição estratégica** e ao **nível de complexidade** correspondente.
""")

st.markdown("""
---
""")

st.markdown("""
<div class="section">
<h3>1. Finalidade Estratégica</h3>
<p>
A Job Architecture visa construir uma estrutura corporativa coerente, que assegura que todas as posições da SIG sejam avaliadas e categorizadas de forma consistente em todas as regiões, negócios e funções.
</p>
<p>
Ela atua como um **framework global de governança de cargos**, servindo de base para políticas de remuneração, movimentações internas, sucessão e benchmarking externo.  
O objetivo central é garantir que o crescimento profissional esteja diretamente relacionado à complexidade e ao impacto organizacional das funções exercidas.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section">
<h3>2. Componentes da Arquitetura</h3>
<p>
A arquitetura é composta por quatro dimensões interconectadas que definem a estrutura organizacional da SIG:
</p>
<ul>
<li><strong>Job Families:</strong> grandes áreas funcionais que agrupam conjuntos de cargos com propósito e competências semelhantes.</li>
<li><strong>Sub-Job Families:</strong> subdivisões especializadas dentro de cada família, refletindo nichos de atuação e foco técnico.</li>
<li><strong>Career Bands:</strong> agrupamentos que refletem amplitude de responsabilidades e escopo de contribuição, servindo como referência de progressão profissional.</li>
<li><strong>Global Grades:</strong> níveis globais que asseguram comparabilidade entre funções e equidade interna na remuneração e no reconhecimento.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section">
<h3>3. Benefícios Organizacionais</h3>
<p>
A adoção de uma Job Architecture sólida proporciona uma série de benefícios estratégicos:
</p>
<ul>
<li>Facilita a <strong>transparência</strong> e a <strong>mobilidade de carreira</strong> entre áreas e geografias.</li>
<li>Promove <strong>equidade interna</strong> ao alinhar cargos com responsabilidades semelhantes em diferentes funções.</li>
<li>Fornece uma base analítica para decisões de <strong>remuneração, classificação e sucessão.</strong></li>
<li>Contribui para a <strong>eficiência organizacional</strong> e para o fortalecimento da cultura corporativa baseada em meritocracia e clareza de papéis.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section">
<h3>4. Aplicação Prática na SIG</h3>
<p>
Na prática, a Job Architecture é o ponto de partida para todas as iniciativas de gestão de pessoas na SIG.  
Ela é utilizada para:
</p>
<ul>
<li>Classificar cargos e alinhar responsabilidades a níveis corporativos padronizados;</li>
<li>Estruturar faixas salariais e políticas de remuneração de forma justa e competitiva;</li>
<li>Definir trilhas de carreira e planos de sucessão baseados em competências e performance;</li>
<li>Garantir coerência global em avaliações de cargos e decisões organizacionais.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section">
<h3>5. Princípios de Governança</h3>
<p>
A governança da Job Architecture é sustentada por critérios objetivos e mensuráveis:
</p>
<ul>
<li>Classificação de cargos baseada em <strong>escopo de responsabilidade, complexidade e impacto.</strong></li>
<li>Aplicação uniforme dos princípios de <strong>equidade e comparabilidade global.</strong></li>
<li>Revisões periódicas para assegurar <strong>alinhamento com a estratégia corporativa e o mercado.</strong></li>
<li>Gestão integrada com os processos de <strong>Compensation &amp; Benefits, Talent Management</strong> e <strong>Organizational Design.</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
---
""")

st.markdown("""
### Síntese Executiva
A Job Architecture é o pilar que garante que cada cargo na SIG tenha **propósito, proporção e reconhecimento adequados**.
Ela consolida a base sobre a qual se constroem práticas justas e sustentáveis de **remuneração, carreira e governança** —  
alinhando pessoas, estrutura e estratégia em uma visão global e integrada.
""")

# ===========================================================
# 5. AJUSTES VISUAIS FINAIS
# ===========================================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
}
ul {
    margin-left: 1.5rem;
    line-height: 1.6;
}
hr {
    margin-top: 30px;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)
