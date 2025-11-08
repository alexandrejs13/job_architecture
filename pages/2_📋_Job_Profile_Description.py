import re
import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section

# -----------------------------
# Utilidades
# -----------------------------
def safe_get(row, keys, default=""):
    """Retorna o primeiro campo válido na lista (ignora diferenças de caixa/espaço)."""
    for k in keys if isinstance(keys, list) else [keys]:
        for col in row.index:
            if col.strip().lower() == k.strip().lower():
                val = str(row[col]).strip()
                if val and val.lower() != "nan":
                    return val
    return default

def format_paragraphs(text):
    """Converte em parágrafos simples (sem bullets)."""
    if not text:
        return "-"
    parts = re.split(r"\n+|•|\r", text.strip())
    return "".join(
        f"<p class='ja-p'>{p.strip()}</p>"
        for p in parts if len(p.strip()) > 2
    )

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

# -----------------------------
# Página
# -----------------------------
data = load_data()
section("📋 Job Profile Description")

if "job_profile" not in data:
    st.error("Job Profile.csv não encontrado em /data")
    st.stop()

df = data["job_profile"]

# ---------- CSS ----------
st.markdown("""
<style>
/* Tipografia base */
.ja-p { margin: 0 0 6px 0; text-align: justify; }

/* Header do cargo (nome + grade) */
.ja-hd { display:flex; align-items:baseline; gap:10px; margin:0 0 6px 0; }
.ja-hd-title { font-size:1.05rem; font-weight:700; }
.ja-hd-grade { color:#1E56E0; font-weight:700; }

/* Caixa de classificação */
.ja-class {
  background:#fff; border:1px solid #e0e4f0; border-radius:8px;
  padding:10px; display:inline-block; width:100%;
}

/* Título da seção — ícone largura fixa para alinhar */
.ja-sec { margin-bottom: 14px; }
.ja-sec-h {
  display:flex; align-items:center; gap:8px;
  margin: 8px 0 6px 0;
}
.ja-ic { width:24px; display:inline-block; text-align:center; line-height:1; }
.ja-ttl { font-weight:700; color:#1E56E0; font-size:0.98rem; }

/* Cartão */
.ja-card {
  background:#f9f9f9; padding:12px 14px; border-radius:8px;
  border-left:4px solid #1E56E0; box-shadow:0 1px 3px rgba(0,0,0,0.05);
  width:100%; display:inline-block;
}

/* GRID por seção (alinha colunas obrigatoriamente) */
.ja-grid { display:grid; gap:16px; margin: 4px 0 18px 0; }
.ja-grid.cols-1 { grid-template-columns: repeat(1, 1fr); }
.ja-grid.cols-2 { grid-template-columns: repeat(2, 1fr); }
.ja-grid.cols-3 { grid-template-columns: repeat(3, 1fr); }

/* Multiselect próximo aos filtros */
.compare-box { margin-top:-18px; }
.compare-box .compare-label { margin:4px 0 6px 0; font-weight:600; color:#2b2d42; }

/* Tags do multiselect sem cortar texto */
div[data-baseweb="tag"] { max-width:none !important; }
div[data-baseweb="tag"] span {
  white-space: normal !important;
  word-break: break-word !important;
  line-height: 1.25 !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
}
div[data-baseweb="select"] > div { min-height:44px !important; height:auto !important; }
</style>
""", unsafe_allow_html=True)

# ---------- Filtros ----------
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

# ---------- Multiselect colado aos filtros ----------
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

# ---------- Coleta dos perfis selecionados ----------
if selected_labels:
    st.markdown("---")
    st.markdown("### 🧾 Comparativo de Cargos Selecionados")

    # Constrói lista de rows na mesma ordem da seleção
    rows = []
    for label in selected_labels:
        parts = re.split(r"\s*[–—-]\s*", label)
        label_grade = parts[0].replace("GG", "").strip() if parts else ""
        label_title = parts[1].strip() if len(parts) > 1 else label.strip()

        sel = career_df_sorted[
            career_df_sorted["Job Profile"].str.strip().str.lower() == label_title.lower()
        ]
        if label_grade:
            sel = sel[ sel["Global Grade"].astype(str).str.strip() == label_grade ]
        if sel.empty:
            rows.append(None)
        else:
            rows.append(sel.iloc[0])

    n = len(rows)
    grid_class = f"ja-grid cols-{n}"

    # ===== Linha 1: cabeçalho (título + grade)
    html_cells = []
    for r in rows:
        if r is None:
            html_cells.append("<div></div>")
        else:
            html_cells.append(f"<div>{header_badge(r['Job Profile'], r['Global Grade'])}</div>")
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

    # ===== Linha 2: classificação (família, códigos etc.)
    html_cells = []
    for r in rows:
        if r is None:
            html_cells.append("<div></div>")
        else:
            html_cells.append(f"<div>{class_box(r)}</div>")
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

    # ===== Demais linhas: seções alinhadas por grid =====
    SECTIONS = [
        ("🧭", "Sub Job Family Description", lambda r: safe_get(r, "Sub Job Family Description")),
        ("🧠", "Job Profile Description",   lambda r: safe_get(r, "Job Profile Description")),
        ("🎯", "Role Description",          lambda r: safe_get(r, "Role Description")),
        ("🏅", "Grade Differentiator",      lambda r: safe_get(r, [
                                               "Grade Differentiator",
                                               "Grade Differentiation",
                                               "Grade Differentiatior",  # como está no seu CSV
                                               " Grade Differentiator", "Grade Differentiator ",
                                               "Grade Differentiators"
                                             ])),
        ("📊", "KPIs / Specific Parameters", lambda r: safe_get(r, ["Specific parameters KPIs",
                                                                   "Specific parameters / KPIs"])),
        ("💡", "Competency 1",              lambda r: safe_get(r, "Competency 1")),
        ("💡", "Competency 2",              lambda r: safe_get(r, "Competency 2")),
        ("💡", "Competency 3",              lambda r: safe_get(r, "Competency 3")),
        ("🎓", "Qualifications",            lambda r: safe_get(r, "Qualifications")),
    ]

    for emoji, title, getter in SECTIONS:
        html_cells = []
        for r in rows:
            if r is None:
                html_cells.append("<div></div>")
            else:
                raw = getter(r)
                if raw:
                    html_cells.append(
                        "<div>" + cell_card(emoji, title, format_paragraphs(raw)) + "</div>"
                    )
                else:
                    html_cells.append("<div></div>")
        st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)
