# ==============================================================
# 🧩 Job Match — Versão Corrigida (Family/Subfamily fix + layout limpo)
# ==============================================================

import streamlit as st
import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="🧩 Job Match", layout="wide")


# ==============================================================
# 1️⃣ Função para carregar base
# ==============================================================

@st.cache_data(show_spinner=False)
def load_data():
    path = "data/Job Profile.csv"

    try:
        df = pd.read_csv(path, sep=",", dtype=str, engine="python", on_bad_lines="skip")
    except Exception:
        df = pd.read_csv(path, sep=";", dtype=str, engine="python", on_bad_lines="skip")

    df = df.fillna("")

    # Normaliza nomes das colunas
    normalized_cols = {re.sub(r'[^a-zA-Z0-9]', '', c.strip().lower()): c for c in df.columns}

    def match_col(possibles):
        for key, val in normalized_cols.items():
            for p in possibles:
                if re.search(p, key):
                    return val
        return None

    # Detecta Family/Subfamily independentemente da grafia
    family_col = match_col(["family", "jobfamily"])
    subfamily_col = match_col(["subfamily", "subfamily", "subjobfamily"])

    # Cria ou renomeia colunas
    if family_col:
        df.rename(columns={family_col: "Family"}, inplace=True)
    else:
        df["Family"] = ""

    if subfamily_col:
        df.rename(columns={subfamily_col: "Subfamily"}, inplace=True)
    else:
        df["Subfamily"] = ""

    # Normaliza capitalização
    df["Family"] = df["Family"].astype(str).str.strip().str.title()
    df["Subfamily"] = df["Subfamily"].astype(str).str.strip().str.title()

    # Garante colunas obrigatórias
    obrigatorias = [
        "Job Title", "Grade", "Sub Job Family Description", "Job Profile Description",
        "Role Description", "Grade Differentiator", "KPIs/Specific Parameters", "Qualifications"
    ]
    for col in obrigatorias:
        if col not in df.columns:
            df[col] = ""

    # Texto semântico
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
O sistema identifica automaticamente o **nível de senioridade** e o **escopo** com base na descrição das suas atividades.
""")

col1, col2 = st.columns(2)

with col1:
    families = sorted([f for f in df["Family"].unique() if f])
    family_selected = st.selectbox("Selecione a Family", [""] + families)

with col2:
    if family_selected:
        sub_opts = sorted(df[df["Family"] == family_selected]["Subfamily"].unique())
        if len(sub_opts) > 0:
            subfamily_selected = st.selectbox("Selecione a Subfamily", [""] + sub_opts)
        else:
            subfamily_selected = ""
    else:
        subfamily_selected = ""

# Caixa de texto padrão estilo Streamlit
descricao = st.text_area(
    "✍️ Descreva brevemente suas atividades:",
    placeholder="Exemplo: Apoio no processamento de folha de pagamento, controle de ponto e benefícios...",
    height=120
)

# ==============================================================
# 4️⃣ Processamento da busca
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
