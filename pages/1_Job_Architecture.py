import streamlit as st
from utils.ui import sidebar_logo_and_title
from pathlib import Path

# ===========================================================
# 1) CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Architecture",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2) CSS GLOBAL E SIDEBAR
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

# ===========================================================
# 3) HEADER + CSS LOCAL (inclui animação fade-in)
# ===========================================================
st.markdown("""
<style>
/* ---------- Animações ---------- */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.fade-in       { opacity: 0; animation: fadeUp .48s ease-out forwards; }
.fade-in-0     { animation-delay: .00s; }
.fade-in-1     { animation-delay: .08s; }
.fade-in-2     { animation-delay: .16s; }
.fade-in-3     { animation-delay: .24s; }

/* ---------- Header padrão ---------- */
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
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.page-header img { width: 54px; height: 54px; }

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

/* ---------- Seções ---------- */
.section-title {
    font-weight: 700;
    font-size: 1.2rem;
    color: #000;
    margin-top: 35px;
    margin-bottom: 10px;
}
.section-text {
    font-size: 1rem;
    color: #202020;
    line-height: 1.65;
    text-align: justify;
}

/* ---------- Cards dos pilares (mesma altura + responsivo) ---------- */
.pillar-row {
    display: flex;
    justify-content: space-between;
    align-items: stretch;
    gap: 20px;
    flex-wrap: wrap;
    margin-top: 10px;
}
.pillar-card {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    background-color: #fff;
    border-left: 5px solid #145efc;
    border-radius: 10px;
    padding: 22px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    min-height: 280px;                 /* altura mínima uniforme */
    transition: transform .2s ease, box-shadow .2s ease;
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
    color: #333;
    font-size: 0.98rem;
    line-height: 1.6;
    flex-grow: 1;                      /* iguala alturas entre os cards */
}

/* ---------- Tabela conceitual (se você usar abaixo) ---------- */
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

<div class="page-header fade-in fade-in-0">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png" alt="icon">
    Job Architecture — Fundamentos e Governança
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4) CONCEITO CENTRAL (exemplo de conteúdo acima dos pilares)
# ===========================================================
st.markdown("""
<div class="section-text fade-in fade-in-1">
A <strong>Job Architecture (JA)</strong> é o modelo corporativo que estrutura de forma integrada todas as posições da organização,
definindo a lógica de agrupamento de funções, níveis de responsabilidade, critérios de progressão e diferenciais de complexidade.<br><br>
Baseada na metodologia global da <strong>Willis Towers Watson (WTW)</strong>, a Job Architecture fornece um framework que garante
<strong>equidade interna, consistência organizacional e comparabilidade externa</strong>, sustentando decisões estratégicas sobre
estrutura, remuneração, carreira e sucessão.<br><br>
Mais do que um catálogo de cargos, trata-se de uma <strong>infraestrutura de governança</strong> que conecta o desenho organizacional
à gestão de talentos, assegurando que as práticas de gestão de pessoas sejam <strong>claras, coerentes e orientadas por propósito</strong>.
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 5) FUNÇÃO PARA RENDERIZAR A SEÇÃO "PILARES ESTRUTURANTES"
#    (isola o HTML dentro de UM st.markdown -> evita NameError)
# ===========================================================
def render_pillars_section():
    st.markdown("""
    <div class="section-title fade-in fade-in-1">Pilares Estruturantes</div>

    <div class="pillar-row">

        <div class="pillar-card fade-in fade-in-1">
            <div class="pillar-title">Governança Global</div>
            <div class="pillar-text">
                Define princípios, critérios e regras universais para a criação, atualização e manutenção dos cargos,
                garantindo comparabilidade entre países, funções e níveis organizacionais.<br><br>
                Essa governança assegura que toda posição seja avaliada de acordo com padrões globais e práticas de mercado reconhecidas.
            </div>
        </div>

        <div class="pillar-card fade-in fade-in-2">
            <div class="pillar-title">Clareza de Carreira</div>
            <div class="pillar-text">
                Cada cargo é vinculado a um <strong>Career Band</strong> e <strong>Global Grade</strong>, refletindo o escopo de atuação,
                o grau de autonomia e a natureza da contribuição.<br><br>
                Essa estrutura fornece visibilidade sobre oportunidades de progressão, diferenciação de níveis e mobilidade lateral entre áreas.
            </div>
        </div>

        <div class="pillar-card fade-in fade-in-3">
            <div class="pillar-title">Integração de Sistemas</div>
            <div class="pillar-text">
                A Job Architecture serve como base única de referência para os principais processos de
                <strong>Remuneração, Performance Management, Talent Review</strong> e
                <strong>Benchmarking de Mercado</strong>.<br><br>
                Isso garante que as decisões de pessoas estejam ancoradas em um modelo técnico e sustentável.
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)

# ===========================================================
# 6) CHAMADA DA SEÇÃO (AGORA SEM ERRO)
# ===========================================================
render_pillars_section()

# ===========================================================
# 7) (Opcional) OUTRAS SEÇÕES ABAIXO...
#    Ex.: tabela conceitual, importância estratégica, etc.
# ===========================================================
