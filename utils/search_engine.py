from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# Modelo leve multilíngue
_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def find_best_match(user_text, df, text_column='Job Profile'):
    if df.empty or user_text.strip() == "":
        return None

    sentences = df[text_column].astype(str).tolist()
    corpus_embeddings = _model.encode(sentences)
    query_embedding = _model.encode([user_text])

    similarities = cosine_similarity(query_embedding, corpus_embeddings)[0]
    best_idx = int(np.argmax(similarities))
    return df.iloc[best_idx], float(similarities[best_idx])
