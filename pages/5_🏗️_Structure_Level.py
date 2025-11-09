import streamlit as st
import pandas as pd
from utils.data_loader import load_excel_data

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="🏗️ Level Structure")

st.markdown("""
<style>
.block-container {max-width: 1500px !important;}
h1 {
    color: #1E56E0;
    font-weight: 800;
}
.dataframe {
    font-size: 0.9rem;
}
table {
    border-collapse: collapse;
}
th {
    background-color: #1E56E0;
    color: white;
    text-align: center !important;
    padding: 8px;
}
td {
    padding: 6px 10px;
}
tr:nth-child(even) {background-color: #f9f9f9;}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# CARREGAR DADOS
# ===========================================================
data = load_excel_data()
if "level_structure" not in data:
    st.error("⚠️ Arquivo 'Level Structure.xlsx' não encontrado.")
    st.stop()

df = data["level_structure"].copy()

# Normaliza e ordena
df.columns = df.columns.str.strip()
if "Global Grade" in df.columns:
    df["Global Grade"] = df["Global Grade"].astype(str).str.extract(r"(\d+)").fillna("0").astype(int)
    df = df.sort_values("Global Grade", ascending=False)

st.markdown("## 🏗️ Estrutura de Níveis Globais (Level Structure)")
st.markdown("""
Esta tabela mostra a hierarquia dos **Global Grades (GG)**, seus **nomes de nível**, **descrições** e **tipos de carreira**.
Essas informações são usadas em páginas como *Job Maps* e *Job Match* para manter coerência hierárquica e precisão nas comparações.
""")

# ===========================================================
# VISUALIZAÇÃO
# ===========================================================
st.dataframe(df, use_container_width=True, hide_index=True)

# ===========================================================
# DOWNLOAD
# ===========================================================
st.download_button(
    "⬇️ Baixar Level Structure.xlsx",
    data=df.to_excel(index=False),
    file_name="Level Structure.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ===========================================================
# INSIGHT VISUAL
# ===========================================================
if "Description" in df.columns and "Global Grade" in df.columns:
    st.markdown("### 📊 Distribuição dos Níveis")
    st.bar_chart(df.set_index("Global Grade")["Global Grade"].value_counts().sort_index(ascending=False))
