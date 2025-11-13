import streamlit as st
import pandas as pd
import re
from pathlib import Path
import html 
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
# 2. CSS GLOBAL, HEADER PADRÃO E ESTILO DE COMPARAÇÃO
# ===========================================================
# Não alterado, mantém o layout
# ... (restante do CSS omitido por brevidade, mas o código completo o incluiria)
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Supondo que você tem a função sidebar_logo_and_title no utils.ui
try:
    from utils.ui import sidebar_logo_and_title
    sidebar_logo_and_title()
except ImportError:
    st.sidebar.title("📋 Job Profile Description")

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
    max-width: 95% !important; 
    padding-left: 1rem !important; 
    padding-right: 1rem !important;
}

/* ============ ESTILOS DE COMPARAÇÃO (REPLICADOS DA PAG 5) ============ */
.comparison-grid {
    display: grid;
    gap: 20px;
    margin-top: 20px;
}
.grid-cell {
    background: #fff;
    border: 1px solid #e0e0e0;
    padding: 15px;
    display: flex;
    flex-direction: column;
}
.header-cell {
    background: #f8f9fa;
    border-radius: 12px 12px 0 0;
    border-bottom: none;
}
.fjc-title { 
    font-size: 18px; 
    font-weight: 800; 
    color: #2c3e50; 
    margin-bottom: 2px; /* AJUSTE: DIMINUI ESPAÇO ENTRE TÍTULO E GG */
    min-height: 50px; 
}
.fjc-gg-row { display: flex; justify-content: space-between; align-items: center; }
.fjc-gg { color: #145efc; font-weight: 700; }
.fjc-score { color: #145efc; font-weight: 700; padding: 4px 10px; border-radius: 12px; font-size: 0.9rem; } 
.meta-cell {
    border-top: 1px solid #eee;
    border-bottom: 1px solid #eee;
    font-size: 0.85rem;
    color: #555;
    min-height: 120px;
}
.meta-row { margin-bottom: 5px; }
.section-cell {
    border-left-width: 5px;
    border-left-style: solid;
    border-top: none;
    background: #fdfdfd;
}
.section-title { font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; color: #333; display: flex; align-items: center; gap: 5px;}
.section-content { color: #444; font-size: 0.9rem; line-height: 1.5; white-space: pre-wrap; }
.footer-cell {
    height: 10px;
    border-top: none;
    border-radius: 0 0 12px 12px;
    background: #fff;
}
</style>

<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/business%20review%20clipboard.png" alt="icon">
  Descrição do Perfil de Cargo (Job Profile Description)
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 3. FUNÇÕES AUXILIARES
# ===========================================================
def normalize_grade(val):
    s = str(val).strip()
    if s.lower() in ("nan", "none", "", "na", "-"):
        return ""
    return re.sub(r"\.0$", "", s)

# NOVA FUNÇÃO: Normaliza nomes das colunas
def sanitize_columns(df):
    """Converte nomes de colunas para snake_case e remove caracteres especiais."""
    cols = {}
    for col in df.columns:
        # Substitui espaços, barras e traços por underscore
        new_col = re.sub(r'[ /-]+', '_', col.strip())
        # Remove quaisquer outros caracteres não alfanuméricos ou underscore
        new_col = re.sub(r'[^\w_]', '', new_col).lower()
        cols[col] = new_col
    return df.rename(columns=cols)

@st.cache_data
def load_excel(path):
    try:
        df = pd.read_excel(path)
        # Aplicar sanitização na leitura
        df = sanitize_columns(df) 
        for c in df.select_dtypes(include="object"):
            df[c] = df[c].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar {path}: {e}")
        return pd.DataFrame()

# ===========================================================
# 4. DADOS
# ===========================================================
# Atenção: os nomes das colunas AGORA devem estar em snake_case minúsculo
df = load_excel("data/Job Profile.xlsx")
levels = load_excel("data/Level Structure.xlsx")

if df.empty:
    st.error("❌ Arquivo 'Job Profile.xlsx' não encontrado ou inválido.")
    st.stop()

# Usando nomes de colunas normalizados (minúsculas e underscore)
df["global_grade"] = df["global_grade"].apply(normalize_grade)
df["gg"] = df["global_grade"].str.replace(r"\.0$", "", regex=True) 
df["global_grade_num"] = pd.to_numeric(df["global_grade"], errors='coerce').fillna(0).astype(int)

if not levels.empty and "global_grade" in levels.columns:
    levels["global_grade"] = levels["global_grade"].apply(normalize_grade)
    levels["global_grade_num"] = pd.to_numeric(levels["global_grade"], errors='coerce').fillna(0).astype(int)

# ===========================================================
# 5. FILTROS
# ===========================================================
st.markdown("## 🔍 Explorador de Perfis")

# Usando nomes de colunas normalizados
familias = sorted(df["job_family"].dropna().unique())

col1, col2, col3 = st.columns(3)
with col1:
    familia = st.selectbox("Família (Job Family):", ["Selecione..."] + familias, index=0)
with col2:
    # Usando nomes de colunas normalizados
    subs = sorted(df[df["job_family"] == familia]["sub_job_family"].dropna().unique()) if familia != "Selecione..." else []
    sub = st.selectbox("Sub-Família:", ["Selecione..."] + subs, index=0)
with col3:
    # Usando nomes de colunas normalizados
    paths = sorted(df[df["sub_job_family"] == sub]["career_path"].dropna().unique()) if sub != "Selecione..." else []
    trilha = st.selectbox("Trilha (Career Path):", ["Selecione..."] + paths, index=0)

filtered = df.copy()
if familia != "Selecione...":
    filtered = filtered[filtered["job_family"] == familia]
if sub != "Selecione...":
    filtered = filtered[filtered["sub_job_family"] == sub]
if trilha != "Selecione...":
    filtered = filtered[filtered["career_path"] == trilha]

if filtered.empty:
    st.info("Ajuste os filtros para visualizar os perfis.")
    st.stop()

# ===========================================================
# 6. PICKLIST (GG + CARGO)
# ===========================================================
# Usando nomes de colunas normalizados
filtered["label"] = filtered.apply(
    lambda r: f'GG {r["gg"] or "-"} • {r["job_profile"]}', axis=1
)
label_to_profile = dict(zip(filtered["label"], filtered["job_profile"]))

selecionados_labels = st.multiselect(
    "Selecione até 3 perfis para comparar:",
    options=list(label_to_profile.keys()),
    max_selections=3,
)

if not selecionados_labels:
    st.info("Selecione ao menos 1 perfil para exibir a comparação.")
    st.stop()

selecionados = [label_to_profile[l] for l in selecionados_labels]

# ===========================================================
# 7. GRID DE COMPARAÇÃO (REPLICAÇÃO DO LAYOUT DA PAG 5)
# ===========================================================
st.markdown("---")
st.header("✨ Comparativo de Perfis Selecionados")

cards_data = []
for nome in selecionados:
    # Usando nomes de colunas normalizados
    row = filtered[filtered["job_profile"] == nome]
    if row.empty:
        continue

    data = row.iloc[0].copy()
    gg = data.get("global_grade", "")
    gg_num = data.get("global_grade_num", 0)
    level_name = ""

    # Buscar Level Name (usando nomes de colunas normalizados)
    if not levels.empty and "global_grade_num" in levels.columns and "level_name" in levels.columns:
        match = levels[levels["global_grade_num"] == gg_num]
        if not match.empty:
            level_name = f"• {match['level_name'].iloc[0]}"

    cards_data.append({"row": data, "lvl": level_name})

if not cards_data:
    st.warning("Nenhum perfil de cargo válido encontrado após a filtragem.")
    st.stop()

num_results = len(cards_data)
grid_style = f"grid-template-columns: repeat({num_results}, 1fr);"
grid_html = f'<div class="comparison-grid" style="{grid_style}">'

# Configuração das seções com o título de exibição e o nome da coluna no DataFrame
sections_config = [
    ("🧭 Sub Job Family Description", "sub_job_family_description", "#95a5a6"),
    ("🧠 Job Profile Description", "job_profile_description", "#e91e63"),
    ("🏛️ Career Band Description", "career_band_description", "#673ab7"),
    ("🎯 Role Description", "role_description", "#145efc"), 
    ("🏅 Grade Differentiator", "grade_differentiator", "#ff9800"),
    ("🎓 Qualifications", "qualifications", "#009688"),
    
    # NOVAS COLUNAS - usando nomes de colunas normalizados (snake_case)
    ("📊 Specific parameters / KPIs", "specific_parameters_kpis", "#c0392b"),
    ("💡 Competencies 1", "competencies_1", "#c0392b"),
    ("💡 Competencies 2", "competencies_2", "#c0392b"),
    ("💡 Competencies 3", "competencies_3", "#c0392b"),
]

# 1. Cabeçalho
for card in cards_data:
    grid_html += f"""
    <div class="grid-cell header-cell">
        <div class="fjc-title">{html.escape(card['row'].get('job_profile', '-'))}</div>
        <div class="fjc-gg-row">
            <div class="fjc-gg">GG {card['row'].get('global_grade', '-')} {card['lvl']}</div>
        </div>
    </div>"""

# 2. Metadados
for card in cards_data:
    d = card['row']
    meta = []
    
    # Lista de metadados, usando nomes de colunas normalizados
    for lbl, col in [
        ("Família", "job_family"), 
        ("Subfamília", "sub_job_family"), 
        ("Carreira", "career_path"), 
        ("Cód", "full_job_code") 
    ]:
        val = str(d.get(col, "") or "-").strip()
        meta.append(f'<div class="meta-row"><strong>{lbl}:</strong> {html.escape(val)}</div>')
    
    grid_html += f"""
    <div class="grid-cell meta-cell">
        {''.join(meta)}
    </div>"""

# 3. Seções de Conteúdo (agora forçando a renderização de todas as células)
for title, field, color in sections_config:
    for card in cards_data:
        # Pega o conteúdo usando o nome da coluna normalizado.
        content = str(card['row'].get(field, '')).strip()
        
        # Se o conteúdo for 'nan' ou '-' (tratado no normalize_grade, mas garantindo), ele fica vazio.
        if content.lower() in ('nan', '-'):
            content = ''
        
        # Renderiza a célula SEMPRE
        grid_html += f"""
        <div class="grid-cell section-cell" style="border-left-color: {color};">
            <div class="section-title" style="color: {color};">{title}</div>
            <div class="section-content">{html.escape(content)}</div>
        </div>"""

# 4. Rodapé
for card in cards_data:
    grid_html += '<div class="grid-cell footer-cell"></div>'

grid_html += '</div>'
st.markdown(grid_html, unsafe_allow_html=True)
