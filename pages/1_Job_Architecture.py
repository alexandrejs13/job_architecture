import streamlit as st
from utils.ui import sidebar_logo_and_title
from pathlib import Path

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Architecture",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. CSS GLOBAL E SIDEBAR UNIFICADA
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
    max-width: 1000px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}

/* ===== PILARES ===== */
.pillar-row {
    display: flex;
    justify-content: space-between;
    align-items: stretch;
    gap: 20px;
    margin-top: 10px;
}
.pillar-card {
    background-color: #ffffff;
    border-left: 5px solid #145efc;
    border-radius: 10px;
    padding: 22px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    min-height: 280px; /* altura uniforme */
    transition: all 0.2s ease-in-out;
}
.pillar-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.08);
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

/* ===== SEÇÕES ===== */
.section-title {
    font-weight: 700;
    font-size: 1.2rem;
    color: #000000;
    margin-top: 35px;
    margin-bottom: 10px;
}
.section-text {
    font-size: 1rem;
    color: #202020;
    line-height: 1.65;
    text-align: justify;
}
.job-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}
.job-table th {
    text-align: left;
    padding: 10px;
    border-bottom: 2px solid #145efc;
    font-weight: 700;
    color: #145efc;
}
.job-table td {
    padding: 10px;
    border-bottom: 1px solid #e6e6e6;
    vertical-align: top;
    color: #333;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png" alt="icon">
    Job Architecture — Fundamentos e Governança
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. CONCEITO CENTRAL
# ===========================================================
st.markdown("""
<div class="section-text">
A <strong>Job Architecture (JA)</strong> é o modelo corporativo que estrutura de forma integrada todas as posições da organização, 
definindo a lógica de agrupamento de funções, níveis de responsabilidade, critérios de progressão e diferenciais de complexidade.  

Baseada na metodologia global da <strong>Willis Towers Watson (WTW)</strong>, a Job Architecture fornece um framework que garante 
<strong>equidade interna, consistência organizacional e comparabilidade externa</strong>, sustentando decisões estratégicas sobre 
estrutura, remuneração, carreira e sucessão.  

Mais do que um catálogo de cargos, trata-se de uma <strong>infraestrutura de governança</strong> que conecta o desenho organizacional 
à gestão de talentos, assegurando que as práticas de gestão de pessoas sejam <strong>claras, coerentes e orientadas por propósito.</strong>
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 5. PILARES DA ARQUITETURA
# ===========================================================
st.markdown('<div class="section-title">Pilares Estruturantes</div>', unsafe_allow_html=True)
st.markdown("""
<div class="pillar-row">
    <div class="pillar-card">
        <div class="pillar-title">Governança Global</div>
        <div class="pillar-text">
        Define princípios, critérios e regras universais para a criação, atualização e manutenção dos cargos, garantindo comparabilidade entre países, funções e níveis organizacionais. 
        Essa governança assegura que toda posição seja avaliada de acordo com padrões globais e práticas de mercado reconhecidas.
        </div>
    </div>

    <div class="pillar-card">
        <div class="pillar-title">Clareza de Carreira</div>
        <div class="pillar-text">
        Cada cargo é vinculado a um <strong>Career Band</strong> e <strong>Global Grade</strong>, refletindo o escopo de atuação, 
        o grau de autonomia e a natureza da contribuição.  
        Essa estrutura fornece visibilidade sobre oportunidades de progressão, diferenciação de níveis e mobilidade lateral entre áreas.
        </div>
    </div>

    <div class="pillar-card">
        <div class="pillar-title">Integração de Sistemas</div>
        <div class="pillar-text">
        A Job Architecture serve como base única de referência para os principais processos de <strong>Remuneração, Performance Management, Talent Review</strong> e <strong>Benchmarking de Mercado</strong>.  
        Isso garante que as decisões de pessoas estejam ancoradas em um modelo técnico e sustentável.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 6. ESTRUTURA CONCEITUAL
# ===========================================================
st.markdown("""
<div class="section-title">Estrutura da Arquitetura</div>
<div class="section-text">
A arquitetura é composta por cinco elementos integrados, que formam um modelo organizacional padronizado e comparável globalmente:
</div>

<table class="job-table">
    <tr>
        <th>Elemento</th>
        <th>Propósito</th>
        <th>Exemplo de Aplicação</th>
    </tr>
    <tr>
        <td>Job Family</td>
        <td>Agrupa funções com natureza de trabalho e competências similares, que contribuem para um mesmo domínio funcional ou objetivo estratégico.</td>
        <td>Finanças, Engenharia, Recursos Humanos</td>
    </tr>
    <tr>
        <td>Sub-Job Family</td>
        <td>Distingue especializações técnicas ou áreas de foco dentro de uma Job Family, permitindo maior precisão na definição de responsabilidades.</td>
        <td>Contabilidade, Engenharia de Processo, Desenvolvimento Organizacional</td>
    </tr>
    <tr>
        <td>Career Band</td>
        <td>Representa o nível hierárquico e o escopo de influência — desde funções técnicas até posições de liderança executiva — 
        orientando expectativas de entrega e amplitude de impacto.</td>
        <td>Profissional, Gerencial, Executivo</td>
    </tr>
    <tr>
        <td>Global Grade</td>
        <td>Reflete a diferenciação de complexidade e contribuição dentro de cada banda, suportando análises salariais e equidade interna.</td>
        <td>GG07, GG09, GG12</td>
    </tr>
    <tr>
        <td>Generic Profile</td>
        <td>Fornece descrições corporativas de referência, que representam o propósito essencial e os principais resultados esperados de cada nível.</td>
        <td>“Finance Specialist”, “HR Manager”</td>
    </tr>
</table>
""", unsafe_allow_html=True)

# ===========================================================
# 7. IMPORTÂNCIA ESTRATÉGICA
# ===========================================================
st.markdown("""
<div class="section-title">Importância Estratégica</div>
<div class="section-text">
A <strong>Job Architecture</strong> é o alicerce das práticas de <strong>Gestão de Pessoas e Governança Corporativa</strong>.  
Ela fornece uma linguagem comum para estruturar, comparar e avaliar cargos, promovendo decisões justas e sustentáveis.  

Com base em critérios consistentes de complexidade e contribuição, o modelo da WTW permite <strong>análises de equidade interna, 
benchmarking de mercado e mapeamento de carreiras</strong> de forma padronizada.  

Ao integrar estrutura organizacional, remuneração e desenvolvimento, a Job Architecture fortalece a conexão entre 
<strong>estratégia de negócios, desempenho organizacional e evolução profissional</strong>, 
garantindo coerência global e meritocracia nas decisões de talento.
</div>
""", unsafe_allow_html=True)
