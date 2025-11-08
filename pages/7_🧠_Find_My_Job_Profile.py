import streamlit as st
import pandas as pd
import numpy as np
import os, re, time
from openai import OpenAI
from utils.data_loader import load_data
from utils.ui_components import section
from sklearn.metrics.pairwise import cosine_similarity

# ===========================================================
# CONFIGURAÇÃO E INICIALIZAÇÃO
# ===========================================================
st.set_page_config(layout="wide")
section("🧠 Find My Job Profile")

# --- Validação da chave ---
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ Chave da OpenAI não encontrada. Adicione em Settings → Secrets.")
    st.stop()
else:
    st.success("✅ Chave da OpenAI carregada com sucesso.")
client = OpenAI(api_key=api_key)

# ===========================================================
# FUNÇÕES AUXILIARES
# ===========================================================
def safe_get(row, keys, default=""):
    for k in keys if isinstance(keys, list) else [keys]:
        for col in row.index:
            if col.strip().lower() == k.strip().lower():
                val = str(row[col]).strip()
                if val and val.lower() != "nan":
                    return val
    return default

def format_paragraphs(text):
    if not text:
        return "-"
    parts = re.split(r"\n+|•|\r", text.strip())
    return "".join(f"<p class='ja-p'>{p.strip()}</p>" for p in parts if len(p.strip()) > 2)

def cell_card(emoji, title, html_text):
    return f"""
    <div class="ja-sec">
      <div class="ja-sec-h">
        <span class="ja-ic">{emoji}</span>
        <span class="ja-ttl">{title}</span>
      </div>
      <div class="ja-card">{html_text}</div>
    </div>
    """

# ===========================================================
# CSS
# ===========================================================
st.markdown("""
<style>
.block-container {max-width: 1600px !important; margin: 0 auto !important;}
.ja-p { margin: 0 0 6px 0; text-align: justify; }
.ja-sec { margin: 0 !important; }
.ja-sec-h { display:flex; align-items:center; gap:8px; margin:0 0 4px 0 !important; }
.ja-ic { width:24px; text-align:center; line-height:1; }
.ja-ttl { font-weight:700; color:#1E56E0; font-size:0.98rem; }
.ja-card {
  background:#f9f9f9; padding:10px 14px; border-radius:8px;
  border-left:4px solid #1E56E0;
  box-shadow:0 1px 3px rgba(0,0,0,0.05);
  width:100%;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# CARREGAR BASE DE DADOS
# ===========================================================
data = load_data()
if "job_profile" not in data:
    st.error("Job Profile.csv não encontrado em /data")
    st.stop()

df = data["job_profile"].copy()

# ===========================================================
# GERAR EMBEDDINGS
# ===========================================================
@st.cache_data(show_spinner=False)
def generate_embeddings(df):
    if "embedding" in df.columns:
        return df

    df["merged_text"] = df.apply(lambda row:
        " ".join([
            safe_get(row, "Job Profile Description"),
            safe_get(row, "Role Description"),
            safe_get(row, "Grade Differentiator"),
            safe_get(row, "Qualifications")
        ]), axis=1)

    embeddings = []
    total = len(df)
    progress = st.progress(0, text="🔄 Gerando embeddings dos cargos... isso é feito apenas uma vez.")

    for i, text in enumerate(df["merged_text"]):
        try:
            emb = client.embeddings.create(
                model="text-embedding-3-small",
                input=text[:5000]
            ).data[0].embedding
        except Exception as e:
            emb = [0]*1536
        embeddings.append(emb)
        progress.progress((i + 1) / total)

    df["embedding"] = embeddings
    progress.empty()
    st.success("✅ Embeddings gerados e armazenados em cache.")
    return df

with st.spinner("Preparando base de dados..."):
    df_embeddings = generate_embeddings(df)
    time.sleep(1)

# ===========================================================
# ENTRADA DO USUÁRIO
# ===========================================================
st.markdown("#### Descreva as principais atividades do cargo que você busca")
user_input = st.text_area(
    "Exemplo: Gerenciar campanhas de comunicação interna e externa, coordenar equipe de marketing e relações públicas.",
    height=120
)

# ===========================================================
# BUSCA SEMÂNTICA
# ===========================================================
if user_input:
    with st.spinner("🔍 Buscando o cargo mais compatível..."):
        try:
            query_emb = client.embeddings.create(
                model="text-embedding-3-small",
                input=user_input
            ).data[0].embedding
        except Exception as e:
            st.error(f"Erro ao gerar embedding da consulta: {e}")
            st.stop()

        df_embeddings["score"] = df_embeddings["embedding"].apply(lambda emb: cosine_similarity([emb], [query_emb])[0][0])
        best = df_embeddings.sort_values("score", ascending=False).iloc[0]

    st.markdown("---")
    st.markdown("### 🎯 Cargo mais compatível encontrado")
    st.markdown(f"**{best['Job Profile']} (GG {best['Global Grade']})** — Similaridade: {best['score']:.2%}")

    # exibir descrição formatada
    st.markdown(cell_card("🧭", "Sub Job Family Description", format_paragraphs(safe_get(best, "Sub Job Family Description"))), unsafe_allow_html=True)
    st.markdown(cell_card("🧠", "Job Profile Description", format_paragraphs(safe_get(best, "Job Profile Description"))), unsafe_allow_html=True)
    st.markdown(cell_card("🎯", "Role Description", format_paragraphs(safe_get(best, "Role Description"))), unsafe_allow_html=True)
    st.markdown(cell_card("🏅", "Grade Differentiator", format_paragraphs(safe_get(best, "Grade Differentiator"))), unsafe_allow_html=True)
    st.markdown(cell_card("🎓", "Qualifications", format_paragraphs(safe_get(best, "Qualifications"))), unsafe_allow_html=True)
else:
    st.info("✏️ Digite uma descrição acima para encontrar o cargo correspondente.")
