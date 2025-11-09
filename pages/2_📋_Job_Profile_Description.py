# 2_📋_Job_Profile_Description.py
import streamlit as st
import pandas as pd
from utils.data_loader import load_job_profile
from utils.ui_components import inject_base_css, page_title

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="📋 Job Profile Description")
inject_base_css()
page_title("📋 Job Profile Description")

# ===========================================================
# CARREGAMENTO DOS DADOS
# ===========================================================
df = load_job_profile()

required = [
    "Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade", "Full Job Code",
    "Role Description", "Grade Differentiator", "Specific parameters KPIs", "Qualifications",
    "Sub Job Family Description", "Job Profile Description"
]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes no CSV: {', '.join(missing)}")
    st.stop()

# ===========================================================
# FILTROS DE FAMILY E SUBFAMILY
# ===========================================================
col1, col2 = st.columns([2, 2])
with col1:
    families = ["Selecione"] + sorted(df["Job Family"].dropna().unique().tolist())
    selected_family = st.selectbox("Família", families)
with col2:
    subfams = ["Selecione"]
    if selected_family != "Selecione":
        subfams += sorted(df[df["Job Family"] == selected_family]["Sub Job Family"].dropna().unique().tolist())
    selected_subfamily = st.selectbox("Subfamília", subfams)

if selected_family == "Selecione" or selected_subfamily == "Selecione":
    st.info("🔹 Selecione uma *Família* e *Subfamília* para visualizar as descrições.")
    st.stop()

# ===========================================================
# FILTRO DE CARGOS DENTRO DA SUBFAMILY
# ===========================================================
subset = df[(df["Job Family"] == selected_family) & (df["Sub Job Family"] == selected_subfamily)]
if subset.empty:
    st.warning("Nenhum cargo encontrado para essa combinação.")
    st.stop()

profiles = ["Selecione"] + sorted(subset["Job Profile"].dropna().unique().tolist())
selected_profile = st.selectbox("📌 Cargo (Job Profile)", profiles)

if selected_profile == "Selecione":
    st.info("🧭 Escolha um cargo para visualizar os detalhes do perfil.")
    st.stop()

# ===========================================================
# EXIBIÇÃO DOS DETALHES DO CARGO
# ===========================================================
row = subset[subset["Job Profile"] == selected_profile].iloc[0]

# Cabeçalho resumido
st.markdown(
    f"""
    <div class='ja-card'>
    <div class='ja-card-title'>{row['Job Profile']}</div>
    <div><b>GG:</b> {row['Global Grade']} | <b>Família:</b> {row['Job Family']} | <b>Subfamília:</b> {row['Sub Job Family']} | <b>Carreira:</b> {row['Career Path']}</div>
    <div><b>Função:</b> {row.get('Function Code','-')} | <b>Disciplina:</b> {row.get('Discipline Code','-')} | <b>Código:</b> {row.get('Full Job Code','-')}</div>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("")

# Descrições
def section(icon, title, text):
    """Renderiza se houver conteúdo válido."""
    if pd.notna(text) and str(text).strip():
        st.markdown(f"**{icon} {title}**")
        # quebra por marcadores ou separadores
        bullets = [b.strip() for b in str(text).replace("•", "●").split("●") if b.strip()]
        if len(bullets) > 1:
            for b in bullets:
                st.markdown(f"- {b}")
        else:
            st.markdown(text.strip())
        st.write("")

# Sub Job Family Description (geral)
section("🧭", "Sub Job Family Description", row.get("Sub Job Family Description", ""))

# Job Profile Description (geral)
section("🧠", "Job Profile Description", row.get("Job Profile Description", ""))

# Role Description (detalhado)
section("🎯", "Role Description", row.get("Role Description", ""))

# Grade Differentiator
section("🏅", "Grade Differentiator", row.get("Grade Differentiator", ""))

# KPIs / Specific Parameters
section("📊", "KPIs / Specific Parameters", row.get("Specific parameters KPIs", ""))

# Qualifications
section("🎓", "Qualifications", row.get("Qualifications", ""))

# ===========================================================
# CONTADOR FINAL
# ===========================================================
count = len(subset)
st.markdown(f"<p style='color:#666'>Total de cargos nesta subfamília: <b>{count}</b></p>", unsafe_allow_html=True)
