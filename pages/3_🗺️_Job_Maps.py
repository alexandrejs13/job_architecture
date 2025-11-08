import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section, card

data = load_data()
section("🗺️ Job Maps")

if "map" in data:
    families = sorted(data["map"]["Job Family"].unique())
    fam = st.selectbox("Família:", families)
    subf = st.selectbox(
        "Subfamília:",
        sorted(data["map"][data["map"]["Job Family"] == fam]["Sub Job Family"].unique())
    )

    df = data["map"][data["map"]["Sub Job Family"] == subf]
    cols = st.columns(3)
    for i, (_, row) in enumerate(df.iterrows()):
        with cols[i % 3]:
            card(f"{row['SIG Full Title']}", f"{row['Career Path']} - GG {row['Global Grade']}")
else:
    st.error("Arquivo Map.csv não encontrado em /data")
