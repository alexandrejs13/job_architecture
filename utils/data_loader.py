import pandas as pd
import os
import streamlit as st

@st.cache_data
def load_data():
    data = {}
    folder = "data"
    for file in os.listdir(folder):
        if file.endswith(('.csv', '.xlsx')):
            name = os.path.splitext(file)[0].lower().replace(" ", "_")
            path = os.path.join(folder, file)
            try:
                if file.endswith(".csv"):
                    df = pd.read_csv(path)
                else:
                    df = pd.read_excel(path)
                data[name] = df
            except Exception as e:
                st.warning(f"Erro ao carregar {file}: {e}")
    return data
