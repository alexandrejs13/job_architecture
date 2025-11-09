import pandas as pd
import os
import streamlit as st

DATA_DIR = "data"

def _read_xlsx(filename: str):
    """Lê um arquivo Excel do diretório /data."""
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        st.error(f"❌ Arquivo não encontrado: {path}")
        st.stop()
    df = pd.read_excel(path, engine="openpyxl")
    df.columns = [c.strip() for c in df.columns]
    return df

@st.cache_data
def load_data():
    """Carrega todas as planilhas Excel do app."""
    data = {}
    for file in os.listdir(DATA_DIR):
        if file.endswith(".xlsx"):
            df = _read_xlsx(file)
            key = file.replace(".xlsx", "").replace(" ", "_").lower()
            data[key] = df
    return data

@st.cache_data
def load_job_profile_df():
    return _read_xlsx("Job Profile.xlsx")

@st.cache_data
def load_level_structure_df():
    return _read_xlsx("Level Structure.xlsx")

@st.cache_data
def load_job_family_df():
    return _read_xlsx("Job Family.xlsx")
