import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
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
# 3. HEADER PADRONIZADO
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
    max-width: 1300px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
.metric-card {
    background-color: white;
    border-left: 5px solid #145efc;
    border-radius: 8px;
    padding: 18px 24px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.07);
    text-align: center;
}
.metric-title {
    color: #555;
    font-size: 0.9rem;
    font-weight: 600;
}
.metric-value {
    color: #145efc;
    font-size: 2rem;
    font-weight: 800;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/data%202%20perfromance.png" alt="icon">
    Dashboard — Job Architecture Overview
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. CARREGAMENTO DE DADOS
# ===========================================================
@st.cache_data(ttl="1h")
def load_job_data():
    file_path = Path("data/Job Profile.xlsx")
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    return df

df = load_job_data()

# ===========================================================
# 5. INDICADORES RESUMIDOS
# ===========================================================
total_profiles = len(df)
total_families = df["Job Family"].nunique()
total_subfamilies = df["Sub Job Family"].nunique()
total_career_paths = df["Career Path"].nunique()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Perfis de Cargo</div>
        <div class="metric-value">{total_profiles}</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Famílias</div>
        <div class="metric-value">{total_families}</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Sub-Famílias</div>
        <div class="metric-value">{total_subfamilies}</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Trilhas de Carreira</div>
        <div class="metric-value">{total_career_paths}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ===========================================================
# 6. VISUALIZAÇÕES
# ===========================================================

# ---- 6.1 Cargos por Família ----
st.subheader("📂 Quantidade de Cargos por Família (Job Family)")
df_familia = df["Job Family"].value_counts().reset_index()
df_familia.columns = ["Job Family", "Count"]

fig1 = px.bar(
    df_familia,
    x="Job Family",
    y="Count",
    text="Count",
    color="Job Family",
    color_discrete_sequence=px.colors.qualitative.Safe,
)
fig1.update_traces(textposition="outside")
fig1.update_layout(
    xaxis_title=None, yaxis_title="Quantidade de Cargos",
    showlegend=False, plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# ---- 6.2 Sub-Famílias por Família ----
st.subheader("🧩 Número de Sub-Famílias por Família")
df_sub = df.groupby("Job Family")["Sub Job Family"].nunique().reset_index()
df_sub.columns = ["Job Family", "Sub-Families"]

fig2 = px.treemap(
    df_sub,
    path=["Job Family"],
    values="Sub-Families",
    color="Sub-Families",
    color_continuous_scale="Blues",
)
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---- 6.3 Cargos por Trilha de Carreira ----
st.subheader("🚀 Distribuição de Cargos por Trilha de Carreira")
df_trilha = df["Career Path"].value_counts().reset_index()
df_trilha.columns = ["Career Path", "Count"]

fig3 = px.pie(
    df_trilha,
    names="Career Path",
    values="Count",
    color_discrete_sequence=px.colors.sequential.Blues,
    hole=0.4
)
fig3.update_traces(textinfo="label+percent", pull=[0.05]*len(df_trilha))
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ---- 6.4 Distribuição por Global Grade (caso exista) ----
if "Global Grade" in df.columns:
    st.subheader("🏅 Distribuição por Global Grade")
    df_grade = df["Global Grade"].astype(str).value_counts().reset_index()
    df_grade.columns = ["Global Grade", "Count"]
    fig4 = px.bar(
        df_grade,
        x="Global Grade",
        y="Count",
        text="Count",
        color="Global Grade",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig4.update_traces(textposition="outside")
    fig4.update_layout(
        xaxis_title="Global Grade", yaxis_title="Qtd. de Cargos",
        showlegend=False, plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig4, use_container_width=True)

# ===========================================================
# 7. FOOTER
# ===========================================================
st.markdown("""
---
📘 *Dashboard de Arquitetura de Cargos — SIG*  
Visualização analítica das famílias, trilhas e níveis de cargos.
""")
