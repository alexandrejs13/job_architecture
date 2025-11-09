import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from deep_translator import GoogleTranslator

# ==========================================================
# ⚙️ CONFIGURAÇÕES INICIAIS
# ==========================================================
st.set_page_config(page_title="🧩 Job Match", layout="wide")
st.markdown("## 🧩 Job Match")
st.markdown(
    "Encontre automaticamente o cargo mais compatível com base na **Family**, **Subfamily** e descrição detalhada de atividades."
)

# ==========================================================
# 📂 CARREGAMENTO E CACHE
# ==========================================================
@st.cache_data(show_spinner=False)
def load_data():
    try:
        df = pd.read_csv("data/Job Profile.csv", encoding="utf-8")
    except FileNotFoundError:
        df = pd.read_csv("Job Profile.csv", encoding="utf-8")

    df.columns = df.columns.str.strip()
    for col in ["Family", "Subfamily", "Job Title", "Grade"]:
        if col not in df.columns:
            st.error(f"Coluna ausente na base: {col}")
            st.stop()

    # Normaliza texto e converte grade
    df["Family"] = df["Family"].astype(str).str.strip().str.title()
    df["Subfamily"] = df["Subfamily"].astype(str).str.strip().str.title()
    df["Job Title"] = df["Job Title"].astype(str).str.strip()
    df["Grade"] = df["Grade"].astype(str).str.extract(r"(\d+)").fillna("0").astype(int)
    return df


@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer("paraphrase-MiniLM-L6-v2")


df = load_data()
model = load_model()

# ==========================================================
# 🧭 DETECÇÃO DE NÍVEL (senioridade)
# ==========================================================
LEVEL_KEYWORDS = {
    "estagiário": 1, "estágio": 1,
    "assistente": 3, "auxiliar": 3,
    "analista júnior": 4, "junior": 4,
    "analista pleno": 5, "pleno": 5,
    "analista sênior": 6, "senior": 6,
    "especialista": 7,
    "coordenador": 8, "supervisor": 8,
    "gerente": 10, "manager": 10,
    "diretor": 13, "head": 14
}

def detect_level(text):
    text_low = text.lower()
    for k, v in LEVEL_KEYWORDS.items():
        if k in text_low:
            return v
    return 6  # padrão = médio


# ==========================================================
# 🧠 PROCESSAMENTO DE BUSCA
# ==========================================================
def find_best_match(df, family, subfamily, description):
    if not family or not subfamily:
        st.warning("⚠️ É necessário selecionar **Family** e **Subfamily** antes de continuar.")
        return None

    if len(description.split()) < 50:
        st.warning("⚠️ A descrição deve conter pelo menos **50 palavras** para uma análise precisa.")
        return None

    df_filtered = df[(df["Family"] == family) & (df["Subfamily"] == subfamily)]
    if df_filtered.empty:
        st.error("Nenhum cargo encontrado para essa Family/Subfamily.")
        return None

    desc_en = GoogleTranslator(source="auto", target="en").translate(description)
    expected_grade = detect_level(description)

    query_emb = model.encode(desc_en, convert_to_tensor=True)
    texts = df_filtered["Job Profile Description"].fillna("").astype(str).tolist()
    corpus_emb = model.encode(texts, convert_to_tensor=True)

    scores = util.cos_sim(query_emb, corpus_emb)[0].cpu().numpy()
    df_filtered["similarity"] = scores

    df_filtered["adjusted"] = df_filtered.apply(
        lambda x: x["similarity"] - (abs(x["Grade"] - expected_grade) * 0.05),
        axis=1
    )

    best = df_filtered.sort_values("adjusted", ascending=False).iloc[0]
    return best


# ==========================================================
# 🎛️ INTERFACE
# ==========================================================
col1, col2 = st.columns(2)
with col1:
    family = st.selectbox("👨‍👩‍👧‍👦 Family:", sorted(df["Family"].unique()), index=None, placeholder="Selecione a Family")
with col2:
    subfamily = st.selectbox("🏷️ Subfamily:", sorted(df["Subfamily"].unique()), index=None, placeholder="Selecione a Subfamily")

st.markdown("✍️ **Descreva brevemente suas atividades:**")
example_text = (
    "Exemplo: Executar atividades operacionais e de apoio técnico relacionadas aos processos contábeis da empresa, "
    "assegurando o correto registro, classificação e conciliação das contas, conforme normas contábeis e políticas internas. "
    "Contribuir para a apuração de resultados, elaboração de demonstrações financeiras e cumprimento das obrigações fiscais e societárias, "
    "sob supervisão de profissionais mais experientes. Formação em Ciências Contábeis e até 3 anos de experiência."
)
description = st.text_area("", placeholder=example_text, height=180)

if st.button("🔍 Encontrar Job Match"):
    with st.spinner("Analisando descrição e buscando cargo compatível..."):
        result = find_best_match(df, family, subfamily, description)

    if result is not None:
        st.markdown("---")
        st.markdown(
            f"### {result['Subfamily']} / GG {result['Grade']} – {result['Job Title']}\n"
            f"**Família:** {result['Family']}\n"
            f"**Subfamília:** {result['Subfamily']}\n"
            f"**Carreira:** {result.get('Career', '-')}\n"
            f"**Função:** {result.get('Function', '-')}\n"
            f"**Disciplina:** {result.get('Discipline', '-')}\n"
            f"**Código:** {result.get('Code', '-')}\n"
        )

        def section(title, text):
            if pd.notna(text) and str(text).strip():
                st.markdown(f"### {title}")
                st.markdown(str(text).replace("|", "\n"))

        section("🧭 Sub Job Family Description", result.get("Sub Job Family Description", ""))
        section("🧠 Job Profile Description", result.get("Job Profile Description", ""))
        section("🎯 Role Description", result.get("Role Description", ""))
        section("🏅 Grade Differentiator", result.get("Grade Differentiator", ""))
        section("📊 KPIs / Specific Parameters", result.get("KPIs / Specific Parameters", ""))
        section("🎓 Qualifications", result.get("Qualifications", ""))
