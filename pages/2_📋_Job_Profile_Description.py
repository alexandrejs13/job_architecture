import re
import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section

# ----------------------------------
# Utilidades
# ----------------------------------
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
    """Quebra em parágrafos simples (sem bullets)."""
    if not text:
        return "-"
    parts = re.split(r"\n+|•|\r", text.strip())
    return "".join(
        f"<p class='ja-p'>{p.strip()}</p>"
        for p in parts if len(p.strip()) > 2
    )

def render_section(emoji, title, html_text):
    """Bloco padronizado (título + cartão) 100% alinhado."""
    st.markdown(
        f"""
        <div class="ja-sec">
          <div class="ja-sec-h">
            <span class="ja-ic">{emoji}</span>
            <span class="ja-ttl">{title}</span>
          </div>
          <div class="ja-card">{html_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------------------------------
# Página
# ----------------------------------
data = load_data()
section("📋 Job Profile Description")

if "job_profile" not in data:
    st.error("Job Profile.csv não encontrado em /data")
    st.stop()

df = data["job_profile"]

# ---------- CSS de alinhamento rígido ----------
st.markdown("""
<style>
/* Tipografia base */
.ja-p { margin: 0 0 6px 0; text-align: justify; }

/* Cabeçalho da seção: ícone largura fixa e texto alinhado */
.ja-sec { margin-bottom: 14px; }
.ja-sec-h {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 8px 0 6px 0;
}
.ja-ic {
  width: 24px; /* fixa o espaço do ícone para todos os títulos */
  display: inline-block;
  text-align: center;
  line-height: 1;
}
.ja-ttl {
  font-weight: 700;
  color: #1E56E0;
  font-size: 0.98rem;
}

/* Cartão padronizado para todas as seções */
.ja-card {
  background-color: #f9f9f9;
  padding: 12px 14px;
  border-radius: 8px;
  border-left: 4px solid #1E56E0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  width: 100%;
  display: inline-block;
}

/* Select/multiselect proximidade visual */
.compare-box { margin-top: -18px; }
.compare-box .compare-label { margin: 4px 0 6px 0; font-weight: 600; color: #2b2d42; }

/* Tags do multiselect não cortarem texto */
div[data-baseweb="tag"] { max-width: none !important; }
div[data-baseweb="tag"] span {
  white-space: normal !important;
  word-break: break-word !important;
  line-height: 1.25 !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
}
div[data-baseweb="select"] > div { min-height: 44px !important; height: auto !important; }

/* Caixa de classificação (topo do cargo) */
.ja-class {
  background:#fff; border:1px solid #e0e4f0; border-radius:8px;
  padding:10px; display:inline-block; width:100%;
}
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

# ---------- Render comparativo ----------
if selected_labels:
    st.markdown("---")
    st.markdown("### 🧾 Comparativo de Cargos Selecionados")

    cols = st.columns(len(selected_labels))
    for idx, label in enumerate(selected_labels):
        with cols[idx]:
            parts = re.split(r"\s*[–—-]\s*", label)
            label_grade = parts[0].replace("GG", "").strip() if parts else ""
            label_title = parts[1].strip() if len(parts) > 1 else label.strip()

            sel = career_df_sorted[
                career_df_sorted["Job Profile"].str.strip().str.lower() == label_title.lower()
            ]
            if label_grade:
                sel = sel[ sel["Global Grade"].astype(str).str.strip() == label_grade ]
            if sel.empty:
                st.warning(f"Cargo não encontrado: {label}")
                continue

            row = sel.iloc[0]

            # Cabeçalho do cargo
            st.markdown(f"#### {row['Job Profile']}")
            st.markdown(f"<p style='color:#1E56E0; font-weight:bold;'>GG {row['Global Grade']}</p>", unsafe_allow_html=True)

            # Classificação do cargo (sempre igual)
            st.markdown(
                f"""
                <div class="ja-class">
                    <b>Família:</b> {row['Job Family']}<br>
                    <b>Subfamília:</b> {row['Sub Job Family']}<br>
                    <b>Carreira:</b> {row['Career Path']}<br>
                    <b>Função:</b> {row['Function Code']}<br>
                    <b>Disciplina:</b> {row['Discipline Code']}<br>
                    <b>Código:</b> {row['Full Job Code']}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Seções padronizadas (com detecção robusta do Grade Differentiator)
            sections = [
                ("🧭", "Sub Job Family Description", safe_get(row, "Sub Job Family Description")),
                ("🧠", "Job Profile Description",   safe_get(row, "Job Profile Description")),
                ("🎯", "Role Description",          safe_get(row, "Role Description")),
                ("🏅", "Grade Differentiator",      safe_get(row, [
                                                      "Grade Differentiator",
                                                      "Grade Differentiation",
                                                      "Grade Differentiatior",   # sua coluna
                                                      " Grade Differentiator",
                                                      "Grade Differentiator ",
                                                      "Grade Differentiators"
                                                    ])),
                ("📊", "KPIs / Specific Parameters", safe_get(row, ["Specific parameters KPIs", "Specific parameters / KPIs"])),
                ("💡", "Competency 1",               safe_get(row, "Competency 1")),
                ("💡", "Competency 2",               safe_get(row, "Competency 2")),
                ("💡", "Competency 3",               safe_get(row, "Competency 3")),
                ("🎓", "Qualifications",              safe_get(row, "Qualifications")),
            ]

            for emoji, title, raw in sections:
                if raw:
                    render_section(emoji, title, format_paragraphs(raw))
