import os
import pandas as pd
import streamlit as st

# ===========================================================
# 🔧 FUNÇÃO BASE PARA LEITURA DE EXCEL
# ===========================================================
@st.cache_data(show_spinner=False)
def _read_xlsx(filename: str) -> pd.DataFrame:
    """Lê um arquivo Excel da pasta /data e retorna um DataFrame limpo."""
    base_path = os.path.join("data", filename)
    if not os.path.exists(base_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {base_path}")

    df = pd.read_excel(base_path, engine="openpyxl")

    # Limpeza de colunas e strings
    df.columns = [str(c).strip() for c in df.columns]
    df = df.map(lambda x: str(x).strip() if isinstance(x, str) else x)
    return df


# ===========================================================
# 🔄 CARREGAMENTO GERAL DE DADOS
# ===========================================================
@st.cache_data(show_spinner=False)
def load_data():
    """Carrega todos os arquivos Excel relevantes do app."""
    data = {}

    try:
        data["job_profile"] = _read_xlsx("Job Profile.xlsx")
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar Job Profile.xlsx: {e}")

    try:
        data["job_family"] = _read_xlsx("Job Family.xlsx")
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar Job Family.xlsx: {e}")

    try:
        data["structure_level"] = _read_xlsx("Level Structure.xlsx")
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar Level Structure.xlsx: {e}")

    return data


# ===========================================================
# 🔍 FUNÇÃO ESPECÍFICA POR ARQUIVO
# ===========================================================
def load_job_profile_df() -> pd.DataFrame:
    """Retorna o DataFrame do Job Profile."""
    return _read_xlsx("Job Profile.xlsx")


def load_job_family_df() -> pd.DataFrame:
    """Retorna o DataFrame do Job Family."""
    return _read_xlsx("Job Family.xlsx")


def load_structure_level_df() -> pd.DataFrame:
    """Retorna o DataFrame do Level Structure."""
    return _read_xlsx("Level Structure.xlsx")
