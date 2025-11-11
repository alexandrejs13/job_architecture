# -*- coding: utf-8 -*-
# pages/4_🗺️_Job_Maps.py

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from utils.data_loader import load_excel_data
from utils.ui_components import section, lock_sidebar 
from utils.ui import setup_sidebar
from pathlib import Path

# ===========================================================
# 1. CONFIGURAÇÃO DE PÁGINA E ESTADO
# ===========================================================
st.set_page_config(
    page_title="Job Map", 
    page_icon="🗺️", # Ícone usado na aba e na sidebar
    layout="wide"
)

# ===========================================================
# 2. APLICA VISUAL E SIDEBAR CSS
# ===========================================================
# --- INJEÇÃO DO CSS DE SIDEBAR/HEADER ---
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# ----------------------------------------

setup_sidebar() 
lock_sidebar()

if 'fullscreen' not in st.session_state:
    st.session_state.fullscreen = False

def toggle_fullscreen():
    st.session_state.fullscreen = not st.session_state.fullscreen

# ===========================================================
# 3. CSS BASE (REVISADO PARA ESTILO DOS BOTÕES)
# ===========================================================
css_base = """
<style>
:root {
    --blue: #145efc;    
    --gray-line: #e0e0e0;
    --gray-bg: #f8f9fa; 
    --dark-gray: #333333;
    --red-exit: #dc3545; /* Mantendo vermelho para contraste visual de 'sair' */
}

/* ============ NOVO HEADER PADRÃO ============ */
.page-header {
    background-color: var(--blue);
    color: white;
    font-weight: 750;
    font-size: 1.35rem;
    border-radius: 12px;
    padding: 22px 36px;
    display: flex;
    align-items: center;
    gap: 18px;
    width: 100%;
    margin-bottom: 20px; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
/* Removida a tag .page-header img pois estamos usando emoji */
/* =========================================================== */

.block-container {
    max-width: 1600px !important;
    margin: auto !important;
    padding: 2rem 5rem !important;
}

/* Topbar: ZERADO o padding e fundo para remover o container vazio. */
.topbar {
    position: relative; 
    z-index: 10;
    background: transparent; 
    padding: 0px 0px 20px 0px; 
    border-bottom: 0px none;
    margin-bottom: 0px; 
    border-radius: 0;
    box-shadow: none; 
}

/* === ESTILO DO BOTÃO TELA CHEIA (NORMAL) === */
[data-testid="stButton"] button {
    border-color: var(--blue) !important;
    background-color: var(--blue) !important; /* Fundo AZUL */
    color: white !important; /* Letra BRANCA */
    font-weight: 600 !important;
}
[data-testid="stButton"] button:hover {
    background-color: #1a62ff !important; /* Azul um pouco mais claro no hover */
    color: white !important;
}

/* ... (Estilos do mapa: .map-wrapper, .jobmap-grid, headers, etc. permanecem inalterados) ... */

</style>
"""

# ===========================================================
# CSS MODO TELA CHEIA (AJUSTE NO BOTÃO SAIR)
# ===========================================================
css_fullscreen = f"""
<style>
    header, section[data-testid="stSidebar"], .topbar, footer { display: none !important; }
    .block-container { max-width: 100vw !important; padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
    .map-wrapper { position: fixed !important; top: 0; left: 0; width: 100vw !important; height: 100vh !important; z-index: 9999; border: none !important; border-top: 5px solid var(--blue) !important; margin: 0 !important; border-radius: 0 !important; }
    
    #fixed-exit-container { position: fixed !important; bottom: 30px !important; right: 30px !important; z-index: 100000 !important; }
    
    /* === ESTILO DO BOTÃO SAIR (TELA CHEIA) === */
    #fixed-exit-container button {{ 
        background-color: var(--blue) !important; /* AZUL */
        color: white !important; /* BRANCA */
        border: none !important; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important; 
        padding: 12px 25px !important; 
        font-weight: 800 !important; 
        border-radius: 30px !important; 
    }}
    #fixed-exit-container button:hover {{ 
        background-color: #1a62ff !important; 
        transform: scale(1.05); 
    }}
</style>
"""
st.markdown(css_base, unsafe_allow_html=True)
if st.session_state.fullscreen: st.markdown(css_fullscreen, unsafe_allow_html=True)

# ===========================================================
# 4. FUNÇÕES DE CACHE E UTILITÁRIOS (Permanecem inalteradas)
# ===========================================================
@st.cache_data(ttl=3600)
def get_prepared_data():
    data = load_excel_data()
    df = data.get("job_profile", pd.DataFrame())
    required = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade"]
    if not all(c in df.columns for c in required): return pd.DataFrame()
    for col in required: df[col] = df[col].astype(str).str.strip()
    df["Sub Job Family"] = df["Sub Job Family"].replace(['nan', 'None', '', '<NA>'], '-')
    df = df[~df["Job Family"].isin(['nan', 'None', ''])]
    df = df[~df["Job Profile"].isin(['nan', 'None', ''])]
    df = df[~df["Global Grade"].isin(['nan', 'None', ''])]
    df["Global Grade"] = df["Global Grade"].str.replace(r"\.0$", "", regex=True)
    return df

def get_path_color(path_name):
    p_lower = str(path_name).lower().strip()
    if "manage" in p_lower or "executive" in p_lower: return "var(--blue)"
    if "professional" in p_lower or "specialist" in p_lower: return "var(--green)"
    if "techni" in p_lower or "support" in p_lower: return "var(--orange)"
    return "var(--purple)"

@st.cache_data(ttl=600, show_spinner="Gerando mapa...")
def generate_map_html(df_filtered, families_order):
    if df_filtered.empty: return "<div style='padding: 20px;'>Nenhum dado encontrado.</div>"
    
    active_families = [f for f in families_order if f in df_filtered["Job Family"].unique()]
    grades = sorted(df_filtered["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else 999, reverse=True)

    subfamilias_map = {}
    col_index = 2
    header_spans = {}
    for f in active_families:
        subs = sorted(df_filtered[df_filtered["Job Family"] == f]["Sub Job Family"].unique().tolist())
        header_spans[f] = len(subs)
        for sf in subs:
            subfamilias_map[(f, sf)] = col_index
            col_index += 1

    grouped = df_filtered.groupby(["Job Family", "Sub Job Family", "Global Grade"])
    cards_data = {}
    for name, group in grouped:
        cards_data[name] = group.to_dict('records')

    cards_count_map = {}
    content_map = {}
    for g in grades:
        for (f, sf), c_idx in subfamilias_map.items():
            key = (f, sf, g)
            records = cards_data.get(key, [])
            count = len(records)
            cards_count_map[(g, c_idx)] = count
            if count > 0:
                content_map[(g, c_idx)] = "|".join(sorted(set(r["Job Profile"] + r["Career Path"] for r in records)))
            else:
                content_map[(g, c_idx)] = None

    span_map = {}
    skip_set = set()
    for (_, c_idx) in subfamilias_map.items():
        for i, g in enumerate(grades):
            if (g, c_idx) in skip_set: continue
            current_sig = content_map.get((g, c_idx))
            if current_sig is None:
                span_map[(g, c_idx)] = 1
                continue
            span = 1
            for next_g in grades[i+1:]:
                if content_map.get((next_g, c_idx)) == current_sig:
                    span += 1
                    skip_set.add((next_g, c_idx))
                else:
                    break
            span_map[(g, c_idx)] = span

    cell_html_cache = {}
    for i, g in enumerate(grades):
        for (f, sf), c_idx in subfamilias_map.items():
            if (g, c_idx) in skip_set or content_map.get((g, c_idx)) is None: continue
            span = span_map.get((g, c_idx), 1)
            gg_label = f"GG {g}"
            if span > 1:
                covered = grades[i : i + span]
                nums = [int(x) for x in covered if x.isdigit()]
                if nums: gg_label = f"GG {min(nums)}-{max(nums)}"
            
            records = cards_data.get((f, sf, g), [])
            cards_html = []
            for row in records:
                path_color = get_path_color(row['Career Path'])
                tooltip = f"{row['Job Profile']} | {row['Career Path']} ({gg_label})"
                cards_html.append(
                    f"<div class='job-card' style='border-left-color: {path_color} !important;' title='{tooltip}'>"
                    f"<b>{row['Job Profile']}</b><span>{row['Career Path']} - {gg_label}</span></div>"
                )
            cell_html_cache[(g, c_idx)] = "".join(cards_html)

    col_widths = ["100px"]
    for (_, sf), c_idx in subfamilias_map.items():
        max_cards = 0
        for g in grades:
            if (g, c_idx) not in skip_set:
                max_cards = max(max_cards, cards_count_map.get((g, c_idx), 0))
        width_cards = 135 + 25 if max_cards <= 1 else (min(max(1, max_cards), 6) * 135) + ((min(max(1, max_cards), 6) - 1) * 8) + 25
        col_widths.append(f"{max(len(str(sf)) * 5 + 30, width_cards)}px")
    grid_template = f"grid-template-columns: {' '.join(col_widths)};"

    palette = [("#4F6D7A", "#E6EFF2"), ("#5C7A67", "#E8F2EB"), ("#7A5C5C", "#F2E6E6"), ("#6B5C7A", "#EBE6F2"),
               ("#7A725C", "#F2EFE6"), ("#5C6B7A", "#E6EBF2"), ("#7A5C74", "#F2E6EF"), ("#5C7A78", "#E6F2F1")]
    map_cor_fam = {f: palette[i % len(palette)][0] for i, f in enumerate(families_order)}
    map_cor_sub = {f: palette[i % len(palette)][1] for i, f in enumerate(families_order)}

    html = [f"<div class='map-wrapper'><div class='jobmap-grid' style='{grid_template}'>"]
    html.append("<div class='gg-header'>GG</div>")
    
    curr = 2
    for f in active_families:
        span = header_spans[f]
        html.append(f"<div class='header-family' style='grid-column: {curr} / span {span}; background:{map_cor_fam[f]};'>{f}</div>")
        curr += span
    for (f, sf), c_idx in subfamilias_map.items():
        html.append(f"<div class='header-subfamily' style='grid-column: {c_idx}; background:{map_cor_sub[f]};'>{sf}</div>")
    for i, g in enumerate(grades):
        row_idx = i + 3
        html.append(f"<div class='gg-cell' style='grid-row: {row_idx};'>GG {g}</div>")
        for (f, sf), c_idx in subfamilias_map.items():
            if (g, c_idx) in skip_set: continue
            span = span_map.get((g, c_idx), 1)
            row_str = f"grid-row: {row_idx} / span {span};" if span > 1 else f"grid-row: {row_idx};"
            html.append(f"<div class='cell' style='grid-column: {c_idx}; {row_str}'>{cell_html_cache.get((g, c_idx), '')}</div>")
    html.append("</div></div>")
    return "".join(html)

# ===========================================================
# 5. LÓGICA DA PÁGINA E RENDERIZAÇÃO DO NOVO HEADER
# ===========================================================
df = get_prepared_data()
if df.empty:
    st.error("Erro ao carregar dados.")
    st.stop()

# NOVO HEADER PADRÃO COM EMOJI (RESOLVE O PROBLEMA DO ÍCONE)
st.markdown(f"""
<div class="page-header">
  <span style='font-size: 3rem; margin-top: -8px;'>🗺️</span>
  Mapeamento de Cargos (Job Map)
</div>
""", unsafe_allow_html=True)


preferred_order = ["Top Executive/General Management", "Corporate Affairs/Communications", "Legal & Internal Audit", "Finance", "IT", "People & Culture", "Sales", "Marketing", "Technical Services", "Research & Development", "Technical Engineering", "Operations", "Supply Chain & Logistics", "Quality Management", "Facility & Administrative Services"]
existing_families = set(df["Job Family"].unique())
families_order = [f for f in preferred_order if f in existing_families] + sorted(list(existing_families - set(preferred_order)))

if not st.session_state.fullscreen:
    # Topbar com padding zerado verticalmente para remover o container vazio
    st.markdown("<div class='topbar'>", unsafe_allow_html=True) 
    c1, c2, c3 = st.columns([2, 2, 0.8])
    with c1: fam_filter = st.selectbox("Família", ["Todas"] + families_order)
    paths = df["Career Path"].unique().tolist() if fam_filter == "Todas" else df[df["Job Family"] == fam_filter]["Career Path"].unique().tolist()
    with c2: path_filter = st.selectbox("Trilha", ["Todas"] + sorted([p for p in paths if pd.notna(p) and p != 'nan' and p != '']))
    with c3:
        st.write("")
        st.markdown('<div style="margin-top: 15px;">', unsafe_allow_html=True)
        # O botão já é azul e branco devido ao CSS global que ajustamos.
        if st.button("⛶ Tela Cheia", use_container_width=True): toggle_fullscreen(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Lógica de tela cheia
    fam_filter, path_filter = st.session_state.get('fam_filter', 'Todas'), st.session_state.get('path_filter', 'Todas')
    st.markdown('<div id="fixed-exit-container">', unsafe_allow_html=True)
    # O botão Sair é azul e branco devido ao CSS do css_fullscreen.
    if st.button("❌ Sair"): toggle_fullscreen(); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # FUNCIONALIDADE ESC PARA SAIR DA TELA CHEIA (JÁ EXISTIA, APENAS CONFIRMANDO)
    components.html("""
        <script>
            document.addEventListener('keydown', (e) => { 
                if (e.key === 'Escape') {
                    // Clica no botão 'Sair' simulado para sair da tela cheia
                    const exitButton = window.parent.document.querySelector('#fixed-exit-container button');
                    if (exitButton) {
                        exitButton.click();
                    }
                }
            });
        </script>
        """, height=0, width=0)

st.session_state.fam_filter, st.session_state.path_filter = fam_filter, path_filter
df_filtered = df.copy()
if fam_filter != "Todas": df_filtered = df_filtered[df["Job Family"] == fam_filter]
if path_filter != "Todas": df_filtered = df_filtered[df["Career Path"] == path_filter]

# Renderiza o mapa otimizado
st.markdown(generate_map_html(df_filtered, families_order), unsafe_allow_html=True)
