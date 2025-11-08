import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section

data = load_data()
section("📋 Job Profile Description")

if "job_profile" in data:
    df = data["job_profile"]
    families = sorted(df["Job Family"].dropna().unique())
    family = st.selectbox("Selecione a Família:", families)
    filtered = df[df["Job Family"] == family]

    subs = sorted(filtered["Sub Job Family"].dropna().unique())
    sub = st.selectbox("Selecione a Subfamília:", subs)
    result = filtered[filtered["Sub Job Family"] == sub]
    st.dataframe(result, use_container_width=True)
else:
    st.error("Arquivo 'Job Profile.csv' não encontrado em /data")
