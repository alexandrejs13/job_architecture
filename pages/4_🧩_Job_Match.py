import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from utils.data_loader import load_excel_data

st.set_page_config(layout="wide", page_title="🧩 Job Match Pro")

# === Estilo Aprimorado ===
st.markdown("""
<style>
.block-container {max-width: 1200px !important;}
.job-card {
    background: white;
    border-radius: 12px;
    padding: 20px 25px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border-left: 6px solid #1E56E0;
    transition: transform 0.2s;
}
.job-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(0,0,0,0.1);
}
.match-score {
    float: right;
    background: #eef2ff;
    color: #1E56E0;
    padding: 5px 12px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.9rem;
}
.highlight-label {
    font-weight: 600;
    color: #2c3e50;
    margin-top: 12px;
    display: block;
}
</style>
""", unsafe_allow_html=True)

# === Carregamento Otimizado ===
@st.cache_resource
def load_model():
    # O modelo 'all-mpnet-base-v2' geralmente é mais preciso que o MiniLM, 
    # embora um pouco mais lento. Se precisão for crucial, considere trocar.
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@st.cache_data(show_spinner=False)
def load_data_and_embeddings():
    data = load_excel_data()
    df_jobs = data.get("job_profile", pd.DataFrame()).fillna("")
    df_levels = data.get("level_structure", pd.DataFrame())

    # Garante colunas necessárias
    required_cols = ["Job Family", "Sub Job Family", "Job Profile", "Role Description", 
                     "Grade Differentiator", "KPIs / Specific Parameters", "Qualifications", "Global Grade"]
    for c in required_cols:
        if c not in df_jobs.columns: df_jobs[c] = ""

    # Limpeza do Grade
    df_jobs["Global Grade"] = df_jobs["Global Grade"].astype(str).str.extract(r"(\d+)").fillna("0").astype(int)

    # Engenharia de Prompt para o Modelo (Contexto explícito)
    # Adicionamos rótulos para ajudar o modelo a entender o que é cada parte do texto
    df_jobs["Rich_Text"] = (
        "Cargo: " + df_jobs["Job Profile"] + ". " +
        "Descrição: " + df_jobs["Role Description"] + ". " +
        "Diferencial de Nível: " + df_jobs["Grade Differentiator"] + ". " +
        "Requisitos: " + df_jobs["Qualifications"]
    )

    # Pré-computa todos os embeddings uma única vez
    model = load_model()
    embeddings = model.encode(df_jobs["Rich_Text"].tolist(), show_progress_bar=True)

    return df_jobs, df_levels, embeddings

# Carrega tudo na inicialização
df, levels, job_embeddings = load_data_and_embeddings()
model = load_model()

# === Interface ===
st.title("🧩 Job Match Inteligente")
st.markdown("Descreva as atividades e encontre o cargo mais aderente na estrutura.")

with st.container():
    c1, c2 = st.columns([1, 3])
    with c1:
        st.write("### 🎯 Filtros (Opcionais)")
        st.info("💡 Se não selecionar filtros, a busca será feita em **toda** a base de cargos.")
        
        families = sorted(df["Job Family"].unique())
        selected_family = st.selectbox("Família", ["Todas"] + families)
        
        subfamilies = []
        if selected_family != "Todas":
            subfamilies = sorted(df[df["Job Family"] == selected_family]["Sub Job Family"].unique())
        selected_subfamily = st.selectbox("Subfamília", ["Todas"] + subfamilies)

    with c2:
        desc_input = st.text_area(
            "✍️ Descreva as responsabilidades, requisitos e senioridade:",
            placeholder="Ex: Liderança de equipe de desenvolvimento de software, definição de arquitetura em nuvem AWS, gestão de KPIs de performance e mentoria técnica. Necessário inglês fluente e 8 anos de experiência.",
            height=250,
            help="Quanto mais detalhes sobre a senioridade (ex: 'liderança', 'apoio operacional', 'estratégia'), melhor será o match do Grade."
        )
        
        run_match = st.button("🔍 Analisar Aderência", type="primary", use_container_width=True)

# === Lógica de Matching ===
if run_match:
    if len(desc_input.split()) < 15:
        st.warning("⚠️ A descrição está muito curta para uma análise precisa. Tente adicionar mais detalhes (mínimo 15 palavras).")
        st.stop()

    # 1. Filtragem Base (Máscara Booleana)
    mask = pd.Series([True] * len(df))
    if selected_family != "Todas":
        mask &= (df["Job Family"] == selected_family)
    if selected_subfamily != "Todas":
        mask &= (df["Sub Job Family"] == selected_subfamily)

    if not mask.any():
        st.error("Nenhum cargo encontrado com os filtros selecionados.")
        st.stop()

    # 2. Cálculo de Similaridade (Apenas para os filtrados)
    # Pegamos os índices dos filtrados para usar os embeddings corretos
    filtered_indices = df[mask].index
    filtered_embeddings = job_embeddings[filtered_indices]
    
    query_embedding = model.encode([desc_input])
    
    # Cosine Similarity: retorna valores entre 0 e 1 (quanto mais próximo de 1, melhor)
    similarities = cosine_similarity(query_embedding, filtered_embeddings)[0]
    
    # 3. Montagem dos Resultados
    results = df.loc[filtered_indices].copy()
    results["similarity_score"] = similarities
    
    # Ordena e pega os Top 3
    top_matches = results.sort_values("similarity_score", ascending=False).head(3)

    # === Exibição dos Resultados ===
    st.markdown("---")
    st.subheader("🏆 Top 3 Cargos Mais Compatíveis")

    for idx, row in top_matches.iterrows():
        score_pct = row['similarity_score'] * 100
        
        # Define cor da borda baseada no score (Visual Cues)
        border_color = "#1E56E0" if score_pct > 75 else "#fd7e14" if score_pct > 60 else "#6c757d"
        
        level_name = "-"
        if not levels.empty and row["Global Grade"] in levels["Global Grade"].values:
             level_name = levels.loc[levels["Global Grade"] == row["Global Grade"], "Level Name"].values[0]

        # Card HTML Renderizado
        st.markdown(f"""
        <div class='job-card' style='border-left: 6px solid {border_color};'>
            <div class='match-score' style='color: {border_color}; background-color: {border_color}15;'>
                ⚡ {score_pct:.1f}% de Aderência
            </div>
            <h3 style='color: #2c3e50; margin-bottom: 8px;'>
                GG {row['Global Grade']} • {row['Job Profile']}
            </h3>
             <div style='margin-bottom: 15px; color: #666; font-size: 0.95rem;'>
                🏛️ {level_name} &nbsp; | &nbsp; 📂 {row['Job Family']} &rsaquo; {row['Sub Job Family']}
            </div>
            <hr style='margin: 10px 0; opacity: 0.2;'>
            <div style='display: flex; gap: 20px; flex-wrap: wrap;'>
                <div style='flex: 2; min-width: 300px;'>
                    <span class='highlight-label'>🎯 Descrição do Papel:</span>
                    <div style='color: #444; font-size: 0.95rem;'>{row['Role Description']}</div>
                    
                    <span class='highlight-label'>🏅 Diferencial de Nível:</span>
                    <div style='color: #444; font-size: 0.95rem;'>{row['Grade Differentiator']}</div>
                </div>
                <div style='flex: 1; min-width: 250px; background: #f8f9fa; padding: 15px; border-radius: 8px;'>
                    <span class='highlight-label' style='margin-top:0;'>🎓 Requisitos Chave:</span>
                    <div style='font-size: 0.9rem; color: #555;'>{row['Qualifications']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if top_matches.iloc[0]['similarity_score'] < 0.5:
        st.warning("⚠️ Atenção: A aderência encontrada é baixa (< 50%). Tente detalhar mais a descrição ou revisar os filtros de Família.")
