# ==============================================================
# 🧩 Job Match — versão aprimorada com layout igual ao Job Profile Description
# ==============================================================

import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import re

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
            rename_map[c] = "KPIs / Specific Parameters"
        elif "qualification" in c_norm:
            rename_map[c] = "Qualifications"
        elif "career" in c_norm:
            rename_map[c] = "Career Path"
        elif "function" in c_norm:
            rename_map[c] = "Function Code"
        elif "discipline" in c_norm:
            rename_map[c] = "Discipline Code"
        elif "full job code" in c_norm or "job code" in c_norm:
            rename_map[c] = "Full Job Code"

    df.rename(columns=rename_map, inplace=True)

    obrig = [
        "Family", "Subfamily", "Job Title", "Grade",
        "Career Path", "Function Code", "Discipline Code", "Full Job Code",
        "Job Profile Description", "Role Description",
        "Grade Differentiator", "KPIs / Specific Parameters", "Qualifications"
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
            "Career Path", "Function Code", "Discipline Code",
            "Job Profile Description", "Role Description",
            "Grade Differentiator", "KPIs / Specific Parameters", "Qualifications"
        ]:
            val = row.get(col, "")
            if isinstance(val, str) and val.strip():
                parts.append(f"{col}: {val.strip()}")
        return " | ".join(parts)

    df["Merged_Text"] = df.apply(lambda r: safe_concat(r), axis=1)
    return df


# --------------------------------------------------------------
# Função para formatar parágrafos como no Job Profile Description
# --------------------------------------------------------------
def format_paragraphs(text):
    if not text:
        return "-"
    parts = re.split(r"\n+|•|\r", text.strip())
    return "".join(f"<p class='ja-p'>{p.strip()}</p>" for p in parts if len(p.strip()) > 2)


# --------------------------------------------------------------
# Carrega base e modelo
# --------------------------------------------------------------
df = load_data()
if df.empty:
    st.error("⚠️ A base está vazia ou corrompida.")
    st.stop()

model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# --------------------------------------------------------------
# CSS estilo Job Profile Description
# --------------------------------------------------------------
st.markdown("""
<style>
.css-1d391kg, .block-container {
  max-width: 1600px !important;
  min-width: 1600px !important;
  margin: 0 auto !important;
}
[data-testid="stSidebar"][aria-expanded="true"] {
  width: 320px !important;
  min-width: 320px !important;
}
.ja-p { margin: 0 0 6px 0; text-align: justify; }
.ja-hd { display:flex; align-items:baseline; gap:10px; margin:0 0 6px 0; }
.ja-hd-title { font-size:1.2rem; font-weight:700; color:#1E56E0; }
.ja-hd-grade { color:#1E56E0; font-weight:700; }
.ja-class {
  background:#fff; border:1px solid #e0e4f0; border-radius:8px;
  padding:10px; width:100%; display:inline-block;
}
.ja-sec-h { display:flex; align-items:center; gap:8px; margin:12px 0 4px 0 !important; }
.ja-ic { width:24px; text-align:center; line-height:1; }
.ja-ttl { font-weight:700; color:#1E56E0; font-size:1rem; }
.ja-card {
  background:#f9f9f9; padding:10px 14px; border-radius:8px;
  border-left:4px solid #1E56E0; box-shadow:0 1px 3px rgba(0,0,0,0.05);
  width:100%;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------
# Interface
# --------------------------------------------------------------
st.markdown("## 🧩 Job Match")
st.markdown("""
Descubra o **cargo mais compatível** com suas responsabilidades e experiência.  
O sistema analisa as **atividades descritas**, o **nível de senioridade** e as **características do cargo**.
""")

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

descricao = st.text_area(
    "✍️ Descreva brevemente suas atividades:",
    placeholder=(
        "Exemplo: Responsável pelo processamento de folha de pagamento, controle de ponto eletrônico, "
        "benefícios e obrigações legais (INSS, FGTS, IRRF). "
        "Graduado em Administração, com 5 anos de experiência na área de Departamento Pessoal."
    ),
    height=140
)

# --------------------------------------------------------------
# Botão de busca
# --------------------------------------------------------------
if st.button("🔍 Encontrar Job Profile"):
    if not family_selected or not subfamily_selected:
        st.warning("⚠️ Campos 'Family' e 'Subfamily' são obrigatórios.")
        st.stop()
    if len(descricao.split()) <= 10:
        st.warning("⚠️ Descreva suas atividades com mais detalhes (mínimo de 10 palavras).")
        st.stop()

    df_filtered = df[(df["Family"] == family_selected) & (df["Subfamily"] == subfamily_selected)].copy()
    if df_filtered.empty:
        st.error("Nenhum cargo encontrado nessa Family/Subfamily.")
        st.stop()

    q_emb = model.encode(descricao, convert_to_tensor=True)
    c_emb = model.encode(df_filtered["Merged_Text"].tolist(), convert_to_tensor=True)
    scores = util.cos_sim(q_emb, c_emb)[0].cpu().numpy()

    best_idx = int(np.argmax(scores))
    best = df_filtered.iloc[best_idx]
    best_score = round(float(scores[best_idx]) * 100, 1)

    # ----------------------------------------------------------
    # Exibe resultado formatado
    # ----------------------------------------------------------
    st.markdown("### 🎯 Cargo mais compatível encontrado")
    st.markdown(f"""
    <div class="ja-hd">
      <div class="ja-hd-title">{best['Job Title']}</div>
      <div class="ja-hd-grade">GG {best['Grade']}</div>
    </div>
    <div class="ja-class">
      <b>Família:</b> {best['Family']}<br>
      <b>Subfamília:</b> {best['Subfamily']}<br>
      <b>Carreira:</b> {best['Career Path']}<br>
      <b>Função:</b> {best['Function Code']}<br>
      <b>Disciplina:</b> {best['Discipline Code']}<br>
      <b>Código:</b> {best['Full Job Code']}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='ja-sec-h'><span class='ja-ic'>🧭</span><span class='ja-ttl'>Sub Job Family Description</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ja-card'>{format_paragraphs(best['Job Profile Description'])}</div>", unsafe_allow_html=True)

    st.markdown("<div class='ja-sec-h'><span class='ja-ic'>🧠</span><span class='ja-ttl'>Job Profile Description</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ja-card'>{format_paragraphs(best['Job Profile Description'])}</div>", unsafe_allow_html=True)

    st.markdown("<div class='ja-sec-h'><span class='ja-ic'>🎯</span><span class='ja-ttl'>Role Description</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ja-card'>{format_paragraphs(best['Role Description'])}</div>", unsafe_allow_html=True)

    st.markdown("<div class='ja-sec-h'><span class='ja-ic'>🏅</span><span class='ja-ttl'>Grade Differentiator</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ja-card'>{format_paragraphs(best['Grade Differentiator'])}</div>", unsafe_allow_html=True)

    st.markdown("<div class='ja-sec-h'><span class='ja-ic'>📊</span><span class='ja-ttl'>KPIs / Specific Parameters</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ja-card'>{format_paragraphs(best['KPIs / Specific Parameters'])}</div>", unsafe_allow_html=True)

    st.markdown("<div class='ja-sec-h'><span class='ja-ic'>🎓</span><span class='ja-ttl'>Qualifications</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ja-card'>{format_paragraphs(best['Qualifications'])}</div>", unsafe_allow_html=True)

else:
    st.info("Preencha as informações e clique em **🔍 Encontrar Job Profile**.")
