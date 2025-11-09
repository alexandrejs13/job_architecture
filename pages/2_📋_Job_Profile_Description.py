import streamlit as st
import pandas as pd
from utils.data_loader import load_job_profile_df

st.set_page_config(page_title="📘 Job Profile Description", layout="wide")

st.markdown("""
<style>
h1 { color: #1E56E0; font-weight: 800; }
.card {
  background: #f8f9ff;
  border-left: 5px solid #1E56E0;
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.card h4 {
  margin-top: 0; color: #1E56E0;
}
</style>
""", unsafe_allow_html=True)

df = load_job_profile_df()

# Verifica colunas essenciais
required = [
    "Job Family", "Sub Job Family", "Job Profile", "Job Profile Description",
    "Role Description", "Grade Differentiator", "Qualifications", "Career Path"
]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"As seguintes colunas não foram encontradas no Excel: {', '.join(missing)}")
    st.stop()

st.markdown("## 📘 Job Profile Description")

# Filtros
col1, col2, col3 = st.columns(3)
familia = col1.selectbox("Família", sorted(df["Job Family"].dropna().unique()))
subfam = col2.selectbox("Subfamília", sorted(df[df["Job Family"] == familia]["Sub Job Family"].dropna().unique()))
trilha = col3.selectbox("Trilha de Carreira", sorted(df["Career Path"].dropna().unique()))

# Filtragem
filtros = (df["Job Family"] == familia) & (df["Sub Job Family"] == subfam) & (df["Career Path"] == trilha)
df_filtrado = df[filtros]

if df_filtrado.empty:
    st.warning("Nenhum cargo encontrado com os filtros selecionados.")
    st.stop()

# Seleção múltipla de cargos
opcoes = df_filtrado["Job Profile"].dropna().unique().tolist()
selecionados = st.multiselect("Selecione até 3 cargos:", opcoes, max_selections=3)

if not selecionados:
    st.info("Selecione um ou mais cargos para visualizar.")
    st.stop()

cols = st.columns(len(selecionados))
for i, cargo in enumerate(selecionados):
    cargo_df = df_filtrado[df_filtrado["Job Profile"] == cargo].iloc[0]
    with cols[i]:
        st.markdown(f"<div class='card'><h4>💼 {cargo}</h4>", unsafe_allow_html=True)
        st.markdown(f"<b>Job Profile Description:</b><br>{cargo_df['Job Profile Description']}", unsafe_allow_html=True)
        st.markdown(f"<b>Role Description:</b><br>{cargo_df['Role Description']}", unsafe_allow_html=True)
        st.markdown(f"<b>Grade Differentiator:</b><br>{cargo_df['Grade Differentiator']}", unsafe_allow_html=True)
        st.markdown(f"<b>Qualifications:</b><br>{cargo_df['Qualifications']}</div>", unsafe_allow_html=True)
