import streamlit as st
import pandas as pd
import numpy as np
import re
import unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.data_loader import load_data
from utils.ui_components import section

# ===============================================
# CONFIG
# ===============================================
st.set_page_config(layout="wide")
section("🧠 Find My Job Profile")

# ===============================================
# LIMPEZA DE TEXTO
# ===============================================
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    text = re.sub(r"[^a-z0-9áéíóúãõâêîôûç\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# ===============================================
# MERGE TEXT
# ===============================================
def merge_row_text(row):
    parts = [
        str(row.get("Sub Job Family Description", "")),
        str(row.get("Job Profile Description", "")),
        str(row.get("Role Description", "")),
        str(row.get("Grade Differentiator", "")) or str(row.get("Grade Differentiatior", "")),
        str(row.get("Specific parameters KPIs", "")) or str(row.get("Specific parameters / KPIs", "")),
        str(row.get("Qualifications", "")),
    ]
    return clean_text(" ".join([p for p in parts if p and p.lower() != "nan"]).strip())

# ===============================================
# LOAD DATA
# ===============================================
data = load_data()
if "job_profile" not in data:
    st.error("❌ Arquivo Job Profile.csv não encontrado em /data")
    st.stop()

df = data["job_profile"].copy()
df["merged_text"] = df.apply(merge_row_text, axis=1)

# ===============================================
# EMBEDDINGS TF-IDF
# ===============================================
@st.cache_data(show_spinner=False)
def generate_local_embeddings(df):
    corpus = df["merged_text"].tolist()
    vectorizer = TfidfVectorizer(
        analyzer="word",
        ngram_range=(1, 3),
        lowercase=True,
        min_df=1,
        max_df=0.95
    )
    X = vectorizer.fit_transform(corpus)
    return {"X": X, "vectorizer": vectorizer}

with st.spinner("🔄 Preparando base local para busca semântica..."):
    tfidf_pack = generate_local_embeddings(df)
st.success("✅ Base preparada localmente. (Sem uso de API)")

# ===============================================
# CAMPO DE BUSCA
# ===============================================
st.markdown("#### Descreva as atividades ou responsabilidades do cargo desejado:")
query = st.text_area(
    "Exemplo: Gerenciar folha de pagamento, processar encargos e liderar equipe de analistas.",
    height=120
)
buscar = st.button("🔍 Encontrar cargo correspondente", type="primary")

# ===============================================
# BUSCA SEMÂNTICA
# ===============================================
if buscar and query.strip():
    q_clean = clean_text(query)
    X = tfidf_pack["X"]
    vectorizer = tfidf_pack["vectorizer"]
    q = vectorizer.transform([q_clean])
    sims = cosine_similarity(q, X).ravel()
    idx = np.argsort(-sims)

    best = idx[0]
    score = float(sims[best])
    row = df.iloc[best]

    st.markdown("---")
    st.markdown(f"### 🎯 Cargo mais compatível: **{row.get('Job Profile','-')}**  "
                f"(similaridade: {score*100:.1f}%)")

    st.markdown(f"**Família:** {row.get('Job Family','')}")
    st.markdown(f"**Subfamília:** {row.get('Sub Job Family','')}")
    st.markdown(f"**Carreira:** {row.get('Career Path','')}")
    st.markdown(f"**Função:** {row.get('Function Code','')}")
    st.markdown(f"**Disciplina:** {row.get('Discipline Code','')}")
    st.markdown(f"**Código:** {row.get('Full Job Code','')}")

    st.markdown("### 🧭 Sub Job Family Description")
    st.write(row.get("Sub Job Family Description","-") or "-")

    st.markdown("### 🧠 Job Profile Description")
    st.write(row.get("Job Profile Description","-") or "-")

    st.markdown("### 🎯 Role Description")
    st.write(row.get("Role Description","-") or "-")

    st.markdown("### 🏅 Grade Differentiator")
    gd = row.get("Grade Differentiator","") or row.get("Grade Differentiatior","") or "-"
    st.write(gd)

    st.markdown("### 📊 KPIs / Specific Parameters")
    kp = row.get("Specific parameters KPIs","") or row.get("Specific parameters / KPIs","") or "-"
    st.write(kp)

    st.markdown("### 🎓 Qualifications")
    st.write(row.get("Qualifications","-") or "-")

elif buscar:
    st.warning("⚠️ Por favor, digite uma descrição para buscar o cargo correspondente.")
else:
    st.info("✏️ Digite uma descrição acima e clique em 'Encontrar cargo correspondente'.")
