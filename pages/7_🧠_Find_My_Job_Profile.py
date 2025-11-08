import streamlit as st
import pandas as pd
import numpy as np
import json, os, glob, io, csv, hashlib
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="🧠 Find My Job Profile", layout="wide")

# ===============================================================
# 🔹 1. Carregar base (robusto contra vírgulas internas)
# ===============================================================

def _normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
    cols_low = {c.lower().strip(): c for c in df.columns}
    def pick(*opts, default=None):
        for o in opts:
            if o.lower().strip() in cols_low:
                return cols_low[o.lower().strip()]
        return default

    rename = {}
    def set_alias(srcs, tgt):
        c = pick(*srcs)
        if c and c != tgt:
            rename[c] = tgt

    set_alias(["job title", "job profile", "title", "cargo"], "Job Title")
    set_alias(["global grade", "gg", "grade"], "Global Grade")
    set_alias(["family", "job family"], "Family")
    set_alias(["sub family", "sub job family", "subfamily"], "Sub Family")
    set_alias(["career track", "career path"], "Career Track")
    set_alias(["function", "function code"], "Function")
    set_alias(["job code", "full job code", "código"], "Job Code")

    set_alias(["sub job family description", "subfamily description"], "Sub Job Family Description")
    set_alias(["job profile description", "profile description"], "Job Profile Description")
    set_alias(["role description"], "Role Description")
    set_alias(["grade differentiator", "grade differentiation", "grade differentiatior"], "Grade Differentiator")
    set_alias(["kpis / specific parameters", "specific parameters kpis", "specific parameters / kpis"], "KPIs / Specific Parameters")
    set_alias(["qualifications"], "Qualifications")

    return df.rename(columns=rename) if rename else df

def _try_read(path: str):
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
    for enc in ("utf-8-sig", "latin1"):
        for sep in (",",";","\t","|"):
            try:
                df = pd.read_csv(path, sep=sep, engine="python",
                                 quoting=csv.QUOTE_NONE, escapechar='\\',
                                 dtype=str, keep_default_na=False,
                                 encoding=enc, on_bad_lines="skip")
                st.warning("⚠️ Algumas linhas foram ignoradas por formatação inconsistente.")
                return df
            except Exception:
                continue
    raise ValueError("Não foi possível ler o CSV.")

def _find_csv():
    for f in sorted(glob.glob("data/*.csv")):
        nm = os.path.basename(f).lower()
        if "job" in nm and "profile" in nm:
            return f
    return None

csv_path = _find_csv()
if not csv_path:
    st.error("❌ Nenhum CSV de Job Profile encontrado em `data/`.")
    st.stop()

try:
    df = _try_read(csv_path)
except Exception as e:
    st.error(f"Erro ao ler `{os.path.basename(csv_path)}`: {e}")
    st.stop()

df = _normalize_cols(df)
if "Job Title" not in df.columns or "Job Profile Description" not in df.columns:
    st.error("❌ Colunas obrigatórias ausentes: 'Job Title' e 'Job Profile Description'.")
    st.stop()

st.success(f"✅ Base carregada: `{os.path.basename(csv_path)}` — {df.shape[0]} linhas, {df.shape[1]} colunas.")

def get_val(row, col, default=""):
    return str(row.get(col, "")).strip() if col in row.index else default

# ===============================================================
# 🔹 2. Preparar embeddings (cache local)
# ===============================================================
def df_signature(df: pd.DataFrame) -> str:
    return hashlib.sha256(pd.util.hash_pandas_object(df, index=True).values).hexdigest()

def ensure_embeddings(df, path_data="data"):
    os.makedirs(path_data, exist_ok=True)
    emb_file = os.path.join(path_data, "job_embeddings.npy")
    meta_file = os.path.join(path_data, "job_embeddings.meta.json")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    current_sig = df_signature(df)

    if os.path.exists(emb_file) and os.path.exists(meta_file):
        with open(meta_file, "r") as f:
            meta = json.load(f)
        if meta.get("signature") == current_sig:
            return np.load(emb_file), model

    texts = (df["Job Profile Description"].fillna("") + " " + df["Sub Job Family Description"].fillna("")).tolist()
    embeddings = model.encode(texts, convert_to_tensor=True)
    np.save(emb_file, embeddings)
    with open(meta_file, "w") as f:
        json.dump({"signature": current_sig}, f)
    return embeddings, model

with st.spinner("🔄 Preparando base semântica..."):
    embeddings, model = ensure_embeddings(df)

# ===============================================================
# 🔹 3. Busca e interface
# ===============================================================
st.title("🧠 Find My Job Profile")

query = st.text_input("✏️ Descreva suas atividades ou responsabilidades:")

selected_jobs = []

if query:
    with st.spinner("🔍 Buscando cargos compatíveis..."):
        query_emb = model.encode(query, convert_to_tensor=True)
        scores = util.cos_sim(query_emb, embeddings)[0]
        top_k = min(10, len(df))
        best_idx = np.argsort(scores)[-top_k:][::-1]

        st.markdown("## 🎯 Cargos mais compatíveis:")

        for idx in best_idx:
            cargo = df.iloc[idx]
            sim = float(scores[idx]) * 100
            gg = get_val(cargo, "Global Grade")
            titulo = get_val(cargo, "Job Title")

            with st.container():
                col1, col2 = st.columns([0.05, 0.95])
                with col1:
                    check = st.checkbox("", key=f"check_{idx}")
                with col2:
                    st.markdown(f"""
                        <div style="background:#f9f9ff;border-left:6px solid #2e6ef7;
                                    border-radius:12px;padding:18px;margin-bottom:16px;
                                    box-shadow:0 2px 4px rgba(0,0,0,0.05);">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <div style="font-weight:700;font-size:17px;color:#1f3a93;">
                                    🟦 GG {gg} — {titulo}
                                </div>
                                <div style="font-weight:600;font-size:15px;color:#333;">
                                    Similaridade: {sim:.1f}%
                                </div>
                            </div>
                            <details style="margin-top:10px;">
                                <summary style="cursor:pointer;color:#2e6ef7;">📋 Ver detalhes</summary>
                                <div style="margin-top:10px;font-size:14px;color:#333;">
                                    {get_val(cargo, "Job Profile Description")}
                                </div>
                            </details>
                        </div>
                    """, unsafe_allow_html=True)

                if check:
                    selected_jobs.append(cargo)

        if selected_jobs:
            st.markdown("### 🧾 Comparar cargos selecionados")
            if st.button("🔍 Exibir comparação lado a lado"):
                st.markdown("---")
                st.markdown("## 📊 Comparativo entre cargos selecionados")

                cols = st.columns(len(selected_jobs))
                for i, c in enumerate(selected_jobs):
                    with cols[i]:
                        st.markdown(f"""
                            <div style="background:#fdfdff;border-left:5px solid #2e6ef7;
                                        border-radius:10px;padding:14px;">
                                <b>GG {get_val(c, 'Global Grade')}</b><br>
                                <b>{get_val(c, 'Job Title')}</b><br><br>
                                <b>Descrição</b><br>{get_val(c, 'Job Profile Description')}
                            </div>
                        """, unsafe_allow_html=True)
else:
    st.info("💡 Digite uma descrição acima para encontrar o cargo correspondente.")
