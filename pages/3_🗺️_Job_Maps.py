# -*- coding: utf-8 -*-
# pages/3_🗺️_Job_Maps.py

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from utils.data_loader import load_excel_data
from utils.ui_components import section, lock_sidebar

# ===========================================================
# CONFIGURAÇÃO DE PÁGINA E ESTADO
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")
lock_sidebar()

if 'fullscreen' not in st.session_state:
    st.session_state.fullscreen = False

def toggle_fullscreen():
    st.session_state.fullscreen = not st.session_state.fullscreen

# ===========================================================
# CSS BASE
# ===========================================================
css_base = """
<style>
:root {
  --blue: #145efc;    /* Management/Executive */
  --green: #28a745;   /* Professional/Specialist */
  --orange: #fd7e14;  /* Technical/Support */
  --purple: #6f42c1;  /* Outros */
  --red: #dc3545;     /* Vermelho para botões de ação */
  --gray-line: #dadada;
  --gray-bg: #f8f9fa;
  --dark-gray: #333333;
}

.block-container {
  max-width: 1600px !important;
  margin: auto !important;
  padding: 2rem 5rem !important;
}

/* Topbar apenas para os filtros */
.topbar {
  position: sticky;
  top: 0;
  z-index: 200;
  background: white;
  padding: 15px 0 15px 0;
  border-bottom: 2px solid var(--blue);
  margin-bottom: 20px;
}

/* Título sem linhas acima */
h1 {
  color: var(--blue);
  font-weight: 900 !important;
  font-size: 1.9rem !important;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 0px !important;
  margin-bottom: 10px !important;
  padding-top: 0px !important;
}

.map-wrapper {
  height: 75vh;
  overflow: auto;
  border-top: 3px solid var(--blue);
  border-bottom: 3px solid var(--blue);
  background: white;
  position: relative;
  will-change: transform;
  box-shadow: 0 0 15px rgba(0,0,0,0.05);
}

.jobmap-grid {
  display: grid;
  border-collapse: collapse;
  width: max-content;
  font-size: 0.88rem;
  /* Alturas fixas para cabeçalhos e linhas de conteúdo */
  grid-template-rows: 50px 45px repeat(auto-fill, 110px) !important;
  grid-auto-rows: 110px !important;
  align-content: start !important;
  row-gap: 0px !important;
  column-gap: 0px !important;
  background-color: white !important;
}

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
}

.gg-header {
  background: #000 !important;
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
  background: #000 !important;
  color: white;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  position: sticky;
  left: 0;
  z-index: 55;
  border-right: 2px solid white !important;
  border-top: 1px solid white !important;
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
  background: #f9f9f9;
  /* Borda base, a cor será injetada pelo Python */
  border-left-width: 5px !important;
  border-left-style: solid !important;
  border-radius: 6px;
  padding: 6px 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
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
  transform: translateY(-2px);
  box-shadow: 0 5px 10px rgba(0,0,0,0.15);
}
.job-card b {
  display: block;
  font-weight: 700;
  margin-bottom: 3px;
  line-height: 1.15;
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
  background: linear-gradient(to right, rgba(0,0,0,0.15), transparent);
  pointer-events: none;
}

/* Estilo para o botão "Tela Cheia" no modo normal (VERMELHO) */
/* Seletor simplificado para maior robustez */
button[data-testid*="stButton"] > div > p { /* Streamlit 1.30+ usa <p> dentro do botão para o texto */
    color: white !important;
    background-color: var(--red) !important;
    border-color: var(--red) !important;
    font-weight: 600 !important;
}
button[data-testid*="stButton"] > div > p:hover {
    background-color: #c82333 !important; /* Um tom mais escuro ao passar o mouse */
    border-color: #bd2130 !important;
}
/* Estiliza o próprio botão para ter borda e cor de fundo consistentes */
button[data-testid*="stButton"] {
    background-color: var(--red) !important;
    border-color: var(--red) !important;
}
button[data-testid*="stButton"]:hover {
    background-color: #c82333 !important; 
    border-color: #bd2130 !important;
}


@media (max-width: 1500px) { .block-container { zoom: 0.9; } }
</style>
"""

# ===========================================================
# CSS MODO TELA CHEIA (COM BOTÃO DE SAIR FIXO E MARGENS)
# ===========================================================
css_fullscreen = """
<style>
    /* Esconde elementos padrão */
    header[data-testid="stHeader"], 
    section[data-testid="stSidebar"],
    .topbar, 
    footer { display: none !important; }

    /* Maximiza o container principal */
    .block-container {
        max-width: 100vw !important;
        padding: 0 !important;
        margin: 0 !important;
        overflow: hidden !important;
    }

    /* Força o mapa a ocupar 100% da tela */
    .map-wrapper {
        position: fixed !important;
        top: 0;
        left: 0;
        width: 100vw !important;
        height: 100vh !important;
        z-index: 9999;
        border: none !important;
        border-top: 5px solid var(--blue) !important;
        margin: 0 !important;
    }

    /* Estilo para o container do botão de sair - com margens flutuantes (CORRIGIDO) */
    div[data-testid="stVerticalBlock"] > div:has(button[kind="primary"]) {
        position: fixed !important; /* Reforça fixed */
        bottom: 1cm !important;     /* Margem de 1cm inferior */
        right: 1cm !important;      /* Margem de 1cm direita */
        left: unset !important;     /* Garante que não está preso à esquerda */
        z-index: 100000 !important; /* Garante que está no topo */
        background: transparent !important;
    }
    
    /* Estilo específico para o botão de sair */
    button[kind="primary"] {
        background-color: var(--red) !important;
        color: white !important;
        border-color: var(--red) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        font-weight: 800 !important;
        padding: 0.5rem 1.5rem !important;
    }
    button[kind="primary"]:hover {
        background-color: #c82333 !important; /* Um tom mais escuro ao passar o mouse */
        border-color: #bd2130 !important;
    }
</style>
"""

st.markdown(css_base, unsafe_allow_html=True)
if st.session_state.fullscreen:
    st.markdown(css_fullscreen, unsafe_allow_html=True)

# ===========================================================
# DADOS
# ===========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

required = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes: {', '.join(missing)}")
    st.stop()

for col in required:
    df[col] = df[col].astype(str).str.strip()

df["Sub Job Family"] = df["Sub Job Family"].replace(['nan', 'None', '', '<NA>'], '-')
df = df[~df["Job Family"].isin(['nan', 'None', ''])]
df = df[~df["Job Profile"].isin(['nan', 'None', ''])]
df = df[~df["Global Grade"].isin(['nan', 'None', ''])]
df["Global Grade"] = df["Global Grade"].str.replace(r"\.0$", "", regex=True)

# ===========================================================
# FILTROS E CONTROLES
# ===========================================================
section("🗺️ Job Map")

if not st.session_state.fullscreen:
    st.markdown("<div class='topbar'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 0.8])

    preferred_order = [
        "Top Executive/General Management", "Corporate Affairs/Communications", "Legal & Internal Audit",
        "Finance", "IT", "People & Culture", "Sales", "Marketing", "Technical Services",
        "Research & Development", "Technical Engineering", "Operations", "Supply Chain & Logistics",
        "Quality Management", "Facility & Administrative Services"
    ]
    existing_families = set(df["Job Family"].unique())
    families_order = [f for f in preferred_order if f in existing_families]
    families_order.extend(sorted(list(existing_families - set(families_order))))

    with col1:
        family_filter = st.selectbox("Família", ["Todas"] + families_order)

    if family_filter != "Todas":
        available_paths = df[df["Job Family"] == family_filter]["Career Path"].unique().tolist()
    else:
        available_paths = df["Career Path"].unique().tolist()
    paths_options = ["Todas"] + sorted([p for p in available_paths if pd.notna(p) and p != 'nan' and p != ''])

    with col2:
        path_filter = st.selectbox("Trilha de Carreira", paths_options)

    with col3:
        st.write("")
        # Adicionei um div para ajudar no alinhamento vertical
        st.markdown('<div style="margin-top: 15px;">', unsafe_allow_html=True) 
        if st.button("⛶ Tela Cheia", use_container_width=True):
            toggle_fullscreen()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True) # Fecha o div

    st.markdown("</div>", unsafe_allow_html=True)
    st.session_state.fam_filter = family_filter
    st.session_state.path_filter = path_filter

else:
    family_filter = st.session_state.get('fam_filter', 'Todas')
    path_filter = st.session_state.get('path_filter', 'Todas')
    preferred_order = [
        "Top Executive/General Management", "Corporate Affairs/Communications", "Legal & Internal Audit",
        "Finance", "IT", "People & Culture", "Sales", "Marketing", "Technical Services",
        "Research & Development", "Technical Engineering", "Operations", "Supply Chain & Logistics",
        "Quality Management", "Facility & Administrative Services"
    ]
    existing_families = set(df["Job Family"].unique())
    families_order = [f for f in preferred_order if f in existing_families]
    families_order.extend(sorted(list(existing_families - set(families_order))))

    # Botão de Sair (o CSS agora lida com a posição fixa e as margens)
    if st.button("❌ Sair da Tela Cheia", type="primary"):
        toggle_fullscreen()
        st.rerun()

    components.html(
        """
        <script>
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                const buttons = window.parent.document.getElementsByTagName('button');
                for (let i = 0; i < buttons.length; i++) {
                    // Verifica o texto do botão para garantir que é o botão correto de sair
                    if (buttons[i].innerText.includes("Sair da Tela Cheia")) {
                        buttons[i].click();
                        break;
                    }
                }
            }
        });
        </script>
        """,
        height=0, width=0
    )

# --- APLICAÇÃO DOS FILTROS ---
df_filtered = df.copy()
if family_filter != "Todas":
    df_filtered = df_filtered[df_filtered["Job Family"] == family_filter]
if path_filter != "Todas":
    df_filtered = df_filtered[df_filtered["Career Path"] == path_filter]

if df_filtered.empty:
    st.warning("Nenhum cargo encontrado com os filtros atuais.")
    if st.session_state.fullscreen:
         if st.button("Voltar ao Normal"):
             toggle_fullscreen()
             st.rerun()
    st.stop()

# ===========================================================
# PREPARAÇÃO DO GRID
# ===========================================================
active_families = [f for f in families_order if f in df_filtered["Job Family"].unique()]
grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else 999, reverse=True)

subfamilias_map = {}
col_index = 2
header_spans = {}

for f in active_families:
    subs = sorted(df_filtered[df["Job Family"] == f]["Sub Job Family"].unique().tolist()) # Use df aqui para pegar todas as subfamílias da família, não apenas as filtradas
    header_spans[f] = len(subs)
    for sf in subs:
        subfamilias_map[(f, sf)] = col_index
        col_index += 1

content_map = {}
cards_count_map = {}

for g in grades:
    for (f, sf), c_idx in subfamilias_map.items():
        cell_df = df_filtered[(df_filtered["Job Family"] == f) & (df_filtered["Sub Job Family"] == sf) & (df_filtered["Global Grade"] == g)]
        count = len(cell_df)
        cards_count_map[(g, c_idx)] = count
        if count == 0:
            content_map[(g, c_idx)] = None
            continue
        jobs_sig = "|".join(sorted((cell_df["Job Profile"] + cell_df["Career Path"]).unique()))
        content_map[(g, c_idx)] = jobs_sig

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

# --- FUNÇÃO DE CORES (REINTEGRADA E VERIFICADA) ---
def get_path_color(path_name):
    p_lower = str(path_name).lower().strip()
    if "manage" in p_lower or "executive" in p_lower: return "var(--blue)"
    if "professional" in p_lower or "specialist" in p_lower: return "var(--green)"
    if "techni" in p_lower or "support" in p_lower: return "var(--orange)"
    return "var(--purple)"

cell_html_cache = {}
for i, g in enumerate(grades):
    for (f, sf), c_idx in subfamilias_map.items():
        if (g, c_idx) in skip_set or content_map.get((g, c_idx)) is None: continue
        
        span = span_map.get((g, c_idx), 1)
        if span > 1:
            covered = grades[i : i + span]
            try:
                nums = [int(x) for x in covered if x.isdigit()]
                gg_label = f"GG {min(nums)}-{max(nums)}"
            except:
                gg_label = f"GG {covered[-1]}-{covered[0]}"
        else:
            gg_label = f"GG {g}"

        cell_df = df_filtered[(df_filtered["Job Family"] == f) & (df_filtered["Sub Job Family"] == sf) & (df_filtered["Global Grade"] == g)]
        
        cards = []
        for _, row in cell_df.iterrows():
            path_color = get_path_color(row['Career Path']) # Garante que a cor é obtida
            tooltip = f"{row['Job Profile']} | {row['Career Path']} ({gg_label})"
            # INJEÇÃO DA COR DIRETO NO STYLE
            cards.append(
                f"<div class='job-card' style='border-left-color: {path_color} !important;' title='{tooltip}'>"
                f"<b>{row['Job Profile']}</b>"
                f"<span>{row['Career Path']} - {gg_label}</span>"
                f"</div>"
            )
        cell_html_cache[(g, c_idx)] = "".join(cards)

# ===========================================================
# CÁLCULO DE LARGURAS
# ===========================================================
def largura_texto_minima(text): return len(str(text)) * 5 + 30
col_widths = ["100px"]
for (f, sf), c_idx in subfamilias_map.items():
    width_title = largura_texto_minima(sf)
    max_cards = 0
    for g in grades:
        if (g, c_idx) not in skip_set:
             max_cards = max(max_cards, cards_count_map.get((g, c_idx), 0))
    if max_cards <= 1: width_cards = 135 + 25
    elif max_cards == 2: width_cards = (2 * 135) + 8 + 25
    else:
        cap = min(max(1, max_cards), 6)
        width_cards = (cap * 135) + ((cap - 1) * 8) + 25
    col_widths.append(f"{max(width_title, width_cards)}px")
grid_template = f"grid-template-columns: {' '.join(col_widths)};"

# ===========================================================
# PALETA DE CORES
# ===========================================================
palette_pairs = [
    ("#4F6D7A", "#E6EFF2"), ("#5C7A67", "#E8F2EB"), ("#7A5C5C", "#F2E6E6"),
    ("#6B5C7A", "#EBE6F2"), ("#7A725C", "#F2EFE6"), ("#5C6B7A", "#E6EBF2"),
    ("#7A5C74", "#F2E6EF"), ("#5C7A78", "#E6F2F1"), ("#736A62", "#F0EDEB"),
    ("#626A73", "#EBEDF0"),
]
map_cor_fam = {f: palette_pairs[i % len(palette_pairs)][0] for i, f in enumerate(families_order)}
map_cor_sub = {f: palette_pairs[i % len(palette_pairs)][1] for i, f in enumerate(families_order)}

# ===========================================================
# RENDERIZAÇÃO FINAL
# ===========================================================
html = ["<div class='map-wrapper'><div class='jobmap-grid' style='{grid_template}'>".format(grid_template=grid_template)]
html.append("<div class='gg-header'>GG</div>")

current_col = 2
for f in active_families:
    span = header_spans[f]
    style = f"grid-column: {current_col} / span {span}; background:{map_cor_fam[f]};"
    html.append(f"<div class='header-family' style='{style}'>{f}</div>")
    current_col += span

for (f, sf), c_idx in subfamilias_map.items():
    style = f"grid-column: {c_idx}; background:{map_cor_sub[f]};"
    html.append(f"<div class='header-subfamily' style='{style}'>{sf}</div>")

for i, g in enumerate(grades):
    row_idx = i + 3
    html.append(f"<div class='gg-cell' style='grid-row: {row_idx};'>GG {g}</div>")
    for (f, sf), c_idx in subfamilias_map.items():
        if (g, c_idx) in skip_set: continue
        span = span_map.get((g, c_idx), 1)
        row_str = f"grid-row: {row_idx} / span {span};" if span > 1 else f"grid-row: {row_idx};"
        html.append(f"<div class='cell' style='grid-column: {c_idx}; {row_str}'>{cell_html_cache.get((g, c_idx), '')}</div>")

html.append("</div></div>")
st.markdown("".join(html), unsafe_allow_html=True)
