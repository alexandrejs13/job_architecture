import re
import unicodedata
import pandas as pd
import streamlit as st
from utils.ui_components import section

# =========================
# Setup básico
# =========================
st.set_page_config(layout="wide")

# =========================
# CSS — idêntico ao seu layout
# =========================
st.markdown("""
<style>
.block-container { max-width:1200px !important; min-width:900px !important; margin:0 auto !important; padding:2.5rem 1.5rem 2rem 1.5rem; zoom:0.9; }
html, body, [class*="css"] { font-size: calc(13px + 0.18vw) !important; }
h1 { text-align:left !important; margin-top:0.8rem !important; margin-bottom:1.4rem !important; line-height:1.25 !important; font-size:1.9rem !important; }
.ja-p { margin:0 0 4px 0; text-align:left; line-height:1.48; }
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

# =========================
# Normalização e utilitários
# =========================
def norm(s: str) -> str:
    """Minúsculas, sem acento, só letras/números/underscore."""
    s = str(s or "").strip()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s)
    return s.lower().strip("_")

def split_paragraphs(text: str) -> str:
    if not text or str(text).strip() in ("nan", "-", ""):
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

def pick_col(columns_norm, *keyword_groups):
    """
    Retorna o nome normalizado da melhor coluna que contém TODAS as palavras de
    pelo menos um dos grupos de palavras-chave.
    Ex.: pick_col(cols, ["job","profile","description"], ["role","description"])
    """
    best = None
    best_len = 10**9
    for col in columns_norm:
        for group in keyword_groups:
            if all(k in col for k in group):
                # desempate: pega o mais curto (tende a ser o "certo")
                if len(col) < best_len:
                    best = col
                    best_len = len(col)
    return best  # coluna normalizada ou None

def get_val(row, col_map, key, default="-"):
    """Pega valor pela key lógica usando o mapa real (normalizado->real)."""
    col_norm = col_map.get(key)
    if not col_norm:
        return default
    real_col = col_map["_real"][col_norm]  # nome real da coluna no DF
    val = row.get(real_col, default)
    if pd.isna(val) or str(val).strip() == "":
        return default
    return str(val).strip()

def format_grade(g):
    try:
        f = float(str(g).replace(",", "."))
        if f.is_integer():
            return str(int(f))
        return str(f)
    except:
        return str(g)

# =========================
# Carregamento do Excel
# =========================
section("📘 Job Profile Description")

try:
    df = pd.read_excel("data/Job Profile.xlsx")
except Exception as e:
    st.error(f"❌ Erro ao carregar 'data/Job Profile.xlsx': {e}")
    st.stop()

# Mantemos um mapa nome-normalizado -> nome-real
cols_real = list(df.columns)
cols_norm = [norm(c) for c in cols_real]
norm_to_real = {n: r for n, r in zip(cols_norm, cols_real)}

# =========================
# Descoberta de colunas (fuzzy)
# =========================
col_job_family      = pick_col(cols_norm, ["job","family"])
col_sub_job_family  = pick_col(cols_norm, ["sub","job","family"], ["subfamily"], ["sub","family"])
col_career_path     = pick_col(cols_norm, ["career","path"], ["trilha","carreira"])
col_job_profile     = pick_col(cols_norm, ["job","profile"], ["profile","name"], ["role","title"])
col_grade           = pick_col(cols_norm, ["global","grade"], ["grade","global"], ["grade"])
col_function_code   = pick_col(cols_norm, ["function","code"])
col_discipline_code = pick_col(cols_norm, ["discipline","code"])
col_full_job_code   = pick_col(cols_norm, ["full","job","code"], ["job","code"])

col_sjfd = pick_col(cols_norm, ["sub","job","family","description"], ["subfamily","description"])
col_jpd  = pick_col(cols_norm, ["job","profile","description"], ["profile","description"], ["job","description"])
col_rd   = pick_col(cols_norm, ["role","description"], ["responsibilities"])
col_gd   = pick_col(cols_norm, ["grade","differenti"], ["level","differenti"])
col_kpi  = pick_col(cols_norm, ["kpi"], ["specific","parameters"], ["parameters","kpi"])
col_qual = pick_col(cols_norm, ["qualification"], ["education"])

required = {
    "job_family": col_job_family,
    "sub_job_family": col_sub_job_family,
    "career_path": col_career_path,
    "job_profile": col_job_profile,
    "grade": col_grade,
}
missing = [k for k, v in required.items() if not v]
if missing:
    st.error("❌ Não consegui identificar automaticamente estas colunas no Excel: " +
             ", ".join(missing) +
             ".\n\nConfirme se o cabeçalho contém palavras como 'Job Family', 'Sub Job Family', 'Career Path', 'Job Profile' e 'Global Grade'.")
    st.stop()

# Mapa lógico -> normalizado + mapa de normalizado -> real
col_map = {
    "job_family": col_job_family,
    "sub_job_family": col_sub_job_family,
    "career_path": col_career_path,
    "job_profile": col_job_profile,
    "grade": col_grade,
    "function_code": col_function_code,
    "discipline_code": col_discipline_code,
    "full_job_code": col_full_job_code,
    "sub_job_family_description": col_sjfd,
    "job_profile_description": col_jpd,
    "role_description": col_rd,
    "grade_differentiator": col_gd,
    "kpis": col_kpi,
    "qualifications": col_qual,
    "_real": norm_to_real,  # para resolver nome real
}

# =========================
# Filtros (Família / Subfamília / Trilha)
# =========================
def uniq(series):
    vals = sorted(set([str(v).strip() for v in series if str(v).strip() not in ("", "nan")]))
    return vals

families = uniq(df[norm_to_real[col_map["job_family"]]])
col1, col2, col3 = st.columns([1.2, 2.2, 1])

with col1:
    fam = st.selectbox("Família", families)

filtered = df[df[norm_to_real[col_map["job_family"]]].astype(str).str.strip() == fam]

subs = uniq(filtered[norm_to_real[col_map["sub_job_family"]]])
with col2:
    sub = st.selectbox("Subfamília", subs)

sub_df = filtered[filtered[norm_to_real[col_map["sub_job_family"]]].astype(str).str.strip() == sub]

careers = uniq(sub_df[norm_to_real[col_map["career_path"]]])
with col3:
    career = st.selectbox("Trilha de Carreira", careers)

career_df = sub_df[sub_df[norm_to_real[col_map["career_path"]]].astype(str).str.strip() == career]

# =========================
# Multiselect de perfis
# =========================
def option_label(row):
    g = get_val(row, col_map, "grade", "")
    p = get_val(row, col_map, "job_profile", "")
    g_fmt = format_grade(g)
    return f"GG{g_fmt} — {p}" if g_fmt not in ("", "nan", None) else p

grade_real = norm_to_real[col_map["grade"]]
career_df_sorted = career_df.sort_values(by=grade_real, ascending=False, kind="mergesort")
pick_options = [option_label(r) for _, r in career_df_sorted.iterrows()]

selected_labels = st.multiselect("Selecione até 3 cargos para comparar:", options=pick_options, max_selections=3)

# =========================
# Renderização
# =========================
def class_box(row):
    return f"""
    <div class="ja-class">
      <b>Família:</b> {get_val(row, col_map, "job_family")}<br>
      <b>Subfamília:</b> {get_val(row, col_map, "sub_job_family")}<br>
      <b>Carreira:</b> {get_val(row, col_map, "career_path")}<br>
      <b>Função:</b> {get_val(row, col_map, "function_code")}<br>
      <b>Disciplina:</b> {get_val(row, col_map, "discipline_code")}<br>
      <b>Código:</b> {get_val(row, col_map, "full_job_code")}
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

if selected_labels:
    st.markdown("---")
    st.markdown("### 🧾 Comparativo de Cargos Selecionados")

    # Encontra as linhas pelos títulos que o usuário escolheu
    rows = []
    jp_real = norm_to_real[col_map["job_profile"]]
    for label in selected_labels:
        title = label.split("—")[-1].strip()
        match = career_df_sorted[
            career_df_sorted[jp_real].astype(str).str.strip().str.lower() == title.lower()
        ]
        rows.append(match.iloc[0] if not match.empty else None)

    n = len(rows)
    grid_class = f"ja-grid cols-{n}"

    # Cabeçalho (título + grade)
    html_cells = []
    for r in rows:
        if r is None:
            html_cells.append("<div></div>")
        else:
            title = get_val(r, col_map, "job_profile", "-")
            grade = format_grade(get_val(r, col_map, "grade", "-"))
            html_cells.append(f"<div>{header_badge(title, grade)}</div>")
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

    # Classificação (família, códigos, etc.)
    html_cells = [f"<div>{class_box(r)}</div>" if r is not None else "<div></div>" for r in rows]
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

    # Secções de texto
    SECTIONS = [
        ("🧭", "Sub Job Family Description", "sub_job_family_description"),
        ("🧠", "Job Profile Description",   "job_profile_description"),
        ("🎯", "Role Description",          "role_description"),
        ("🏅", "Grade Differentiator",      "grade_differentiator"),
        ("📊", "KPIs / Specific Parameters","kpis"),
        ("🎓", "Qualifications",            "qualifications"),
    ]

    for emoji, title, key in SECTIONS:
        html_cells = []
        for r in rows:
            if r is None:
                html_cells.append("<div></div>")
            else:
                raw = get_val(r, col_map, key, "-")
                html_cells.append("<div>" + cell_card(emoji, title, split_paragraphs(raw)) + "</div>")
        st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)
else:
    st.info("👆 Selecione até 3 cargos para comparar.")
