import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from utils.data_loader import load_excel_data

st.set_page_config(layout="wide", page_title="🧩 Job Match")

# === Estilo ===
st.markdown("""
<style>
.block-container {max-width: 1500px !important;}
.job-card {
  background: #f9fafc;
  border-left: 5px solid #1E56E0;
  border-radius: 10px;
  padding: 15px 20px;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.job-card h4 {color: #1E56E0; margin-bottom: 0.3rem;}
.job-card small {color: #555;}
</style>
""", unsafe_allow_html=True)

# === Carrega dados ===
@st.cache_data(show_spinner=False)
def load_data():
    data = load_excel_data()
    return data.get("job_profile", pd.DataFrame()), data.get("level_structure", pd.DataFrame())

@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

df, levels = load_data()
model = load_model()

for c in ["Job Family", "Sub Job Family", "Job Profile", "Role Description", "Grade Differentiator",
          "KPIs / Specific Parameters", "Qualifications", "Global Grade"]:
    if c not in df.columns:
        df[c] = ""

df["Global Grade"] = df["Global Grade"].astype(str).str.extract(r"(\d+)").fillna("0").astype(int)

# === Interface ===
st.markdown("## 🧩 Job Match")
col1, col2 = st.columns([2, 2])
with col1:
    families = sorted(df["Job Family"].dropna().unique())
    family = st.selectbox("Família", ["Selecione..."] + families)
with col2:
    if family != "Selecione...":
        subfamilies = sorted(df[df["Job Family"] == family]["Sub Job Family"].dropna().unique())
    else:
        subfamilies = []
    subfamily = st.selectbox("Subfamília", ["Selecione..."] + subfamilies)

desc = st.text_area(
    "✍️ Descreva brevemente suas atividades:",
    placeholder="Exemplo: Responsável por lançamentos contábeis, conciliações, apoio no fechamento financeiro e relatórios. Graduação em Contabilidade e 3 anos de experiência.",
    height=160
)

# === Lógica ===
if st.button("🔍 Encontrar Job Match"):
    if family == "Selecione..." or subfamily == "Selecione...":
        st.warning("⚠️ Família e Subfamília são obrigatórias.")
        st.stop()

    if len(desc.split()) < 50:
        st.warning("⚠️ Descrição deve conter pelo menos 50 palavras.")
        st.stop()

    base = df[(df["Job Family"] == family) & (df["Sub Job Family"] == subfamily)].copy()
    if base.empty:
        st.error("Nenhum cargo encontrado nesta Família/Subfamília.")
        st.stop()

    base["Combined"] = (
        base["Role Description"].fillna("") + " " +
        base["Grade Differentiator"].fillna("") + " " +
        base["KPIs / Specific Parameters"].fillna("") + " " +
        base["Qualifications"].fillna("")
    )

    query_emb = model.encode([desc])
    job_embs = model.encode(base["Combined"].tolist())
    sims = cosine_similarity(query_emb, job_embs)[0]
    base["Similarity"] = sims

    avg_grade = base["Global Grade"].median()
    base["Grade_Penalty"] = (abs(base["Global Grade"] - avg_grade) / 10)
    base["Adjusted_Sim"] = base["Similarity"] - base["Grade_Penalty"]

    best = base.sort_values("Adjusted_Sim", ascending=False).head(1).iloc[0]
    level_name = "-"
    if not levels.empty and best["Global Grade"] in levels["Global Grade"].values:
        level_name = levels.loc[levels["Global Grade"] == best["Global Grade"], "Level Name"].squeeze()

    st.success("Cargo mais compatível encontrado:")
    st.markdown(f"""
    <div class='job-card'>
        <h4>GG {best['Global Grade']} — {level_name} — {best['Job Profile']}</h4>
        <small><b>Família:</b> {best['Job Family']} | <b>Subfamília:</b> {best['Sub Job Family']}</small><br>
        <small><b>Carreira:</b> {best.get('Career Path', '-')} | <b>Código:</b> {best.get('Full Job Code', '-')}</small>
        <hr>
        <b>🎯 Role Description</b><br>{best['Role Description']}<br><br>
        <b>🏅 Grade Differentiator</b><br>{best['Grade Differentiator']}<br><br>
        <b>📊 KPIs / Specific Parameters</b><br>{best['KPIs / Specific Parameters']}<br><br>
        <b>🎓 Qualifications</b><br>{best['Qualifications']}
    </div>
    """, unsafe_allow_html=True)
