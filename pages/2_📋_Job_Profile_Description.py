import re
import pandas as pd
import streamlit as st
from utils.ui_components import section

# ===========================================================
# CONFIGURAÇÃO
# ===========================================================
st.set_page_config(layout="wide")

# ===========================================================
# CSS — idêntico ao modelo original
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
html, body, [class*="css"] {
  font-size: calc(13px + 0.18vw) !important;
}
h1 {
  text-align: left !important;
  margin-top: 0.8rem !important;
  margin-bottom: 1.4rem !important;
  line-height: 1.25 !important;
  font-size: 1.9rem !important;
}
.ja-p { margin: 0 0 4px 0; text-align: left; line-height: 1.48; }
.ja-hd { display:flex; flex-direction:column; align-items:flex-start; gap:4px; margin:0 0 6px 0; text-align:left; }
.ja-hd-title { font-size:1.15rem; font-weight:700; }
.ja-hd-grade { color:#1E56E0; font-weight:700; font-size:1rem; }
.ja-class { background:#fff; border:1px solid #e0e4f0; border-radius:6px; padding:8px 12px; min-height:130px; }
.ja-sec { margin:0 !important; text-align:left; }
.ja-sec-h { display:flex; align-items:center; gap:6px; margin:0 0 3px 0 !important; }
.ja-ic { width:18px; text-align:center; }
.ja-ttl { font-weight:700; color:#1E56E0; font-size:0.95rem; }
.ja-card { background:#f9f9f9; padding:10px 14px; border-radius:6px; border-left:3px solid #1E56E0; min-height:120px; box-sizing:border-box; }
.ja-grid { display:grid; gap:14px 14px; margin:6px 0 12px 0 !important; }
.ja-grid.cols-1 { grid-template-columns: repeat(1, 1fr); }
.ja-grid.cols-2 { grid-template-columns: repeat(2, 1fr); }
.ja-grid.cols-3 { grid-template-columns: repeat(3, 1fr); }
</style>
""", unsafe_allow_html=True)

# ===========================================================
# FUNÇÕES
# ===========================================================
def format_paragraphs(text):
    if not text or str(text).strip() in ("", "nan", None):
        return "-"
    parts = re.split(r"\n+|•|\r", str(text).strip())
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
      <b>Função:</b> {row.get('Function Code', '-')}<br>
      <b>Disciplina:</b> {row.get('Discipline Code', '-')}<br>
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
# CARREGAMENTO DO EXCEL
# ===========================================================
section("📘 Job Profile Description")

try:
    df = pd.read_excel("data/Job Profile.xlsx")
except Exception as e:
    st.error(f"❌ Erro ao carregar o arquivo Job Profile.xlsx: {e}")
    st.stop()

# ===========================================================
# MAPEAMENTO FIXO DAS COLUNAS (conforme estrutura enviada)
# ===========================================================
COLUMN_MAP = {
    "job_family": "Job Family",
    "sub_job_family": "Sub Job Family",
    "career_path": "Career Path",
    "job_profile": "Job Profile",
    "global_grade": "Global Grade",
    "full_job_code": "Full Job Code",
    "sub_job_family_description": "Sub Job Family Description",
    "job_profile_description": "Job Profile Description",
    "role_description": "Role Description",
    "grade_differentiator": "Grade Differentiator",
    "qualifications": "Qualifications",
}

missing_cols = [v for v in COLUMN_MAP.values() if v not in df.columns]
if missing_cols:
    st.error(f"⚠️ As seguintes colunas não foram encontradas no Excel: {', '.join(missing_cols)}")
    st.stop()

# ===========================================================
# FILTROS
# ===========================================================
col1, col2, col3 = st.columns([1.2, 2.2, 1])
with col1:
    families = sorted(df[COLUMN_MAP["job_family"]].dropna().unique())
    fam = st.selectbox("Família", families)

filtered = df[df[COLUMN_MAP["job_family"]] == fam]

with col2:
    subs = sorted(filtered[COLUMN_MAP["sub_job_family"]].dropna().unique())
    sub = st.selectbox("Subfamília", subs)

sub_df = filtered[filtered[COLUMN_MAP["sub_job_family"]] == sub]

with col3:
    careers = sorted(sub_df[COLUMN_MAP["career_path"]].dropna().unique())
    career = st.selectbox("Trilha de Carreira", careers)

career_df = sub_df[sub_df[COLUMN_MAP["career_path"]] == career]

# ===========================================================
# MULTISELECT DE CARGOS
# ===========================================================
def option_label(row):
    g = row[COLUMN_MAP["global_grade"]]
    p = row[COLUMN_MAP["job_profile"]]
    return f"GG{int(g)} — {p}" if pd.notna(g) else p

career_df_sorted = career_df.sort_values(by=COLUMN_MAP["global_grade"], ascending=False)
options = [option_label(r) for _, r in career_df_sorted.iterrows()]
selected = st.multiselect("Selecione até 3 cargos para comparar:", options, max_selections=3)

# ===========================================================
# RENDERIZAÇÃO
# ===========================================================
if selected:
    st.markdown("---")
    st.markdown("### 🧾 Comparativo de Cargos Selecionados")

    rows = []
    for sel in selected:
        parts = re.split(r"\s*[–—-]\s*", sel)
        title = parts[-1].strip()
        match = career_df_sorted[
            career_df_sorted[COLUMN_MAP["job_profile"]].astype(str).str.strip().str.lower() == title.lower()
        ]
        rows.append(match.iloc[0] if not match.empty else None)

    n = len(rows)
    grid_class = f"ja-grid cols-{n}"

    # Cabeçalhos
    headers = [f"<div>{header_badge(r[COLUMN_MAP['job_profile']], r[COLUMN_MAP['global_grade']])}</div>" if r is not None else "<div></div>" for r in rows]
    st.markdown(f"<div class='{grid_class}'>" + "".join(headers) + "</div>", unsafe_allow_html=True)

    # Classes
    classes = [f"<div>{class_box(r)}</div>" if r is not None else "<div></div>" for r in rows]
    st.markdown(f"<div class='{grid_class}'>" + "".join(classes) + "</div>", unsafe_allow_html=True)

    # Seções (sem KPIs)
    SECTIONS = [
        ("🧭", "Sub Job Family Description", "sub_job_family_description"),
        ("🧠", "Job Profile Description", "job_profile_description"),
        ("🎯", "Role Description", "role_description"),
        ("🏅", "Grade Differentiator", "grade_differentiator"),
        ("🎓", "Qualifications", "qualifications"),
    ]

    for emoji, title, key in SECTIONS:
        html_cells = []
        for r in rows:
            if r is None:
                html_cells.append("<div></div>")
            else:
                val = r[COLUMN_MAP[key]]
                html_cells.append("<div>" + cell_card(emoji, title, format_paragraphs(val)) + "</div>")
        st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)
else:
    st.info("👆 Selecione até 3 cargos para comparar.")
