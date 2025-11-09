import re
import streamlit as st
from utils.data_loader import load_excel_data
from utils.ui_components import section

# ===========================================================
# ✅ A PRIMEIRA LINHA EXECUTÁVEL DO STREAMLIT
# ===========================================================
st.set_page_config(layout="wide")

# ===========================================================
# CSS — mantido idêntico ao modelo que estava perfeito
# ===========================================================
st.markdown("""
<style>

/* ====== CONTAINER CENTRAL ====== */
.block-container {
  max-width: 1200px !important;
  min-width: 900px !important;
  margin: 0 auto !important;
  padding: 2.5rem 1.5rem 2rem 1.5rem;
  zoom: 0.9;
}

/* ====== ESCALA RESPONSIVA ====== */
html, body, [class*="css"] {
  font-size: calc(13px + 0.18vw) !important;
}

/* ====== TÍTULO DA PÁGINA ====== */
h1 {
  text-align: left !important;
  margin-top: 0.8rem !important;
  margin-bottom: 1.4rem !important;
  line-height: 1.25 !important;
  overflow-wrap: break-word !important;
  white-space: normal !important;
  word-break: break-word !important;
  font-size: 1.9rem !important;
}
h2, h3 {
  text-align: left !important;
  margin-top: 1rem !important;
  margin-bottom: 1.1rem !important;
}

/* ====== SIDEBAR ====== */
[data-testid="stSidebar"][aria-expanded="true"]{
  width: 300px !important;
  min-width: 300px !important;
  max-width: 300px !important;
}
[data-testid="stSidebarCollapsedControl"]{
  width: 300px !important;
}

/* ====== TEXTOS ====== */
.ja-p {
  margin: 0 0 4px 0;
  text-align: left;
  line-height: 1.48;
}

/* ====== TÍTULOS DE CARGO ====== */
.ja-hd {
  display:flex;
  flex-direction:column;
  align-items:flex-start;
  justify-content:flex-start;
  gap:4px;
  margin:0 0 6px 0;
  text-align:left;
}
.ja-hd-title {
  font-size:1.15rem;
  font-weight:700;
}
.ja-hd-grade {
  color:#1E56E0;
  font-weight:700;
  font-size:1rem;
}

/* ====== CLASSE DE CARGO ====== */
.ja-class {
  background:#fff;
  border:1px solid #e0e4f0;
  border-radius:6px;
  padding:8px 12px;
  width:100%;
  text-align:left;
  box-sizing:border-box;
  min-height:130px;
}

/* ====== SEÇÕES ====== */
.ja-sec { margin: 0 !important; text-align:left; }
.ja-sec-h {
  display:flex;
  align-items:center;
  justify-content:flex-start;
  gap:6px;
  margin:0 0 3px 0 !important;
}
.ja-ic { width:18px; text-align:center; line-height:1; }
.ja-ttl {
  font-weight:700;
  color:#1E56E0;
  font-size:0.95rem;
}
.ja-card {
  background:#f9f9f9;
  padding:10px 14px;
  border-radius:6px;
  border-left:3px solid #1E56E0;
  box-shadow:0 1px 2px rgba(0,0,0,0.05);
  width:100%;
  text-align:left;
  display:block;
  min-height:120px;
  box-sizing:border-box;
}

/* ====== GRID ====== */
.ja-grid {
  display:grid;
  gap:14px 14px;
  justify-items:stretch;
  align-items:start;
  margin:6px 0 12px 0 !important;
}
.ja-grid.cols-1 { grid-template-columns: repeat(1, minmax(250px, 1fr)); }
.ja-grid.cols-2 { grid-template-columns: repeat(2, minmax(300px, 1fr)); }
.ja-grid.cols-3 { grid-template-columns: repeat(3, minmax(340px, 1fr)); }

/* ====== MULTISELECT ====== */
.compare-box { margin-top:-14px; }
.compare-box .compare-label {
  margin:4px 0 5px 0;
  font-weight:600;
  color:#2b2d42;
  font-size:0.85rem;
}
div[data-baseweb="tag"] span {
  white-space: normal !important;
  word-break: break-word !important;
  line-height: 1.15 !important;
  font-weight: 600 !important;
  font-size: 0.82rem !important;
}
div[data-baseweb="select"] > div {
  min-height:38px !important;
  height:auto !important;
}

</style>
""", unsafe_allow_html=True)

# ===========================================================
# Funções utilitárias
# ===========================================================
def safe_get(row, keys, default=""):
    for k in keys if isinstance(keys, list) else [keys]:
        for col in row.index:
            if col.strip().lower() == k.strip().lower():
                val = str(row[col]).strip()
                if val and val.lower() != "nan":
                    return val
    return default

def format_paragraphs(text):
    if not text:
        return "-"
    parts = re.split(r"\n+|•|\r", text.strip())
    return "".join(f"<p class='ja-p'>{p.strip()}</p>" for p in parts if len(p.strip()) > 2)

def header_badge(title, grade):
    return f"""
    <div class="ja-hd">
      <div class="ja-hd-title">{title}</div>
      <div class="ja-hd-grade">GG {grade}</div>
    </div>
    """

def class_box(row):
    return f"""
    <div class="ja-class">
      <b>Família:</b> {row['Job Family']}<br>
      <b>Subfamília:</b> {row['Sub Job Family']}<br>
      <b>Carreira:</b> {row['Career Path']}<br>
      <b>Função:</b> {row['Function Code']}<br>
      <b>Disciplina:</b> {row['Discipline Code']}<br>
      <b>Código:</b> {row['Full Job Code']}
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

# ===========================================================
# Página principal
# ===========================================================
data = load_excel_data()
section("📘 Job Profile Description")

if "job_profile" not in data:
    st.error("Job Profile.xlsx não encontrado em /data")
    st.stop()

df = data["job_profile"]

# ===========================================================
# Filtros
# ===========================================================
col1, col2, col3 = st.columns([1.2, 2.2, 1])
with col1:
    families = sorted(df["Job Family"].dropna().unique())
    fam = st.selectbox("Família", families)
filtered = df[df["Job Family"] == fam]

with col2:
    subs = sorted(filtered["Sub Job Family"].dropna().unique())
    sub = st.selectbox("Subfamília", subs)
sub_df = filtered[filtered["Sub Job Family"] == sub]

with col3:
    careers = sorted(sub_df["Career Path"].dropna().unique())
    career = st.selectbox("Trilha de Carreira", careers)
career_df = sub_df[sub_df["Career Path"] == career]

# ===========================================================
# Multiselect de cargos
# ===========================================================
def option_label(row):
    g = row.get("Global Grade", "")
    p = row.get("Job Profile", "")
    return f"GG{int(g)} — {p}" if str(g).isdigit() else p

career_df_sorted = career_df.sort_values(by="Global Grade", ascending=False)
pick_options = career_df_sorted.apply(option_label, axis=1).tolist()

st.markdown('<div class="compare-box">', unsafe_allow_html=True)
st.markdown('<div class="compare-label">Selecione até 3 cargos para comparar:</div>', unsafe_allow_html=True)
selected_labels = st.multiselect("", options=pick_options, max_selections=3, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# ===========================================================
# Renderização comparativa
# ===========================================================
if selected_labels:
    st.markdown("---")
    st.markdown("### 🧾 Comparativo de Cargos Selecionados")

    rows = []
    for label in selected_labels:
        parts = re.split(r"\s*[–—-]\s*", label)
        label_grade = parts[0].replace("GG", "").strip() if parts else ""
        label_title = parts[1].strip() if len(parts) > 1 else label.strip()
        sel = career_df_sorted[
            career_df_sorted["Job Profile"].str.strip().str.lower() == label_title.lower()
        ]
        if label_grade:
            sel = sel[sel["Global Grade"].astype(str).str.strip() == label_grade]
        rows.append(sel.iloc[0] if not sel.empty else None)

    n = len(rows)
    grid_class = f"ja-grid cols-{n}"

    # Cabeçalhos
    html_cells = [f"<div>{header_badge(r['Job Profile'], r['Global Grade'])}</div>" if r is not None else "<div></div>" for r in rows]
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

    # Classificação
    html_cells = [f"<div>{class_box(r)}</div>" if r is not None else "<div></div>" for r in rows]
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

    # Seções principais
    SECTIONS = [
        ("🧭", "Sub Job Family Description", lambda r: safe_get(r, "Sub Job Family Description")),
        ("🧠", "Job Profile Description",   lambda r: safe_get(r, "Job Profile Description")),
        ("🎯", "Role Description",          lambda r: safe_get(r, "Role Description")),
        ("🏅", "Grade Differentiator",      lambda r: safe_get(r, [
            "Grade Differentiator", "Grade Differentiation",
            "Grade Differentiatior", "Grade Differentiators"
        ])),
        ("📊", "KPIs / Specific Parameters", lambda r: safe_get(r, [
            "Specific parameters KPIs", "Specific parameters / KPIs"
        ])),
        ("🎓", "Qualifications",            lambda r: safe_get(r, "Qualifications")),
    ]

    for emoji, title, getter in SECTIONS:
        html_cells = []
        for r in rows:
            if r is None:
                html_cells.append("<div></div>")
            else:
                raw = getter(r)
                html_cells.append("<div>" + cell_card(emoji, title, format_paragraphs(raw)) + "</div>")
        st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)
