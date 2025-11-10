# -*- coding: utf-8 -*-
import re
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.data_loader import load_job_profile_df
from utils.ui_components import section, lock_sidebar

# ===========================================================
# CONFIGURAÇÃO
# ===========================================================
st.set_page_config(layout="wide", page_title="🧭 Job Match")
lock_sidebar()
section("🧭 Job Match")

# ===========================================================
# CSS — igual ao Job Profile Description
# ===========================================================
st.markdown("""
<style>
.block-container {
  max-width: 1200px !important;
  min-width: 900px !important;
  margin: 0 auto !important;
  padding: 2.5rem 1.5rem 2rem 1.5rem;
  zoom: 0.9;
}
h1 {
  text-align: left !important;
  margin-top: 0.8rem !important;
  margin-bottom: 1.4rem !important;
  font-size: 1.9rem !important;
  line-height: 1.25 !important;
  font-weight: 800 !important;
  color: #145efc !important;
}
.ja-grid {
  display: grid;
  gap: 14px 14px;
  justify-items: stretch;
  align-items: stretch;
  margin: 6px 0 12px 0 !important;
}
.ja-grid.cols-3 { grid-template-columns: repeat(3, minmax(340px, 1fr)); }
.ja-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  background: #f9f9f9;
  padding: 10px 14px;
  border-radius: 6px;
  border-left: 3px solid #1E56E0;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  width: 100%;
  text-align: left;
  box-sizing: border-box;
  flex: 1;
}
.ja-sec { margin: 0 !important; text-align: left; display: flex; flex-direction: column; height: 100%; }
.ja-sec-h { display: flex; align-items: center; justify-content: flex-start; gap: 6px; margin: 0 0 3px 0 !important; }
.ja-ic { width: 18px; text-align: center; line-height: 1; }
.ja-ttl { font-weight: 700; color: #1E56E0; font-size: 0.95rem; }
.ja-hd { display: flex; flex-direction: column; align-items: flex-start; justify-content: flex-start; gap: 4px; margin: 0 0 6px 0; text-align: left; }
.ja-hd-title { font-size: 1.15rem; font-weight: 700; }
.ja-hd-grade { color: #1E56E0; font-weight: 700; font-size: 1rem; }
.ja-p { margin: 0 0 4px 0; text-align: left; line-height: 1.48; }
.match-score {
  font-weight: 700;
  color: #145efc;
  background: #eaf1ff;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# FUNÇÕES
# ===========================================================
def format_paragraphs(text):
    if not text:
        return "-"
    parts = re.split(r"\n+|•|\r", text.strip())
    return "".join(f"<p class='ja-p'>{p.strip()}</p>" for p in parts if len(p.strip()) > 2)

def header_badge(title, grade, score):
    return f"""
    <div class="ja-hd">
      <div class="ja-hd-title">{title}</div>
      <div class="ja-hd-grade">GG {grade}</div>
      <div class="match-score">Compatibilidade: {score:.1f}%</div>
    </div>
    """

def cell_card(emoji, title, html_text):
    return f"""
    <div class="ja-sec">
      <div class="ja-sec-h">
        <span class="ja-ic">{emoji}</span>
        <span class="ja-ttl">{title}</span>
      </div>
      <div class="ja-card">{html_text}</div>
    </div>
    """

def compute_similarity(df, input_text):
    text_fields = [
        "Sub Job Family Description",
        "Job Profile Description",
        "Career Band Description",
        "Role Description",
        "Grade Differentiator",
        "Qualifications"
    ]
    df["combined"] = df[text_fields].fillna("").agg(" ".join, axis=1)
    vectorizer = TfidfVectorizer(stop_words="portuguese")
    tfidf_matrix = vectorizer.fit_transform(df["combined"])
    query_vec = vectorizer.transform([input_text])
    df["similarity"] = cosine_similarity(query_vec, tfidf_matrix)[0] * 100
    return df.sort_values("similarity", ascending=False).head(3)

# ===========================================================
# INTERFACE
# ===========================================================
df = load_job_profile_df()

st.markdown("### Informe o texto base para análise de compatibilidade")
input_text = st.text_area(
    "Cole aqui o conteúdo do cargo, descrição ou responsabilidades do colaborador:",
    height=180,
    placeholder="Ex: Responsável por conciliações contábeis, análise de lançamentos e apoio ao fechamento mensal..."
)

if st.button("🔍 Buscar os 3 cargos mais compatíveis"):
    if not input_text.strip():
        st.warning("Por favor, insira um texto para análise.")
    else:
        ranked = compute_similarity(df, input_text)
        rows = [ranked.iloc[i] for i in range(len(ranked))]
        n = len(rows)
        grid_class = f"ja-grid cols-{n}"

        # Cabeçalhos
        html_cells = [
            f"<div>{header_badge(r['Job Profile'], r['Global Grade'], r['similarity'])}</div>" for r in rows
        ]
        st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

        # Seções principais
        SECTIONS = [
            ("🧠", "Job Profile Description", lambda r: r["Job Profile Description"]),
            ("🏛️", "Career Band Description", lambda r: r["Career Band Description"]),
            ("🎯", "Role Description", lambda r: r["Role Description"]),
            ("🎓", "Qualifications", lambda r: r["Qualifications"]),
        ]

        for emoji, title, getter in SECTIONS:
            html_cells = []
            for r in rows:
                raw = getter(r)
                html_cells.append("<div>" + cell_card(emoji, title, format_paragraphs(raw)) + "</div>")
            st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)
