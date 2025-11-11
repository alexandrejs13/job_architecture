import streamlit as st
import pandas as pd
import re
from pathlib import Path
from utils.ui import sidebar_logo_and_title
import html # Adicionado para escapar caracteres HTML no output

# ===========================================================
# 1. CONFIGURAÇÃO GERAL
# ===========================================================
st.set_page_config(
    page_title="Job Profile Description",
    page_icon="📋",
    layout="wide", # Mantido 'wide' para a comparação
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. CSS GLOBAL, HEADER PADRÃO E ESTILO DE COMPARAÇÃO (REPLICADO DA PAG 5)
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

# Incluído o estilo do header padronizado (da Pag 2) e o estilo de comparação (da Pag 5)
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

/* Ajuste o max-width para ser mais amplo, como na Pag 5 (95% ou valor fixo maior) */
.block-container {
    max-width: 95% !important; 
    padding-left: 1rem !important; 
    padding-right: 1rem !important;
}

/* ============ ESTILOS DE COMPARAÇÃO (REPLICADOS DA PAG 5) ============ */
.comparison-grid {
    display: grid;
    /* Colunas dinâmicas serão definidas no Python com style="grid-template-columns:..." */
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
.fjc-title { font-size: 18px; font-weight: 800; color: #2c3e50; margin-bottom: 10px; min-height: 50px; }
.fjc-gg-row { display: flex; justify-content: space-between; align-items: center; }
.fjc-gg { color: #145efc; /* Azul SIG */ font-weight: 700; }
/* Removido fjc-score pois não é usado aqui, mas vou deixar um placeholder para cor */
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
/* ===================================================================== */
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
    if s.lower() in ("nan", "none", "", "na", "-"): # Adicionado "-"
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

# Garantir que a coluna GG seja numérica e limpa para comparação
df["Global Grade"] = df["Global Grade"].apply(normalize_grade)
df["GG"] = df["Global Grade"].str.replace(r"\.0$", "", regex=True) # GG limpo para exibição
df["Global Grade Num"] = pd.to_numeric(df["Global Grade"], errors='coerce').fillna(0).astype(int)

if not levels.empty and "Global Grade" in levels.columns:
    levels["Global Grade"] = levels["Global Grade"].apply(normalize_grade)
    levels["Global Grade Num"] = pd.to_numeric(levels["Global Grade"], errors='coerce').fillna(0).astype(int)

# ===========================================================
# 5. FILTROS
# ===========================================================
st.markdown("## 🔍 Explorador de Perfis")

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
    row = filtered[filtered["Job Profile"] == nome]
    if row.empty:
        continue

    data = row.iloc[0].copy()
    gg = data.get("Global Grade", "")
    gg_num = data.get("Global Grade Num", 0)
    level_name = ""

    # Buscar Level Name
    if not levels.empty and "Global Grade Num" in levels.columns and "Level Name" in levels.columns:
        match = levels[levels["Global Grade Num"] == gg_num]
        if not match.empty:
            level_name = f"• {match['Level Name'].iloc[0]}"

    cards_data.append({"row": data, "lvl": level_name})

if not cards_data:
    st.warning("Nenhum perfil de cargo válido encontrado após a filtragem.")
    st.stop()

num_results = len(cards_data)
grid_style = f"grid-template-columns: repeat({num_results}, 1fr);"
grid_html = f'<div class="comparison-grid" style="{grid_style}">'

# Configuração das seções com cores (usando as cores do Page 5 para consistência)
sections_config = [
    ("🧭 Sub Job Family Description", "Sub Job Family Description", "#95a5a6"),
    ("🧠 Job Profile Description", "Job Profile Description", "#e91e63"),
    ("🏛️ Career Band Description", "Career Band Description", "#673ab7"),
    ("🎯 Role Description", "Role Description", "#145efc"), # Azul SIG para Role Description
    ("🏅 Grade Differentiator", "Grade Differentiator", "#ff9800"),
    ("🎓 Qualifications", "Qualifications", "#009688")
]

# 1. Cabeçalho
for card in cards_data:
    grid_html += f"""
    <div class="grid-cell header-cell">
        <div class="fjc-title">{html.escape(card['row'].get('Job Profile', '-'))}</div>
        <div class="fjc-gg-row">
            <div class="fjc-gg">GG {card['row'].get('Global Grade', '-')} {card['lvl']}</div>
        </div>
    </div>"""

# 2. Metadados
for card in cards_data:
    d = card['row']
    meta = []
    
    # Lista de metadados, incluindo Full Job Code
    for lbl, col in [
        ("Família", "Job Family"), 
        ("Subfamília", "Sub Job Family"), 
        ("Carreira", "Career Path"), 
        ("Cód", "Full Job Code") # <- CAMPO ADICIONADO
    ]:
        val = str(d.get(col, "") or "-").strip()
        meta.append(f'<div class="meta-row"><strong>{lbl}:</strong> {html.escape(val)}</div>')
    
    grid_html += f"""
    <div class="grid-cell meta-cell">
        {''.join(meta)}
    </div>"""

# 3. Seções de Conteúdo
for title, field, color in sections_config:
    for card in cards_data:
        content = str(card['row'].get(field, '-'))
        # Condição para pular a seção se o conteúdo estiver vazio/nan
        if len(content.strip()) < 2 or content.lower() == 'nan':
            grid_html += f'<div class="grid-cell section-cell" style="border-left-color: transparent; background: transparent; border: none;"></div>'
        else:
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
