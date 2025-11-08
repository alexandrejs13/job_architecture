import streamlit as st
import pandas as pd
import numpy as np
import json, os, io, csv, glob, hashlib
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="🧠 Find My Job Profile", layout="wide")

# ===============================================================
# 1. Carregamento robusto da base
# ===============================================================
@st.cache_data(show_spinner="📦 Carregando base de dados...")
def load_job_profiles():
    def _normalize_cols(df):
        cols_low = {c.lower().strip(): c for c in df.columns}
        def pick(*opts): 
            for o in opts:
                if o.lower().strip() in cols_low:
                    return cols_low[o.lower().strip()]
            return None
        rename = {}
        def alias(srcs, tgt):
            c = pick(*srcs)
            if c and c != tgt:
                rename[c] = tgt
        alias(["job title", "cargo"], "Job Title")
        alias(["global grade", "gg", "grade"], "Global Grade")
        alias(["family", "job family"], "Family")
        alias(["sub family", "sub job family"], "Sub Family")
        alias(["job profile description"], "Job Profile Description")
        alias(["sub job family description"], "Sub Job Family Description")
        return df.rename(columns=rename)

    def _try_read(path):
        with open(path, 'rb') as f:
            raw = f.read()
        for enc in ("utf-8-sig", "latin1"):
            try:
                text = raw.decode(enc, errors="replace")
                sample = "\n".join(text.splitlines()[:50])
                dialect = csv.Sniffer().sniff(sample, delimiters=[",",";","\t","|"])
                sep = dialect.delimiter
                df = pd.read_csv(io.StringIO(text), sep=sep, dtype=str, engine="python")
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
        st.error("❌ Nenhum arquivo Job Profile encontrado em `data/`.")
        st.stop()

    df = _try_read(csv_path)
    df = _normalize_cols(df)
    df["Global Grade"] = pd.to_numeric(df["Global Grade"], errors="coerce")
    return df

df = load_job_profiles()

# ===============================================================
# 2. Cache de embeddings (rápido)
# ===============================================================
@st.cache_resource(show_spinner="🧠 Preparando base semântica...")
def prepare_embeddings(df):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = (df["Job Profile Description"].fillna("") + " " + df["Sub Job Family Description"].fillna("")).tolist()
    emb = model.encode(texts, convert_to_tensor=True)
    return emb, model

embeddings, model = prepare_embeddings(df)

# ===============================================================
# 3. Interface
# ===============================================================
st.title("🧠 Find My Job Profile")

# Dropdowns Family/Subfamily
families = sorted(df["Family"].dropna().unique())
selected_family = st.selectbox("Selecione a Family:", [""] + families)

subfamilies = []
if selected_family:
    subfamilies = sorted(df[df["Family"] == selected_family]["Sub Family"].dropna().unique())
selected_subfamily = st.selectbox("Selecione a Subfamily:", [""] + subfamilies)

query = st.text_area(
    "Descreva brevemente suas atividades:",
    placeholder="Ex: Lidero equipe de folha de pagamento, remuneração e benefícios...",
)

if st.button("🔎 Encontrar Job Profile"):
    # Validação
    if not selected_family or not selected_subfamily:
        st.warning("Selecione a Family e Subfamily antes de continuar.")
        st.stop()

    if len(query.split()) < 10:
        st.warning("💬 Parece que sua descrição está muito curta. Dê mais detalhes sobre suas responsabilidades.")
        st.stop()

    # Filtrar por Family/Subfamily
    filtered = df[(df["Family"] == selected_family) & (df["Sub Family"] == selected_subfamily)]
    if filtered.empty:
        st.error("Nenhum cargo encontrado nessa Family/Subfamily.")
        st.stop()

    # Calcular similaridade
    with st.spinner("🔍 Buscando cargos compatíveis..."):
        query_emb = model.encode(query, convert_to_tensor=True)
        idxs = filtered.index.tolist()
        filtered_emb = embeddings[idxs]
        scores = util.cos_sim(query_emb, filtered_emb)[0].cpu().numpy()

        filtered = filtered.copy()
        filtered["score"] = scores
        filtered = filtered.sort_values("score", ascending=False)

        # Selecionar os top 3 coerentes por grade
        top_k = 3
        top3 = filtered.head(10)
        gg_top = top3["Global Grade"].dropna()
        if not gg_top.empty:
            gg_ref = int(round(gg_top.iloc[0]))
            top3 = top3[top3["Global Grade"].between(gg_ref - 2, gg_ref + 2)]
        top3 = top3.head(top_k)

    st.markdown("## 🎯 Cargos mais compatíveis:")

    if top3.empty:
        st.info("Nenhum cargo coerente encontrado. Tente descrever um pouco mais as responsabilidades.")
    else:
        for _, cargo in top3.iterrows():
            gg = cargo.get("Global Grade", "")
            titulo = cargo.get("Job Title", "")
            family = cargo.get("Family", "")
            subfam = cargo.get("Sub Family", "")
            sim = float(cargo["score"]) * 100
            desc = cargo.get("Job Profile Description", "")

            st.markdown(f"""
            <div style="background:#f9f9ff;border-left:6px solid #2e6ef7;
                        border-radius:14px;padding:20px;margin-bottom:20px;
                        box-shadow:0 2px 6px rgba(0,0,0,0.08);">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div style="font-size:18px;font-weight:700;color:#1f3a93;">
                        🟦 GG {int(gg)} — {titulo}
                    </div>
                    <div style="font-size:15px;font-weight:600;color:#333;">
                        Similaridade: {sim:.1f}%
                    </div>
                </div>
                <div style="font-size:14px;color:#555;">
                    <b>Family:</b> {family} | <b>Subfamily:</b> {subfam}
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
