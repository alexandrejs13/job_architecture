import re
import pandas as pd
import streamlit as st
from utils.data_loader import load_excel_tables

# =========================
# Layout base idêntico
# =========================
st.set_page_config(layout="wide")
st.markdown("""
<style>
.block-container { max-width: 1200px !important; min-width: 900px !important; margin: 0 auto !important; padding: 2.5rem 1.5rem 2rem 1.5rem; zoom: 0.9; }
html, body, [class*="css"] { font-size: calc(13px + 0.18vw) !important; }
h1 { text-align:left !important; margin-top:.8rem !important; margin-bottom:1.4rem !important; line-height:1.25 !important; font-size:1.9rem !important; }
.ja-p { margin:0 0 4px 0; text-align:left; line-height:1.48; }
.ja-hd { display:flex; flex-direction:column; align-items:flex-start; gap:4px; margin:0 0 6px 0; text-align:left; }
.ja-hd-title { font-size:1.15rem; font-weight:700; }
.ja-hd-grade { color:#1E56E0; font-weight:700; font-size:1rem; }
.ja-class { background:#fff; border:1px solid #e0e4f0; border-radius:6px; padding:8px 12px; min-height:130px; }
.ja-sec { margin:0 !important; text-align:left; }
.ja-sec-h { display:flex; align-items:center; gap:6px; margin:0 0 3px 0 !important; }
.ja-ic { width:18px; text-align:center; }
.ja-ttl { font-weight:700; color:#1E56E0; font-size:.95rem; }
.ja-card { background:#f9f9f9; padding:10px 14px; border-radius:6px; border-left:3px solid #1E56E0; min-height:120px; box-sizing:border-box; }
.ja-grid { display:grid; gap:14px 14px; margin:6px 0 12px 0 !important; }
.ja-grid.cols-1 { grid-template-columns: repeat(1, 1fr); }
.ja-grid.cols-2 { grid-template-columns: repeat(2, 1fr); }
.ja-grid.cols-3 { grid-template-columns: repeat(3, 1fr); }
</style>
""", unsafe_allow_html=True)

st.markdown("## 📘 Job Profile Description")

# =========================
# Helpers
# =========================
def fmt(text):
    if not pd.notna(text) or str(text).strip() == "":
        return "-"
    parts = re.split(r"\n+|•|\r", str(text).strip())
    return "".join(f"<p class='ja-p'>{p.strip()}</p>" for p in parts if len(p.strip()) > 2)

def header_badge(title, grade):
    g = "-" if not pd.notna(grade) else str(grade)
    return f"""
    <div class="ja-hd">
      <div class="ja-hd-title">{title}</div>
      <div class="ja-hd-grade">GG {g}</div>
    </div>
    """

def class_box(row):
    fam = row.get("Job Family", "-")
    sub = row.get("Sub Job Family", "-")
    car = row.get("Career Path", "-")
    fun = row.get("Function Code", "-")
    dis = row.get("Discipline Code", "-")
    code = row.get("Full Job Code", "-")
    return f"""
    <div class="ja-class">
      <b>Família:</b> {fam}<br>
      <b>Subfamília:</b> {sub}<br>
      <b>Carreira:</b> {car}<br>
      <b>Função:</b> {fun}<br>
      <b>Disciplina:</b> {dis}<br>
      <b>Código:</b> {code}
    </div>
    """

def cell(emoji, title, value):
    return f"""
    <div class="ja-sec">
      <div class="ja-sec-h"><span class="ja-ic">{emoji}</span><span class="ja-ttl">{title}</span></div>
      <div class="ja-card">{fmt(value)}</div>
    </div>
    """

# =========================
# Dados
# =========================
DATA = load_excel_tables()
if "job_profile" not in DATA:
    st.error("❌ Não encontrei `data/Job Profile.xlsx`.")
    st.stop()

df = DATA["job_profile"]

required_min = ["Job Family", "Sub Job Family", "Career Path", "Job Profile"]
missing = [c for c in required_min if c not in df.columns]
if missing:
    st.error("⚠️ Faltam colunas essenciais no Excel: " + ", ".join(missing))
    st.stop()

# =========================
# Filtros
# =========================
c1, c2, c3 = st.columns([1.2, 2.2, 1])
with c1:
    fam = st.selectbox("Família", sorted(df["Job Family"].dropna().unique()))
subdf1 = df[df["Job Family"] == fam]

with c2:
    subs = sorted(subdf1["Sub Job Family"].dropna().unique())
    sub = st.selectbox("Subfamília", subs)
subdf2 = subdf1[subdf1["Sub Job Family"] == sub]

with c3:
    careers = sorted(subdf2["Career Path"].dropna().unique())
    car = st.selectbox("Trilha de Carreira", careers)
pool = subdf2[subdf2["Career Path"] == car].copy()

# =========================
# Multiselect
# =========================
def opt_label(r):
    g = r.get("Global Grade", "")
    p = r.get("Job Profile", "")
    try:
        g_int = int(str(g))
        return f"GG{g_int} — {p}"
    except:
        return str(p)

pool = pool.sort_values(by="Global Grade", ascending=False) if "Global Grade" in pool.columns else pool
options = [opt_label(r) for _, r in pool.iterrows()]
picked = st.multiselect("Selecione até 3 cargos para comparar:", options, max_selections=3)

if not picked:
    st.info("👆 Selecione até 3 cargos para comparar.")
    st.stop()

# Match pelas labels
rows = []
for lb in picked:
    title = lb.split("—", 1)[-1].strip()
    sel = pool[pool["Job Profile"].astype(str).str.strip().str.lower() == title.lower()]
    rows.append(sel.iloc[0] if not sel.empty else None)

n = len(rows)
grid = f"ja-grid cols-{n}"

# Cabeçalho
st.markdown(
    "<div class='%s'>%s</div>" % (
        grid,
        "".join([
            f"<div>{header_badge(r.get('Job Profile','-'), r.get('Global Grade','-'))}</div>" if r is not None else "<div></div>"
            for r in rows
        ])
    ),
    unsafe_allow_html=True
)

# Classe
st.markdown(
    "<div class='%s'>%s</div>" % (
        grid,
        "".join([f"<div>{class_box(r)}</div>" if r is not None else "<div></div>" for r in rows])
    ),
    unsafe_allow_html=True
)

# Seções (SEM KPIs, conforme você pediu)
def getcol(r, name):
    return r.get(name, "-") if r is not None else "-"

sections = [
    ("🧭", "Sub Job Family Description", "Sub Job Family Description"),
    ("🧠", "Job Profile Description",    "Job Profile Description"),
    ("🎯", "Role Description",           "Role Description"),
    ("🏅", "Grade Differentiator",       "Grade Differentiator"),
    ("🎓", "Qualifications",             "Qualifications"),
]

for emoji, title, colname in sections:
    st.markdown(
        "<div class='%s'>%s</div>" % (
            grid,
            "".join([
                f"<div>{cell(emoji, title, getcol(r, colname))}</div>" for r in rows
            ])
        ),
        unsafe_allow_html=True
    )
