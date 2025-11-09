import streamlit as st
from utils.data_loader import load_excel_data

st.set_page_config(layout="wide", page_title="📖 Job Profile Description")

data = load_excel_data()
if "job_profile" not in data:
    st.error("⚠️ Arquivo 'Job Profile.xlsx' não encontrado.")
    st.stop()

df = data["job_profile"]

st.markdown("## 📖 Job Profile Description")

selected = st.selectbox("Selecione um cargo:", sorted(df["Job Profile"].dropna().unique()))

if selected:
    job = df[df["Job Profile"] == selected].iloc[0]
    st.markdown(f"### {job['Job Profile']}")
    st.write(f"**GG:** {job.get('Global Grade', '-')}")
    st.write(f"**Família:** {job.get('Job Family', '-')}")
    st.write(f"**Subfamília:** {job.get('Sub Job Family', '-')}")
    st.write(f"**Carreira:** {job.get('Career Path', '-')}")
    st.write(f"**Função:** {job.get('Function Code', '-')}")
    st.write(f"**Código:** {job.get('Full Job Code', '-')}")
    st.divider()
    st.markdown(f"#### 🧭 Sub Job Family Description")
    st.write(job.get("Sub Job Family Description", "-"))
    st.markdown(f"#### 🧠 Job Profile Description")
    st.write(job.get("Job Profile Description", "-"))
    st.markdown(f"#### 🎯 Role Description")
    st.write(job.get("Role Description", "-"))
    st.markdown(f"#### 🏅 Grade Differentiator")
    st.write(job.get("Grade Differentiator", "-"))
    st.markdown(f"#### 📊 KPIs / Specific Parameters")
    st.write(job.get("KPIs / Specific Parameters", "-"))
    st.markdown(f"#### 🎓 Qualifications")
    st.write(job.get("Qualifications", "-"))
