import streamlit as st
import pandas as pd
import re
import unicodedata
from difflib import get_close_matches
from utils.data_loader import load_job_profile_df

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="📋 Job Profile Description")

# ===========================================================
# CSS — Mantém o layout original bonito e limpo
# ===========================================================
st.markdown("""
<style>
.block-container {
  max-width: 1200px !important;
  min-width: 900px !important;
  margin: 0 auto !important;
  padding: 2.5rem 1.5rem;
  zoom: 0.9;
}
h1 {
  margin-bottom: 1.4rem !important;
  font-size: 1.9rem !important;
  color: #1E56E0;
}
.ja-card {
  background: #f9f9f9;
  padding: 10px 14px;
  border-radius: 6px;
  border-left: 3px solid #1E56E0;
  min-height: 120px;
}
.ja-ttl {
  font-weight: 700;
  color: #1E56E0;
  font-size: 0.95rem;
}
.ja-grid {
  display: grid;
  gap: 14px;
  margin: 6px 0 12px 0 !important;
}
.ja-grid.cols-1 { grid-template-columns: repeat(1, 1fr); }
.ja-grid.cols-2 { grid-template-columns: repeat(2, 1fr); }
.ja-grid.cols-3 { grid-template-columns: repeat(3, 1fr); }
</style>
""", unsafe_allow_html=True)

st.markdown("## 📘 Job Profile Description")

# ===========================================================
# LIMPEZA AVANÇADA DE COLUNAS (Unicode-safe)
# ===========================================================
def normalize_columns(df):
    cleaned = {}
    for c in df.columns:
        base = unicodedata.normalize("NFKD", str(c))
        clean = (
            base.replace("\n", " ")
            .replace("\r", "")
            .replace("\t", "")
            .replace("\xa0", " ")  # espaço não quebrável
            .replace("\u200b", "") # zero width space
            .replace("–", "-")
            .replace("—", "-")
            .strip()
        )
        cleaned[c] = re.sub(r"\s+", " ", clean)
    df.rename(columns=cleaned, inplace=True)
    df.columns = [c.strip() for c in df.columns]
    return df

# ===========================================================
# LEITURA DO ARQUIVO
# ===========================================================
df = load_job_profile_df()
df = normalize_columns(df)

st.caption("✅ Colunas detectadas (após limpeza Unicode):")
for col in df.columns:
    st.text(f"→ [{col}] (len={len(col)})")

# ===========================================================
# MAPEAMENTO INTELIGENTE
# ===========================================================
expected = [
    "Job Profile", "Job Family", "Sub Job Family", "Career Path",
    "Function Code", "Discipline Code", "Global Grade", "Full Job Code",
    "Sub Job Family Description", "Job Profile Description",
    "Career Band Description", "Role Description",
    "Grade Differentiator", "Qualifications"
]

column_map = {}
for exp in expected:
    if exp in df.columns:
        column_map[exp] = exp
    else:
        close = get_close_matches(exp, df.columns, n=1, cutoff=0.7)
        column_map[exp] = close[0] if close else None
        if close:
            st.caption(f"⚙️ Coluna '{exp}' mapeada automaticamente para '{close[0]}'")

missing = [k for k, v in column_map.items() if v is None]
if missing:
    st.error(f"⚠️ As seguintes colunas não foram encontradas nem por aproximação: {', '.join(missing)}")
    st.stop()

df = df.rename(columns={v: k for k, v in column_map.items() if v})

# ===========================================================
# FILTROS
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
# MULTISELECT
# ===========================================================
def option_label(row: pd.Series) -> str:
    g = str(row.get("Global Grade", "")).strip()
    p = str(row.get("Job Profile", "")).strip()
    if g.replace('.', '').isdigit():
        g = str(int(float(g)))
    return f"GG {g} — {p}" if g else p

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
# FUNÇÕES DE DISPLAY
# ===========================================================
def safe_get(row, col):
    val = row.get(col) if row is not None and col in row else ""
    return "-" if pd.isna(val) or str(val).strip() == "" else str(val).strip()

def format_paragraphs(text):
    if not text or text == "-":
        return "-"
    parts = re.split(r"\n+|•|\r", text.strip())
    return "".join(f"<p>{p.strip()}</p>" for p in parts if len(p.strip()) > 1)

# ===========================================================
# RENDERIZAÇÃO FINAL
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

    SECTIONS = [
        ("🧭 Sub Job Family Description", "Sub Job Family Description"),
        ("🧠 Job Profile Description", "Job Profile Description"),
        ("🎓 Career Band Description", "Career Band Description"),
        ("🎯 Role Description", "Role Description"),
        ("🏅 Grade Differentiator", "Grade Differentiator"),
        ("📘 Qualifications", "Qualifications"),
    ]

    for emoji, col in SECTIONS:
        html_cells = [
            f"<div class='ja-card'><b>{emoji}</b><br>{format_paragraphs(safe_get(r, col))}</div>"
            for r in rows
        ]
        st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)
