# --- IMPORTS (mantenha os demais) ---
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# flag de modo
MODE = "openai"  # será trocado para "local" se a API falhar

# --- FUNÇÕES AUXILIARES ---
def merge_row_text(row):
    parts = [
        str(row.get("Sub Job Family Description", "")),
        str(row.get("Job Profile Description", "")),
        str(row.get("Role Description", "")),
        str(row.get("Grade Differentiator", "")) or str(row.get("Grade Differentiatior", "")),
        str(row.get("Specific parameters KPIs", "")) or str(row.get("Specific parameters / KPIs", "")),
        str(row.get("Qualifications", "")),
    ]
    return " \n".join([p for p in parts if p and p.lower() != "nan"]).strip()

# --- OPENAI (embeddings) ---
def get_openai_client():
    import openai  # usando pacote "openai"
    api_key = st.secrets.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY ausente em st.secrets")
    openai.api_key = api_key
    return openai

@st.cache_data(show_spinner=False)
def generate_embeddings_openai(df):
    client = get_openai_client()
    merged = df["merged_text"].tolist()
    vecs = []
    for txt in merged:
        try:
            emb = client.Embeddings.create(model="text-embedding-3-small", input=txt)  # type: ignore
            vecs.append(np.array(emb["data"][0]["embedding"], dtype="float32"))
        except Exception as e:
            raise RuntimeError(f"Falha ao gerar embedding na OpenAI: {e}")
    M = np.vstack(vecs)
    return M  # matriz [n_docs x 1536]

# --- TF-IDF LOCAL (fallback) ---
@st.cache_data(show_spinner=False)
def generate_embeddings_local(df):
    corpus = df["merged_text"].tolist()
    vectorizer = TfidfVectorizer(
        analyzer="word",
        lowercase=True,
        ngram_range=(1,2),
        min_df=1,
        max_df=0.95
    )
    X = vectorizer.fit_transform(corpus)
    return {"X": X, "vectorizer": vectorizer}

def search_openai(query, M, df):
    client = get_openai_client()
    try:
        qemb = client.Embeddings.create(model="text-embedding-3-small", input=query)  # type: ignore
        qv = np.array(qemb["data"][0]["embedding"], dtype="float32").reshape(1, -1)
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar embedding da consulta: {e}")
    # cosseno manual
    A = M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)
    B = qv / (np.linalg.norm(qv, axis=1, keepdims=True) + 1e-9)
    scores = A @ B.T
    scores = scores.ravel()
    idx = np.argsort(-scores)
    return idx, scores

def search_local(query, tfidf_pack, df):
    X = tfidf_pack["X"]
    vectorizer = tfidf_pack["vectorizer"]
    q = vectorizer.transform([query])
    sims = cosine_similarity(q, X).ravel()
    idx = np.argsort(-sims)
    return idx, sims

# =========================
# PREPARO DOS DADOS
# =========================
df = data["job_profile"].copy()
df["merged_text"] = df.apply(merge_row_text, axis=1)

embeddings_ready = False
openai_error_msg = None
tfidf_pack = None
M = None

try:
    # tenta OpenAI
    M = generate_embeddings_openai(df)
    embeddings_ready = True
    MODE = "openai"
except Exception as e:
    # fallback local
    openai_error_msg = str(e)
    MODE = "local"
    tfidf_pack = generate_embeddings_local(df)
    embeddings_ready = True

# =========================
# UI DE BUSCA (sempre aparece)
# =========================
if openai_error_msg:
    st.info("🔎 Modo **LOCAL** ativo (TF-IDF). A API de embeddings não pôde ser usada.\n\n"
            f"Detalhe técnico: {openai_error_msg}")

query = st.text_area(
    "Descreva as atividades do cargo:",
    placeholder="Ex.: processar folha de pagamento, recolher encargos, liderar equipe de 4 analistas...",
    height=120
)
buscar = st.button("Encontrar perfil correspondente", type="primary", disabled=not embeddings_ready)

if buscar and query.strip():
    if MODE == "openai":
        idx, scores = search_openai(query, M, df)
    else:
        idx, scores = search_local(query, tfidf_pack, df)

    # pega o top 1 (ou mostre top 3 se preferir)
    best = idx[0]
    score = float(scores[best])
    row = df.iloc[best]

    st.success(f"Cargo sugerido: **{row.get('Job Profile', '—')}** (similaridade: {score:.1%})")

    # aqui reaproveite a mesma função de renderização da página “Job Profile Description”
    # para exibir Sub Job Family Description, Job Profile Description, Role Description,
    # Grade Differentiator, KPIs e Qualifications exatamente com o mesmo layout.
    # Exemplo simplificado:
    st.markdown("—")
    st.markdown("### Classificação & Código")
    st.markdown(f"**Família:** {row.get('Job Family','')}")
    st.markdown(f"**Subfamília:** {row.get('Sub Job Family','')}")
    st.markdown(f"**Carreira:** {row.get('Career Path','')}")
    st.markdown(f"**Função:** {row.get('Function Code','')}")
    st.markdown(f"**Disciplina:** {row.get('Discipline Code','')}")
    st.markdown(f"**Código:** {row.get('Full Job Code','')}")

    st.markdown("### Sub Job Family Description")
    st.write(row.get("Sub Job Family Description","-") or "-")

    st.markdown("### Job Profile Description")
    st.write(row.get("Job Profile Description","-") or "-")

    st.markdown("### Role Description")
    st.write(row.get("Role Description","-") or "-")

    st.markdown("### Grade Differentiator")
    gd = row.get("Grade Differentiator","") or row.get("Grade Differentiatior","") or "-"
    st.write(gd)

    st.markdown("### KPIs / Specific Parameters")
    kp = row.get("Specific parameters KPIs","") or row.get("Specific parameters / KPIs","") or "-"
    st.write(kp)

    st.markdown("### Qualifications")
    st.write(row.get("Qualifications","-") or "-")
