import streamlit as st
import pandas as pd
from utils.data_loader import load_job_profile_df

st.set_page_config(layout="wide", page_title="🗺️ Job Map")

# ===========================================================
# CSS — refinado e corporativo
# ===========================================================
st.markdown("""
<style>
.block-container {
  max-width: 1700px !important;
  margin: 0 auto !important;
}

/* ===== TÍTULO ===== */
h1 {
  color: #1E56E0;
  font-weight: 800;
  font-size: 1.9rem;
  margin-bottom: 1rem;
}

/* ===== ÁREA DE SCROLL ===== */
.map-wrapper {
  overflow: auto;
  border-top: 2px solid #c7d3f7;
  border-bottom: 2px solid #c7d3f7;
  background: #fff;
  padding-bottom: 1rem;
}

/* ===== GRID ===== */
.jobmap-grid {
  display: grid;
  border-collapse: collapse;
  font-size: 0.9rem;
  text-align: center;
  width: max-content;
  position: relative;
}
.jobmap-grid > div {
  border: 1px solid #ddd;
  box-sizing: border-box;
}

/* ===== PRIMEIRA COLUNA (GG) ===== */
.grade-header {
  background: #000;
  color: #fff;
  font-weight: 800;
  font-size: 1rem;
  padding: 10px 6px;
  text-align: center;
  position: sticky;
  left: 0;
  top: 0;
  z-index: 50;
}
.grade-cell {
  background: #fff;
  color: #000;
  font-weight: 700;
  padding: 6px 8px;
  position: sticky;
  left: 0;
  z-index: 40;
  border-right: 2px solid #000;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* ===== FAMÍLIAS ===== */
.header-family {
  font-weight: 700;
  color: #fff;
  padding: 8px 10px;
  font-size: 1rem;
  text-align: center;
  height: 42px;
  position: sticky;
  top: 0;
  z-index: 40;
  border-right: 2px solid #fff;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

/* ===== SUBFAMÍLIAS ===== */
.header-subfamily {
  font-weight: 600;
  background: #E9ECF9;
  color: #222;
  padding: 6px 10px;
  white-space: normal;
  text-align: center;
  font-size: 0.92rem;
  height: 38px;
  position: sticky;
  top: 42px;
  z-index: 38;
  border-bottom: 1px solid #d3d7e0;
}

/* ===== CÉLULAS DE CARGO ===== */
.job-card {
  background: #fafafa;
  border-left: 4px solid #A3B8F0;
  border-radius: 6px;
  padding: 8px 10px;
  margin: 3px 0;
  text-align: left;
  font-size: 0.85rem;
  white-space: normal;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.job-card b {
  display: block;
  font-weight: 700;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.job-card span {
  font-size: 0.78rem;
  color: #444;
  font-weight: 400;
}
.job-card:hover { background: #f5f7ff; }

/* ===== ZEBRA ===== */
.grade-row:nth-child(even) { background: #fcfcfc; }

/* ===== CORES ===== */
.family-color-green { background: #3C7A4D; } /* escuro */
.subfamily-color-green { background: #D8EBD9; } /* claro */
.family-color-blue { background: #1E56E0; }
.subfamily-color-blue { background: #E4E9FB; }
.family-color-orange { background: #BF6E30; }
.subfamily-color-orange { background: #F6E4D1; }
.family-color-gray { background: #4A4A4A; }
.subfamily-color-gray { background: #E8E8E8; }

</style>
""", unsafe_allow_html=True)

# ===========================================================
# LEITURA DE DADOS
# ===========================================================
try:
    df = load_job_profile_df()
except Exception as e:
    st.error(f"Erro ao carregar Job Profile.xlsx: {e}")
    st.stop()

df = df.dropna(subset=["Job Family", "Sub Job Family", "Job Profile", "Global Grade"])
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\\.0$", "", regex=True)

# ===========================================================
# FILTROS
# ===========================================================
st.markdown("<h1>🗺️ Job Map</h1>", unsafe_allow_html=True)
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

# ===========================================================
# DEFINIÇÃO DE CORES POR FAMÍLIA
# ===========================================================
family_colors = {
    "Corporate Affairs": ("family-color-green", "subfamily-color-green"),
    "Finance": ("family-color-blue", "subfamily-color-blue"),
    "Operations": ("family-color-orange", "subfamily-color-orange"),
    "General": ("family-color-gray", "subfamily-color-gray"),
}

families = sorted(filtered["Job Family"].unique().tolist())
grades = sorted(filtered["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else x, reverse=True)

subfam_map = {
    f: sorted(filtered[filtered["Job Family"] == f]["Sub Job Family"].unique().tolist())
    for f in families
}

col_sizes = [120]
for f in families:
    for sf in subfam_map[f]:
        width = max(150, len(sf) * 8)
        col_sizes.append(width)
grid_template = f"grid-template-columns: {' '.join(str(x)+'px' for x in col_sizes)};"

# ===========================================================
# CONSTRUÇÃO DO MAPA
# ===========================================================
html = "<div class='map-wrapper'>"

# Cabeçalho 1 — FAMÍLIAS (mesclado A1:A2 para GG)
html += f"<div class='jobmap-grid' style='{grid_template}; z-index:5;'>"
html += "<div class='grade-header' rowspan='2'>GG</div>"
for f in families:
    fam_class, sub_class = family_colors.get(f, ("family-color-gray", "subfamily-color-gray"))
    span = len(subfam_map[f])
    html += f"<div class='header-family {fam_class}' style='grid-column: span {span};'>{f}</div>"
html += "</div>"

# Cabeçalho 2 — SUBFAMÍLIAS
html += f"<div class='jobmap-grid' style='{grid_template}; z-index:4;'>"
html += "<div class='grade-cell'></div>"
for f in families:
    fam_class, sub_class = family_colors.get(f, ("family-color-gray", "subfamily-color-gray"))
    for sf in subfam_map[f]:
        html += f"<div class='header-subfamily {sub_class}'>{sf}</div>"
html += "</div>"

# Linhas — Grades
for g in grades:
    html += f"<div class='jobmap-grid grade-row' style='{grid_template};'>"
    html += f"<div class='grade-cell'>GG {g}</div>"
    for f in families:
        fam_df = filtered[filtered["Job Family"] == f]
        for sf in subfam_map[f]:
            cell_df = fam_df[(fam_df["Sub Job Family"] == sf) & (fam_df["Global Grade"] == g)]
            if not cell_df.empty:
                cards = "".join([
                    f"<div class='job-card'><b>{r['Job Profile']}</b><span>{r['Career Path']}</span></div>"
                    for _, r in cell_df.iterrows()
                ])
                html += f"<div>{cards}</div>"
            else:
                html += "<div></div>"
    html += "</div>"

html += "</div>"
st.markdown(html, unsafe_allow_html=True)
