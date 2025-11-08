# --- FAST EMBEDDINGS CACHE (.npy persistente) ---
import os, time, numpy as np, pandas as pd
from sentence_transformers import SentenceTransformer
import hashlib

EMB_PATH = "data/job_embeddings.npy"           # arquivo de cache
META_PATH = "data/job_embeddings.meta.json"    # metadados do cache (opcional)

@st.cache_resource(show_spinner=True)
def load_st_model():
    # carrega uma única vez por sessão
    return SentenceTransformer("all-MiniLM-L6-v2")

def df_signature(df: pd.DataFrame) -> str:
    """Gera uma assinatura leve do CSV para invalidar cache quando mudar."""
    cols = "|".join(df.columns.tolist())
    size = df.shape
    sample = "|".join(df.head(5).fillna("").astype(str).agg(" ".join, axis=1).tolist())
    payload = f"{cols}::{size}::{sample}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def ensure_embeddings(df: pd.DataFrame) -> np.ndarray:
    os.makedirs(os.path.dirname(EMB_PATH), exist_ok=True)

    sig = df_signature(df)
    # se existir e assinar igual, só carregar
    if os.path.exists(EMB_PATH) and os.path.exists(META_PATH):
        try:
            import json
            meta = json.load(open(META_PATH, "r"))
            if meta.get("signature") == sig:
                return np.load(EMB_PATH)
        except Exception:
            pass  # cai para regerar

    # (re)gerar e salvar
    with st.spinner("Preparando base semântica (apenas na primeira vez)..."):
        model = load_st_model()
        texts = df["merged_text"].tolist()
        embs = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
        np.save(EMB_PATH, embs)
        try:
            import json
            json.dump({"signature": sig, "generated_at": time.time()}, open(META_PATH, "w"))
        except Exception:
            pass
        return embs
