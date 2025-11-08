import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from deep_translator import GoogleTranslator
from utils.data_loader import load_data
from utils.ui_components import section

# ===============================================
# CONFIG
# ===============================================
st.set_page_config(layout="wide")
section("🧠 Find My Job Profile")

# ===============================================
# CARREGAR BASE
# ===============================================
data = load_data()
if "job_profile" not in data:
    st.error("❌ Arquivo Job Profile.csv não encontrado em /data")
    st.stop()

df = data["job_profile"].copy()

def merge_row_text(row):
    parts = [
        str(row.get("Sub Job Family Description", "")),
        str(row.get("Job Profile Description", "")),
        str(row.get("Role Description", "")),
        str(row.get("Grade Differentiator", "")) or str(row.get("Grade Differentiatior", "")),
        str(row.get("Specific parameters KPIs", "")) or str(row.get("Specific parameters / KPIs", "")),
        str(row.get("Qualifications", "")),
    ]
    return " ".join([p for p in parts if p and p.lower() != "nan"]).strip()

df["merged_text"] = df.apply(merge_row_text, axis=1)

# ===============================================
# EMBEDDINGS SEMÂNTICOS
# ===============================================
@st.cache_resource(show_spinner=True)
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_data(show_spinner=False)
def generate_embeddings(df):
    model = load_model()
    embeddings = model.encode(df["merged_text"].tolist(), show_progress_bar=False, normalize_embeddings=True)
    return embeddings

with st.spinner("🔄 Preparando base semântica local..."):
    matrix = generate_embeddings(df)
st.success("✅ Base semântica pronta.")

# ===============================================
# FUNÇÃO DE TRADUÇÃO
# ===============================================
def translate_to_english(text):
    try:
        translated = GoogleTranslator(source="auto", target="en").translate(text)
        return translated
    except Exception as e:
        st.warning(f"⚠️ Falha ao traduzir automaticamente: {e}")
        return text

# ===============================================
# INTERFACE DE BUSCA
# ===============================================
st.markdown("#### Descreva as atividades ou responsabilidades do cargo desejado (em qualquer idioma):")
query = st.text_area(
    "Exemplo: Gerenciar folha de pagamento, processar encargos e liderar equipe de analistas.",
    height=120
)
buscar = st.button("🔍 Encontrar cargo correspondente", type="primary")

# ===============================================
# BUSCA
# ===============================================
if buscar and query.strip():
    with st.spinner("🌐 Traduzindo e analisando a descrição..."):
        translated_query = translate_to_english(query)

    model = load_model()
    q_emb = model.encode([translated_query], normalize_embeddings=True)
    sims = cosine_similarity(q_emb, matrix).ravel()
    idx = np.argsort(-sims)

    # Mostrar top 3
    st.markdown("---")
    st.subheader("🎯 Cargos mais compatíveis:")

    for rank, i in enumerate(idx[:3], start=1):
        row = df.iloc[i]
        score = sims[i] * 100
        st.markdown(f"**{rank}. {row.get('Job Profile','-')}** — Similaridade: **{score:.1f}%**")
        with st.expander("Ver detalhes"):
            st.markdown(f"**Família:** {row.get('Job Family','')}")
            st.markdown(f"**Subfamília:** {row.get('Sub Job Family','')}")
            st.markdown(f"**Carreira:** {row.get('Career Path','')}")
            st.markdown(f"**Função:** {row.get('Function Code','')}")
            st.markdown(f"**Disciplina:** {row.get('Discipline Code','')}")
            st.markdown(f"**Código:** {row.get('Full Job Code','')}")
            st.markdown("**Job Profile Description:**")
            st.write(row.get("Job Profile Description","-") or "-")
            st.markdown("**Role Description:**")
            st.write(row.get("Role Description","-") or "-")
            st.markdown("**Qualifications:**")
            st.write(row.get("Qualifications","-") or "-")

elif buscar:
    st.warning("⚠️ Por favor, digite uma descrição para buscar o cargo correspondente.")
else:
    st.info("✏️ Digite uma descrição acima e clique em 'Encontrar cargo correspondente'.")
