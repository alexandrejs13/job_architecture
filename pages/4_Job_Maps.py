# -*- coding: utf-8 -*-
# pages/4_🗺️_Job_Maps.py

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from utils.data_loader import load_excel_data
from utils.ui_components import section, lock_sidebar 
from utils.ui import setup_sidebar

# ===========================================================
# 1. CONFIGURAÇÃO DE PÁGINA E ESTADO (PRIMEIRO COMANDO ST)
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")

# ===========================================================
# 2. APLICA VISUAL
# ===========================================================
setup_sidebar() 
lock_sidebar()

if 'fullscreen' not in st.session_state:
    st.session_state.fullscreen = False

def toggle_fullscreen():
    st.session_state.fullscreen = not st.session_state.fullscreen

# ===========================================================
# 3. CSS BASE (REVISADO)
# ===========================================================
css_base = """
<style>
:root {
    --blue: #145efc;    /* SIG Sky - Destaque principal */
    --green: #28a745;   
    --orange: #fd7e14;  
    --purple: #6f42c1;  
    --red: #dc3545;     
    --gray-line: #e0e0e0;
    --gray-bg: #f8f9fa; /* Fundo cinza claro da topbar */
    --dark-gray: #333333;
}

/* ============ NOVO HEADER PADRÃO (DA PAG 2/3) ============ */
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
.page-header img { width: 48px; height: 48px; }
/* =========================================================== */

.block-container {
    max-width: 1600px !important;
    margin: auto !important;
    padding: 2rem 5rem !important;
}

/* RESTAURADO: Topbar para agrupar os filtros. Removida a borda inferior que causava a barra branca. */
.topbar {
    position: sticky;
    top: 0;
    z-index: 200;
    background: var(--gray-bg);
    padding: 15px 20px;
    border-bottom: 0px none; /* REMOVIDO PARA EVITAR A LINHA BRANCA */
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05); 
}

/* h1 foi removido e substituído pelo .page-header */

.map-wrapper {
    height: 75vh;
    overflow: auto;
    border-top: 3px solid var(--blue);
    border-bottom: 3px solid var(--blue);
    background: white;
    position: relative;
    will-change: transform;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    border-radius: 8px;
}

.jobmap-grid {
    display: grid;
    border-collapse: collapse;
    width: max-content;
    font-size: 0.88rem;
    grid-template-rows: 50px 45px repeat(auto-fill, 110px) !important;
    grid-auto-rows: 110px !important;
    align-content: start !important;
    row-gap: 0px !important;
    column-gap: 0px !important;
    background-color: white !important;
}

/* ... (Demais estilos do grid permanecem) ... */
.jobmap-grid > div {
    background-color: white;
    border-right: 1px solid var(--gray-line);
    border-bottom: 1px solid var(--gray-line);
    box-sizing: border-box;
}

.header-family {
    font-weight: 800;
    color: #fff;
    padding: 0 5px;
    text-align: center;
    border-right: 1px solid rgba(255,255,255,0.3) !important;
    border-bottom: 0px none !important;
    outline: none !important;
    margin-bottom: 0px !important;
    position: sticky;
    top: 0;
    z-index: 57;
    white-space: normal;
    height: 50px !important;
    max-height: 50px !important;
    display: flex;
    align-items: center;
    justify-content: center;
    grid-row: 1;
    font-size: 0.9rem;
    overflow: hidden;
}

.header-subfamily {
    font-weight: 600;
    padding: 0 5px;
    text-align: center;
    position: sticky;
    top: 50px;
    z-index: 56;
    white-space: normal;
    border-top: 0px none !important;
    margin-top: 0px !important;
    border-bottom: 0px none !important;
    outline: none !important;
    height: 45px !important;
    max-height: 45px !important;
    display: flex;
    align-items: center;
    justify-content: center;
    grid-row: 2;
    font-size: 0.85rem;
    overflow: hidden;
    color: var(--dark-gray);
}

.gg-header {
    background: var(--dark-gray) !important;
    color: white;
    font-weight: 800;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    grid-row: 1 / span 2;
    grid-column: 1;
    position: sticky;
    left: 0;
    top: 0;
    z-index: 60;
    border-right: 2px solid white !important;
    border-bottom: 0px none !important;
    height: 95px !important;
}

.gg-cell {
    background: var(--dark-gray) !important;
    color: white;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    left: 0;
    z-index: 55;
    border-right: 2px solid white !important;
    border-top: 1px solid #555 !important;
    grid-column: 1;
    font-size: 0.9rem;
    height: 110px !important;
}

.cell {
    background: white !important;
    padding: 8px;
    text-align: left;
    vertical-align: middle;
    z-index: 1;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    align-content: center;
    height: 100% !important;
    overflow: hidden;
}

.job-card {
    background: #ffffff;
    border: 1px solid var(--gray-line);
    border-left-width: 5px !important;
    border-left-style: solid !important;
    border-radius: 6px;
    padding: 6px 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    font-size: 0.75rem;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: normal;
    width: 135px;
    height: 75px;
    flex: 0 0 135px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow: hidden;
    transition: all 0.2s ease-in-out;
}
.job-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 12px rgba(0,0,0,0.1);
    border-color: var(--blue);
}
.job-card b {
    display: block;
    font-weight: 700;
    margin-bottom: 3px;
    line-height: 1.2;
    color: #222;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.job-card span {
    display: block;
    font-size: 0.7rem;
    color: #666;
    line-height: 1.1;
    margin-top: 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.gg-header::after, .gg-cell::after {
    content: "";
    position: absolute;
    right: -5px;
    top: 0;
    bottom: 0;
    width: 5px;
    background: linear-gradient(to right, rgba(0,0,0,0.1), transparent);
    pointer-events: none;
}
[data-testid="stButton"] button {
    border-color: var(--blue) !important;
    color: var(--blue) !important;
    font-weight: 600 !important;
}
[data-testid="stButton"] button:hover {
    background-color: var(--blue) !important;
    color: white !important;
}

@media (max-width: 1500px) { .block-container { zoom: 0.9; } }
</style>
"""

# ===========================================================
# CSS MODO TELA CHEIA
# ===========================================================
css_fullscreen = """
<style>
    header, section[data-testid="stSidebar"], .topbar, footer { display: none !important; }
    .block-container { max-width: 100vw !important; padding: 0 !important; margin: 0 !important; overflow: hidden !important; }
    .map-wrapper { position: fixed !important; top: 0; left: 0; width: 100vw !important; height: 100vh !important; z-index: 9999; border: none !important; border-top: 5px solid var(--blue) !important; margin: 0 !important; border-radius: 0 !important; }
    #fixed-exit-container { position: fixed !important; bottom: 30px !important; right: 30px !important; z-index: 100000 !important; }
    #fixed-exit-container button { background-color: var(--red) !important; color: white !important; border: none !important; box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important; padding: 12px 25px !important; font-weight: 800 !important; border-radius: 30px !important; }
    #fixed-exit-container button:hover { background-color: #c82333 !important; transform: scale(1.05); }
</style>
"""
st.markdown(css_base, unsafe_allow_html=True)
if st.session_state.fullscreen: st.markdown(css_fullscreen, unsafe_allow_html=True)

# ===========================================================
# 4. FUNÇÕES DE CACHE E UTILITÁRIOS
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

# NOVO HEADER PADRÃO (Ícone correto e estrutura padronizada)
st.markdown("""
<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/job%20map%20globe%20location.png" alt="icon">
  Mapeamento de Cargos (Job Map)
</div>
""", unsafe_allow_html=True)


preferred_order = ["Top Executive/General Management", "Corporate Affairs/Communications", "Legal & Internal Audit", "Finance", "IT", "People & Culture", "Sales", "Marketing", "Technical Services", "Research & Development", "Technical Engineering", "Operations", "Supply Chain & Logistics", "Quality Management", "Facility & Administrative Services"]
existing_families = set(df["Job Family"].unique())
families_order = [f for f in preferred_order if f in existing_families] + sorted(list(existing_families - set(preferred_order)))

if not st.session_state.fullscreen:
    # RESTAURADO: topbar para dar o fundo cinza claro e o espaçamento correto
    st.markdown("<div class='topbar'>", unsafe_allow_html=True) 
    c1, c2, c3 = st.columns([2, 2, 0.8])
    with c1: fam_filter = st.selectbox("Família", ["Todas"] + families_order)
    paths = df["Career Path"].unique().tolist() if fam_filter == "Todas" else df[df["Job Family"] == fam_filter]["Career Path"].unique().tolist()
    with c2: path_filter = st.selectbox("Trilha", ["Todas"] + sorted([p for p in paths if pd.notna(p) and p != 'nan' and p != '']))
    with c3:
        st.write("")
        st.markdown('<div style="margin-top: 15px;">', unsafe_allow_html=True) # Valor de margin-top ajustado para alinhamento
        if st.button("⛶ Tela Cheia", use_container_width=True): toggle_fullscreen(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True) # FECHA A TOPBAR
else:
    # Lógica de tela cheia
    fam_filter, path_filter = st.session_state.get('fam_filter', 'Todas'), st.session_state.get('path_filter', 'Todas')
    st.markdown('<div id="fixed-exit-container">', unsafe_allow_html=True)
    if st.button("❌ Sair"): toggle_fullscreen(); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    components.html("<script>document.addEventListener('keydown', (e) => { if (e.key === 'Escape') window.parent.document.querySelector('#fixed-exit-container button').click(); });</script>", height=0, width=0)

st.session_state.fam_filter, st.session_state.path_filter = fam_filter, path_filter
df_filtered = df.copy()
if fam_filter != "Todas": df_filtered = df_filtered[df_filtered["Job Family"] == fam_filter]
if path_filter != "Todas": df_filtered = df_filtered[df_filtered["Career Path"] == path_filter]

# Renderiza o mapa otimizado
st.markdown(generate_map_html(df_filtered, families_order), unsafe_allow_html=True)
