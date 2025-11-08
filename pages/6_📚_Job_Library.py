import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section

data = load_data()
section("📚 Job Library")

if "job_profile" in data:
    st.dataframe(data["job_profile"], use_container_width=True)
else:
    st.error("Job Profile.csv não encontrado em /data")
