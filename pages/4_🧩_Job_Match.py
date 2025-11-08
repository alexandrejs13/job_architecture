# ==============================================================
# 🧩 Job Match — versão estável e com layout aprimorado
# ==============================================================

import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util

# --------------------------------------------------------------
# Configuração da página
# --------------------------------------------------------------
st.set_page_config(page_title="🧩 Job Match", layout="wide")

# --------------------------------------------------------------
# Função para carregar a base
# --------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data():
    path = "data/Job Profile.csv"

    try:
        df = pd.read_csv(path, sep=None, engine="python", dtype=str, on_bad_lines="skip")
    except Exception:
        df = pd.read_csv(path, sep=";", engine="python", dtype=str, on_bad_lines="skip")

    # Limpeza e normalização
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.duplicated(keep="first")]
    df = df.fillna("")

    rename_map = {}
    for c in df.columns:
        c_norm = c.strip().lower()
        if c_norm == "job family":
            rename_map[c] = "Family"
        elif c_norm == "sub job family":
            rename_map[c] = "Subfamily"
        elif c_norm == "job profile":
            rename_map[c] = "Job Title"
        elif "grade" in c_norm:
            rename_map[c] = "Grade"
        elif "profile description" in c_norm:
            rename_map[c] = "Job Profile Description"
        elif "role description" in c_norm:
            rename_map[c] = "Role Description"
        elif "differentiator" in c_norm:
            rename_map[c] = "Grade Differentiator"
        elif "kpi" in c_norm or "specific" in c_norm:
            rename_map[c] = "KPIs/Specific Parameters"
        elif "qualification" in c_norm:
            rename_map[c] = "Qualifications"

    df.rename(columns=rename_map, inplace=True)

    obrig = [
        "Family", "Subfamily", "Job Title", "Grade",
        "Job Profile Description", "Role Description",
        "Grade Differentiator", "KPIs/Specific Parameters", "Qualifications"
    ]
    for c in obrig:
        if c not in df.columns:
            df[c] = ""

    df["Family"] = df["Family"].astype(str).str.strip().str.title()
    df["Subfamily"] = df["Subfamily"].astype(str).str.strip().str.title()

    def safe_concat(row):
        parts = []
        for col in [
            "Job Title", "Family", "Subfamily", "Grade",
            "Job Profile Description", "Role Description",
            "Grade Differentiator", "KPIs/Specific Parameters", "Qualifications"
        ]:
            val = row.get(col, "")
            if isinstance(val, str) and val.strip():
                parts.append(f"{col}: {val.strip()}")
        return " | ".join(parts)

    df["Merged_Text"] = df.apply(lambda r: safe_concat(r), axis=1)
    return df

# --------------------------------------------------------------
# Carrega base e modelo
# --------------------------------------------------------------
df = load_data()
if df.empty:
    st.error("⚠️ A base está vazia ou corrompida.")
    st.stop()

model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# --------------------------------------------------------------
# Layout
# --------------------------------------------------------------
st.markdown("## 🧩 Job Match")
st.markdown("""
Descubra o **cargo mais compatível** com suas responsabilidades e área de atuação.  
O sistema identifica automaticamente o **nível de senioridade** e o **escopo** com base na descrição das suas atividades.
""")

# Seleção Family/Subfamily
c1, c2 = st.columns(2)
families = sorted(df.loc[df["Family"].ne(""), "Family"].unique().tolist())
family_selected = c1.selectbox("Selecione a Family", [""] + families)

if family_selected:
    subs = (
        df.loc[(df["Family"] == family_selected) & (df["Subfamily"].ne("")), "Subfamily"]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )
else:
    subs = []

subfamily_selected = c2.selectbox(
    "Selecione a Subfamily",
    [""] + subs if subs else [""],
    disabled=(not family_selected)
)

# Campo de descrição
descricao = st.text_area(
    "✍️ Descreva brevemente suas atividades:",
    placeholder="Exemplo: Apoio no processamento de folha de pagamento, controle de ponto e benefícios...",
    height=120
)

# --------------------------------------------------------------
# Botão de busca
# --------------------------------------------------------------
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
        st.markdown(f"**Family:** {best['Family']} | **Subfamily:** {best['Subfamily']}  \n**Similaridade:** {best_score:.1f}%")

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
    st.info("Preencha as informações e clique em **🔍 Identificar Cargo**.")
