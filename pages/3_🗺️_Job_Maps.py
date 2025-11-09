# pages/3_🗺️_Job_Maps.py
import streamlit as st
import pandas as pd
import math
from utils.data_loader import load_excel_data
from utils.ui_components import section, lock_sidebar

# -----------------------------------------------------------
# Config
# -----------------------------------------------------------
st.set_page_config(layout="wide", page_title="🗺️ Job Map")
lock_sidebar()

# Top fixed title + filters
st.markdown("""
<style>
.block-container { max-width: 1700px !important; min-width: 1200px !important; margin: 0 auto !important; padding-top: 0 !important; }

/* top bar */
.top-fixed { position: sticky; top: 0; z-index: 120; background: #fff; padding: 14px 0 10px 0; border-bottom: 1px solid #e6e6e6; }
.top-fixed .stSelectbox, .top-fixed .stMultiselect { margin-top: 6px; }
h1.app-title { color: #145efc !important; font-weight: 800 !important; font-size: 1.8rem !important; margin: 0 !important; display:flex; align-items:center; gap:8px; }

/* main map wrapper */
.map-wrapper {
  overflow-x: auto;
  overflow-y: auto;
  border-top: 3px solid #145efc;
  border-bottom: 3px solid #145efc;
  background: #fff;
  white-space: nowrap;
  padding: 12px;
}

/* jobmap-grid base - each row is a grid with the same template columns */
.jobmap-grid {
  display: grid;
  grid-auto-rows: auto;
  align-items: stretch;
  font-size: 0.95rem;
  width: max-content;
  position: relative;
  gap: 0;
}

/* neutral cell */
.cell {
  box-sizing: border-box;
  border: 1px solid rgba(0,0,0,0.04);
  background: transparent;
  padding: 0;
}

/* GG header (mesclado verticalmente: A1+A2) */
.grade-header {
  background: #000;
  color: #fff;
  font-weight: 800;
  display:flex;
  align-items:center;
  justify-content:center;
  padding: 18px 12px;
  grid-row: 1 / span 2; /* mescla visual A1 + A2 */
  position: sticky;
  left: 0;
  top: 0;
  z-index: 160;
  border-right: 2px solid #fff;
}

/* sticky header family (linha 1) */
.header-family {
  color: #fff;
  font-weight: 800;
  padding: 14px 12px;
  display:flex;
  align-items:center;
  justify-content:center;
  text-align:center;
  white-space:normal;
  border-right: 1px solid rgba(255,255,255,0.6);
  position: sticky;
  top: 0;
  z-index: 140;
  box-shadow: 0 1px 0 rgba(0,0,0,0.03);
}

/* sticky subfamily (linha 2) */
.header-subfamily {
  padding: 12px 10px;
  font-weight: 700;
  display:flex;
  align-items:center;
  justify-content:center;
  text-align:center;
  white-space:normal;
  position: sticky;
  top: 56px; /* abaixo da family */
  z-index: 135;
  border-right: 1px solid rgba(255,255,255,0.6);
  background: transparent;
}

/* grade cell labels (GG 20, GG 19...) - sticky left first column */
.grade-cell {
  background: #000;
  color: #fff;
  font-weight: 700;
  padding: 18px 12px;
  display:flex; align-items:center; justify-content:center;
  position: sticky;
  left: 0;
  z-index: 120;
  border-right: 1px solid rgba(255,255,255,0.6);
}

/* job cell (where cards live) */
.job-cell {
  padding: 10px 12px;            /* margem interna para os cards não grudarem nas bordas */
  vertical-align: top;
  min-height: 100px;
  box-sizing: border-box;
  background: #fff;
}

/* individual card inside a cell */
.job-card {
  background: #fafafa;
  border-left: 4px solid #145efc;
  border-radius: 8px;
  padding: 10px 12px;
  margin: 6px 0;                /* vertical spacing between cards */
  text-align: left;
  font-size: 0.88rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.06);
  word-wrap: break-word;
  overflow-wrap: break-word;
}
.job-card b { display:block; font-weight:700; margin-bottom:4px; }
.job-card span { display:block; font-size:0.78rem; color:#555; }

/* subtle zebra */
.grade-row:nth-of-type(even) .job-cell { background: #fcfcfd; }

/* small visual separator for header rows to avoid "stuck together" */
.header-family, .header-subfamily { border-bottom: 2px solid #ffffff; }

/* ensure sticky elements overlay correctly when intersecting */
.jobmap-grid .header-family, .jobmap-grid .header-subfamily, .grade-header { box-shadow: inset 0 -1px 0 rgba(255,255,255,0.15); }

/* responsive scaling */
@media (max-width: 1400px) { .block-container { zoom: 0.9; } }
@media (max-width: 1200px) { .block-container { zoom: 0.8; } }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Top fixed title & filters
# -------------------------
st.markdown("<div class='top-fixed'>", unsafe_allow_html=True)
st.markdown('<h1 class="app-title">🗺️ Job Map</h1>', unsafe_allow_html=True)

fcol, pcol = st.columns([2, 2])
with fcol:
    family_filter = st.selectbox("Família", ["Todas"])
with pcol:
    path_filter = st.selectbox("Trilha de Carreira", ["Todas"])
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------
# Load data
# -----------------------------------------------------------
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

required_cols = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade", "Full Job Code"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes no Excel: {', '.join(missing)}")
    st.stop()

# normalize and filter
df = df.dropna(subset=["Job Family", "Sub Job Family", "Job Profile", "Global Grade"])
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\\.0$", "", regex=True)

if family_filter != "Todas":
    df = df[df["Job Family"] == family_filter]
if path_filter != "Todas":
    df = df[df["Career Path"] == path_filter]

if df.empty:
    st.warning("Nenhum cargo encontrado com os filtros selecionados.")
    st.stop()

# -----------------------------------------------------------
# Paleta (harmônica) - dark & light per family
# -----------------------------------------------------------
families = sorted(df["Job Family"].unique().tolist())
palette_dark = [
    "#4B6FA3", "#7A5A8A", "#A46C49", "#5E7A85", "#6D8066", "#6B8899",
    "#9B6F94", "#A07D5F", "#6F7F8F", "#7C6F85"
]
palette_light = [
    "#e9eef8", "#f3ebf2", "#f7efe6", "#eef3f6", "#eef4eb", "#edf4f7",
    "#fbf0f7", "#f7f4ea", "#eef2f4", "#f3eff6"
]
fam_colors_dark = {f: palette_dark[i % len(palette_dark)] for i, f in enumerate(families)}
fam_colors_light = {f: palette_light[i % len(palette_light)] for i, f in enumerate(families)}

# -----------------------------------------------------------
# grouping and dynamic width calculation by column
# -----------------------------------------------------------
subfam_map = {f: sorted(df[df["Job Family"] == f]["Sub Job Family"].unique().tolist()) for f in families}
grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x) if str(x).isdigit() else x, reverse=True)

# compute width per subfamily column based on longest job profile length in that subfamily
# heuristic: chars * px_per_char (approx 9) + padding, bounded min/max
def col_width_for(subfamily_df):
    if subfamily_df.empty:
        return 180
    max_len = subfamily_df["Job Profile"].astype(str).map(len).max()
    # px per char heuristic; tune if needed
    px_per_char = 9
    width = max(160, min(520, int(max_len * px_per_char + 80)))
    return width

col_widths = []
# first column fixed for GG
col_widths.append(140)
for f in families:
    for sf in subfam_map[f]:
        subdf = df[(df["Job Family"] == f) & (df["Sub Job Family"] == sf)]
        col_widths.append(col_width_for(subdf))

# create grid-template string matching computed widths (first column GG fixed + each subfam width)
grid_template = "grid-template-columns: " + " ".join(f"{w}px" for w in col_widths) + ";"

# -----------------------------------------------------------
# Build HTML grid
# -----------------------------------------------------------
html = "<div class='map-wrapper'>"

# LINE 1 -> Family headers (sticky top)
html += f"<div class='jobmap-grid' style='{grid_template}'>"
html += "<div class='grade-header'>GG</div>"  # this spans 2 rows visually via CSS
for f in families:
    span = len(subfam_map[f])
    color = fam_colors_dark[f]
    # span columns for family header
    html += f"<div class='cell header-family' style='grid-column: span {span}; background:{color};'>{f}</div>"
html += "</div>"

# LINE 2 -> Subfamily headers (sticky just below family)
html += f"<div class='jobmap-grid' style='{grid_template}'>"
html += "<div class='cell' style='background:transparent;'></div>"
for f in families:
    for sf in subfam_map[f]:
        color = fam_colors_light[f]
        html += f"<div class='cell header-subfamily' style='background:{color};'>{sf}</div>"
html += "</div>"

# Subsequent lines: for each grade, a grid row with first column GG label + each subfamily cell
for g in grades:
    html += f"<div class='jobmap-grid grade-row' style='{grid_template}'>"
    html += f"<div class='cell grade-cell'>GG {g}</div>"
    for f in families:
        for sf in subfam_map[f]:
            cell_df = df[(df["Job Family"] == f) & (df["Sub Job Family"] == sf) & (df["Global Grade"] == g)]
            if not cell_df.empty:
                cards = "".join(
                    f"<div class='job-card'><b>{row['Job Profile']}</b><span>{row['Career Path']}</span></div>"
                    for _, row in cell_df.iterrows()
                )
                html += f"<div class='cell job-cell'>{cards}</div>"
            else:
                html += "<div class='cell job-cell'></div>"
    html += "</div>"

html += "</div>"
st.markdown(html, unsafe_allow_html=True)
