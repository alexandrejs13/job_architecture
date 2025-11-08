import os
import re
import json
import time
import hashlib
import numpy as np
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer

# ===========================================================
# CONFIGURAÇÃO DE PÁGINA
# ===========================================================
st.set_page_config(page_title="Find My Job Profile", layout="wide")
st.markdown("<h1>🧠 Find My Job Profile</h1>", unsafe_allow_html=True)

# ===========================================================
# FUNÇÕES DE SUPORTE
# ===========================================================
EMB_PATH = "data/job_embeddings.npy"
META_PATH = "data/job_embeddings.meta.json"


@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def build_merged_text(row):
    """Concatena todas as colunas relevantes em um único texto para embeddings"""
    parts = [
        str(row.get("Job Profile", "")),
        str(row.get("Sub Job Family", "")),
        str(row.get("Job Profile Description", "")),
        str(row.get("Role Description", "")),
        str(row.get("Grade Differentiator", "")),
        str(row.get("Qualifications", "")),
        str(row.get("Specific parameters KPIs", "")),
    ]
    return " ".join([p for p in parts if p and p.lower() != "nan"])


def df_signature(df: pd.DataFrame) -> str:
    """Cria uma assinatura única para saber se o CSV mudou"""
    cols = "|".join(df.columns.tolist())
    size = df.shape
    sample = "|".join(df.head(5).fillna("").astype(str).agg(" ".join, axis=1).tolist())
    payload = f"{cols}::{size}::{sample}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def ensure_embeddings(df: pd.DataFrame) -> np.ndarray:
    """Gera ou carrega embeddings persistentes (cache local .npy)"""
    os.makedirs(os.path.dirname(EMB_PATH), exist_ok=True)
    sig = df_signature(df)

    # tenta carregar se cache válido
    if os.path.exists(EMB_PATH) and os.path.exists(META_PATH):
        try:
            meta = json.load(open(META_PATH, "r"))
            if meta.get("signature") == sig:
                return np.load(EMB_PATH)
        except Exception:
            pass

    # caso contrário, gera do zero
    with st.spinner("🧩 Preparando base semântica (apenas na primeira vez)..."):
        model = load_model()
        texts = df["merged_text"].tolist()
        embs = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
        np.save(EMB_PATH, embs)
        json.dump({"signature": sig, "generated_at": time.time()}, open(META_PATH, "w"))
        return embs


# ===========================================================
# CSS — VISUAL LIMPO DOS CARDS
# ===========================================================
st.markdown("""
<style>
.res-card{
  border:1px solid #e7eaf3; border-radius:14px; padding:14px 16px; margin: 14px 0;
  background:#fbfbfe;
  box-shadow: 0 1px 4px rgba(0,0,0,.04);
}
.res-head{ display:flex; align-items:center; justify-content:space-between; gap:12px; }
.res-title{ font-weight:800; font-size:1.05rem; color:#1e40af; }
.res-sim{ color:#111827; font-weight:700; font-size:0.95rem; }
.badge{ background:#eef2ff; color:#1e40af; font-weight:800; padding:2px 8px; border-radius:8px; margin-right:8px; }
.res-sub{ color:#4b5563; font-size:0.9rem; margin-top:2px; }
.res-divider{ height:1px; background:#eceff7; margin:10px 0 6px 0; }
.sec-ttl{ font-weight:700; color:#1E56E0; margin:6px 0 4px 0; font-size:0.92rem;}
.sec-box{ background:#fff; border-left:4px solid #1E56E0; border-radius:8px; padding:10px 12px; border:1px solid #edf0f6; }
</style>
""", unsafe_allow_html=True)


def html_paragraphs(text: str) -> str:
    if not text or str(text).strip().lower() == "nan":
        return "-"
    parts = re.split(r"\n+|•|\r", str(text).strip())
    return "".join(f"<p style='margin:0 0 6px 0; text-align:justify;'>{p.strip()}</p>" for p in parts if len(p.strip())>2)


def render_detail_box(title, html_text):
    return f"""
      <div class="sec-ttl">{title}</div>
      <div class="sec-box">{html_text}</div>
    """


def render_result_card(row, sim_pct: float):
    gg = str(row.get("Global Grade", "")).strip()
    title = str(row.get("Job Profile", "")).strip() or "-"
    subfam = str(row.get("Sub Job Family", "")).strip()

    # Cabeçalho do card
    st.markdown(
        f"""
        <div class="res-card">
          <div class="res-head">
            <div class="res-title">
              <span class="badge">GG {gg}</span>{title}
              <div class="res-sub">{subfam}</div>
            </div>
            <div class="res-sim">Similaridade: {sim_pct:.1f}%</div>
          </div>
          <div class="res-divider"></div>
        """,
        unsafe_allow_html=True
    )

    # Expander – Ver detalhes
    with st.expander("📋 Ver detalhes", expanded=False):
        sec = []
        sec.append(render_detail_box("Sub Job Family Description", html_paragraphs(row.get("Sub Job Family Description", ""))))
        sec.append(render_detail_box("Job Profile Description",    html_paragraphs(row.get("Job Profile Description", ""))))
        sec.append(render_detail_box("Role Description",           html_paragraphs(row.get("Role Description", ""))))
        gd = None
        for c in ["Grade Differentiator","Grade Differentiation","Grade Differentiatior"," Grade Differentiator","Grade Differentiator ","Grade Differentiators"]:
            if c in row.index:
                gd = row.get(c, None)
                if gd: break
        sec.append(render_detail_box("Grade Differentiator",       html_paragraphs(gd or "")))
        sec.append(render_detail_box("Qualifications",             html_paragraphs(row.get("Qualifications",""))))
        sec.append(render_detail_box("KPIs / Specific Parameters", html_paragraphs(row.get("Specific parameters KPIs","") or row.get("Specific parameters / KPIs",""))))
        st.markdown("".join(sec), unsafe_allow_html=True)

    # fecha o card
    st.markdown("</div>", unsafe_allow_html=True)


# ===========================================================
# CARREGAMENTO DE DADOS
# ===========================================================
from utils.data_loader import load_data

data = load_data()
if "job_profile" not in data:
    st.error("❌ Arquivo Job Profile.csv não encontrado em /data")
    st.stop()

df = data["job_profile"].copy()
df["merged_text"] = df.apply(build_merged_text, axis=1)
matrix = ensure_embeddings(df)

# ===========================================================
# CAMPO DE BUSCA
# ===========================================================
st.markdown("### 🔍 Descreva suas atividades principais ou responsabilidades")
query = st.text_area("Digite aqui sua descrição (pode ser em português ou inglês):", height=110, placeholder="Exemplo: Coordeno projetos de desenvolvimento de produto, liderando equipes técnicas e garantindo prazos e qualidade.")

if st.button("🔎 Buscar cargo correspondente"):
    if not query.strip():
        st.warning("Por favor, digite uma descrição para buscar.")
        st.stop()

    # traduz automaticamente se estiver em português
    from deep_translator import GoogleTranslator
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(query)
    except Exception:
        translated = query

    model = load_model()
    query_emb = model.encode([translated], normalize_embeddings=True)[0]
    sims = matrix @ query_emb

    df["_sim"] = sims
    df["_gg_int"] = df["Global Grade"].apply(lambda x: int(re.sub(r'[^0-9]', '', str(x))) if re.search(r'\d', str(x)) else -1)
    df_sorted = df.sort_values(by=["_sim", "_gg_int"], ascending=[False, False]).head(10)

    st.markdown("## 🎯 Cargos mais compatíveis:")

    for _, row in df_sorted.iterrows():
        render_result_card(row, sim_pct=float(row["_sim"] * 100.0))
