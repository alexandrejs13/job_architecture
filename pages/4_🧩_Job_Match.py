import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from utils.data_loader import load_excel_data

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="🧩 Job Match")

st.markdown("""
<style>
.block-container {max-width: 1500px !important;}
h1 {color: #1E56E0; font-weight: 800;}
.job-card {
    background: #f9fafc;
    border-left: 5px solid #1E56E0;
    border-radius: 10px;
    padding: 15px 20px;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.job-card h4 {
    color: #1E56E0;
    margin-bottom: 0.3rem;
}
.job-card small {
    color: #555;
}
.job-card button {
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# FUNÇÃO DE CARGA
# ===========================================================
@st.cache_data(show_spinner=False)
def load_data():
    data = load_excel_data()
    if "job_profile" not in data:
        st.error("⚠️ Arquivo 'Job Profile.xlsx' não encontrado.")
        st.stop()
    return data["job_profile"]

# ===========================================================
# EMBEDDINGS
# ===========================================================
@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

model = load_model()
df = load_data()

# Normaliza colunas
for c in ["Job Family", "Sub Job Family", "Job Profile", "Role Description", "Grade Differentiator",
          "KPIs / Specific Parameters", "Qualifications", "Global Grade"]:
    if c not in df.columns:
        df[c] = ""

df["Global Grade"] = df["Global Grade"].astype(str).str.extract(r"(\d+)").fillna("0").astype(int)

# ===========================================================
# INTERFACE
# ===========================================================
st.markdown("## 🧩 Job Match")
st.markdown("""
Selecione a Família e Subfamília, depois descreva suas atividades.  
O sistema encontrará automaticamente o cargo mais compatível dentro da estrutura de cargos.
""")

col1, col2 = st.columns([2, 2])
with col1:
    families = sorted(df["Job Family"].dropna().unique().tolist())
    family = st.selectbox("Família", ["Selecione..."] + families)
with col2:
    if family != "Selecione...":
        subfamilies = sorted(df[df["Job Family"] == family]["Sub Job Family"].dropna().unique().tolist())
    else:
        subfamilies = []
    subfamily = st.selectbox("Subfamília", ["Selecione..."] + subfamilies)

desc = st.text_area(
    "✍️ Descreva brevemente suas atividades:",
    placeholder=(
        "Exemplo: Responsável por realizar lançamentos contábeis, conciliações de contas, apoio na "
        "elaboração de demonstrações financeiras e fechamento mensal. Graduação em Ciências Contábeis "
        "com 3 anos de experiência na área."
    ),
    height=160
)

# ===========================================================
# VALIDAÇÕES
# ===========================================================
if st.button("🔍 Encontrar Job Match"):
    if family == "Selecione..." or subfamily == "Selecione...":
        st.warning("⚠️ Por favor, selecione Família e Subfamília antes de continuar.")
        st.stop()

    word_count = len(desc.split())
    if word_count < 50:
        st.warning("⚠️ Por favor, descreva suas atividades com pelo menos 50 palavras para uma análise precisa.")
        st.stop()

    with st.spinner("🔎 Analisando compatibilidade..."):
        # Filtra base
        base = df[(df["Job Family"] == family) & (df["Sub Job Family"] == subfamily)].copy()

        if base.empty:
            st.error("Nenhum cargo encontrado nesta Família/Subfamília.")
            st.stop()

        # Prepara texto composto das descrições relevantes
        base["Combined"] = (
            base["Role Description"].fillna("") + " " +
            base["Grade Differentiator"].fillna("") + " " +
            base["KPIs / Specific Parameters"].fillna("") + " " +
            base["Qualifications"].fillna("")
        )

        # Cria embeddings
        query_emb = model.encode([desc])
        job_embs = model.encode(base["Combined"].tolist())

        # Similaridade
        sims = cosine_similarity(query_emb, job_embs)[0]
        base["Similarity"] = sims

        # Aplica coerência por grade
        avg_grade = base["Global Grade"].median()
        base["Grade_Penalty"] = (abs(base["Global Grade"] - avg_grade) / 10)
        base["Adjusted_Sim"] = base["Similarity"] - base["Grade_Penalty"]

        best = base.sort_values("Adjusted_Sim", ascending=False).head(1).iloc[0]

    # =======================================================
    # RESULTADO
    # =======================================================
    st.success(f"Cargo mais compatível encontrado com base em Family/Subfamily e descrição detalhada:")
    with st.container():
        st.markdown(f"""
        <div class='job-card'>
            <h4>GG {best['Global Grade']} — {best['Job Profile']}</h4>
            <small><b>Família:</b> {best['Job Family']} | <b>Subfamília:</b> {best['Sub Job Family']}</small><br>
            <small><b>Carreira:</b> {best.get('Career Path', '-')} | <b>Código:</b> {best.get('Full Job Code', '-')}</small>
            <hr>
            <b>🎯 Role Description</b><br>{best['Role Description']}<br><br>
            <b>🏅 Grade Differentiator</b><br>{best['Grade Differentiator']}<br><br>
            <b>📊 KPIs / Specific Parameters</b><br>{best['KPIs / Specific Parameters']}<br><br>
            <b>🎓 Qualifications</b><br>{best['Qualifications']}
        </div>
        """, unsafe_allow_html=True)
