import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section

data = load_data()
section("🏗️ Structure Level")

if "level_structure" in data:
    st.dataframe(data["level_structure"], use_container_width=True)
else:
    st.error("Level Structure.csv não encontrado em /data")
