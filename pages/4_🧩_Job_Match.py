# 🧩 Job Match — Identificador de Cargo Ideal
# Autor: Alexandre & GPT-5 — 2025

import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import csv

# ------------------------------------------------------------
# 🎨 CONFIGURAÇÃO INICIAL
# ------------------------------------------------------------
st.set_page_config(page_title="🧩 Job Match", layout="wide")

st.markdown("""
<h1>🧩 Job Match</h1>
<p>Descubra o <b>cargo mais compatível</b> com suas responsabilidades e área de atuação.<br>
O sistema identifica automaticamente o <b>nível de senioridade</b> e o <b>escopo</b> com base no conteúdo da sua descrição.</p>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 📂 CARREGAMENTO ROBUSTO + NORMALIZAÇÃO DE COLUNAS
# ------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data():
    path = "data/Job Profile.csv"

    try:
        df = pd.read_csv(
            path,
            sep=",",
            engine="python",
            dtype=str,
            quotechar='"',
            escapechar="\\",
            quoting=csv.QUOTE_MINIMAL,
            on_bad_lines="error",
        )
    except Exception:
        df = pd.read_csv(
            path,
            sep=";",
            engine="python",
            dtype=str,
            quotechar='"',
            escapechar="\\",
            quoting=csv.QUOTE_MINIMAL,
            on_bad_lines="error",
        )

    df = df.fillna("")

    # Normaliza nomes de colunas
    rename_patterns = {
        "job title": "Job Title",
        "title": "Job Title",
        "job": "Job Title",
        "family": "Family",
        "job family": "Family",
        "sub-family": "Subfamily",
        "sub family": "Subfamily",
        "job sub-family": "Subfamily",
        "subfamily": "Subfamily",
        "grade differentiation": "Grade Differentiator",
        "grade differentiator": "Grade Differentiator",
        "grade": "Grade",
        "kpis": "KPIs/Specific Parameters",
        "specific parameters": "KPIs/Specific Parameters",
        "qualifications": "Qualifications",
        "role description": "Role Description",
        "sub job family description": "Sub Job Family Description",
        "job profile description": "Job Profile Description",
    }

    df.rename(
        columns={
            c: rename_patterns.get(c.strip().lower(), c)
            for c in df.columns
        },
        inplace=True,
    )

    # Garante colunas obrigatórias
    required_cols = [
        "Job Title", "Family", "Subfamily", "Grade",
        "Sub Job Family Description", "Job Profile Description",
        "Role Description", "Grade Differentiator",
        "KPIs/Specific Parameters", "Qualifications"
    ]
    for c in required_cols:
        if c not in df.columns:
            df[c] = ""

    # Normaliza espaços e capitalização
    df["Family"] = df["Family"].str.strip().str.title()
    df["Subfamily"] = df["Subfamily"].str.strip().str.title()

    # Campo unificado para embeddings
    df["Merged_Text"] = (
        "Job Title: " + df["Job Title"] +
        " | Family: " + df["Family"] +
        " | Subfamily: " + df["Subfamily"] +
        " | Grade: " + df["Grade"] +
        " | Job Profile Description: " + df["Job Profile Description"] +
        " | Role Description: " + df["Role Description"] +
        " | Grade Differentiator: " + df["Grade Differentiator"] +
        " | KPIs: " + df["KPIs/Specific Parameters"]
    )

    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Erro ao carregar base: {e}")
    st.stop()


# ------------------------------------------------------------
# 🧠 EMBEDDINGS
# ------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

model = load_model()

# ------------------------------------------------------------
# 🧭 INTERFACE
# ------------------------------------------------------------
st.markdown("### 🔧 Parâmetros de busca")

col1, col2 = st.columns(2)
with col1:
    family = st.selectbox(
        "Selecione a Family",
        sorted([f for f in df["Family"].unique() if f.strip()])
    )

# 🔹 Fallback para garantir Subfamily
subfamilias_filtradas = df[df["Family"] == family]["Subfamily"].dropna().unique()
subfamilias_filtradas = sorted([s for s in subfamilias_filtradas if s.strip()])

with col2:
    if len(subfamilias_filtradas) == 0:
        st.warning("Nenhuma Subfamily encontrada para essa Family.")
        subfamily = ""
    else:
        subfamily = st.selectbox("Selecione a Subfamily", subfamilias_filtradas)

descricao = st.text_area(
    "✍️ Descreva brevemente suas atividades:",
    placeholder="Exemplo: Apoio no processamento de folha de pagamento, controle de ponto e benefícios..."
)

if st.button("🔍 Identificar Cargo"):
    if len(descricao.strip().split()) < 5:
        st.warning("Por favor, descreva suas atividades com um pouco mais de detalhes.")
        st.stop()

    st.info("🔎 Analisando sua descrição e comparando com cargos existentes...")

    # 🔹 Filtra Family/Subfamily
    subset = df[(df["Family"] == family)]
    if subfamily:
        subset = subset[subset["Subfamily"] == subfamily]

    if subset.empty:
        st.warning("Nenhum cargo encontrado para a Family/Subfamily selecionadas.")
        st.stop()

    # 🔹 Calcula similaridade
    model_embeddings = model.encode(subset["Merged_Text"].tolist(), convert_to_tensor=True)
    query_embedding = model.encode(descricao, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, model_embeddings)[0].cpu().numpy()

    subset["Score"] = scores
    subset = subset.sort_values("Score", ascending=False)

    # 🔹 Seleciona o mais compatível
    best = subset.iloc[0]
    similarity = float(best["Score"]) * 100
    gg = best["Grade"]
    job_title = best["Job Title"]

    # ------------------------------------------------------------
    # 🎯 RESULTADO FINAL
    # ------------------------------------------------------------
    st.markdown("## 🎯 Cargo mais compatível encontrado:")

    with st.container():
        st.markdown(f"""
        <div style="background-color:#f8f9ff; padding:20px; border-radius:12px; border-left:6px solid #3366ff; margin-bottom:20px;">
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
