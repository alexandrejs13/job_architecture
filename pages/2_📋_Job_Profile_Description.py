import re
import unicodedata
import pandas as pd
import streamlit as st
from utils.ui_components import section

# ===========================================================
# CONFIGURAÇÃO INICIAL
# ===========================================================
st.set_page_config(layout="wide")

# ===========================================================
# CSS ORIGINAL (mantido)
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
# FUNÇÕES AUXILIARES
# ===========================================================
def normalize_col(col):
    """Remove acentos, espaços, caracteres especiais e põe tudo em minúsculas."""
    col = str(col).strip()
    col = unicodedata.normalize("NFKD", col)
    col = "".join(c for c in col if not unicodedata.combining(c))
    col = re.sub(r"[^a-zA-Z0-9]+", "_", col)
    return col.lower()

def safe_get(row, possible_keys):
    """Busca valor em colunas já normalizadas, aceitando várias variações."""
    for key in possible_keys:
        norm_key = normalize_col(key)
        for col in row.index:
            if normalize_col(col) == norm_key:
                val = str(row[col]).strip()
                if val and val.lower() != "nan":
                    return val
    return "-"

def format_paragraphs(text):
    if not text or text == "-":
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
      <b>Família:</b> {safe_get(row, ["Job Family"])}<br>
      <b>Subfamília:</b> {safe_get(row, ["Sub Job Family"])}<br>
      <b>Carreira:</b> {safe_get(row, ["Career Path"])}<br>
      <b>Função:</b> {safe_get(row, ["Function Code"])}<br>
      <b>Disciplina:</b> {safe_get(row, ["Discipline Code"])}<br>
      <b>Código:</b> {safe_get(row, ["Full Job Code"])}
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
# CARREGAMENTO SEGURO DO EXCEL
# ===========================================================
section("📘 Job Profile Description")

try:
    df = pd.read_excel("data/Job Profile.xlsx")
    df.columns = [normalize_col(c) for c in df.columns]
except Exception as e:
    st.error(f"❌ Erro ao carregar 'Job Profile.xlsx': {e}")
    st.stop()

# ===========================================================
# FILTROS
# ===========================================================
def get_values(col_name):
    matches = [c for c in df.columns if col_name in c]
    if not matches:
        return []
    return sorted(df[matches[0]].dropna().unique())

families = get_values("job_family")
if not families:
    st.error("❌ Coluna 'Job Family' não encontrada no Excel.")
    st.stop()

col1, col2, col3 = st.columns([1.2, 2.2, 1])
with col1:
    fam = st.selectbox("Família", families)
filtered = df[df[df.columns[df.columns.str.contains("job_family")][0]] == fam]

with col2:
    subs = get_values("sub_job_family")
    sub = st.selectbox("Subfamília", subs)
sub_df = filtered[filtered[filtered.columns[filtered.columns.str.contains("sub_job_family")][0]] == sub]

with col3:
    careers = get_values("career_path")
    career = st.selectbox("Trilha de Carreira", careers)
career_df = sub_df[sub_df[sub_df.columns[sub_df.columns.str.contains("career_path")][0]] == career]

# ===========================================================
# MULTISELECT DE CARGOS
# ===========================================================
def option_label(row):
    g = safe_get(row, ["Global Grade", "Grade", "GG"])
    p = safe_get(row, ["Job Profile", "Profile Name", "Role Title"])
    return f"GG{int(float(g))} — {p}" if g.replace(".", "", 1).isdigit() else p

career_df_sorted = career_df.sort_values(by=[c for c in df.columns if "grade" in c][0], ascending=False)
pick_options = career_df_sorted.apply(option_label, axis=1).tolist()

selected_labels = st.multiselect("Selecione até 3 cargos para comparar:", options=pick_options, max_selections=3)

# ===========================================================
# RENDERIZAÇÃO FINAL
# ===========================================================
if selected_labels:
    st.markdown("---")
    st.markdown("### 🧾 Comparativo de Cargos Selecionados")

    rows = []
    for label in selected_labels:
        title = label.split("—")[-1].strip()
        match = career_df_sorted[career_df_sorted.apply(
            lambda r: title.lower() in str(safe_get(r, ["Job Profile", "Profile Name", "Role Title"])).lower(),
            axis=1
        )]
        rows.append(match.iloc[0] if not match.empty else None)

    n = len(rows)
    grid_class = f"ja-grid cols-{n}"

    html_cells = [f"<div>{header_badge(safe_get(r, ['Job Profile']), safe_get(r, ['Global Grade']))}</div>" if r is not None else "<div></div>" for r in rows]
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

    html_cells = [f"<div>{class_box(r)}</div>" if r is not None else "<div></div>" for r in rows]
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

    SECTIONS = [
        ("🧭", "Sub Job Family Description", ["sub_job_family_description"]),
        ("🧠", "Job Profile Description", ["job_profile_description", "job_description", "profile_description"]),
        ("🎯", "Role Description", ["role_description", "responsibilities", "key_responsibilities"]),
        ("🏅", "Grade Differentiator", ["grade_differentiator", "grade_differentiation", "level_differentiator"]),
        ("📊", "KPIs / Specific Parameters", ["kpis", "kpis_specific_parameters", "specific_parameters_kpis"]),
        ("🎓", "Qualifications", ["qualifications", "education", "required_qualifications"]),
    ]

    for emoji, title, keys in SECTIONS:
        html_cells = []
        for r in rows:
            if r is None:
                html_cells.append("<div></div>")
            else:
                value = safe_get(r, keys)
                html_cells.append("<div>" + cell_card(emoji, title, format_paragraphs(value)) + "</div>")
        st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)
else:
    st.info("👆 Selecione até 3 cargos para comparar.")
