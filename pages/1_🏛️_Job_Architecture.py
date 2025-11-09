import streamlit as st
import pandas as pd
from utils.data_loader import load_job_family_df
from utils.ui_components import section

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="🏛️ Job Architecture")

st.markdown("""
<style>
.block-container {
  max-width: 1400px !important;
  padding: 2rem 2rem;
}
h1 {
  color: #1E56E0;
  font-weight: 800;
  font-size: 1.8rem !important;
}
table {
  border-collapse: collapse;
  width: 100%;
  font-size: 0.9rem;
}
th, td {
  border: 1px solid #e0e0e0;
  padding: 8px 10px;
  text-align: left;
}
th {
  background: #1E56E0;
  color: white;
  font-weight: 700;
}
tr:nth-child(even) {
  background-color: #fafafa;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# LEITURA DO ARQUIVO
# ===========================================================
try:
    df = load_job_family_df()
except Exception as e:
    st.error(f"❌ Erro ao carregar Job Family.xlsx: {e}")
    st.stop()

section("🏛️ Estrutura de Job Architecture")

# ===========================================================
# VISUALIZAÇÃO
# ===========================================================
if not df.empty:
    st.markdown("### 📚 Visualização Completa da Tabela Job Family")
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.warning("⚠️ Nenhum dado encontrado em Job Family.xlsx.")
