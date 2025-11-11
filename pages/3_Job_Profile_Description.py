import streamlit as st
import pandas as pd
import re
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO GERAL
# ===========================================================
st.set_page_config(
    page_title="Job Profile Description",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. CSS GLOBAL E HEADER
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

st.markdown("""
<style>
.page-header {
    background-color: #145efc;
    color: white;
    font-weight: 750;
    font-size: 1.35rem;
    border-radius: 12px;
    padding: 22px 36px;
    display: flex;
    align-items: center;
    gap: 18px;
    width: 100%;
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.page-header img { width: 48px; height: 48px; }

[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro","Helvetica",sans-serif;
}

.block-container {
    max-width: 1300px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}

/* ===== CORREÇÃO DE ESPAÇAMENTO ENTRE CARDS ===== */
[data-testid="stHorizontalBlock"] > div {
    gap: 30px !important;
}
.profile-card {
    background: #fff;
    border-radius: 12px;
    border-left: 5px solid #145efc;
    padding: 20px 26px;
    flex: 1;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 8px rgba(0,0,0,0.06);
    min-height: 170px;
    margin-bottom: 30px !important;
}

/* ===== TÍTULOS E METADADOS ===== */
.profile-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #000;
    margin-bottom: 6px;
}
.profile-meta {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 12px;
    line-height: 1.4;
}

/* ===== SEÇÕES ===== */
.section-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 25px;
    align-items: stretch;
    margin-top: 15px;
}
.section-box {
    background: #fff;
    border-left: 4px solid #145efc;
    border-radius: 8px;
    padding: 18px 22px;
    box-shadow: 0 3px 6px rgba(0,0,0,0.05);
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    height: 100%;
}
.section-title {
    font-weight: 700;
    color: #145efc;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}
.section-content {
    color: #333;
    line-height: 1.55;
    font-size: 0.95rem;
    white-space: pre-wrap;
    flex-grow: 1;
}
</style>

<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/business%20review%20clipboard.png" alt="icon">
  Job Profile Description
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 3. FUNÇÕES AUXILIARES
# ===========================================================
def normalize_grade(val):
    s = str(val).strip()
    if s.lower() in ("nan", "none", "", "na"):
        return ""
    return re.sub(r"\.0$", "", s)

@st.cache_data
def load_excel(path):
    try:
        df = pd.read_excel(path)
        for c in df.select_dtypes(include="object"):
            df[c] = df[c].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar {path}: {e}")
        return pd.DataFrame()

# ===========================================================
# 4. DADOS
# ===========================================================
df = load_excel("data/Job Profile.xlsx")
levels = load_excel("data/Level Structure.xlsx")

if df.empty:
    st.error("❌ Arquivo 'Job Profile.xlsx' não encontrado ou inválido.")
    st.stop()

df["Global Grade"] = df["Global Grade"].apply(normalize_grade)
if not levels.empty and "Global Grade" in levels.columns:
    levels["Global Grade"] = levels["Global Grade"].apply(normalize_grade)

# ===========================================================
# 5. FILTROS
# ===========================================================
familias = sorted(df["Job Family"].dropna().unique())

col1, col2, col3 = st.columns(3)
with col1:
    familia = st.selectbox("Família (Job Family):", ["Selecione..."] + familias, index=0)
with col2:
    subs = sorted(df[df["Job Family"] == familia]["Sub Job Family"].dropna().unique()) if familia != "Selecione..." else []
    sub = st.selectbox("Sub-Família:", ["Selecione..."] + subs, index=0)
with col3:
    paths = sorted(df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique()) if sub != "Selecione..." else []
    trilha = st.selectbox("Trilha (Career Path):", ["Selecione..."] + paths, index=0)

filtered = df.copy()
if familia != "Selecione...":
    filtered = filtered[filtered["Job Family"] == familia]
if sub != "Selecione...":
    filtered = filtered[filtered["Sub Job Family"] == sub]
if trilha != "Selecione...":
    filtered = filtered[filtered["Career Path"] == trilha]

if filtered.empty:
    st.info("Ajuste os filtros para visualizar os perfis.")
    st.stop()

# ===========================================================
# 6. PICKLIST (GG + CARGO)
# ===========================================================
filtered["GG"] = filtered["Global Grade"].apply(normalize_grade)
filtered["label"] = filtered.apply(
    lambda r: f'GG {r["GG"] or "-"} • {r["Job Profile"]}', axis=1
)
label_to_profile = dict(zip(filtered["label"], filtered["Job Profile"]))

selecionados_labels = st.multiselect(
    "Selecione até 3 perfis para comparar:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)

if not selecionados_labels:
    st.info("Selecione ao menos 1 perfil para exibir.")
    st.stop()

selecionados = [label_to_profile[l] for l in selecionados_labels]

# ===========================================================
# 7. GRID DE COMPARAÇÃO
# ===========================================================
cols = st.columns(len(selecionados))

for idx, nome in enumerate(selecionados):
    row = filtered[filtered["Job Profile"] == nome]
    if row.empty:
        continue

    data = row.iloc[0].copy()
    gg = normalize_grade(data.get("Global Grade", ""))
    level_name = ""
    if not levels.empty and {"Global Grade", "Level Name"}.issubset(levels.columns):
        match = levels[levels["Global Grade"].astype(str).str.strip() == gg]
        if not match.empty:
            level_name = match["Level Name"].iloc[0]

    meta = []
    for lbl, col in [("Família", "Job Family"), ("Subfamília", "Sub Job Family"), ("Carreira", "Career Path")]:
        val = str(data.get(col, "") or "").strip()
        if val:
            meta.append(f"<b>{lbl}:</b> {val}")
    meta_html = "<br>".join(meta)

    with cols[idx]:
        st.markdown(f"""
        <div class="profile-card">
            <div class="profile-title">{data.get('Job Profile', '-')}</div>
            <div class="profile-meta">GG {gg or '-'} • {level_name}</div>
            {f'<div class="profile-meta">{meta_html}</div>' if meta_html else ''}
        </div>
        """, unsafe_allow_html=True)

        # Seções
        sections = [
            ("🧭 Sub Job Family Description", "Sub Job Family Description"),
            ("🧠 Job Profile Description", "Job Profile Description"),
            ("🏛️ Career Band Description", "Career Band Description"),
            ("🎯 Role Description", "Role Description"),
            ("🏅 Grade Differentiator", "Grade Differentiator"),
            ("🎓 Qualifications", "Qualifications"),
        ]

        st.markdown('<div class="section-grid">', unsafe_allow_html=True)
        for title, field in sections:
            content = str(data.get(field, "") or "").strip()
            if not content:
                continue
            st.markdown(f"""
            <div class="section-box">
                <div class="section-title">{title}</div>
                <div class="section-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
