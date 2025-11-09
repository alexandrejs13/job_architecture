import re
import streamlit as st
import pandas as pd
from utils.data_loader import load_job_profile_df

st.set_page_config(layout="wide", page_title="📋 Job Profile Description")

# ===========================================================
# CSS mantido idêntico ao layout aprovado
# ===========================================================
st.markdown("""
<style>
.block-container { max-width:1200px !important; min-width:900px !important; margin:0 auto !important; padding:2.5rem 1.5rem 2rem 1.5rem; zoom:0.9; }
h1 { text-align:left !important; margin-top:0.8rem !important; margin-bottom:1.4rem !important; font-size:1.9rem !important; }
.ja-p { margin:0 0 4px 0; text-align:left; line-height:1.48; }
.ja-hd { display:flex; flex-direction:column; align-items:flex-start; gap:4px; margin:0 0 6px 0; text-align:left; }
.ja-hd-title { font-size:1.15rem; font-weight:700; }
.ja-hd-grade { color:#1E56E0; font-weight:700; font-size:1rem; }
.ja-class { background:#fff; border:1px solid #e0e4f0; border-radius:6px; padding:8px 12px; width:100%; text-align:left; min-height:130px; }
.ja-sec-h { display:flex; align-items:center; gap:6px; margin:0 0 3px 0 !important; }
.ja-ic { width:18px; text-align:center; }
.ja-ttl { font-weight:700; color:#1E56E0; font-size:0.95rem; }
.ja-card { background:#f9f9f9; padding:10px 14px; border-radius:6px; border-left:3px solid #1E56E0; min-height:120px; }
.ja-grid { display:grid; gap:14px; margin:6px 0 12px 0 !important; }
.ja-grid.cols-1 { grid-template-columns: repeat(1, 1fr); }
.ja-grid.cols-2 { grid-template-columns: repeat(2, 1fr); }
.ja-grid.cols-3 { grid-template-columns: repeat(3, 1fr); }
</style>
""", unsafe_allow_html=True)

st.markdown("## 📘 Job Profile Description")

# ===========================================================
# Carrega a planilha Excel
# ===========================================================
df = load_job_profile_df()

required_cols = [
    "Job Profile", "Job Family", "Sub Job Family", "Career Path",
    "Function Code", "Discipline Code", "Global Grade", "Full Job Code",
    "Sub Job Family Description", "Job Profile Description",
    "Career Band Description", "Role Description",
    "Grade Differentiator", "Qualifications"
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"As seguintes colunas não foram encontradas no Excel: {', '.join(missing)}")
    st.stop()

# ===========================================================
# Filtros
# ===========================================================
col1, col2, col3 = st.columns([1.2, 2.2, 1])
with col1:
    families = sorted(df["Job Family"].dropna().astype(str).unique())
    fam = st.selectbox("Família", families)

filtered = df[df["Job Family"] == fam]

with col2:
    subs = sorted(filtered["Sub Job Family"].dropna().astype(str).unique())
    sub = st.selectbox("Subfamília", subs)

sub_df = filtered[filtered["Sub Job Family"] == sub]

with col3:
    careers = sorted(sub_df["Career Path"].dropna().astype(str).unique())
    career = st.selectbox("Trilha de Carreira", careers)

career_df = sub_df[sub_df["Career Path"] == career]

# ===========================================================
# Multiselect
# ===========================================================
def option_label(row: pd.Series) -> str:
    g = str(row.get("Global Grade", "")).strip()
    p = str(row.get("Job Profile", "")).strip()
    return f"GG{int(float(g)) if str(g).replace('.','',1).isdigit() else g} — {p}" if g else p

career_df_sorted = career_df.copy()
def grade_key(v):
    s = str(v).strip()
    try:
        return float(s)
    except:
        return -1
career_df_sorted = career_df_sorted.sort_values(by="Global Grade", key=lambda s: s.map(grade_key), ascending=False)

pick_options = career_df_sorted.apply(option_label, axis=1).tolist()
selected_labels = st.multiselect("Selecione até 3 cargos:", options=pick_options, max_selections=3)

# ===========================================================
# Funções utilitárias
# ===========================================================
def safe_get(row, col):
    val = row.get(col) if row is not None and col in row else ""
    return "-" if pd.isna(val) or str(val).strip() == "" else str(val).strip()

def format_paragraphs(text):
    if not text or text == "-":
        return "-"
    parts = re.split(r"\n+|•|\r", text.strip())
    return "".join(f"<p class='ja-p'>{p.strip()}</p>" for p in parts if len(p.strip()) > 1)

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
      <b>Família:</b> {safe_get(row, 'Job Family')}<br>
      <b>Subfamília:</b> {safe_get(row, 'Sub Job Family')}<br>
      <b>Carreira:</b> {safe_get(row, 'Career Path')}<br>
      <b>Função:</b> {safe_get(row, 'Function Code')}<br>
      <b>Disciplina:</b> {safe_get(row, 'Discipline Code')}<br>
      <b>Código:</b> {safe_get(row, 'Full Job Code')}
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
# Renderização
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
            career_df_sorted["Job Profile"].astype(str).str.strip().str.lower() == label_title.lower()
        ]
        if label_grade:
            sel = sel[sel["Global Grade"].astype(str).str.strip() == label_grade]

        rows.append(sel.iloc[0] if not sel.empty else None)

    n = len(rows)
    grid_class = f"ja-grid cols-{n}"

    html_cells = [f"<div>{header_badge(safe_get(r, 'Job Profile'), safe_get(r, 'Global Grade'))}</div>" for r in rows]
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

    html_cells = [f"<div>{class_box(r)}</div>" for r in rows]
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

    SECTIONS = [
        ("🧭", "Sub Job Family Description"),
        ("🧠", "Job Profile Description"),
        ("🎓", "Career Band Description"),
        ("🎯", "Role Description"),
        ("🏅", "Grade Differentiator"),
        ("📘", "Qualifications"),
    ]

    for emoji, col in SECTIONS:
        html_cells = [f"<div>{cell_card(emoji, col, format_paragraphs(safe_get(r, col)))}</div>" for r in rows]
        st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)
