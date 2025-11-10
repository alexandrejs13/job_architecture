import streamlit as st
import pandas as pd
import re
import html
from utils.ui import setup_sidebar, section

# ==============================================================================
# 1. CONFIGURAÇÃO INICIAL
# ==============================================================================
st.set_page_config(page_title="Job Profile Description", page_icon="📋", layout="wide")
setup_sidebar()

# ==============================================================================
# 2. CSS ESPECÍFICO DA PÁGINA
# ==============================================================================
st.markdown("""
<style>
:root {
  --blue: #145efc;
  --gray-line: #e0e0e0;
  --gray-bg: #f8f9fa;
  --dark-gray: #2c3e50;
}
.block-container { max-width: 95% !important; }
.comparison-grid { display: grid; gap: 25px; margin-top: 20px; }
.grid-cell { background: #fff; border: 1px solid var(--gray-line); padding: 20px; display: flex; flex-direction: column; }
.header-cell { background: var(--gray-bg); border-radius: 12px 12px 0 0; border-bottom: none; min-height: 100px; justify-content: center; }
.jp-title { font-size: 22px; font-weight: 800; color: var(--dark-gray); line-height: 1.2; margin-bottom: 8px; }
.jp-gg { color: var(--blue); font-weight: 700; font-size: 1.1rem; }
.meta-cell { background: #fff; border-top: 1px solid var(--gray-line); border-bottom: 1px solid var(--gray-line); font-size: 0.9rem; color: #555; gap: 8px; padding: 15px 20px; }
.meta-row { display: flex; flex-wrap: wrap; gap: 15px; }
.meta-item strong { color: #333; font-weight: 700; }
.section-cell { border-left-width: 5px; border-left-style: solid; border-top: none; background: #fdfdfd; padding: 15px 20px; }
.section-title { font-weight: 700; font-size: 1rem; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
.section-content { color: #333; line-height: 1.6; font-size: 0.95rem; }
.jp-p { margin: 0 0 8px 0; }
.footer-cell { height: 15px; border-top: none; border-radius: 0 0 12px 12px; background: #fff; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. FUNÇÃO DE CARREGAMENTO DE DADOS
# ==============================================================================
@st.cache_data
def load_job_profile_df():
    # -----------------------------------------------------------
    # 👇 TENTE CARREGAR SEU ARQUIVO AQUI
    # Se o seu arquivo se chama "Base_Cargos.xlsx", mude abaixo:
    # -----------------------------------------------------------
    file_name = "data.xlsx" 
    
    try:
        return pd.read_excel(file_name)
    except Exception:
        # Se der erro ou não achar o arquivo, usa estes dados de teste para não quebrar o app
        return pd.DataFrame({
            "Job Family": ["Tech", "Finance"],
            "Sub Job Family": ["Software Engineering", "Accounting"],
            "Career Path": ["Professional", "Professional"],
            "Global Grade": ["10", "11"],
            "Job Profile": ["Developer Example", "Accountant Example"],
            "Full Job Code": ["T-SE-P3", "F-AC-P3"],
            "Function Code": ["TEC", "FIN"],
            "Discipline Code": ["SWE", "ACC"],
            "Sub Job Family Description": ["Desc Família Tech...", "Desc Família Finança..."],
            "Job Profile Description": ["Faz código...", "Faz contas..."],
            "Career Band Description": ["Nível Pleno...", "Nível Sênior..."],
            "Role Description": ["- Codar\n- Testar", "- Balanços\n- Auditoria"],
            "Grade Differentiator": ["Escopo médio...", "Escopo grande..."],
            "Qualifications": ["Superior completo", "Pós-graduação"]
        })

def safe_get(row, key, default="-"):
    val = row.get(key, default)
    return str(val).strip() if not pd.isna(val) and str(val).strip() != "" else default

def format_paragraphs(text):
    if not text or str(text).strip() in ["-", "nan", "None"]: return "-"
    parts = re.split(r"\n+|•|\r", str(text).strip())
    return "".join(f"<p class='jp-p'>• {html.escape(p.strip())}</p>" for p in parts if len(p.strip()) > 1)

# ==============================================================================
# 4. LÓGICA DA PÁGINA
# ==============================================================================
df = load_job_profile_df()
section("📋 Job Profile Description")

if df is not None and not df.empty:
    # --- FILTROS ---
    c1, c2, c3 = st.columns([1.2, 1.5, 1])
    with c1:
        fam_options = sorted(df["Job Family"].astype(str).unique())
        fam = st.selectbox("📂 Família", fam_options)
        filtered = df[df["Job Family"] == fam]
    with c2:
        sub_options = sorted(filtered["Sub Job Family"].astype(str).unique())
        sub = st.selectbox("📂 Subfamília", sub_options)
        sub_df = filtered[filtered["Sub Job Family"] == sub]
    with c3:
        career_options = sorted(sub_df["Career Path"].astype(str).unique())
        career = st.selectbox("🛤️ Trilha", career_options)
        career_df = sub_df[sub_df["Career Path"] == career]

    # --- SELEÇÃO ---
    career_df["GG_Num"] = pd.to_numeric(career_df["Global Grade"], errors='coerce').fillna(0)
    career_df = career_df.sort_values(by="GG_Num", ascending=False)
    career_df["Label"] = career_df.apply(lambda x: f"GG{int(x['GG_Num'])} — {x['Job Profile']}" if x['GG_Num']>0 else x['Job Profile'], axis=1)

    selected_labels = st.multiselect("📌 Selecione até 3 cargos:", career_df["Label"].unique(), max_selections=3)

    if selected_labels:
        rows = [career_df[career_df["Label"] == label].iloc[0] for label in selected_labels]
        grid_html = f'<div class="comparison-grid" style="grid-template-columns: repeat({len(rows)}, 1fr);">'

        # HEADER
        for r in rows:
            gg = safe_get(r, 'Global Grade').replace('.0', '')
            grid_html += f'<div class="grid-cell header-cell"><div class="jp-title">{html.escape(safe_get(r,"Job Profile"))}</div><div class="jp-gg">Global Grade {gg}</div></div>'
        
        # META
        for r in rows:
            grid_html += f'''<div class="grid-cell meta-cell">
                <div class="meta-row"><div class="meta-item"><strong>Família:</strong> {html.escape(safe_get(r,'Job Family'))}</div><div class="meta-item"><strong>Subfamília:</strong> {html.escape(safe_get(r,'Sub Job Family'))}</div></div>
                <div class="meta-row"><div class="meta-item"><strong>Carreira:</strong> {html.escape(safe_get(r,'Career Path'))}</div><div class="meta-item"><strong>Cód:</strong> {html.escape(safe_get(r,'Full Job Code'))}</div></div>
                <div class="meta-row"><div class="meta-item"><strong>Função:</strong> {html.escape(safe_get(r,'Function Code'))}</div><div class="meta-item"><strong>Disciplina:</strong> {html.escape(safe_get(r,'Discipline Code'))}</div></div>
            </div>'''

        # CONTEÚDO
        sections_map = [("🧭", "Sub Job Family Description", "#95a5a6"), ("🧠", "Job Profile Description", "#e91e63"),
                        ("🏛️", "Career Band Description", "#673ab7"), ("🎯", "Role Description", "#1E56E0"),
                        ("🏅", "Grade Differentiator", "#ff9800"), ("🎓", "Qualifications", "#009688")]
        for emoji, col, color in sections_map:
            for r in rows:
                grid_html += f'<div class="grid-cell section-cell" style="border-left-color:{color};"><div class="section-title" style="color:{color};"><span>{emoji}</span> {col}</div><div class="section-content">{format_paragraphs(safe_get(r, col))}</div></div>'

        # FOOTER
        for _ in rows: grid_html += '<div class="grid-cell footer-cell"></div>'
        st.markdown(grid_html + '</div>', unsafe_allow_html=True)
    else:
        st.info("👆 Selecione cargos acima para visualizar.")
else:
    st.error("Erro ao carregar dados.")
