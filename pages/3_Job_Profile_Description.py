import streamlit as st
import pandas as pd
import re
import html
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Profile Description",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. CSS GLOBAL E SIDEBAR
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

# ===========================================================
# 3. CABEÇALHO AZUL PADRÃO
# ===========================================================
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
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.page-header img {
    width: 48px;
    height: 48px;
}
.block-container {
    max-width: 950px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/business%20review%20clipboard.png" alt="icon">
    Job Profile Description
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. FUNÇÕES AUXILIARES
# ===========================================================
@st.cache_data
def load_job_profile_df():
    file_path = "data/Job Profile.xlsx"
    try:
        df = pd.read_excel(file_path)
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo '{file_path}'. Detalhe: {e}")
        return pd.DataFrame()

def safe_get(row, key, default="-"):
    val = row.get(key, default)
    return str(val).strip() if not pd.isna(val) and str(val).strip() not in ["", "nan", "None"] else default

def format_paragraphs(text):
    if not text or str(text).strip() in ["-", "nan", "None"]:
        return "-"
    parts = re.split(r"\n+|•|\r", str(text).strip())
    return "".join(f"<p style='margin:0 0 8px 0;'>• {html.escape(p.strip())}</p>" for p in parts if len(p.strip()) > 1)

# ===========================================================
# 5. CONTEÚDO PRINCIPAL
# ===========================================================
df = load_job_profile_df()

if not df.empty:
    col1, col2, col3 = st.columns([1.2, 1.5, 1])
    with col1:
        families = sorted(df["Job Family"].dropna().unique())
        fam = st.selectbox("📂 Família", families)
        filtered = df[df["Job Family"] == fam]

    with col2:
        subs = sorted(filtered["Sub Job Family"].dropna().unique())
        sub = st.selectbox("📁 Subfamília", subs)
        sub_df = filtered[filtered["Sub Job Family"] == sub]

    with col3:
        careers = sorted(sub_df["Career Path"].dropna().unique())
        career = st.selectbox("🛤️ Trilha", careers)
        career_df = sub_df[sub_df["Career Path"] == career]

    if "Job Profile" in career_df.columns:
        career_df["GG_Num"] = pd.to_numeric(career_df.get("Global Grade", 0), errors="coerce").fillna(0)
        career_df = career_df.sort_values("GG_Num", ascending=False)
        career_df["Label"] = career_df.apply(
            lambda x: f"GG{int(x['GG_Num'])} — {safe_get(x,'Job Profile')}" if x["GG_Num"] > 0 else safe_get(x, "Job Profile"),
            axis=1
        )

        selected = st.multiselect("📌 Selecione até 3 cargos:", career_df["Label"].unique(), max_selections=3)

        if selected:
            rows = [career_df[career_df["Label"] == s].iloc[0] for s in selected]
            st.markdown(f"<div style='display:grid;grid-template-columns:repeat({len(rows)},1fr);gap:25px;'>", unsafe_allow_html=True)

            for r in rows:
                gg = safe_get(r, "Global Grade").replace(".0", "")
                st.markdown(f"""
                <div style="background:white;border-left:5px solid #145efc;padding:20px;border-radius:10px;box-shadow:0 4px 8px rgba(0,0,0,0.05);">
                    <h4 style="color:#145efc;margin-bottom:8px;">{html.escape(safe_get(r, "Job Profile"))}</h4>
                    <p><b>Global Grade:</b> {gg}</p>
                    <p><b>Família:</b> {html.escape(safe_get(r, "Job Family"))}</p>
                    <p><b>Subfamília:</b> {html.escape(safe_get(r, "Sub Job Family"))}</p>
                    <p><b>Trilha:</b> {html.escape(safe_get(r, "Career Path"))}</p>
                    <hr>
                    <div><b>Descrição:</b><br>{format_paragraphs(safe_get(r, "Job Profile Description"))}</div>
                    <div style="margin-top:10px;"><b>Qualificações:</b><br>{format_paragraphs(safe_get(r, "Qualifications"))}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("👆 Selecione até 3 cargos para comparar.")
    else:
        st.warning("Coluna 'Job Profile' não encontrada na base.")
else:
    st.error("❌ Não foi possível carregar o arquivo 'Job Profile.xlsx'.")
