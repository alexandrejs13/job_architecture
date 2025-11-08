import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section

data = load_data()
section("📘 Glossary")

if "glossary" in data:
    search = st.text_input("Buscar termo:")
    df = data["glossary"]
    if search:
        df = df[df["CONCEPT"].str.contains(search, case=False, na=False)]
    st.dataframe(df, use_container_width=True)
else:
    st.error("Glossary.csv não encontrado em /data")
