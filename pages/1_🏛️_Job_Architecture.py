import streamlit as st

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="SIG | Job Architecture")

# Paleta de cores SIG
SIG_COLORS = {
    "sky": "#145efc",
    "spark": "#dca0ff",
    "black": "#000000",
    "sand1": "#f2efeb",
    "sand4": "#73706d",
    "forest2": "#167665",
    "white": "#ffffff"
}

# CSS estilizado
st.markdown(f"""
<style>
    /* Configurações Gerais do Container */
    .block-container {{
        padding-top: 3rem;
        padding-bottom: 5rem;
        max-width: 1200px !important;
    }}
    body, p, li {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #333333;
        line-height: 1.6;
        font-size: 1.1rem;
    }}

    /* Header Padrão */
    .sig-header {{
        border-left: 6px solid {SIG_COLORS["sky"]};
        padding-left: 1.5rem;
        margin-bottom: 2rem;
        margin-top: 1rem;
    }}
    .sig-header h1 {{
        color: #2c3e50;
        font-weight: 800;
        font-size: 2.8rem !important;
        margin: 0;
        padding: 0;
        line-height: 1.2;
    }}
    .sig-header .subtitle {{
        color: {SIG_COLORS["sand4"]};
        font-size: 1.3rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }}

    /* Subtítulos */
    h2 {{
        color: {SIG_COLORS["sky"]};
        font-weight: 700;
        font-size: 1.8rem !important;
        margin-top: 3rem !important;
        margin-bottom: 1.5rem !important;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
    }}

    /* Cards */
    .sig-card {{
        background-color: {SIG_COLORS["sand1"]};
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        border-left: 4px solid {SIG_COLORS["sand4"]};
        transition: transform 0.2s ease-in-out;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    .sig-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        border-left: 4px solid {SIG_COLORS["sky"]};
    }}
    .sig-card h4 {{
        color: {SIG_COLORS["sky"]};
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-size: 1.2rem !important;
    }}
    .sig-card p {{
        font-size: 1rem;
        margin-bottom: 0;
        color: #444;
    }}

    /* Info Box Customizado */
    .custom-info {{
        background-color: #eefaf8;
        border-left: 6px solid {SIG_COLORS["forest2"]};
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 2rem;
        color: #0a3d35;
    }}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# CONTEÚDO DA PÁGINA
# ===========================================================

# Header
st.markdown("""
<div class="sig-header">
    <h1>Job Architecture</h1>
    <div class="subtitle">A estrutura fundamental de P&C na SIG</div>
</div>
""", unsafe_allow_html=True)

# Intro
st.markdown("""
A **Job Architecture (JA)** organiza e nivela os cargos em toda a organização. Ela serve como base sólida para processos críticos de pessoas, garantindo consistência, clareza e justiça em todas as regiões.
""")

# Seção 4 Elementos
st.markdown("## Os 4 Elementos Chave")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="sig-card">
        <h4>1. Famílias de Cargos<br>(Job Families)</h4>
        <p>Grandes grupos funcionais que agrupam papéis com características similares.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="sig-card">
        <h4>2. Sub-Famílias<br>(Sub-Job Families)</h4>
        <p>Especializações funcionais dentro das grandes famílias.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="sig-card">
        <h4>3. Níveis de Carreira<br>(Career Levels)</h4>
        <p>Definem a senioridade e o foco do papel (ex: Gestão, Especialista, Projetos).</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="sig-card">
        <h4>4. Perfis Genéricos<br>(Generic Profiles)</h4>
        <p>Descrições padronizadas que servem de base sólida para cada função.</p>
    </div>
    """, unsafe_allow_html=True)

# Seção Importância
st.markdown("## Por que é importante?")
col_a, col_b = st.columns(2)
with col_a:
    st.markdown("### 🎯 Caminhos de Carreira Claros")
    st.markdown("Crescimento na SIG não se limita à gestão. Valorizamos a experiência funcional especializada através de bandas de carreira dedicadas.")
    st.markdown("### ⚖️ Benchmarking e Remuneração")
    st.markdown("O **Job Code** liga nossa estrutura aos dados de mercado, garantindo análises salariais justas e competitivas.")
with col_b:
    st.markdown("### 🚀 Desenvolvimento de Talento")
    st.markdown("Facilita a identificação de próximos passos claros e oportunidades de desenvolvimento, dentro ou fora da função atual.")

# Seção Princípios
st.markdown("## Regras de Ouro para Mapeamento")
p1, p2, p3 = st.columns(3)
with p1:
     st.markdown("""
    <div class="sig-card" style="background-color: #fff; border: 1px solid #eee;">
        <h4>📌 Foco no Conteúdo</h4>
        <p>O mapeamento baseia-se nas tarefas e responsabilidades, <strong>nunca</strong> nas habilidades do ocupante atual.</p>
    </div>
    """, unsafe_allow_html=True)
with p2:
     st.markdown("""
    <div class="sig-card" style="background-color: #fff; border: 1px solid #eee;">
        <h4>📊 A Regra dos 50%</h4>
        <p>Uma posição deve ser mapeada para um Perfil que cubra a maioria (pelo menos 50%) de suas atividades.</p>
    </div>
    """, unsafe_allow_html=True)
with p3:
     st.markdown("""
    <div class="sig-card" style="background-color: #fff; border: 1px solid #eee;">
        <h4>🌍 Independência</h4>
        <p>A arquitetura agrupa posições por sua natureza funcional, independentemente de reporte ou região.</p>
    </div>
    """, unsafe_allow_html=True)

# Seção Governança e Callout Final
st.markdown("## Governança")
st.markdown("A Diretiva de JA, ferramentas e formulários de aprovação estão disponíveis no **SharePoint de Global C&B**.")

st.markdown(f"""
<div class="custom-info">
    <strong>💡 Ponto de Atenção Essencial</strong><br>
    O Perfil Genérico não substitui a Descrição do Cargo (Job Description). Ao mapear a posição no SAP, ela herda automaticamente as características chave do perfil.
</div>
""", unsafe_allow_html=True)
