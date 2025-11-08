# 🧩 Job Match (Identificador de Cargo)
# Autor: Alexandre & GPT-5 — 2025
# Posição: abaixo do Job Maps

import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util

# ------------------------------------------------------------
# 🎨 CONFIGURAÇÃO INICIAL
# ------------------------------------------------------------
st.set_page_config(page_title="🧩 Job Match", layout="wide")

st.markdown("""
<h1>🧩 Job Match</h1>
<p>Encontre o <b>cargo mais compatível</b> com base em suas atividades e responsabilidades.<br>
O sistema identifica automaticamente o <b>nível</b> e o <b>escopo de atuação</b> para sugerir o Job Match mais preciso.</p>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 📂 CARREGAMENTO DE BASE
# ------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv("data/Job Profile.csv")
    df.fillna("", inplace=True)

    # Criação do texto consolidado para busca semântica
    df["Merged_Text"] = (
        "Job Title: " + df["Job Title"].astype(str) +
        " | Family: " + df["Family"].astype(str) +
        " | Subfamily: " + df["Subfamily"].astype(str) +
        " | Grade: " + df["Grade"].astype(str) +
        " | Job Profile Description: " + df["Job Profile Description"].astype(str) +
        " | Role Description: " + df["Role Description"].astype(str) +
        " | Grade Differentiator: " + df["Grade Differentiator"].astype(str) +
        " | KPIs: " + df["KPIs/Specific Parameters"].astype(str)
    )
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Erro ao carregar base: {e}")
    st.stop()

# ------------------------------------------------------------
# 🧠 EMBEDDINGS
# ------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

model = load_model()
embeddings = model.encode(df["Merged_Text"].tolist(), convert_to_tensor=True)

# ------------------------------------------------------------
# 🧭 INTERFACE DE BUSCA
# ------------------------------------------------------------
st.markdown("### 🔧 Informe os parâmetros abaixo:")

col1, col2 = st.columns(2)
with col1:
    family = st.selectbox("Selecione a Family", sorted(df["Family"].unique()))
with col2:
    subfamily = st.selectbox(
        "Selecione a Subfamily",
        sorted(df[df["Family"] == family]["Subfamily"].unique())
    )

descricao = st.text_area(
    "✍️ Descreva brevemente suas atividades:",
    placeholder="Exemplo: Apoio na folha de pagamento, controle de ponto e benefícios..."
)

if st.button("🔍 Identificar Cargo"):
    if len(descricao.strip().split()) < 5:
        st.warning("Por favor, descreva suas atividades com um pouco mais de detalhes.")
        st.stop()

    st.info("🔎 Analisando descrição e buscando correspondência mais precisa...")

    # 🔹 Filtra por family e subfamily
    subset = df[(df["Family"] == family) & (df["Subfamily"] == subfamily)].copy()
    if subset.empty:
        st.warning("Nenhum cargo encontrado para a Family/Subfamily selecionadas.")
        st.stop()

    # 🔹 Calcula embeddings da subbase
    subset_embeddings = model.encode(subset["Merged_Text"].tolist(), convert_to_tensor=True)
    query_embedding = model.encode(descricao, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, subset_embeddings)[0].cpu().numpy()

    subset["Score"] = scores
    best = subset.iloc[np.argmax(scores)]
    similarity = np.max(scores) * 100
    gg = best["Grade"]
    job_title = best["Job Title"]

    # ------------------------------------------------------------
    # 🎯 RESULTADO FINAL
    # ------------------------------------------------------------
    st.markdown("## 🎯 Cargo mais compatível encontrado:")
    with st.container():
        st.markdown(f"""
        <div style="background-color:#f8f9ff; padding:20px; border-radius:12px; border-left:6px solid #3366ff;">
        <h3>🧩 {job_title} — GG {gg}</h3>
        <p><b>Family:</b> {best['Family']} &nbsp; | &nbsp; <b>Subfamily:</b> {best['Subfamily']}</p>
        <p><b>Similaridade:</b> {similarity:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

        def render_section(title, content, icon):
            if pd.notna(content) and str(content).strip():
                st.markdown(
                    f"<h5>{icon} {title}</h5><div style='padding:10px 15px; background:#fafaff; border-radius:10px; border:1px solid #eaeaea; margin-bottom:10px;'>{content}</div>",
                    unsafe_allow_html=True
                )

        render_section("Sub Job Family Description", best["Sub Job Family Description"], "💬")
        render_section("Job Profile Description", best["Job Profile Description"], "💼")
        render_section("Role Description", best["Role Description"], "🎯")
        render_section("Grade Differentiator", best["Grade Differentiator"], "📈")
        render_section("KPIs / Specific Parameters", best["KPIs/Specific Parameters"], "📊")
        render_section("Qualifications", best["Qualifications"], "🎓")

else:
    st.markdown(
        "<p style='color:gray;'>Preencha as informações acima e clique em <b>🔍 Identificar Cargo</b> para encontrar o Job Match mais compatível.</p>",
        unsafe_allow_html=True
    )
