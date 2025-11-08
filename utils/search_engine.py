from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# Modelo multilíngue (cobre PT, EN, ES)
_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def find_best_match(user_text: str, df: pd.DataFrame):
    """Busca semântica combinando múltiplas colunas relevantes"""
    if df.empty or not isinstance(user_text, str) or not user_text.strip():
        return None, 0.0

    # Colunas que ajudam a contextualizar melhor o cargo
    text_fields = [
        c for c in df.columns 
        if any(x in c.lower() for x in [
            "profile", "title", "description", "job", "function", "discipline", "family"
        ])
    ]

    if not text_fields:
        return None, 0.0

    # Combina o texto de várias colunas em uma só
    df["combined_text"] = df[text_fields].astype(str).agg(" ".join, axis=1)

    # Cria embeddings
    corpus_embeddings = _model.encode(df["combined_text"].tolist(), convert_to_tensor=False)
    query_embedding = _model.encode([user_text], convert_to_tensor=False)

    # Calcula similaridade
    similarities = cosine_similarity(query_embedding, corpus_embeddings)[0]
    best_idx = int(np.argmax(similarities))

    return df.iloc[best_idx], float(similarities[best_idx])
