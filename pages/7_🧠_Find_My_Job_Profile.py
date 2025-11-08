import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import json, os, hashlib

st.set_page_config(page_title="🧠 Find My Job Profile", layout="wide")

# ------------------ Funções utilitárias ------------------ #
def df_signature(df: pd.DataFrame) -> str:
    return hashlib.sha256(pd.util.hash_pandas_object(df, index=True).values).hexdigest()

def ensure_embeddings(df, path_data="data"):
    os.makedirs(path_data, exist_ok=True)
    emb_file = os.path.join(path_data, "job_embeddings.npy")
    meta_file = os.path.join(path_data, "job_embeddings.meta.json")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    current_sig = df_signature(df)

    # Se já existe cache e é válido
    if os.path.exists(emb_file) and os.path.exists(meta_file):
        with open(meta_file, "r") as f:
            meta = json.load(f)
        if meta.get("signature") == current_sig:
            return np.load(emb_file), model

    # Senão, gera e salva
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
query = st.text_input("✏️ Descreva suas atividades ou responsabilidades:", placeholder="Ex: Gestão de folha de pagamento, benefícios e relações sindicais...")

if query:
    with st.spinner("🔍 Buscando cargos compatíveis..."):
        query_emb = model.encode(query, convert_to_tensor=True)
        scores = util.cos_sim(query_emb, embeddings)[0]
        top_k = min(5, len(df))
        best_idx = np.argsort(scores)[-top_k:][::-1]

        st.markdown("## 🎯 Cargos mais compatíveis:")

        for idx in best_idx:
            cargo = df.iloc[idx]
            sim = float(scores[idx]) * 100

            # Conteúdo principal do card
            gg = cargo.get("Global Grade", "N/A")
            nome = cargo.get("Sub Family", "N/A")
            desc = cargo.get("Job Profile Description", "")
            subdesc = cargo.get("Sub Job Family Description", "")

            # --- Card unificado ---
            st.markdown(
                f"""
                <div style="background-color:#fafbff; border-left: 6px solid #2e6ef7; 
                            border-radius: 12px; padding: 18px 22px; margin-bottom: 16px;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="font-weight:600; font-size:18px; color:#1f3a93;">
                            🟦 GG {gg} — {nome}
                        </div>
                        <div style="font-weight:600; font-size:15px; color:#333;">
                            Similaridade: {sim:.1f}%
                        </div>
                    </div>
                    <div style="color:#444; font-size:15px; margin-top:8px; margin-bottom:10px;">
                        {subdesc}
                    </div>
                    <details style="background:#fff; border-radius:8px; padding:10px; border:1px solid #ddd;">
                        <summary style="cursor:pointer; font-weight:500; color:#2e6ef7; font-size:15px;">
                            📋 Ver detalhes
                        </summary>
                        <div style="margin-top:10px; font-size:14px; color:#333;">
                            {desc}
                        </div>
                    </details>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.info("💡 Digite uma descrição acima para encontrar o cargo correspondente.")
