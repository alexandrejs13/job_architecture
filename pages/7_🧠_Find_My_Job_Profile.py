import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
import numpy as np
import re

# ===========================================================
# CONFIGURAÇÃO
# ===========================================================
st.set_page_config(layout="wide", page_title="🔎 Find My Job")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # definir no Streamlit Cloud

from utils.data_loader import load_data
data = load_data()

if "job_profile" not in data:
    st.error("⚠️ Arquivo 'Job Profile.csv' não encontrado.")
    st.stop()

df = data["job_profile"]

# ===========================================================
# FUNÇÕES AUXILIARES
# ===========================================================
def clean_text(txt):
    if not isinstance(txt, str):
        return ""
    return re.sub(r"\s+", " ", txt.strip())

def get_embedding(text):
    text = clean_text(text)
    if not text:
        return np.zeros(1536)
    emb = client.embeddings.create(model="text-embedding-3-small", input=text)
    return np.array(emb.data[0].embedding)

def build_description(row):
    parts = [
        clean_text(row.get("Sub Job Family Description", "")),
        clean_text(row.get("Job Profile Description", "")),
        clean_text(row.get("Role Description", "")),
        clean_text(row.get("Grade Differentiator", "")),
    ]
    return " ".join(parts)

@st.cache_data(show_spinner=False)
def generate_embeddings(df):
    df = df.copy()
    df["merged_text"] = df.apply(build_description, axis=1)
    df["embedding"] = df["merged_text"].apply(get_embedding)
    return df

# ===========================================================
# INTERFACE
# ===========================================================
st.markdown("<h1>🔎 Find My Job</h1>", unsafe_allow_html=True)
st.markdown("Descreva suas atividades ou responsabilidades e o sistema localizará o cargo mais compatível com base em similaridade semântica.")

user_input = st.text_area("O que você faz?", height=120, placeholder="Ex: Gerencio projetos de engenharia, coordeno equipe técnica e acompanho indicadores de desempenho.")

if st.button("Encontrar cargo mais compatível"):
    if not user_input.strip():
        st.warning("Por favor, descreva suas atividades.")
        st.stop()

    with st.spinner("🔍 Analisando descrições de cargos..."):
        df_embeddings = generate_embeddings(df)
        user_emb = get_embedding(user_input)

        # Calcular similaridade
        similarities = []
        for emb in df_embeddings["embedding"]:
            sim = cosine_similarity([user_emb], [emb])[0][0]
            similarities.append(sim)
        df_embeddings["similarity"] = similarities
        df_embeddings = df_embeddings.sort_values(by="similarity", ascending=False)

        top_job = df_embeddings.iloc[0]
        score = top_job["similarity"] * 100

    # ===========================================================
    # RESULTADO
    # ===========================================================
    st.markdown("---")
    st.markdown(f"### 🧾 Cargo mais compatível — **{score:.2f}% de correspondência**")
    st.markdown(f"#### {top_job['Job Profile']}  —  GG {top_job['Global Grade']}")

    st.markdown(f"""
    **Família:** {top_job['Job Family']}  
    **Subfamília:** {top_job['Sub Job Family']}  
    **Carreira:** {top_job['Career Path']}  
    **Função:** {top_job['Function Code']}  
    **Código:** {top_job['Full Job Code']}
    """)

    # Descrições
    def section(title, content, icon):
        if isinstance(content, str) and content.strip():
            st.markdown(f"### {icon} {title}")
            st.markdown(f"<div style='background:#f9f9f9;border-left:4px solid #1E56E0;padding:10px 14px;border-radius:8px;margin-bottom:10px;'>{content}</div>", unsafe_allow_html=True)

    section("Sub Job Family Description", top_job.get("Sub Job Family Description", ""), "🧭")
    section("Job Profile Description", top_job.get("Job Profile Description", ""), "💼")
    section("Role Description", top_job.get("Role Description", ""), "🎯")
    section("Grade Differentiator", top_job.get("Grade Differentiator", ""), "🏅")
    section("Qualifications", top_job.get("Qualifications", ""), "🎓")

    # Top 3 alternativos
    st.markdown("---")
    st.markdown("### Outras correspondências possíveis:")
    for i, row in df_embeddings.iloc[1:4].iterrows():
        st.markdown(f"- **{row['Job Profile']} (GG {row['Global Grade']})** — {row['similarity']*100:.2f}%")

