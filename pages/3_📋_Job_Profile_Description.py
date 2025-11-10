import streamlit as st
import pandas as pd
import re
import html

# --- IMPORTAÇÕES LOCAIS ---
# Certifique-se de que 'section' está sendo importada
from utils.ui import setup_sidebar, section

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA (PRIMEIRO COMANDO)
# ==============================================================================
st.set_page_config(
    page_title="Job Profile Description",
    page_icon="📋",
    layout="wide"
)

# ==============================================================================
# 2. SETUP UI (CSS GLOBAL)
# ==============================================================================
setup_sidebar()

# ==============================================================================
# 3. CSS ESPECÍFICO DA PÁGINA
# ==============================================================================
st.markdown("""
<style>
:root {
  --blue: #145efc;
  --gray-line: #e0e0e0;
  --gray-bg: #f8f9fa;
  --dark-gray: #2c3e50;
}
.block-container {
    max-width: 95% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}
h1 {
    color: var(--blue) !important;
    font-weight: 900 !important;
    font-size: 1.9rem !important;
    display: flex; align-items: center; gap: 10px;
    margin: 0 !important; padding-top: 15px; margin-bottom: 25px !important;
}
/* GRID DINÂMICO */
.comparison-grid {
    display: grid; gap: 25px; margin-top: 20px;
}
.grid-cell {
    background: #fff; border: 1px solid var(--gray-line);
    padding: 20px; display: flex; flex-direction: column;
}
/* HEADER */
.header-cell {
    background: var(--gray-bg); border-radius: 12px 12px 0 0;
    border-bottom: none; min-height: 100px; justify-content: center;
}
.jp-title { font-size: 22px; font-weight: 800; color: var(--dark-gray); line-height: 1.2; margin-bottom: 8px; }
.jp-gg { color: var(--blue); font-weight: 700; font-size: 1.1rem; }
/* METADADOS */
.meta-cell {
    background: #fff; border-top: 1px solid var(--gray-line);
    border-bottom: 1px solid var(--gray-line);
    font-size: 0.9rem; color: #555; gap: 8px; padding: 15px 20px;
}
.meta-row { display: flex; flex-wrap: wrap; gap: 15px; }
.meta-item strong { color: #333; font-weight: 700; }
/* SEÇÕES */
.section-cell {
    border-left-width: 5px; border-left-style: solid;
    border-top: none; background: #fdfdfd; padding: 15px 20px;
}
.section-title {
    font-weight: 700; font-size: 1rem; margin-bottom: 10px;
    display: flex; align-items: center; gap: 8px;
}
.section-content { color: #333; line-height: 1.6; font-size: 0.95rem; }
.jp-p { margin: 0 0 8px 0; }
/* FOOTER */
.footer-cell {
    height: 15px; border-top: none; border-radius: 0 0 12px 12px; background: #fff;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. FUNÇÕES AUXILIARES & DADOS
# ==============================================================================
@st.cache_data
def load_job_profile_df():
    """
    CARREGA OS DADOS.
    IMPORTANTE: Substitua o conteúdo desta função pela leitura real do seu arquivo.
    Ex: return pd.read_excel("seu_arquivo.xlsx")
    """
    # --- DADOS FICTÍCIOS PARA TESTE ---
    data = {
        "Job Family": ["Tech", "Tech", "People", "Finance"],
        "Sub Job Family": ["Software Eng", "Data Science", "HR BP", "Accounting"],
        "Career Path": ["Professional", "Professional", "Management", "Professional"],
        "Global Grade": ["10", "12", "15", "11"],
        "Job Profile": ["Senior Developer", "Lead Data Scientist", "HR Director", "Senior Accountant"],
        "Full Job Code": ["T-SE-P3", "T-DS-P4", "P-HR-M2", "F-AC-P3"],
        "Function Code": ["TEC", "DAT", "HUM", "FIN"],
        "Discipline Code": ["SWE", "DSC", "HRP", "ACC"],
        "Sub Job Family Description": ["Develops software...", "Analyzes data...", "Manages people strategy...", "Handles books..."],
        "Job Profile Description": ["Responsible for core backend...", "Leads ML initiatives...", "Oversees HR dept...", "Ensures compliance..."],
        "Career Band Description": ["Independent contributor...", "Recognized expert...", "Functional leader...", "Senior professional..."],
        "Role Description": ["- Writes code\n- Reviews PRs", "- Builds models\n- Mentors team", "- Strategic planning\n- Hiring", "- Month-end close\n- Audits"],
        "Grade Differentiator": ["Complex problems...", "Impacts division...", "Impacts entire function...", "Subject matter expert..."],
        "Qualifications": ["BSc CS, 5+ yrs exp", "MSc/PhD, 8+ yrs exp", "MBA, 10+ yrs exp", "CPA, 5+ yrs exp"]
    }
    return pd.DataFrame(data)

def safe_get(row, key, default="-"):
    """Retorna o valor de uma coluna com segurança, tratando NaNs."""
    val = row.get(key, default)
    if pd.isna(val) or str(val).strip() == "":
        return default
    return str(val).strip()

def format_paragraphs(text):
    """Formata texto cru em parágrafos HTML com bullets se necessário."""
    if not text or text == "-": return "-"
    # Divide por quebras de linha ou bullets comuns
    parts = re.split(r"\n+|•|\r", str(text).strip())
    return "".join(f"<p class='jp-p'>• {html.escape(p.strip())}</p>" for p in parts if len(p.strip()) > 1)

# ==============================================================================
# 5. LÓGICA PRINCIPAL DA PÁGINA
# ==============================================================================
# Carrega os dados
try:
    df = load_job_profile_df()
except Exception as e:
    st.error(f"Erro crítico ao carregar dados: {e}")
    st.stop()

# Renderiza o título da seção
section("📋 Job Profile Description")

# --- FILTROS (CASCATA) ---
if df is not None and not df.empty:
    c1, c2, c3 = st.columns([1.2, 1.5, 1])
    with c1:
        families = sorted(df["Job Family"].dropna().unique())
        fam = st.selectbox("📂 Família", families)
        filtered = df[df["Job Family"] == fam]

    with c2:
        subs = sorted(filtered["Sub Job Family"].dropna().unique())
        sub = st.selectbox("📂 Subfamília", subs)
        sub_df = filtered[filtered["Sub Job Family"] == sub]

    with c3:
        careers = sorted(sub_df["Career Path"].dropna().unique())
        career = st.selectbox("🛤️ Trilha de Carreira", careers)
        career_df = sub_df[sub_df["Career Path"] == career]

    # --- SELEÇÃO DE CARGOS ---
    # Cria uma coluna auxiliar para o label do multiselect
    career_df["Global Grade Num"] = pd.to_numeric(career_df["Global Grade"], errors='coerce').fillna(0)
    career_df_sorted = career_df.sort_values(by="Global Grade Num", ascending=False)

    career_df_sorted["Option Label"] = career_df_sorted.apply(
        lambda x: f"GG{int(x['Global Grade Num'])} — {x['Job Profile']}" if x['Global Grade Num'] > 0 else x['Job Profile'],
        axis=1
    )

    selected_labels = st.multiselect(
        "📌 Selecione até 3 cargos para visualizar/comparar:",
        options=career_df_sorted["Option Label"].unique().tolist(),
        max_selections=3
    )

    # ==============================================================================
    # 6. RENDERIZAÇÃO DO GRID
    # ==============================================================================
    if selected_labels:
        # Filtra as linhas selecionadas mantendo a ordem do multiselect
        selected_rows = []
        for label in selected_labels:
            row = career_df_sorted[career_df_sorted["Option Label"] == label].iloc[0]
            selected_rows.append(row)

        num_cols = len(selected_rows)
        # CSS Grid dinâmico: cria X colunas de tamanho igual
        grid_style = f"grid-template-columns: repeat({num_cols}, 1fr);"
        grid_html = f'<div class="comparison-grid" style="{grid_style}">'

        # --- [A] CABEÇALHO ---
        for row in selected_rows:
            gg = safe_get(row, 'Global Grade').replace('.0', '')
            grid_html += f"""
            <div class="grid-cell header-cell">
                <div class="jp-title">{html.escape(safe_get(row, 'Job Profile'))}</div>
                <div class="jp-gg">Global Grade {gg}</div>
            </div>"""

        # --- [B] METADADOS ---
        for row in selected_rows:
            grid_html += f"""
            <div class="grid-cell meta-cell">
                <div class="meta-row">
                    <div class="meta-item"><strong>Família:</strong> {html.escape(safe_get(row, 'Job Family'))}</div>
                    <div class="meta-item"><strong>Subfamília:</strong> {html.escape(safe_get(row, 'Sub Job Family'))}</div>
                </div>
                <div class="meta-row">
                    <div class="meta-item"><strong>Carreira:</strong> {html.escape(safe_get(row, 'Career Path'))}</div>
                    <div class="meta-item"><strong>Cód:</strong> {html.escape(safe_get(row, 'Full Job Code'))}</div>
                </div>
                <div class="meta-row">
                     <div class="meta-item"><strong>Função:</strong> {html.escape(safe_get(row, 'Function Code'))}</div>
                     <div class="meta-item"><strong>Disciplina:</strong> {html.escape(safe_get(row, 'Discipline Code'))}</div>
                </div>
            </div>"""

        # --- [C] SEÇÕES DE CONTEÚDO ---
        sections_config = [
            ("🧭", "Sub Job Family Description", "Sub Job Family Description", "#95a5a6"),
            ("🧠", "Job Profile Description", "Job Profile Description", "#e91e63"),
            ("🏛️", "Career Band Description", "Career Band Description", "#673ab7"),
            ("🎯", "Role Description", "Role Description", "#1E56E0"),
            ("🏅", "Grade Differentiator", "Grade Differentiator", "#ff9800"),
            ("🎓", "Qualifications", "Qualifications", "#009688")
        ]

        for emoji, title, col_name, color in sections_config:
            for row in selected_rows:
                raw_text = safe_get(row, col_name)
                formatted_text = format_paragraphs(raw_text)
                
                grid_html += f"""
                <div class="grid-cell section-cell" style="border-left-color: {color};">
                    <div class="section-title" style="color: {color};">
                        <span>{emoji}</span> {title}
                    </div>
                    <div class="section-content">{formatted_text}</div>
                </div>"""

        # --- [D] RODAPÉ ---
        for _ in selected_rows:
            grid_html += '<div class="grid-cell footer-cell"></div>'

        grid_html += '</div>' # Fecha .comparison-grid
        st.markdown(grid_html, unsafe_allow_html=True)

    else:
        st.info("👆 Utilize os filtros acima e selecione um ou mais cargos para visualizar.")
else:
    st.warning("Não há dados disponíveis para exibir.")
