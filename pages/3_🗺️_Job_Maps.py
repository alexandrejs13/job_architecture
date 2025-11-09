import streamlit as st
import pandas as pd
import random
from utils.data_loader import load_job_map_df, _ensure_columns

st.set_page_config(layout="wide", page_title="🗺️ Job Map")

st.markdown("""
<style>
.block-container { max-width: 1700px !important; min-width: 1700px !important; margin: 0 auto !important; }
h1 { color: #1E56E0 !important; font-weight: 800 !important; font-size: 1.8rem !important; margin-bottom: 1rem !important; }
.map-wrapper { overflow-x: auto; overflow-y: hidden; border-top: 3px solid #1E56E0; border-bottom: 3px solid #1E56E0; background: #fff; padding-bottom: 1rem; white-space: nowrap; }
.jobmap-grid { display: grid; border-collapse: collapse; font-size: 0.85rem; text-align: center; width: max-content; position: relative; z-index: 0; }
.jobmap-grid > div { border: 1px solid #ddd; box-sizing: border-box; }
.header-family { font-weight: 800; color: #fff; padding: 10px; border-right: 2px solid #fff; white-space: normal; font-size: 1rem; display: flex; align-items: center; justify-content: center; text-align: center; }
.header-subfamily { font-weight: 700; background: #f0f2ff; padding: 8px; white-space: normal; font-size: 0.95rem; display: flex; align-items: center; justify-content: center; text-align: center; }
.grade-header { font-weight: 800; font-size: 0.95rem; background: #1E56E0; color: #fff; padding: 8px; border-right: 2px solid #fff; display: flex; align-items: center; justify-content: center; position: sticky; top: 0; left: 0; z-index: 40 !important; }
.grade-cell { font-weight: 700; background: #eef3ff; border-right: 2px solid #1E56E0; padding: 6px 8px; position: sticky; left: 0; z-index: 30 !important; display: flex; align-items: center; justify-content: center; }
.grade-cell::after { content: ""; position: absolute; right: 0; top: 0; height: 100%; width: 2px; background: rgba(0,0,0,0.05); }
.job-card { background: #fafafa; border-left: 4px solid #1E56E0; border-radius: 6px; padding: 5px 8px; margin: 3px 0; text-align: left; font-size: 0.82rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); white-space: normal; }
.job-card span { display: block; font-size: 0.75rem; color: #555; }
.job-card:hover { background: #f0f5ff; }
.grade-row:nth-child(even) { background: #fcfcfc; }
@media (max-width: 1500px) { .block-container { zoom: 0.9; } }
@media (max-width: 1200px) { .block-container { zoom: 0.8; } }
</style>
""", unsafe_allow_html=True)

df = load_job_map_df()

required = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade", "Full Job Code"]
found_map, missing = _ensure_columns(df, required)
if missing:
    st.error(f"Colunas ausentes no Excel: {', '.join(missing)}")
    st.stop()
C = found_map

df = df.dropna(subset=[C["Job Family"], C["Sub Job Family"], C["Job Profile"], C["Global Grade"]]).copy()

# normaliza Global Grade para ordenar corretamente (desc)
def _g(v):
    s = str(v).strip()
    try:
        return int(float(s))
    except:
        return -10
df["_GG_"] = df[C["Global Grade"]].map(_g)

st.markdown("<h1>🗺️ Job Map</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 2])
with col1:
    fam_opts = ["Todas"] + sorted(df[C["Job Family"]].dropna().astype(str).unique().tolist())
    selected_family = st.selectbox("Família", fam_opts)
with col2:
    path_opts = ["Todas"] + sorted(df[C["Career Path"]].dropna().astype(str).unique().tolist())
    selected_path = st.selectbox("Trilha de Carreira", path_opts)

filtered = df.copy()
if selected_family != "Todas":
    filtered = filtered[filtered[C["Job Family"]] == selected_family]
if selected_path != "Todas":
    filtered = filtered[filtered[C["Career Path"]] == selected_path]

if filtered.empty:
    st.warning("Nenhum cargo encontrado com os filtros selecionados.")
    st.stop()

families = sorted(filtered[C["Job Family"]].unique().tolist())

random.seed(10)
palette = ["#1E56E0", "#00796B", "#9C27B0", "#E65100", "#5D4037", "#0288D1", "#558B2F", "#8E24AA", "#F9A825", "#6D4C41", "#0097A7"]
fam_colors = {f: palette[i % len(palette)] for i, f in enumerate(families)}

grades = sorted(filtered["_GG_"].unique(), reverse=True)
# mapeia grade normalizado -> label original mais comum
gg_label = filtered.groupby("_GG_")[C["Global Grade"]].agg(lambda x: x.astype(str).iloc[0]).to_dict()

subfam_map = {
    f: sorted(filtered[filtered[C["Job Family"]] == f][C["Sub Job Family"]].dropna().astype(str).unique().tolist())
    for f in families
}

col_sizes = [100]
for f in families:
    col_sizes += [140 for _ in subfam_map[f]]
grid_template = f"grid-template-columns: {' '.join(str(x)+'px' for x in col_sizes)};"

html = "<div class='map-wrapper'>"

# Cabeçalho 1 (Família)
html += f"<div class='jobmap-grid' style='{grid_template}; z-index:5;'>"
html += "<div class='grade-header'>GG</div>"
for f in families:
    span = len(subfam_map[f])
    color = fam_colors[f]
    html += f"<div class='header-family' style='grid-column: span {span}; background:{color};'>{f}</div>"
html += "</div>"

# Cabeçalho 2 (Subfamily)
html += f"<div class='jobmap-grid' style='{grid_template}; z-index:4;'>"
html += "<div class='grade-cell' style='background:#eef3ff;'></div>"
for f in families:
    for sf in subfam_map[f]:
        html += f"<div class='header-subfamily'>{sf}</div>"
html += "</div>"

# Linhas (Grades)
for g in grades:
    html += f"<div class='jobmap-grid grade-row' style='{grid_template}; z-index:1;'>"
    html += f"<div class='grade-cell'>GG {gg_label.get(g, g)}</div>"
    for f in families:
        fam_df = filtered[filtered[C["Job Family"]] == f]
        for sf in subfam_map[f]:
            cell_df = fam_df[(fam_df[C["Sub Job Family"]] == sf) & (fam_df["_GG_"] == g)]
            if not cell_df.empty:
                cards = "".join([
                    f"<div class='job-card' title='{r[C['Full Job Code']]}'><b>{r[C['Job Profile']]}</b><span>{r[C['Career Path']]}</span></div>"
                    for _, r in cell_df.iterrows()
                ])
                html += f"<div>{cards}</div>"
            else:
                html += "<div></div>"
    html += "</div>"

html += "</div>"
st.markdown(html, unsafe_allow_html=True)
