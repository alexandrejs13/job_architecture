# ==============================================================
# 🧩 Job Match — Versão Final Corrigida
# ==============================================================
import streamlit as st
import pandas as pd
import numpy as np
import csv
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="🧩 Job Match", layout="wide")

# ==============================================================
# 1️⃣ Carregamento inteligente da base
# ==============================================================

@st.cache_data(show_spinner=False)
def load_data():
    path = "data/Job Profile.csv"

    try:
        df = pd.read_csv(path, sep=",", dtype=str, engine="python", on_bad_lines="skip")
    except Exception:
        df = pd.read_csv(path, sep=";", dtype=str, engine="python", on_bad_lines="skip")

    df = df.fillna("")

    # Normaliza todos os nomes de colunas (remove espaços, acentos e minúsculas)
    df.columns = (
        df.columns.str.strip()
        .str.replace("-", " ")
        .str.replace("_", " ")
        .str.replace("  ", " ")
        .str.lower()
    )

    # Detecta colunas equivalentes
    family_aliases = ["family", "job family", "jobfamily"]
    subfamily_aliases = ["subfamily", "sub family", "sub-family", "job subfamily", "job sub-family"]

    def find_col(possibles):
        for col in df.columns:
            if any(alias in col for alias in possibles):
                return col
        return None

    family_col = find_col(family_aliases)
    subfamily_col = find_col(subfamily_aliases)

    if not family_col:
        st.warning("⚠️ Coluna de Family não encontrada. Verifique o nome no CSV.")
        df["family"] = ""
    if not subfamily_col:
        st.warning("⚠️ Coluna de Subfamily não encontrada. Verifique o nome no CSV.")
        df["subfamily"] = ""

    # Padroniza nomes finais
    rename_map = {}
    if family_col:
        rename_map[family_col] = "Family"
    if subfamily_col:
        rename_map[subfamily_col] = "Subfamily"
    df.rename(columns=rename_map, inplace=True)

    # Garante colunas obrigatórias
    obrigatorias = [
        "Job Title", "Grade", "Sub Job Family Description", "Job Profile Description",
        "Role Description", "Grade Differentiator", "KPIs/Specific Parameters", "Qualifications"
    ]
    for col in obrigatorias:
        if col not in df.columns:
            df[col] = ""

    # Ajusta capitalização
    df["Family"] = df.get("Family", "").astype(str).str.strip().str.title()
    df["Subfamily"] = df.get("Subfamily", "").astype(str).str.strip().str.title()

    # Concatena texto de contexto semântico
    df["Merged_Text"] = (
        "Job Title: " + df["Job Title"].fillna("") +
        " | Family: " + df["Family"].fillna("") +
        " | Subfamily: " + df["Subfamily"].fillna("") +
        " | Grade: " + df["Grade"].fillna("") +
        " | Job Profile Description: " + df["Job Profile Description"].fillna("") +
        " | Role Description: " + df["Role Description"].fillna("") +
        " | Grade Differentiator: " + df["Grade Differentiator"].fillna("") +
        " | KPIs: " + df["KPIs/Specific Parameters"].fillna("")
    )

    return df


# ==============================================================
# 2️⃣ Carrega base e modelo
# ==============================================================

df = load_data()
if df.empty:
    st.error("⚠️ A base está vazia ou corrompida. Verifique o arquivo 'data/Job Profile.csv'.")
    st.stop()

model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# ==============================================================
# 3️⃣ Layout principal
# ==============================================================

st.markdown("## 🧩 Job Match")
st.write("""
Descubra o **cargo mais compatível** com suas responsabilidades e área de atuação.  
O sistema identifica automaticamente o **nível de senioridade** e o **escopo** com base no conteúdo da sua descrição.
""")

st.markdown("### 🧰 Parâmetros de busca")

col1, col2 = st.columns(2)

with col1:
    families = sorted([f for f in df["Family"].unique() if f])
    family_selected = st.selectbox("Selecione a Family", [""] + families)

with col2:
    if family_selected:
        subs = sorted(df[df["Family"] == family_selected]["Subfamily"].unique())
        if subs:
            subfamily_selected = st.selectbox("Selecione a Subfamily", [""] + subs)
        else:
            st.warning("⚠️ Nenhuma Subfamily encontrada para essa Family.")
            subfamily_selected = ""
    else:
        subfamily_selected = ""

st.markdown("### ✍️ Descreva brevemente suas atividades:")
descricao = st.text_area(
    "Exemplo: Apoio no processamento de folha de pagamento, controle de ponto e benefícios...",
    height=120,
    label_visibility="collapsed"
)

# ==============================================================
# 4️⃣ Processamento de busca
# ==============================================================

if st.button("🔍 Identificar Cargo"):
    if not family_selected or not descricao.strip():
        st.warning("⚠️ Preencha a Family e a descrição das atividades.")
        st.stop()

    df_filtered = df[df["Family"] == family_selected].copy()
    if subfamily_selected:
        df_filtered = df_filtered[df_filtered["Subfamily"] == subfamily_selected]

    if df_filtered.empty:
        st.error("Nenhum cargo encontrado nessa Family/Subfamily.")
        st.stop()

    query_emb = model.encode(descricao, convert_to_tensor=True)
    corpus_emb = model.encode(df_filtered["Merged_Text"].tolist(), convert_to_tensor=True)
    scores = util.cos_sim(query_emb, corpus_emb)[0].cpu().numpy()

    best_idx = int(np.argmax(scores))
    best_row = df_filtered.iloc[best_idx]
    best_score = round(float(scores[best_idx]) * 100, 1)

    st.markdown("### 🎯 Cargo mais compatível encontrado:")
    with st.container():
        st.markdown(f"### 🧩 **{best_row['Job Title']}**  \n**Grade:** {best_row['Grade']} — **Similaridade:** {best_score:.1f}%")
        st.markdown(f"**Family:** {best_row['Family']} | **Subfamily:** {best_row['Subfamily']}")

        st.markdown("#### 🧠 Job Profile Description")
        st.info(best_row['Job Profile Description'] or "—")

        st.markdown("#### 🎯 Role Description")
        st.info(best_row['Role Description'] or "—")

        st.markdown("#### ⚙️ Grade Differentiator")
        st.info(best_row['Grade Differentiator'] or "—")

        st.markdown("#### 📊 KPIs / Specific Parameters")
        st.info(best_row['KPIs/Specific Parameters'] or "—")

        st.markdown("#### 🎓 Qualifications")
        st.info(best_row['Qualifications'] or "—")

else:
    st.info("Preencha as informações e clique em **🔍 Identificar Cargo** para encontrar o Job Match mais compatível.")
