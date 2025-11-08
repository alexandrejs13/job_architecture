import streamlit as st
import pandas as pd
import numpy as np
import json, os, io, csv, glob, hashlib
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="🧠 Find My Job Profile", layout="wide")

# ===============================================================
# 1. Carregar base (robusto contra vírgulas internas)
# ===============================================================
@st.cache_data(show_spinner="📦 Carregando base de dados...")
def load_job_profiles():
    def _normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
        cols_low = {c.lower().strip(): c for c in df.columns}
        def pick(*opts):
            for o in opts:
                if o.lower().strip() in cols_low:
                    return cols_low[o.lower().strip()]
            return None
        rename = {}
        def set_alias(srcs, tgt):
            c = pick(*srcs)
            if c and c != tgt:
                rename[c] = tgt
        set_alias(["job title", "cargo"], "Job Title")
        set_alias(["global grade", "gg", "grade"], "Global Grade")
        set_alias(["sub job family description"], "Sub Job Family Description")
        set_alias(["job profile description"], "Job Profile Description")
        return df.rename(columns=rename) if rename else df

    def _try_read(path):
        with open(path, 'rb') as f:
            raw = f.read()
        for enc in ("utf-8-sig", "latin1"):
            try:
                text = raw.decode(enc, errors="replace")
                sample = "\n".join(text.splitlines()[:50])
                dialect = csv.Sniffer().sniff(sample, delimiters=[",",";","\t","|"])
                sep = dialect.delimiter
                df = pd.read_csv(io.StringIO(text), sep=sep, engine="python",
                                 quoting=csv.QUOTE_MINIMAL, quotechar='"',
                                 escapechar='\\', dtype=str, keep_default_na=False)
                return df
            except Exception:
                continue
        raise ValueError("Não foi possível ler o CSV.")

    csv_path = None
    for f in glob.glob("data/*.csv"):
        if "job" in f.lower() and "profile" in f.lower():
            csv_path = f
            break
    if not csv_path:
        st.error("❌ Nenhum CSV de Job Profile encontrado em `data/`.")
        st.stop()

    df = _try_read(csv_path)
    df = _normalize_cols(df)
    return df

df = load_job_profiles()

def get_val(row, col):
    return str(row.get(col, "")).strip() if col in row.index else ""

# ===============================================================
# 2. Preparar embeddings (cache local)
# ===============================================================
@st.cache_resource(show_spinner="🧠 Preparando base semântica...")
def prepare_embeddings(df):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = (df["Job Profile Description"].fillna("") + " " + df["Sub Job Family Description"].fillna("")).tolist()
    embeddings = model.encode(texts, convert_to_tensor=True)
    return embeddings, model

embeddings, model = prepare_embeddings(df)

# ===============================================================
# 3. Interface
# ===============================================================
st.title("🧠 Find My Job Profile")
query = st.text_area("Descreva brevemente suas atividades:", placeholder="Ex: Lidero equipe de folha de pagamento e processos de remuneração...")

if st.button("🔎 Encontrar Job Profile"):
    if not query.strip():
        st.warning("Digite uma descrição para iniciar a busca.")
        st.stop()

    with st.spinner("🔍 Analisando perfis mais compatíveis..."):
        query_emb = model.encode(query, convert_to_tensor=True)
        scores = util.cos_sim(query_emb, embeddings)[0].cpu().numpy()
        top_k = 3
        best_idx = np.argsort(scores)[-top_k:][::-1]

    st.markdown("## 🎯 Cargos mais compatíveis:")

    for idx in best_idx:
        cargo = df.iloc[idx]
        sim = float(scores[idx]) * 100
        gg = get_val(cargo, "Global Grade")
        titulo = get_val(cargo, "Job Title")
        desc = get_val(cargo, "Job Profile Description")

        st.markdown(f"""
        <div style="background:#f9f9ff;border-left:6px solid #2e6ef7;
                    border-radius:14px;padding:20px;margin-bottom:20px;
                    box-shadow:0 2px 6px rgba(0,0,0,0.08);">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="font-size:18px;font-weight:700;color:#1f3a93;">
                    🟦 GG {gg} — {titulo}
                </div>
                <div style="font-size:15px;font-weight:600;color:#333;">
                    Similaridade: {sim:.1f}%
                </div>
            </div>
            <details style="margin-top:12px;">
                <summary style="cursor:pointer;color:#2e6ef7;font-weight:600;">
                    📋 Ver detalhes
                </summary>
                <div style="margin-top:10px;font-size:14px;line-height:1.5;color:#333;">
                    {desc}
                </div>
            </details>
        </div>
        """, unsafe_allow_html=True)
