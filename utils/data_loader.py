import streamlit as st
import pandas as pd
import os

@st.cache_data(show_spinner=False)
def load_excel_data():
    """
    Carrega as planilhas Excel em /data e devolve dicionário de DataFrames.
    """
    data_dir = "data"
    files = {
        "job_profile": "Job Profile.xlsx",
        "job_family": "Job Family.xlsx",
        "level_structure": "Level Structure.xlsx",
    }

    data = {}
    for key, fname in files.items():
        path = os.path.join(data_dir, fname)
        if os.path.exists(path):
            try:
                df = pd.read_excel(path)
                df.columns = df.columns.str.strip()
                data[key] = df
            except Exception as e:
                st.error(f"❌ Erro ao ler {fname}: {e}")
        else:
            st.warning(f"⚠️ Arquivo não encontrado: {fname}")
    return data
