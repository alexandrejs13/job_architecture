import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import json, os, hashlib

st.set_page_config(page_title="🧠 Find My Job Profile", layout="wide")

# ------------------ Funções utilitárias ------------------ #
def df_signature(df: pd.DataFrame) -> str:
    """Cria hash único da base para cache de embeddings"""
    return hashlib.sha256(pd.util.hash_pandas_object(df, index=True).values).hexdigest()

def ensure_embeddings(df, path_data="data"):
    """Gera ou carrega cache de embeddings"""
    os.makedirs(path_data, exist_ok=True)
    emb_file = os.path.join(path_data, "job_embeddings.npy")
    meta_file = os.path.join(path_data, "job_embeddings.meta.json")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    current_sig = df_signature(df)

    # Reutiliza cache existente se assinatura for igual
    if os.path.exists(emb_file) and os.path.exists(meta_file):
        with open(meta_file, "r") as f:
            meta = json.load(f)
        if meta.get("signature") == current_sig:
            return np.load(emb_file), model

    # Cria novo cache
    texts = (df["Job Profile Description"].fillna("") + " " + df["Sub Job Family Description"].fillna("")).tolist()
    embeddings = model.encode(texts, convert_to_tensor=True)
    np.save(emb_file, embeddings)
    with open(meta_file, "w") as f:
        json.dump({"signature": current_sig}, f)
    return embeddings, model

# ------------------ Carregar base ------------------ #
st.title("🧠 Find My Job Profile")

try:
    df = pd.read_csv("data/Job_Profile.csv")
    st.success("✅ Base de cargos carregada com sucesso.")
except Exception as e:
    st.error(f"Erro ao carregar base: {e}")
    st.stop()

# ------------------ Carregar embeddings ------------------ #
with st.spinner("🔄 Preparando base semântica..."):
    embeddings, model = ensure_embeddings(df)

# ------------------ Entrada do usuário ------------------ #
query = st.text_input("✏️ Descreva suas atividades ou responsabilidades:",
                      placeholder="Ex: Gestão de folha de pagamento, benefícios e relações sindicais...")

selected_jobs = []  # Armazena IDs dos cargos selecionados

if query:
    with st.spinner("🔍 Buscando cargos compatíveis..."):
        query_emb = model.encode(query, convert_to_tensor=True)
        scores = util.cos_sim(query_emb, embeddings)[0]
        top_k = min(8, len(df))
        best_idx = np.argsort(scores)[-top_k:][::-1]

        st.markdown("## 🎯 Cargos mais compatíveis:")

        for idx in best_idx:
            cargo = df.iloc[idx]
            sim = float(scores[idx]) * 100

            gg = cargo.get("Global Grade", "N/A")
            titulo = cargo.get("Job Title", "N/A")
            familia = cargo.get("Family", "")
            subfamilia = cargo.get("Sub Family", "")
            carreira = cargo.get("Career Track", "")
            funcao = cargo.get("Function", "")
            codigo = cargo.get("Job Code", "")

            subjob = cargo.get("Sub Job Family Description", "")
            profile = cargo.get("Job Profile Description", "")
            role = cargo.get("Role Description", "")
            diff = cargo.get("Grade Differentiator", "")
            kpi = cargo.get("KPIs / Specific Parameters", "")
            qualif = cargo.get("Qualifications", "")

            # Checkbox para comparar
            col1, col2 = st.columns([0.05, 0.95])
            with col1:
                check = st.checkbox("", key=f"check_{idx}")
            with col2:
                st.markdown(
                    f"""
                    <div style="background-color:#fafbff; border-left:6px solid #2e6ef7; 
                                border-radius:12px; padding:20px 24px; margin-bottom:18px;
                                box-shadow:0 2px 4px rgba(0,0,0,0.05);">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="font-weight:700; font-size:18px; color:#1f3a93;">
                                🟦 GG {gg} — {titulo}
                            </div>
                            <div style="font-weight:600; font-size:15px; color:#333;">
                                Similaridade: {sim:.1f}%
                            </div>
                        </div>
                        <div style="color:#444; font-size:15px; margin-top:4px;">
                            <b>{familia} / {subfamilia}</b>
                        </div>

                        <details style="background:#fff; border-radius:8px; padding:12px; border:1px solid #ddd; margin-top:12px;">
                            <summary style="cursor:pointer; font-weight:500; color:#2e6ef7; font-size:15px;">
                                📋 Ver detalhes
                            </summary>
                            <div style="margin-top:10px; font-size:14px; color:#333;">
                                <p><b>Família:</b> {familia}<br>
                                   <b>Subfamília:</b> {subfamilia}<br>
                                   <b>Carreira:</b> {carreira}<br>
                                   <b>Função:</b> {funcao}<br>
                                   <b>Código:</b> {codigo}</p>

                                <p><b>🧩 Sub Job Family Description</b><br>{subjob}</p>
                                <p><b>🧠 Job Profile Description</b><br>{profile}</p>
                                <p><b>🎯 Role Description</b><br>{role}</p>
                                <p><b>⚙️ Grade Differentiator</b><br>{diff}</p>
                                <p><b>📊 KPIs / Specific Parameters</b><br>{kpi}</p>
                                <p><b>🎓 Qualifications</b><br>{qualif}</p>
                            </div>
                        </details>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            if check:
                selected_jobs.append(cargo)

        # Botão para comparar
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
                                <b>GG {c.get("Global Grade","")}</b><br>
                                <b>{c.get("Job Title","")}</b><br>
                                <small>{c.get("Family","")} / {c.get("Sub Family","")}</small><br><br>
                                <b>Role Description</b><br>{c.get("Role Description","")}<br><br>
                                <b>Grade Differentiator</b><br>{c.get("Grade Differentiator","")}<br><br>
                                <b>Qualifications</b><br>{c.get("Qualifications","")}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

else:
    st.info("💡 Digite uma descrição acima para encontrar o cargo correspondente.")
