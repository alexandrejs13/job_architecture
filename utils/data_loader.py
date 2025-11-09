import os
import pandas as pd
import streamlit as st

# ===========================================================
# 🚀 Função genérica — leitura única de qualquer Excel
# ===========================================================
def _read_xlsx(filename: str):
    """
    Lê um arquivo Excel da pasta /data e retorna um DataFrame.
    Identifica automaticamente a primeira aba válida.
    """
    path = os.path.join("data", filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    try:
        xl = pd.ExcelFile(path)
        # tenta encontrar planilha principal
        sheet_name = None
        for s in xl.sheet_names:
            if "job" in s.lower() or "profile" in s.lower():
                sheet_name = s
                break
        if not sheet_name:
            sheet_name = xl.sheet_names[0]

        df = xl.parse(sheet_name)
        df.columns = df.columns.map(lambda c: str(c).strip().replace("\n", " ").replace("\r", " "))
        df = df.dropna(how="all").fillna("")
        return df
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar {filename}: {e}")

# ===========================================================
# 📘 Funções específicas — compatíveis com todas as páginas
# ===========================================================
@st.cache_data(show_spinner=False)
def load_job_family_df():
    return _read_xlsx("Job Family.xlsx")

@st.cache_data(show_spinner=False)
def load_job_profile_df():
    return _read_xlsx("Job Profile.xlsx")

@st.cache_data(show_spinner=False)
def load_level_structure_df():
    return _read_xlsx("Level Structure.xlsx")

@st.cache_data(show_spinner=False)
def load_job_match_df():
    return _read_xlsx("Job Match.xlsx")

# ===========================================================
# 🧩 Interface unificada — usada em Job Maps e outras
# ===========================================================
@st.cache_data(show_spinner=False)
def load_excel_data():
    data = {}
    try:
        data["job_profile"] = load_job_profile_df()
    except Exception:
        data["job_profile"] = pd.DataFrame()
    try:
        data["job_family"] = load_job_family_df()
    except Exception:
        data["job_family"] = pd.DataFrame()
    try:
        data["level_structure"] = load_level_structure_df()
    except Exception:
        data["level_structure"] = pd.DataFrame()
    try:
        data["job_match"] = load_job_match_df()
    except Exception:
        data["job_match"] = pd.DataFrame()
    return data
