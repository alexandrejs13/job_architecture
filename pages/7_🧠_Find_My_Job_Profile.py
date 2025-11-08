import streamlit as st
import pandas as pd
import numpy as np
import json, os, glob, hashlib
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="🧠 Find My Job Profile", layout="wide")

# ===============================================================
# 🔹 1. Carregar base (robusto)
# ===============================================================

def achar_csv_job_profile():
    candidatos = [
        "data/Job_Profile.csv",
        "data/Job Profile.csv",
        "data/job_profile.csv",
        "data/job profile.csv",
        "data/JobProfile.csv",
        "data/JOB_PROFILE.csv",
    ]
    if not any(os.path.exists(p) for p in candidatos):
        glob_found = sorted(glob.glob("data/*.csv"))
        for f in glob_found:
            nome = os.path.basename(f).lower()
            if "job" in nome and "profile" in nome:
                candidatos.insert(0, f)
                break
    for p in candidatos:
        if os.path.exists(p):
            return p
    return None

csv_path = achar_csv_job_profile()
if not csv_path:
    existentes = "\n".join(f"- {os.path.basename(x)}" for x in sorted(glob.glob("data/*.csv")))
    st.error(
        "❌ Base não encontrada em `data/`.\n\n"
        "Renomeie o arquivo para `Job_Profile.csv` ou similar e coloque em `data/`.\n\n"
        "Arquivos encontrados:\n" + (existentes or "(nenhum CSV encontrado)")
    )
    st.stop()

try:
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    st.success(f"✅ Base carregada: `{os.path.basename(csv_path)}` — {df.shape[0]} linhas, {df.shape[1]} colunas.")
except Exception as e:
    st.error(f"Erro ao ler `{csv_path}`: {e}")
    st.stop()


def pick_col(df, candidates, default=None):
    cols = {c.lower().strip(): c for c in df.columns}
    for c in candidates:
        key = c.lower().strip()
        if key in cols:
            return cols[key]
    return default

COL_JOBTITLE = pick_col(df, ["Job Title", "Job Profile", "Title", "Cargo"])
COL_SUBFAM_DESC = pick_col(df, ["Sub Job Family Description", "SubFamily Description"])
COL_PROFILE_DESC = pick_col(df, ["Job Profile Description", "Profile Description"])
COL_ROLE_DESC = pick_col(df, ["Role Description"])
COL_GRADE_DIFF = pick_col(df, ["Grade Differentiator", "Grade Differentiation"])
COL_KPI = pick_col(df, ["KPIs / Specific Parameters", "Specific parameters KPIs", "Specific parameters / KPIs"])
COL_QUAL = pick_col(df, ["Qualifications"])
COL_GG = pick_col(df, ["Global Grade", "GG", "Grade"])
COL_FAMILY = pick_col(df, ["Family", "Job Family"])
COL_SUBFAMILY = pick_col(df, ["Sub Family", "Sub Job Family"])
COL_TRACK = pick_col(df, ["Career Track", "Career Path"])
COL_FUNCTION = pick_col(df, ["Function", "Function Code"])
COL_CODE = pick_col(df, ["Job Code", "Full Job Code", "Código"])


def get_val(row, col_ref, default=""):
    return (
        str(row[col_ref]).strip()
        if col_ref and col_ref in row.index and pd.notna(row[col_ref])
        else default
    )


# ===============================================================
# 🔹 2. Preparar embeddings (cache automático)
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

    texts = (
        df[COL_PROFILE_DESC].fillna("") + " " + df[COL_SUBFAM_DESC].fillna("")
    ).tolist()
    embeddings = model.encode(texts, convert_to_tensor=True)
    np.save(emb_file, embeddings)
    with open(meta_file, "w") as f:
        json.dump({"signature": current_sig}, f)
    return embeddings, model


with st.spinner("🔄 Preparando base semântica..."):
    embeddings, model = ensure_embeddings(df)


# ===============================================================
# 🔹 3. Busca e interface principal
# ===============================================================
st.title("🧠 Find My Job Profile")

query = st.text_input(
    "✏️ Descreva suas atividades ou responsabilidades:",
    placeholder="Ex: Gestão de folha de pagamento, benefícios e relações sindicais...",
)

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

            gg = get_val(cargo, COL_GG, "N/A")
            titulo = get_val(cargo, COL_JOBTITLE, "N/A")
            familia = get_val(cargo, COL_FAMILY)
            subfamilia = get_val(cargo, COL_SUBFAMILY)
            carreira = get_val(cargo, COL_TRACK)
            funcao = get_val(cargo, COL_FUNCTION)
            codigo = get_val(cargo, COL_CODE)

            subjob = get_val(cargo, COL_SUBFAM_DESC)
            profile = get_val(cargo, COL_PROFILE_DESC)
            role = get_val(cargo, COL_ROLE_DESC)
            diff = get_val(cargo, COL_GRADE_DIFF)
            kpi = get_val(cargo, COL_KPI)
            qualif = get_val(cargo, COL_QUAL)

            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                check = st.checkbox("", key=f"check_{idx}")
            with col2:
                st.markdown(
                    f"""
                    <div style="background:#f9f9ff; border-left:6px solid #2e6ef7;
                                border-radius:12px; padding:18px 22px; margin-bottom:20px;
                                box-shadow:0 2px 4px rgba(0,0,0,0.05);">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="font-weight:700; font-size:17px; color:#1f3a93;">
                                🟦 GG {gg} — {titulo}
                            </div>
                            <div style="font-weight:600; font-size:15px; color:#333;">
                                Similaridade: {sim:.1f}%
                            </div>
                        </div>

                        <details style="margin-top:10px;">
                            <summary style="cursor:pointer; font-weight:500; color:#2e6ef7; font-size:15px;">
                                📋 Ver detalhes
                            </summary>
                            <div style="margin-top:10px; font-size:14px; color:#333;">
                                <b>Família:</b> {familia}<br>
                                <b>Subfamília:</b> {subfamilia}<br>
                                <b>Carreira:</b> {carreira}<br>
                                <b>Função:</b> {funcao}<br>
                                <b>Código:</b> {codigo}<br><br>

                                <b>🧩 Sub Job Family Description</b><br>{subjob}<br><br>
                                <b>🧠 Job Profile Description</b><br>{profile}<br><br>
                                <b>🎯 Role Description</b><br>{role}<br><br>
                                <b>⚙️ Grade Differentiator</b><br>{diff}<br><br>
                                <b>📊 KPIs / Specific Parameters</b><br>{kpi}<br><br>
                                <b>🎓 Qualifications</b><br>{qualif}
                            </div>
                        </details>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

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
                        st.markdown(
                            f"""
                            <div style="background:#fdfdff; border-left:5px solid #2e6ef7;
                                        border-radius:10px; padding:14px; margin-bottom:10px;">
                                <b>GG {get_val(c, COL_GG)}</b><br>
                                <b>{get_val(c, COL_JOBTITLE)}</b><br>
                                <small>{get_val(c, COL_FAMILY)} / {get_val(c, COL_SUBFAMILY)}</small><br><br>
                                <b>Role Description</b><br>{get_val(c, COL_ROLE_DESC)}<br><br>
                                <b>Grade Differentiator</b><br>{get_val(c, COL_GRADE_DIFF)}<br><br>
                                <b>Qualifications</b><br>{get_val(c, COL_QUAL)}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

else:
    st.info("💡 Digite uma descrição acima para encontrar o cargo correspondente.")
