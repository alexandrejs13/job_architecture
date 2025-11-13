import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO GERAL
# ===========================================================
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
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
# 3. CABEÇALHO PADRÃO
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
    max-width: 1400px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
.metric-card {
    background-color: #ffffff;
    border-left: 6px solid #145efc;
    border-radius: 10px;
    padding: 20px 30px;
    text-align: left;
    box-shadow: 0 4px 8px rgba(0,0,0,0.06);
    height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #000000;
}
.metric-label {
    font-size: 0.9rem;
    color: #555;
}
</style>

<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/data%202%20perfromance.png" alt="icon">
  Dashboard — Indicadores de Arquitetura de Cargos
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. CARREGAMENTO DOS DADOS
# ===========================================================
@st.cache_data
def load_data():
    df = pd.read_excel("data/Job Profile.xlsx")
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# ===========================================================
# 5. CARDS RESUMO
# ===========================================================
total_cargos = len(df["Job Profile"].unique())
total_familias = len(df["Job Family"].unique())
total_subfamilias = len(df["Sub Job Family"].unique())
total_trilhas = len(df["Career Path"].unique())
total_grades = len(df["Global Grade"].unique())

c1, c2, c3, c4, c5 = st.columns(5)
c1.markdown(f"<div class='metric-card'><div class='metric-value'>{total_cargos}</div><div class='metric-label'>Perfis de Cargo</div></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card'><div class='metric-value'>{total_familias}</div><div class='metric-label'>Famílias</div></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card'><div class='metric-value'>{total_subfamilias}</div><div class='metric-label'>Sub-Famílias</div></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='metric-card'><div class='metric-value'>{total_trilhas}</div><div class='metric-label'>Trilhas de Carreira</div></div>", unsafe_allow_html=True)
c5.markdown(f"<div class='metric-card'><div class='metric-value'>{total_grades}</div><div class='metric-label'>Global Grades</div></div>", unsafe_allow_html=True)

st.markdown("---")

# ===========================================================
# 6. GRÁFICOS INTERATIVOS
# ===========================================================

tab1, tab2, tab3 = st.tabs(["📊 Job Family", "🎯 Trilhas de Carreira", "🏛️ Níveis e Grades"])

with tab1:
    st.subheader("Distribuição de Cargos por Job Family")
    job_family_counts = df["Job Family"].value_counts().reset_index()
    job_family_counts.columns = ["Job Family", "Qtd"]
    fig = px.bar(
        job_family_counts,
        x="Job Family",
        y="Qtd",
        color="Job Family",
        text="Qtd",
        title="Cargos por Família",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_layout(xaxis_title="", yaxis_title="Quantidade", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Perfis por Trilha de Carreira")
    career_path_counts = df["Career Path"].value_counts().reset_index()
    career_path_counts.columns = ["Career Path", "Qtd"]
    fig2 = px.pie(
        career_path_counts,
        names="Career Path",
        values="Qtd",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Distribuição por Trilha de Carreira"
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Distribuição de Cargos por Global Grade")
    grade_counts = df["Global Grade"].value_counts().reset_index()
    grade_counts.columns = ["Global Grade", "Qtd"]
    fig3 = px.bar(
        grade_counts,
        x="Global Grade",
        y="Qtd",
        text="Qtd",
        title="Cargos por Nível Global (Grade)",
        color_discrete_sequence=["#145efc"]
    )
    fig3.update_layout(xaxis_title="Global Grade", yaxis_title="Quantidade")
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ===========================================================
# 7. TABELA DE VISÃO GERAL
# ===========================================================
st.subheader("📋 Visão Geral de Perfis")
st.dataframe(
    df[["Job Family", "Sub Job Family", "Career Path", "Job Profile", "Global Grade"]]
    .sort_values(by=["Job Family", "Sub Job Family"]),
    use_container_width=True
)
