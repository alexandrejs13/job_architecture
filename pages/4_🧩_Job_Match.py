# ==============================================================
# 🧩 Job Match — correção final: garante Subfamily sempre existente
# ==============================================================

import streamlit as st
import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="🧩 Job Match", layout="wide")

# -------------------------------
# Função utilitária de normalização
# -------------------------------
def _norm(s: str) -> str:
    if not isinstance(s, str):
        s = str(s)
    s = s.strip().lower()
    acentos = (("áàâãä", "a"), ("éèêë", "e"), ("íìîï", "i"), ("óòôõö", "o"), ("úùûü", "u"), ("ç", "c"))
    for grupo, rep in acentos:
        for ch in grupo:
            s = s.replace(ch, rep)
    s = re.sub(r"[^a-z0-9]", "", s)
    return s

COL_MAP_CANON = {
    "jobfamily": "Family",
    "subjobfamily": "Subfamily",
    "subfamily": "Subfamily",
    "subjobfamilydescription": "Sub Job Family Description",
    "jobprofile": "Job Title",
    "jobtitle": "Job Title",
    "globalgrade": "Grade",
    "grade": "Grade",
    "careerpath": "Career Path",
    "jobprofiledescription": "Job Profile Description",
    "roledescription": "Role Description",
    "gradedifferentiator": "Grade Differentiator",
    "gradedifferentiatior": "Grade Differentiator",
    "specificparameterskpis": "KPIs/Specific Parameters",
    "specificparameters": "KPIs/Specific Parameters",
    "qualifications": "Qualifications",
}

OBRIGATORIAS = [
    "Family", "Subfamily", "Job Title", "Grade",
    "Job Profile Description", "Role Description",
    "Grade Differentiator", "KPIs/Specific Parameters", "Qualifications"
]

# -------------------------------
# Carregamento da base
# -------------------------------
@st.cache_data(show_spinner=False)
def load_data():
    path = "data/Job Profile.csv"

    try:
        df = pd.read_csv(path, sep=None, engine="python", dtype=str, on_bad_lines="skip")
    except Exception:
        df = pd.read_csv(path, sep=";", engine="python", dtype=str, on_bad_lines="skip")

    df = df.fillna("")

    # Normaliza e renomeia colunas conhecidas
    norm2orig = {_norm(c): c for c in df.columns}
    rename_map = {}
    for norm_src, canon_dst in COL_MAP_CANON.items():
        if norm_src in norm2orig:
            rename_map[norm2orig[norm_src]] = canon_dst
    if rename_map:
        df.rename(columns=rename_map, inplace=True)

    # Garante colunas obrigatórias (cria se não existirem)
    for col in OBRIGATORIAS:
        if col not in df.columns:
            df[col] = ""

    # Normaliza Family/Subfamily
    df["Family"] = df["Family"].astype(str).str.strip().str.title()
    df["Subfamily"] = df["Subfamily"].astype(str).str.strip().str.title()

    # Fallback: se Subfamily está vazia, tenta preencher pela descrição
    if df["Subfamily"].eq("").all():
        for alt in ["Sub Job Family Description", "Sub Job Family"]:
            if alt in df.columns:
                df["Subfamily"] = (
                    df[alt].astype(str)
                    .str.extract(r"^([A-Za-z\s\-]+)")[0]
                    .fillna("")
                    .str.strip()
                    .str.title()
                )
                break

    # Concatenação semântica
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
# Layout principal
# ==============================================================

df = load_data()
if df.empty:
    st.error("⚠️ A base está vazia ou corrompida.")
    st.stop()

model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

st.markdown("## 🧩 Job Match")

# Filtros (Family e Subfamily)
c1, c2 = st.columns(2)
with c1:
    families = sorted(df.loc[df["Family"].ne(""), "Family"].unique().tolist())
    family_selected = st.selectbox("Selecione a Family", [""] + families)

with c2:
    if family_selected:
        subs = (
            df.loc[(df["Family"] == family_selected) & (df["Subfamily"].ne("")), "Subfamily"]
            .drop_duplicates()
            .sort_values()
            .tolist()
        )
        subfamily_selected = st.selectbox("Selecione a Subfamily", [""] + subs) if subs else ""
    else:
        subfamily_selected = ""

# Texto explicativo e entrada
st.write("""
Descubra o **cargo mais compatível** com suas responsabilidades e área de atuação.  
O sistema identifica automaticamente o **nível de senioridade** e o **escopo** com base na descrição das suas atividades.
""")

descricao = st.text_area(
    "✍️ Descreva brevemente suas atividades:",
    placeholder="Exemplo: Apoio no processamento de folha de pagamento, controle de ponto e benefícios...",
    height=120
)

# ==============================================================
# Busca e exibição
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

    q_emb = model.encode(descricao, convert_to_tensor=True)
    c_emb = model.encode(df_filtered["Merged_Text"].tolist(), convert_to_tensor=True)
    scores = util.cos_sim(q_emb, c_emb)[0].cpu().numpy()

    best_idx = int(np.argmax(scores))
    best = df_filtered.iloc[best_idx]
    best_score = round(float(scores[best_idx]) * 100, 1)

    st.markdown("### 🎯 Cargo mais compatível encontrado")
    with st.container():
        st.markdown(f"### **GG {best['Grade']} — {best['Job Title']}**")
        st.markdown(f"**Family:** {best['Family']} | **Subfamily:** {best['Subfamily']}")
        st.markdown(f"**Similaridade:** {best_score:.1f}%")

        st.markdown("#### 🧠 Job Profile Description")
        st.info(best["Job Profile Description"] or "—")

        st.markdown("#### 🎯 Role Description")
        st.info(best["Role Description"] or "—")

        st.markdown("#### 🏅 Grade Differentiator")
        st.info(best["Grade Differentiator"] or "—")

        st.markdown("#### 📊 KPIs / Specific Parameters")
        st.info(best["KPIs/Specific Parameters"] or "—")

        st.markdown("#### 🎓 Qualifications")
        st.info(best["Qualifications"] or "—")

else:
    st.info("Preencha os campos e clique em **🔍 Identificar Cargo**.")
