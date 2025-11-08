import streamlit as st
import pandas as pd
import numpy as np
import re
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from deep_translator import GoogleTranslator
from utils.data_loader import load_data
from utils.ui_components import section

# ===========================================================
# CONFIGURAÇÃO
# ===========================================================
st.set_page_config(layout="wide")
section("🧠 Find My Job Profile")

# ===========================================================
# CSS — igual à página 2
# ===========================================================
st.markdown("""
<style>
.block-container { max-width: 1600px !important; margin: 0 auto !important; }
[data-testid="stSidebar"][aria-expanded="true"]{ width: 320px !important; }
.ja-hd { display:flex; align-items:baseline; gap:10px; margin:0 0 6px 0; }
.ja-hd-title { font-size:1.05rem; font-weight:700; }
.ja-hd-grade { color:#1E56E0; font-weight:700; }
.ja-class {
  background:#fff; border:1px solid #e0e4f0; border-radius:8px;
  padding:10px; width:100%; display:inline-block;
}
.ja-sec { margin:0 !important; }
.ja-sec-h { display:flex; align-items:center; gap:8px; margin:0 0 4px 0 !important; }
.ja-ic { width:24px; text-align:center; line-height:1; }
.ja-ttl { font-weight:700; color:#1E56E0; font-size:0.98rem; }
.ja-card {
  background:#f9f9f9; padding:10px 14px; border-radius:8px;
  border-left:4px solid #1E56E0;
  box-shadow:0 1px 3px rgba(0,0,0,0.05); width:100%;
}
.ja-grid { display:grid; gap:12px 12px; margin:2px 0 14px 0 !important; }
.ja-grid.cols-1 { grid-template-columns: repeat(1, 1fr); }
.ja-grid.cols-2 { grid-template-columns: repeat(2, 1fr); }
.ja-grid.cols-3 { grid-template-columns: repeat(3, 1fr); }
.result-card {
  border: 1px solid #e0e4f0;
  border-radius: 10px;
  padding: 10px 14px;
  margin-bottom: 10px;
  background: #f9f9f9;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.result-title {
  font-weight: 700;
  color: #1E56E0;
  font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# CARREGAR BASE
# ===========================================================
data = load_data()
if "job_profile" not in data:
    st.error("❌ Arquivo Job Profile.csv não encontrado em /data")
    st.stop()

df = data["job_profile"].copy()

def merge_row_text(row):
    parts = [
        str(row.get("Sub Job Family Description", "")),
        str(row.get("Job Profile Description", "")),
        str(row.get("Role Description", "")),
        str(row.get("Grade Differentiator", "")) or str(row.get("Grade Differentiatior", "")),
        str(row.get("Specific parameters KPIs", "")) or str(row.get("Specific parameters / KPIs", "")),
        str(row.get("Qualifications", "")),
    ]
    return " ".join([p for p in parts if p and p.lower() != "nan"]).strip()

df["merged_text"] = df.apply(merge_row_text, axis=1)

# ===========================================================
# EMBEDDINGS
# ===========================================================
@st.cache_resource(show_spinner=True)
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_data(show_spinner=False)
def generate_embeddings(df):
    model = load_model()
    emb = model.encode(df["merged_text"].tolist(), show_progress_bar=False, normalize_embeddings=True)
    return emb

with st.spinner("🔄 Preparando base semântica local..."):
    matrix = generate_embeddings(df)
st.success("✅ Base semântica pronta.")

# ===========================================================
# TRADUÇÃO AUTOMÁTICA
# ===========================================================
def translate_to_english(text):
    try:
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception as e:
        st.warning(f"⚠️ Falha ao traduzir automaticamente: {e}")
        return text

# ===========================================================
# INTERFACE DE BUSCA
# ===========================================================
st.markdown("#### Descreva as atividades ou responsabilidades do cargo desejado (em qualquer idioma):")
query = st.text_area(
    "Exemplo: Gerenciar folha de pagamento, processar encargos e liderar equipe de analistas.",
    height=120
)
buscar = st.button("🔍 Encontrar cargos correspondentes", type="primary")

# ===========================================================
# BUSCA E RESULTADOS
# ===========================================================
if buscar and query.strip():
    with st.spinner("🌐 Traduzindo e analisando sua descrição..."):
        translated_query = translate_to_english(query)

    model = load_model()
    q_emb = model.encode([translated_query], normalize_embeddings=True)
    sims = cosine_similarity(q_emb, generate_embeddings(df)).ravel()
    idx = np.argsort(-sims)

    top_n = 5
    results = [(i, sims[i]) for i in idx[:top_n]]

    st.markdown("---")
    st.subheader("🎯 Cargos mais compatíveis:")

    compare_labels = []
    for i, score in results:
        row = df.iloc[i]
        label = f"{row.get('Job Profile','-')} (GG {row.get('Global Grade','')})"
        compare_labels.append(label)

        st.markdown(f"<div class='result-card'>"
                    f"<div class='result-title'>{row.get('Job Profile','-')}</div>"
                    f"<div>Similaridade: {score*100:.1f}%</div>"
                    f"</div>", unsafe_allow_html=True)

        with st.expander(f"Ver detalhes — {row.get('Job Profile','-')}"):
            st.markdown(f"**Família:** {row.get('Job Family','')}")
            st.markdown(f"**Subfamília:** {row.get('Sub Job Family','')}")
            st.markdown(f"**Carreira:** {row.get('Career Path','')}")
            st.markdown(f"**Função:** {row.get('Function Code','')}")
            st.markdown(f"**Disciplina:** {row.get('Discipline Code','')}")
            st.markdown(f"**Código:** {row.get('Full Job Code','')}")

            st.markdown("### 🧭 Sub Job Family Description")
            st.write(row.get("Sub Job Family Description","-") or "-")

            st.markdown("### 🧠 Job Profile Description")
            st.write(row.get("Job Profile Description","-") or "-")

            st.markdown("### 🎯 Role Description")
            st.write(row.get("Role Description","-") or "-")

            st.markdown("### 🏅 Grade Differentiator")
            gd = row.get("Grade Differentiator","") or row.get("Grade Differentiatior","") or "-"
            st.write(gd)

            st.markdown("### 📊 KPIs / Specific Parameters")
            kp = row.get("Specific parameters KPIs","") or row.get("Specific parameters / KPIs","") or "-"
            st.write(kp)

            st.markdown("### 🎓 Qualifications")
            st.write(row.get("Qualifications","-") or "-")

    st.markdown("---")
    st.markdown("### ⚖️ Selecione cargos para comparar:")
    selected_labels = st.multiselect("", options=compare_labels, max_selections=3)

    if selected_labels:
        st.markdown("---")
        st.subheader("📋 Comparativo de Cargos Selecionados")

        selected_rows = []
        for label in selected_labels:
            name = label.split(" (GG")[0].strip()
            grade = re.findall(r"GG\s*(\d+)", label)
            grade = grade[0] if grade else None
            sel = df[(df["Job Profile"].str.strip().str.lower() == name.lower())]
            if grade:
                sel = sel[sel["Global Grade"].astype(str).str.strip() == grade]
            if not sel.empty:
                selected_rows.append(sel.iloc[0])

        n = len(selected_rows)
        grid_class = f"ja-grid cols-{n}"

        html_cells = [f"<div><div class='ja-hd'><div class='ja-hd-title'>{r['Job Profile']}</div><div class='ja-hd-grade'>GG {r['Global Grade']}</div></div></div>" for r in selected_rows]
        st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

        html_cells = [f"<div class='ja-class'><b>Família:</b> {r['Job Family']}<br><b>Subfamília:</b> {r['Sub Job Family']}<br><b>Carreira:</b> {r['Career Path']}<br><b>Função:</b> {r['Function Code']}<br><b>Disciplina:</b> {r['Discipline Code']}<br><b>Código:</b> {r['Full Job Code']}</div>" for r in selected_rows]
        st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

        SECTIONS = [
            ("🧭", "Sub Job Family Description", lambda r: r.get("Sub Job Family Description")),
            ("🧠", "Job Profile Description",   lambda r: r.get("Job Profile Description")),
            ("🎯", "Role Description",          lambda r: r.get("Role Description")),
            ("🏅", "Grade Differentiator",      lambda r: r.get("Grade Differentiator") or r.get("Grade Differentiatior")),
            ("📊", "KPIs / Specific Parameters", lambda r: r.get("Specific parameters KPIs") or r.get("Specific parameters / KPIs")),
            ("🎓", "Qualifications", lambda r: r.get("Qualifications")),
        ]

        for emoji, title, getter in SECTIONS:
            html_cells = []
            for r in selected_rows:
                raw = getter(r)
                html_cells.append(f"<div class='ja-sec'><div class='ja-sec-h'><span class='ja-ic'>{emoji}</span><span class='ja-ttl'>{title}</span></div><div class='ja-card'>{raw or '-'}</div></div>")
            st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

elif buscar:
    st.warning("⚠️ Por favor, digite uma descrição para buscar o cargo correspondente.")
else:
    st.info("✏️ Digite uma descrição acima e clique em 'Encontrar cargos correspondentes'.")
