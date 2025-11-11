import streamlit as st
import pandas as pd
import re
import html
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO INICIAL
# ===========================================================
st.set_page_config(page_title="Job Profile Description", page_icon="📋", layout="wide")
sidebar_logo_and_title()

# ===========================================================
# 2. CSS GLOBAL + ESTILO PADRÃO
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Cabeçalho azul igual às outras páginas
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
    box-sizing: border-box;
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.page-header img {
    width: 48px;
    height: 48px;
}
.block-container {
    max-width: 95% !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}

/* --- ESTILOS DO GRID DE COMPARAÇÃO --- */
.comparison-grid { display: grid; gap: 25px; margin-top: 20px; }
.grid-cell { background: #fff; border: 1px solid #e0e0e0; padding: 20px; display: flex; flex-direction: column; }
.header-cell { background: #f8f9fa; border-radius: 12px 12px 0 0; border-bottom: none; min-height: 100px; justify-content: center; }
.jp-title { font-size: 1.35rem; font-weight: 800; color: #2c3e50; line-height: 1.2; margin-bottom: 8px; }
.jp-gg { color: #145efc; font-weight: 700; font-size: 1rem; }
.meta-cell { background: #fff; border-top: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0; font-size: 0.9rem; color: #555; gap: 8px; padding: 15px 20px; }
.meta-row { display: flex; flex-wrap: wrap; gap: 15px; }
.meta-item strong { color: #333; font-weight: 700; }
.section-cell { border-left-width: 5px; border-left-style: solid; border-top: none; background: #fdfdfd; padding: 15px 20px; }
.section-title { font-weight: 700; font-size: 1rem; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
.section-content { color: #333; line-height: 1.6; font-size: 0.95rem; }
.jp-p { margin: 0 0 8px 0; }
.footer-cell { height: 15px; border-top: none; border-radius: 0 0 12px 12px; background: #fff; }
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/business%20review%20clipboard.png" alt="icon">
    Job Profile Description
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 3. FUNÇÕES AUXILIARES E CARREGAMENTO DE DADOS
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
        st.error(f"Erro Crítico: Não foi possível carregar o arquivo {file_path}. Detalhe: {e}")
        return pd.DataFrame()

def safe_get(row, key, default="-"):
    val = row.get(key, default)
    return str(val).strip() if not pd.isna(val) and str(val).strip() not in ["", "nan", "None"] else default

def format_paragraphs(text):
    if not text or str(text).strip() in ["-", "nan", "None"]:
        return "-"
    parts = re.split(r"\n+|•|\r", str(text).strip())
    return "".join(f"<p class='jp-p'>• {html.escape(p.strip())}</p>" for p in parts if len(p.strip()) > 1)

# ===========================================================
# 4. LÓGICA PRINCIPAL
# ===========================================================
df = load_job_profile_df()

if df is not None and not df.empty:
    st.markdown("### Selecione os parâmetros abaixo para comparar os perfis de cargo:")

    c1, c2, c3 = st.columns([1.2, 1.5, 1])
    fam_options = sorted(df["Job Family"].astype(str).unique()) if "Job Family" in df.columns else []

    with c1:
        fam = st.selectbox("📂 Família", fam_options)
        filtered = df[df["Job Family"] == fam]

    with c2:
        sub_options = sorted(filtered["Sub Job Family"].astype(str).unique()) if "Sub Job Family" in filtered.columns else []
        sub = st.selectbox("📂 Subfamília", sub_options)
        sub_df = filtered[filtered["Sub Job Family"] == sub]

    with c3:
        career_options = sorted(sub_df["Career Path"].astype(str).unique()) if "Career Path" in sub_df.columns else []
        career = st.selectbox("🛤️ Trilha", career_options)
        career_df = sub_df[sub_df["Career Path"] == career]

    if "Global Grade" in career_df.columns and "Job Profile" in career_df.columns:
        career_df["GG_Num"] = pd.to_numeric(career_df["Global Grade"], errors='coerce').fillna(0)
        career_df = career_df.sort_values(by="GG_Num", ascending=False)
        career_df["Label"] = career_df.apply(lambda x: f"GG{int(x['GG_Num'])} — {safe_get(x, 'Job Profile')}" if x['GG_Num'] > 0 else safe_get(x, 'Job Profile'), axis=1)

        selected_labels = st.multiselect("📌 Selecione até 3 cargos:", career_df["Label"].unique(), max_selections=3)

        if selected_labels:
            rows = [career_df[career_df["Label"] == label].iloc[0] for label in selected_labels]
            grid_html = f'<div class="comparison-grid" style="grid-template-columns: repeat({len(rows)}, 1fr);">'

            # Cabeçalho
            for r in rows:
                gg = safe_get(r, 'Global Grade').replace('.0', '')
                grid_html += f'<div class="grid-cell header-cell"><div class="jp-title">{html.escape(safe_get(r,"Job Profile"))}</div><div class="jp-gg">Global Grade {gg}</div></div>'

            # Metadados
            for r in rows:
                grid_html += f'''<div class="grid-cell meta-cell">
                    <div class="meta-row"><div class="meta-item"><strong>Família:</strong> {html.escape(safe_get(r,'Job Family'))}</div><div class="meta-item"><strong>Subfamília:</strong> {html.escape(safe_get(r,'Sub Job Family'))}</div></div>
                    <div class="meta-row"><div class="meta-item"><strong>Carreira:</strong> {html.escape(safe_get(r,'Career Path'))}</div><div class="meta-item"><strong>Cód:</strong> {html.escape(safe_get(r,'Full Job Code'))}</div></div>
                    <div class="meta-row"><div class="meta-item"><strong>Função:</strong> {html.escape(safe_get(r,'Function Code'))}</div><div class="meta-item"><strong>Disciplina:</strong> {html.escape(safe_get(r,'Discipline Code'))}</div></div>
                </div>'''

            # Seções
            sections_map = [
                ("🧭", "Sub Job Family Description", "#95a5a6"),
                ("🧠", "Job Profile Description", "#e91e63"),
                ("🏛️", "Career Band Description", "#673ab7"),
                ("🎯", "Role Description", "#1E56E0"),
                ("🏅", "Grade Differentiator", "#ff9800"),
                ("🎓", "Qualifications", "#009688")
            ]
            for emoji, col, color in sections_map:
                for r in rows:
                    grid_html += f'<div class="grid-cell section-cell" style="border-left-color:{color};"><div class="section-title" style="color:{color};"><span>{emoji}</span> {col}</div><div class="section-content">{format_paragraphs(safe_get(r, col))}</div></div>'

            # Rodapé
            for _ in rows:
                grid_html += '<div class="grid-cell footer-cell"></div>'

            st.markdown(grid_html + '</div>', unsafe_allow_html=True)
        else:
            st.info("👆 Selecione cargos acima para visualizar.")
    else:
        st.warning("As colunas 'Global Grade' ou 'Job Profile' não foram encontradas na base de dados. Verifique a planilha.")
else:
    st.error("Não foi possível carregar os dados. Verifique o caminho e o nome do arquivo 'data/Job Profile.xlsx'.")
