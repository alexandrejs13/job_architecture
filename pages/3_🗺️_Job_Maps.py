import streamlit as st
import pandas as pd
from utils.data_loader import load_excel_data
from utils.ui_components import section, lock_sidebar

st.set_page_config(layout="wide", page_title="🗺️ Job Map")
lock_sidebar()

# =================== CSS ===================
st.markdown("""
<style>
.block-container {
  max-width: 1700px !important;
  min-width: 1200px !important;
  margin: 0 auto !important;
  padding-top: 0 !important;
}
.top-fixed {
  position: sticky;
  top: 0;
  z-index: 120;
  background: #fff;
  padding: 14px 0 10px 0;
  border-bottom: 1px solid #e6e6e6;
}
h1.app-title {
  color: #145efc !important;
  font-weight: 800 !important;
  font-size: 1.8rem !important;
  margin: 0 !important;
  display:flex; align-items:center; gap:8px;
}

/* ===== MAP WRAPPER ===== */
.map-wrapper {
  overflow-x: auto;
  overflow-y: auto;
  border-top: 3px solid #145efc;
  border-bottom: 3px solid #145efc;
  background: #fff;
  white-space: nowrap;
  padding: 10px;
}

/* ===== GRID BASE ===== */
.jobmap-grid {
  display: grid;
  grid-auto-rows: auto;
  align-items: stretch;
  font-size: 0.95rem;
  width: max-content;
  position: relative;
  border-collapse: collapse;
}
.jobmap-grid > div {
  border: 1px solid rgba(0,0,0,0.07);
  box-sizing: border-box;
}

/* ===== GG HEADER (MESCLADO) ===== */
.grade-header {
  background: #000;
  color: #fff;
  font-weight: 800;
  display:flex;
  align-items:center;
  justify-content:center;
  padding: 16px 12px;
  grid-row: 1 / span 2; /* ocupa as duas linhas */
  position: sticky;
  left: 0;
  top: 0;
  z-index: 160;
  border-right: 2px solid #fff;
}

/* ===== FAMILY ===== */
.header-family {
  color: #fff;
  font-weight: 800;
  padding: 12px 10px;
  text-align:center;
  position: sticky;
  top: 0;
  z-index: 140;
  white-space: normal;
  border-right: 1px solid rgba(255,255,255,0.6);
}

/* ===== SUBFAMILY ===== */
.header-subfamily {
  padding: 10px 8px;
  font-weight: 700;
  text-align:center;
  white-space: normal;
  position: sticky;
  top: 52px;
  z-index: 135;
  border-right: 1px solid rgba(255,255,255,0.6);
  border-top: none !important; /* remove linha branca entre family/subfamily */
}

/* ===== PRIMEIRA COLUNA (GG) ===== */
.grade-cell {
  background: #000;
  color: #fff;
  font-weight: 700;
  padding: 12px 10px;
  display:flex; align-items:center; justify-content:center;
  position: sticky;
  left: 0;
  z-index: 120;
  border-right: 1px solid rgba(255,255,255,0.6);
}

/* ===== CELULAS ===== */
.job-cell {
  padding: 6px 8px;
  text-align: left;
  vertical-align: top;
  background: #fff;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

/* ===== CARDS ===== */
.job-card {
  background: #f9f9f9;
  border-left: 4px solid #145efc;
  border-radius: 6px;
  padding: 6px 8px;
  margin: 5px 0;
  text-align: left;
  font-size: 0.8rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  word-wrap: break-word;
  overflow-wrap: break-word;
  min-height: 62px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  line-height: 1.25;
}
.job-card b {
  display: block;
  font-weight: 700;
  margin-bottom: 3px;
  white-space: normal !important;
  overflow-wrap: break-word !important;
  word-break: break-word !important;
}
.job-card span {
  display: block;
  font-size: 0.74rem;
  color: #555;
}
.job-card:hover {
  background: #eef3ff;
  transform: translateY(-1px);
  transition: all 0.15s ease-in-out;
}

/* ===== ZEBRA ===== */
.grade-row:nth-of-type(even) .job-cell { background: #fcfcfd; }

/* ===== RESPONSIVIDADE ===== */
@media (max-width: 1500px) { .block-container { zoom: 0.9; } }
@media (max-width: 1200px) { .block-container { zoom: 0.8; } }
</style>
""", unsafe_allow_html=True)

# =================== DADOS ===================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

required_cols = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade", "Full Job Code"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes no Excel: {', '.join(missing)}")
    st.stop()

df = df.dropna(subset=["Job Family", "Sub Job Family", "Job Profile", "Global Grade"])
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\\.0$", "", regex=True)

families = sorted(df["Job Family"].unique().tolist())
palette_dark = ["#4B6FA3", "#7A5A8A", "#A46C49", "#5E7A85", "#6D8066", "#6B8899", "#9B6F94", "#A07D5F", "#6F7F8F", "#7C6F85"]
palette_light = ["#e9eef8", "#f3ebf2", "#f7efe6", "#eef3f6", "#eef4eb", "#edf4f7", "#fbf0f7", "#f7f4ea", "#eef2f4", "#f3eff6"]
fam_colors_dark = {f: palette_dark[i % len(palette_dark)] for i, f in enumerate(families)}
fam_colors_light = {f: palette_light[i % len(palette_light)] for i, f in enumerate(families)}

subfam_map = {f: sorted(df[df["Job Family"] == f]["Sub Job Family"].unique().tolist()) for f in families}
grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x) if str(x).isdigit() else x, reverse=True)

def col_width_for(subfamily_df):
    if subfamily_df.empty:
        return 180
    max_len = subfamily_df["Job Profile"].astype(str).map(len).max()
    px_per_char = 8
    width = max(160, min(460, int(max_len * px_per_char + 60)))
    return width

col_widths = [140]
for f in families:
    for sf in subfam_map[f]:
        subdf = df[(df["Job Family"] == f) & (df["Sub Job Family"] == sf)]
        col_widths.append(col_width_for(subdf))
grid_template = "grid-template-columns: " + " ".join(f"{w}px" for w in col_widths) + ";"

# =================== HTML ===================
html = "<div class='map-wrapper'>"

# Linha mesclada GG + Family
html += f"<div class='jobmap-grid' style='{grid_template}'>"
html += "<div class='grade-header'>GG</div>"
for f in families:
    span = len(subfam_map[f])
    color = fam_colors_dark[f]
    html += f"<div class='header-family' style='grid-column: span {span}; background:{color};'>{f}</div>"
html += "</div>"

# Subfamilies (sem linha branca)
html += f"<div class='jobmap-grid' style='{grid_template}'>"
html += ""  # sem célula antes
for f in families:
    for sf in subfam_map[f]:
        color = fam_colors_light[f]
        html += f"<div class='header-subfamily' style='background:{color};'>{sf}</div>"
html += "</div>"

# Demais linhas (GG)
for g in grades:
    html += f"<div class='jobmap-grid grade-row' style='{grid_template}'>"
    html += f"<div class='grade-cell'>GG {g}</div>"
    for f in families:
        for sf in subfam_map[f]:
            cell_df = df[(df["Job Family"] == f) & (df["Sub Job Family"] == sf) & (df["Global Grade"] == g)]
            if not cell_df.empty:
                cards = "".join(
                    f"<div class='job-card'><b>{r['Job Profile']}</b><span>{r['Career Path']}</span></div>"
                    for _, r in cell_df.iterrows()
                )
                html += f"<div class='job-cell'>{cards}</div>"
            else:
                html += "<div class='job-cell'></div>"
    html += "</div>"

html += "</div>"
st.markdown(html, unsafe_allow_html=True)
