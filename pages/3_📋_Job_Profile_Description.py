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
.block-container { max-width: 95% !important; padding-left: 2rem !important; padding-right: 2rem !important; }
/* GRID DINÂMICO */
.comparison-grid { display: grid; gap: 25px; margin-top: 20px; }
.grid-cell { background: #fff; border: 1px solid var(--gray-line); padding: 20px; display: flex; flex-direction: column; }
/* HEADER */
.header-cell { background: var(--gray-bg); border-radius: 12px 12px 0 0; border-bottom: none; min-height: 100px; justify-content: center; }
.jp-title { font-size: 22px; font-weight: 800; color: var(--dark-gray); line-height: 1.2; margin-bottom: 8px; }
.jp-gg { color: var(--blue); font-weight: 700; font-size: 1.1rem; }
/* METADADOS */
.meta-cell { background: #fff; border-top: 1px solid var(--gray-line); border-bottom: 1px solid var(--gray-line); font-size: 0.9rem; color: #555; gap: 8px; padding: 15px 20px; }
.meta-row { display: flex; flex-wrap: wrap; gap: 15px; }
.meta-item strong { color: #333; font-weight: 700; }
/* SEÇÕES */
.section-cell { border-left-width: 5px; border-left-style: solid; border-top: none; background: #fdfdfd; padding: 15px 20px; }
.section-title { font-weight: 700; font-size: 1rem; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
.section-content { color: #333; line-height: 1.6; font-size: 0.95rem; }
.jp-p { margin: 0 0 8px 0; }
/* FOOTER */
.footer-cell { height: 15px; border-top: none; border-radius: 0 0 12px 12px; background: #fff; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. FUNÇÕES DE DADOS
# ==============================================================================
@st.cache_data
def load_job_profile_df():
    # --------------------------------------------------------------------------
    # TENTA CARREGAR O ARQUIVO REAL ('data.xlsx')
    # Certifique-se de fazer upload do seu arquivo Excel para a raiz do projeto
    # --------------------------------------------------------------------------
    try:
        # Tenta ler o arquivo Excel. Ajuste o nome se necessário.
        return pd.read_excel("data.xlsx")
    except FileNotFoundError:
        # SE NÃO ENCONTRAR, USA ESTES DADOS DE EXEMPLO (AVISO NA TELA)
        st.warning("⚠️ Arquivo 'data.xlsx' não encontrado. Usando dados de exemplo.")
        return pd.DataFrame({
            "Job Family": ["Tech", "Tech", "People", "Finance"],
            "Sub Job Family": ["Software Eng", "Data Science", "HR BP", "Accounting"],
            "Career Path": ["Professional", "Professional", "Management", "Professional"],
            "Global Grade": ["10", "12", "15", "11"],
            "Job Profile": ["Senior Developer", "Lead Data Scientist", "HR Director", "Senior Accountant"],
            "Full Job Code": ["T-SE-P3", "T-DS-P4", "P-HR-M2", "F-AC-P3"],
            "Function Code": ["TEC", "DAT", "HUM", "FIN"],
            "Discipline Code": ["SWE", "DSC", "HRP", "ACC"],
            "Sub Job Family Description": ["Dev software...", "Analisa dados...", "Gere pessoas...", "Cuida das contas..."],
            "Job Profile Description": ["Backend core...", "Modelos de ML...", "Diretor de RH...", "Compliance fiscal..."],
            "Career Band Description": ["Contribuinte...", "Expert...", "Líder funcional...", "Sênior..."],
            "Role Description": ["- Coda\n- Revisa PRs", "- Cria modelos\n- Mentora", "- Estratégia\n- Contratação", "- Fechamento mês\n- Auditoria"],
            "Grade Differentiator": ["Problemas complexos...", "Impacto na divisão...", "Impacto funcional...", "Especialista..."],
            "Qualifications": ["BSc CS, 5+ anos", "MSc/PhD, 8+ anos", "MBA, 10+ anos", "CPA, 5+ anos"]
        })

def safe_get(row, key, default="-"):
    val = row.get(key, default)
    return str(val).strip() if not pd.isna(val) and str(val).strip() != "" else default

def format_paragraphs(text):
    if not text or str(text).strip() in ["-", "nan", "None"]: return "-"
    parts = re.split(r"\n+|•|\r", str(text).strip())
    return "".join(f"<p class='jp-p'>• {html.escape(p.strip())}</p>" for p in parts if len(p.strip()) > 1)

# ==============================================================================
# 4. LÓGICA PRINCIPAL
# ==============================================================================
df = load_job_profile_df()
section("📋 Job Profile Description")

if df is not None and not df.empty:
    # --- FILTROS EM CASCATA ---
    c1, c2, c3 = st.columns([1.2, 1.5, 1])
    with c1:
        fam = st.selectbox("📂 Família", sorted(df["Job Family"].dropna().unique()))
        filtered = df[df["Job Family"] == fam]
    with c2:
        sub = st.selectbox("📂 Subfamília", sorted(filtered["Sub Job Family"].dropna().unique()))
        sub_df = filtered[filtered["Sub Job Family"] == sub]
    with c3:
        career = st.selectbox("🛤️ Trilha", sorted(sub_df["Career Path"].dropna().unique()))
        career_df = sub_df[sub_df["Career Path"] == career]

    # --- SELEÇÃO DE CARGOS ---
    career_df["Global Grade Num"] = pd.to_numeric(career_df["Global Grade"], errors='coerce').fillna(0)
    career_df_sorted = career_df.sort_values(by="Global Grade Num", ascending=False)
    career_df_sorted["Label"] = career_df_sorted.apply(lambda x: f"GG{int(x['Global Grade Num'])} — {x['Job Profile']}" if x['Global Grade Num']>0 else x['Job Profile'], axis=1)

    selected = st.multiselect("📌 Selecione até 3 cargos para comparar:", career_df_sorted["Label"].unique(), max_selections=3)

    # --- RENDERIZAÇÃO DO GRID ---
    if selected:
        rows = [career_df_sorted[career_df_sorted["Label"] == label].iloc[0] for label in selected]
        grid_html = f'<div class="comparison-grid" style="grid-template-columns: repeat({len(rows)}, 1fr);">'
        
        # 1. HEADER
        for r in rows:
            gg = safe_get(r, 'Global Grade').replace('.0', '')
            grid_html += f'<div class="grid-cell header-cell"><div class="jp-title">{html.escape(safe_get(r,"Job Profile"))}</div><div class="jp-gg">Global Grade {gg}</div></div>'
        
        # 2. METADADOS
        for r in rows:
            grid_html += f'''<div class="grid-cell meta-cell">
                <div class="meta-row"><div class="meta-item"><strong>Família:</strong> {html.escape(safe_get(r,'Job Family'))}</div><div class="meta-item"><strong>Subfamília:</strong> {html.escape(safe_get(r,'Sub Job Family'))}</div></div>
                <div class="meta-row"><div class="meta-item"><strong>Carreira:</strong> {html.escape(safe_get(r,'Career Path'))}</div><div class="meta-item"><strong>Cód:</strong> {html.escape(safe_get(r,'Full Job Code'))}</div></div>
                <div class="meta-row"><div class="meta-item"><strong>Função:</strong> {html.escape(safe_get(r,'Function Code'))}</div><div class="meta-item"><strong>Disciplina:</strong> {html.escape(safe_get(r,'Discipline Code'))}</div></div>
            </div>'''

        # 3. CONTEÚDO
        sections = [("🧭", "Sub Job Family Description", "#95a5a6"), ("🧠", "Job Profile Description", "#e91e63"),
                    ("🏛️", "Career Band Description", "#673ab7"), ("🎯", "Role Description", "#1E56E0"),
                    ("🏅", "Grade Differentiator", "#ff9800"), ("🎓", "Qualifications", "#009688")]
        for emoji, col, color in sections:
            for r in rows:
                grid_html += f'<div class="grid-cell section-cell" style="border-left-color:{color};"><div class="section-title" style="color:{color};"><span>{emoji}</span> {col}</div><div class="section-content">{format_paragraphs(safe_get(r, col))}</div></div>'

        # 4. FOOTER
        for _ in rows: grid_html += '<div class="grid-cell footer-cell"></div>'
        st.markdown(grid_html + '</div>', unsafe_allow_html=True)
    else:
        st.info("👆 Selecione um ou mais cargos acima para visualizar.")
else:
    st.error("Não foi possível carregar os dados.")
