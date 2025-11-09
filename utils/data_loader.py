import pandas as pd
import os
import streamlit as st

@st.cache_data(show_spinner=False)
def load_excel_data():
    """
    Carrega todos os dados do arquivo Excel Job Profile.xlsx
    Retorna um dicionário com o dataframe principal 'job_profile'
    """
    data_path = os.path.join("data", "Job Profile.xlsx")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {data_path}")

    try:
        xl = pd.ExcelFile(data_path)
        # tenta localizar a planilha principal
        sheet_name = None
        for s in xl.sheet_names:
            if "job" in s.lower() or "profile" in s.lower():
                sheet_name = s
                break
        if not sheet_name:
            sheet_name = xl.sheet_names[0]

        df = xl.parse(sheet_name)

        # remove espaços e caracteres ocultos dos cabeçalhos
        df.columns = df.columns.map(lambda c: str(c).strip().replace("\n", " ").replace("\r", " "))

        # remove linhas vazias
        df = df.dropna(how="all")
        df = df.fillna("")

        return {"job_profile": df}

    except Exception as e:
        raise RuntimeError(f"Erro ao carregar o Excel: {e}")
