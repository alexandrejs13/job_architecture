import streamlit as st
import pandas as pd
import random
from utils.data_loader import load_excel_data

st.set_page_config(layout="wide", page_title="🗺️ Job Map")

data = load_excel_data()
if "job_profile" not in data:
    st.error("⚠️ Arquivo 'Job Profile.xlsx' não encontrado.")
    st.stop()

df = data["job_profile"]
levels = data.get("level_structure", pd.DataFrame())

st.markdown("<h1>🗺️ Job Map</h1>", unsafe_allow_html=True)

# ==== Filtros ====
col1, col2 = st.columns([2, 2])
with col1:
    fam_opts = ["Todas"] + sorted(df["Job Family"].dropna().unique().tolist())
    selected_family = st.selectbox("Família", fam_opts)
with col2:
    path_opts = ["Todas"] + sorted(df["Career Path"].dropna().unique().tolist())
    selected_path = st.selectbox("Trilha de Carreira", path_opts)

filtered = df.copy()
if selected_family != "Todas":
    filtered = filtered[filtered["Job Family"] == selected_family]
if selected_path != "Todas":
    filtered = filtered[filtered["Career Path"] == selected_path]

if filtered.empty:
    st.warning("Nenhum cargo encontrado com os filtros selecionados.")
    st.stop()

# ==== Montagem do Mapa ====
families = sorted(filtered["Job Family"].unique())
grades = sorted(filtered["Global Grade"].astype(str).unique(), key=lambda x: int(x), reverse=True)
subfam_map = {f: sorted(filtered[filtered["Job Family"] == f]["Sub Job Family"].unique()) for f in families}
palette = ["#1E56E0", "#00796B", "#9C27B0", "#E65100", "#558B2F"]
fam_colors = {f: palette[i % len(palette)] for i, f in enumerate(families)}

col_sizes = [100] + [140 for f in families for _ in subfam_map[f]]
grid_template = f"grid-template-columns: {' '.join(str(x)+'px' for x in col_sizes)};"

html = "<div class='map-wrapper'>"
html += f"<div class='jobmap-grid' style='{grid_template}; z-index:5;'>"
html += "<div class='grade-header'>GG</div>"
for f in families:
    span = len(subfam_map[f])
    html += f"<div class='header-family' style='grid-column: span {span}; background:{fam_colors[f]};'>{f}</div>"
html += "</div><div class='jobmap-grid' style='{grid_template}; z-index:4;'>"
html += "<div class='grade-cell' style='background:#eef3ff;'></div>"
for f in families:
    for sf in subfam_map[f]:
        html += f"<div class='header-subfamily'>{sf}</div>"
html += "</div>"

for g in grades:
    html += f"<div class='jobmap-grid grade-row' style='{grid_template}; z-index:1;'>"
    html += f"<div class='grade-cell'>GG {g}</div>"
    for f in families:
        fam_df = filtered[filtered["Job Family"] == f]
        for sf in subfam_map[f]:
            cell_df = fam_df[(fam_df["Sub Job Family"] == sf) & (fam_df["Global Grade"].astype(str) == g)]
            if not cell_df.empty:
                cards = "".join([f"<div class='job-card'><b>{r['Job Profile']}</b><span>{r['Career Path']}</span></div>" for _, r in cell_df.iterrows()])
                html += f"<div>{cards}</div>"
            else:
                html += "<div></div>"
    html += "</div>"
html += "</div>"
st.markdown(html, unsafe_allow_html=True)

# ==== Legenda ====
if not levels.empty:
    st.markdown("### 🧱 Estrutura de Níveis (Legenda)")
    st.dataframe(levels[["Global Grade", "Level Name", "Description"]], use_container_width=True)
