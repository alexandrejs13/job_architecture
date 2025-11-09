# pages/3_🗺️_Job_Maps.py
# -*- coding: utf-8 -*-

import math
import re
import streamlit as st
import pandas as pd

from utils.data_loader import load_excel_data
from utils.ui_components import section, lock_sidebar

# ===========================================================
# 1) PAGE CONFIG — precisa ser a 1ª chamada do Streamlit
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")
lock_sidebar()  # sidebar travada

# ===========================================================
# 2) CSS — layout, congelamentos, paleta e grid
# ===========================================================
TOPBAR_H = 88           # altura área “título + filtros” (px)
HDR_ROW1_H = 44         # altura linha 1 (Família)
HDR_ROW2_H = 56         # altura linha 2 (Subfamília)
COL_A_W   = 168         # largura fixa da coluna GG (px)

st.markdown(f"""
<style>
:root {{
  --topbar-h: {TOPBAR_H}px;
  --hdr1-h:   {HDR_ROW1_H}px;
  --hdr2-h:   {HDR_ROW2_H}px;
  --colA-w:   {COL_A_W}px;
  --grid-border: #E5E7EB;       /* cinza suave para grade geral */
  --grid-border-strong: #FFFFFF;/* branco (coluna A)           */
  --blue-sky: #145EFC;          /* referência SIG Sky           */
}}

.block-container {{
  max-width: 1720px !important;
  min-width: 1420px !important;
  margin: 0 auto !important;
  padding-top: 0 !important;
}}

.top-fixed {{
  position: sticky;
  top: 0;
  z-index: 100;
  background: #fff;
  padding: 16px 0 12px 0;
  border-bottom: 2px solid var(--grid-border);
}}

h1 {{
  color: var(--blue-sky) !important;
  font-weight: 900 !important;
  font-size: 1.9rem !important;
  margin: 0 0 8px 0 !important;
  display: flex; align-items:center; gap:8px;
}}

/* ====== WRAPPER SCROLL ====== */
.map-wrapper {{
  overflow: auto;
  border-top: 3px solid var(--blue-sky);
  border-bottom: 3px solid var(--blue-sky);
  background: #fff;
  white-space: nowrap;
}}

/* ====== GRID BASE ====== */
.jm-grid {{
  display: grid;
  border-collapse: collapse;
  width: max-content;
  position: relative;
  font-size: 0.94rem;
}}
.jm-grid > div {{
  border-right: 1px solid var(--grid-border);
  border-bottom: 1px solid var(--grid-border);
  box-sizing: border-box;
}}

/* ====== COLUNA GG (preta) ====== */
.gg-sticky {{
  position: sticky;
  left: 0;
  z-index: 60 !important;
  background: #000;
  color: #fff;
  width: var(--colA-w);
  display: flex; align-items:center; justify-content:center;
  font-weight: 800;
}}
.gg-sticky.border-white {{
  border-right: 1px solid var(--grid-border-strong) !important;
}}
.gg-sticky .gg-label {{ letter-spacing: .5px; }}

/* GG cabeçalho (A1+A2 mescladas) */
.gg-header {{
  grid-row: 1 / span 2;
  position: sticky;
  top: calc(var(--topbar-h));
  height: calc(var(--hdr1-h) + var(--hdr2-h));
  border-bottom: 1px solid var(--grid-border-strong) !important;
}}
/* GG linhas */
.gg-row {{
  height: 64px;  /* base; as linhas do corpo têm altura fluida por conta dos cards */
}}

/* ====== CABEÇALHOS (família, subfamília) ====== */
.hdr-family {{
  position: sticky;
  top: calc(var(--topbar-h));
  height: var(--hdr1-h);
  z-index: 55 !important;
  display:flex; align-items:center; justify-content:center;
  font-weight: 800; color:#fff;
  border-bottom: 1px solid #FFFFFF !important;   /* divisor branco entre linha 1 e 2 */
  padding: 0 10px;
  white-space: normal; text-align:center; line-height:1.2;
}}
.hdr-subfamily {{
  position: sticky;
  top: calc(var(--topbar-h) + var(--hdr1-h));
  height: var(--hdr2-h);
  z-index: 54 !important;
  background: #F3F4F8;
  display:flex; align-items:center; justify-content:center;
  font-weight: 700; color:#333;
  padding: 0 10px;
  white-space: normal; text-align:center; line-height:1.25;
  border-top: 1px solid #FFFFFF !important;      /* gruda sem linha “fantasma” */
}}

/* bordas verticais fortes para separar famílias (linha branca pedida) */
.family-divider {{
  box-shadow: inset -2px 0 0 0 #FFFFFF;
}}

/* ====== CÉLULAS DO CORPO ====== */
.cell {{
  padding: 8px 8px;  /* margem interna para não “grudar” nas bordas */
  min-height: 64px;
}}
.job-card {{
  background: #FAFAFA;
  border-left: 4px solid var(--blue-sky);
  border-radius: 8px;
  padding: 8px 10px;
  margin: 6px 4px;         /* espaçamento vertical e lateral entre cards */
  text-align: left;
  font-size: 0.92rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.06);
  word-wrap: break-word;
  overflow-wrap: break-word;
}}
.job-card b {{
  display:block; font-weight:800;
  margin-bottom: 2px;
}}
.job-card span {{
  display:block; font-size:0.82rem; color:#555;
}}
.job-card:hover {{ background:#EEF3FF; }}

/* ====== GRADE (linhas) ====== */
.body-row:nth-child(even) > .cell {{ background: #FCFCFC; }}

/* responsividade leve */
@media (max-width: 1500px) {{ .block-container {{ zoom: .92; }} }}
@media (max-width: 1220px) {{ .block-container {{ zoom: .84; }} }}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# 3) Dados (Excel) e filtros
# ===========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

req = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade", "Full Job Code"]
missing = [c for c in req if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes no Excel: {', '.join(missing)}")
    st.stop()

# Normalização básica
df = df.dropna(subset=["Job Family", "Sub Job Family", "Job Profile", "Global Grade"])
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True)

# Top fixo (título + filtros)
st.markdown("<div class='top-fixed'>", unsafe_allow_html=True)
section("🗺️ Job Map")

colf, colp = st.columns([2, 2])

families_all = ["Todas"] + sorted(df["Job Family"].dropna().unique().tolist())
paths_all    = ["Todas"] + sorted(df["Career Path"].dropna().unique().tolist())

with colf:
    family_filter = st.selectbox("Família", families_all)
with colp:
    path_filter   = st.selectbox("Trilha de Carreira", paths_all)

st.markdown("</div>", unsafe_allow_html=True)

# Aplicar filtros
filtered = df.copy()
if family_filter != "Todas":
    filtered = filtered[filtered["Job Family"] == family_filter]
if path_filter != "Todas":
    filtered = filtered[filtered["Career Path"] == path_filter]

if filtered.empty:
    st.warning("Nenhum cargo encontrado com os filtros.")
    st.stop()

# ===========================================================
# 4) Organização: famílias, subfamílias, grades
# ===========================================================
families = sorted(filtered["Job Family"].unique().tolist())

# Paleta elegante (família=escuro; subfamília=claro)
palette_dark = [
    "#4D5F8C", "#63727E", "#6C7C6A", "#736C8A", "#8A735D",
    "#5E7D99", "#7A6E90", "#6F7D58", "#7C6D6D", "#5E6E7F"
]
palette_light = [
    "#E6EAF4", "#EDF0F3", "#EEF2EC", "#F0EDF4", "#F4EFE9",
    "#E9F0F6", "#F2EEF7", "#EEF3E9", "#F3EEEE", "#EAF0F4"
]
fam_color_dark  = {f: palette_dark[i % len(palette_dark)]  for i, f in enumerate(families)}
fam_color_light = {f: palette_light[i % len(palette_light)] for i, f in enumerate(families)}

# Subfamílias por família
subfam_map = {f: sorted(filtered[filtered["Job Family"] == f]["Sub Job Family"].unique().tolist())
              for f in families}

# Grades (linhas) em ordem decrescente
grades = sorted(filtered["Global Grade"].unique(),
                key=lambda x: int(x) if re.fullmatch(r"\d+", x) else 999, reverse=True)

# ===========================================================
# 5) Cálculo automático de largura por coluna (Subfamily)
#    Medimos por caracteres para estimar “px” e aplicamos limites.
# ===========================================================
def est_px_from_text(text: str, base=9.2, pad=48):
    """estimativa simples px; base≈px por caractere; pad=padding/bordas"""
    return int(min(max(len(text) * base + pad, 180), 380))

col_widths = []  # list px somente para as subfamilias (na mesma ordem de families/subfam_map)

for fam in families:
    for sf in subfam_map[fam]:
        # maior entre o nome da subfamily e os Job Profiles daquela coluna
        col_df = filtered[(filtered["Job Family"] == fam) & (filtered["Sub Job Family"] == sf)]
        texts  = [sf] + col_df["Job Profile"].astype(str).tolist()
        target = max(texts, key=lambda t: len(str(t)))
        col_widths.append(est_px_from_text(str(target)))

# Template de colunas do grid (coluna A fixa + subfamilias variáveis)
grid_cols_px = ["var(--colA-w)"] + [f"{w}px" for w in col_widths]
grid_template_cols = "grid-template-columns: " + " ".join(grid_cols_px) + ";"

# Quantas colunas totais (1 GG + subfamilias)
n_cols_total = 1 + len(col_widths)

# ===========================================================
# 6) Renderização HTML
#    Construímos um único grid com 2 linhas fixas (fam/subfam)
#    e N linhas do corpo, repetindo a matriz.
#    GG cabeçalho ocupa row 1-2 (mesclado).
# ===========================================================
html = []
html.append("<div class='map-wrapper'>")

# Cabeçalho: duas linhas “engessadas” + corpo
html.append(f"<div class='jm-grid' style='{grid_template_cols}'>")

# A1+A2: GG (mesclado)
html.append(
    "<div class='gg-sticky gg-header border-white'>"
    "<div class='gg-label'>GG</div></div>"
)

# Linha 1 — Famílias
for fam in families:
    span = len(subfam_map[fam])  # células que essa família cobre
    color = fam_color_dark[fam]
    html.append(
        f"<div class='hdr-family family-divider' "
        f"style='grid-column: span {span}; background:{color}; color:#fff;'>"
        f"{fam}</div>"
    )

# Linha 2 — Subfamílias
# (uma célula dummy NÃO é necessária; GG já ocupa row=1..2)
for fam in families:
    for sf in subfam_map[fam]:
        color = fam_color_light[fam]
        html.append(
            f"<div class='hdr-subfamily family-divider' "
            f"style='background:{color};'>{sf}</div>"
        )

# Corpo (linhas por GG)
for g in grades:
    # Coluna A — GG
    html.append(f"<div class='gg-sticky gg-row border-white'><div class='gg-label'>GG {g}</div></div>")

    # Células por subfamília
    for fam in families:
        fam_df = filtered[filtered["Job Family"] == fam]
        for sf in subfam_map[fam]:
            cell_df = fam_df[(fam_df["Sub Job Family"] == sf) & (fam_df["Global Grade"] == g)]
            if cell_df.empty:
                html.append("<div class='cell'></div>")
            else:
                # cards (tamanho padrão, quebra automática)
                cards = []
                for _, r in cell_df.iterrows():
                    title = str(r["Job Profile"]).strip()
                    path  = str(r["Career Path"]).strip()
                    cards.append(
                        f"<div class='job-card'><b>{title}</b><span>{path}</span></div>"
                    )
                html.append("<div class='cell'>" + "".join(cards) + "</div>")

# fecha grid+wrapper
html.append("</div>")
html.append("</div>")

st.markdown("".join(html), unsafe_allow_html=True)
