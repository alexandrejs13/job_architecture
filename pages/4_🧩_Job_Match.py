# ==============================================================
# 🧩 Job Match — Versão definitiva (mapeamento exato de colunas)
# ==============================================================

import streamlit as st
import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="🧩 Job Match", layout="wide")

# -------------------------------
# Util: normalização de cabeçalhos
# -------------------------------
def _norm(s: str) -> str:
    """
    Normaliza nomes de colunas: minúsculas, remove acentos e tudo que não for [a-z0-9].
    Ex.: "Sub Job Family " -> "subjobfamily"
    """
    if not isinstance(s, str):
        s = str(s)
    s = s.strip().lower()
    # troca acentos básicos
    acentos = (("áàâãä", "a"), ("éèêë", "e"), ("íìîï", "i"), ("óòôõö", "o"), ("úùûü", "u"), ("ç", "c"))
    for grupo, rep in acentos:
        for ch in grupo:
            s = s.replace(ch, rep)
    s = re.sub(r"[^a-z0-9]", "", s)  # remove separadores
    return s

# -------------------------------
# Colunas que queremos (mapeamento exato por nome normalizado)
# -------------------------------
# Base real do seu CSV (pelos exemplos que você mandou):
# "Job Family", "Sub Job Family", "Job Profile", "Function Code", "Discipline Code",
# "Career Path", "Global Grade", "Sub Job Family Description", "Job Profile Description",
# "Role Description", "Grade Differentiatior", "Qualifications", "Specific parameters KPIs"
COL_MAP_CANON = {
    # origem normalizada -> destino padronizado
    "jobfamily": "Family",
    "subjobfamily": "Subfamily",
    "jobprofile": "Job Title",
    "jobtitle": "Job Title",
    "globalgrade": "Grade",
    "grade": "Grade",

    "functioncode": "Function Code",
    "disciplinecode": "Discipline Code",
    "careerpath": "Career Path",

    "subjobfamilydescription": "Sub Job Family Description",
    "jobprofiledescription": "Job Profile Description",
    "roledescription": "Role Description",

    # variações de escrita do CSV
    "gradedifferentiatior": "Grade Differentiator",  # (com erro de grafia no CSV)
    "gradedifferentiator": "Grade Differentiator",
    "gradedifferentiators": "Grade Differentiator",

    # KPIs
    "specificparameterskpis": "KPIs/Specific Parameters",
    "specificparameterskpiss": "KPIs/Specific Parameters",
    "specificparameters": "KPIs/Specific Parameters",
    "kpisspecificparameters": "KPIs/Specific Parameters",

    "qualifications": "Qualifications",
}

OBRIGATORIAS = [
    "Family", "Subfamily", "Job Title", "Grade",
    "Sub Job Family Description", "Job Profile Description", "Role Description",
    "Grade Differentiator", "KPIs/Specific Parameters", "Qualifications"
]

# -------------------------------
# Carregamento robusto de base
# -------------------------------
@st.cache_data(show_spinner=False)
def load_data():
    path = "data/Job Profile.csv"

    # Tenta detectar separador automaticamente
    try:
        df = pd.read_csv(path, sep=None, engine="python", dtype=str, on_bad_lines="skip")
    except Exception:
        # fallback para vírgula
        try:
            df = pd.read_csv(path, sep=",", engine="python", dtype=str, on_bad_lines="skip")
        except Exception:
            # fallback para ponto e vírgula
            df = pd.read_csv(path, sep=";", engine="python", dtype=str, on_bad_lines="skip")

    df = df.fillna("")

    # Cria mapa: normalizado -> original
    norm2orig = {_norm(c): c for c in df.columns}

    # Monta renomeação exata (apenas quando existir normalizado no CSV)
    rename_map = {}
    for norm_src, canon_dst in COL_MAP_CANON.items():
        if norm_src in norm2orig:
            rename_map[norm2orig[norm_src]] = canon_dst

    # Renomeia o que encontrou
    if rename_map:
        df = df.rename(columns=rename_map)

    # Garante existência das obrigatórias (evita KeyError)
    for col in OBRIGATORIAS:
        if col not in df.columns:
            df[col] = ""

    # Normaliza capitalização de Family/Subfamily
    df["Family"] = df["Family"].astype(str).str.strip().str.title()
    df["Subfamily"] = df["Subfamily"].astype(str).str.strip().str.title()

    # Texto semântico consolidado (para comparar)
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

# -------------------------------
# Carrega base e modelo
# -------------------------------
df = load_data()
if df.empty:
    st.error("⚠️ A base está vazia ou corrompida. Verifique 'data/Job Profile.csv'.")
    st.stop()

# Se Family/Subfamily não existirem de fato, não segue (evita pick list louca)
if df["Family"].eq("").all():
    st.error("⚠️ Coluna 'Job Family' não foi localizada no CSV. Confirme o cabeçalho exato.")
    st.stop()

# Modelo local leve e rápido
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# -------------------------------
# UI
# -------------------------------
st.markdown("## 🧩 Job Match")

# Filtros (com listas estritamente derivadas das colunas corretas)
c1, c2 = st.columns(2)
with c1:
    families = sorted(df.loc[df["Family"].ne(""), "Family"].unique().tolist())
    family_selected = st.selectbox("Selecione a Family", [""] + families)

with c2:
    if family_selected:
        subs = df.loc[(df["Family"] == family_selected) & (df["Subfamily"].ne("")), "Subfamily"].unique().tolist()
        subs = sorted(subs)
        subfamily_selected = st.selectbox("Selecione a Subfamily", [""] + subs) if subs else ""
    else:
        subfamily_selected = ""

descricao = st.text_area(
    "✍️ Descreva brevemente suas atividades:",
    placeholder="Ex.: Apoio no processamento de folha de pagamento, controle de ponto e benefícios…",
    height=120
)

# -------------------------------
# Busca
# -------------------------------
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

    # Embeddings e similaridade
    q_emb = model.encode(descricao, convert_to_tensor=True)
    c_emb = model.encode(df_filtered["Merged_Text"].tolist(), convert_to_tensor=True)
    scores = util.cos_sim(q_emb, c_emb)[0].cpu().numpy()

    best_idx = int(np.argmax(scores))
    best = df_filtered.iloc[best_idx]
    best_score = round(float(scores[best_idx]) * 100, 1)

    # Resultado (estrutura igual ao Job Profile Description)
    st.markdown("### 🎯 Cargo mais compatível encontrado")
    with st.container():
        st.markdown(f"### **GG {best['Grade']} — {best['Job Title']}**")
        st.markdown(f"**Family:** {best['Family']} | **Subfamily:** {best['Subfamily']}")

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
