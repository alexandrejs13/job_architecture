import streamlit as st
import pandas as pd
from utils.data_loader import load_job_profile_df

# ===========================================================
# CONFIGURAÇÃO GERAL
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")

# ===========================================================
# CSS — Layout Executivo com Congelamento Real
# ===========================================================
st.markdown("""
<style>
.block-container {
  max-width: 1750px !important;
  margin: 0 auto !important;
  overflow: hidden !important;
}

/* ======= TÍTULO FIXO ======= */
h1 {
  color: #1E56E0;
  font-weight: 800;
  font-size: 1.9rem;
  margin-bottom: 1.2rem;
  position: sticky;
  top: 0;
  background: white;
  padding-top: 8px;
  z-index: 100;
}

/* ======= ÁREA DE SCROLL ======= */
.map-wrapper {
  max-height: 75vh;
  overflow: auto;
  border: 2px solid #d9e1f2;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

/* ======= GRID ======= */
.jobmap-grid {
  display: grid;
  border-collapse: collapse;
  text-align: center;
  width: max-content;
  font-size: 0.9rem;
}
.jobmap-grid > div {
  border: 1px solid #ddd;
  box-sizing: border-box;
  padding: 10px 12px;
  line-height: 1.3;
  overflow-wrap: break-word;
}

/* ======= CONGELAMENTO ======= */
.grade-header {
  background: #000;
  color: #fff;
  font-weight: 700;
  font-size: 1rem;
  text-align: center;
  position: sticky;
  left: 0;
  top: 0;
  z-index: 70;
  border-right: 2px solid #fff;
}
.grade-header span {
  display: block;
  font-weight: 700;
  font-size: 1.05rem;
  padding: 6px 0;
}
.grade-cell {
  background: #fff;
  color: #000;
  font-weight: 700;
  text-align: center;
  position: sticky;
  left: 0;
  z-index: 50;
  border-right: 2px solid #000;
}

/* ======= FAMÍLIA ======= */
.header-family {
  font-weight: 700;
  color: #fff;
  padding: 10px;
  font-size: 1rem;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: normal;
  text-align: center;
  position: sticky;
  top: 0;
  z-index: 60;
  border-right: 2px solid #fff;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

/* ======= SUBFAMÍLIA ======= */
.header-subfamily {
  font-weight: 600;
  padding: 10px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  white-space: normal;
  text-align: center;
  font-size: 0.9rem;
  line-height: 1.3;
  position: sticky;
  top: 50px;
  z-index: 40;
  border-bottom: 1px solid #d3d7e0;
}

/* ======= CELULAS DE CARGOS ======= */
.job-card {
  background: #fafafa;
  border-left: 4px solid #A3B8F0;
  border-radius: 6px;
  padding: 10px 12px;
  margin: 8px 6px;
  text-align: left;
  font-size: 0.85rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.job-card b {
  font-weight: 700;
  display: block;
  margin-bottom: 4px;
  white-space: normal;
}
.job-card span {
  font-size: 0.8rem;
  color: #555;
  font-weight: 500;
}
.job-card:hover { background: #f5f7ff; }

/* ======= CORES ======= */
.family-finance { background: #154360; } .sub-finance { background: #D6EAF8; }
.family-hr { background: #145A32; } .sub-hr { background: #D5F5E3; }
.family-operations { background: #784212; } .sub-operations { background: #F6DDCC; }
.family-it { background: #4A235A; } .sub-it { background: #E8DAEF; }
.family-marketing { background: #1B4F72; } .sub-marketing { background: #D4E6F1; }
.family-corporate { background: #4D5656; } .sub-corporate { background: #E5E8E8; }

.grade-row:nth-child(even) { background: #fcfcfc; }

</style>
""", unsafe_allow_html=True)

# ===========================================================
# DADOS
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
# CORES POR FAMÍLIA
# ===========================================================
color_map = {
    "Finance": ("family-finance", "sub-finance"),
    "HR": ("family-hr", "sub-hr"),
    "Operations": ("family-operations", "sub-operations"),
    "IT": ("family-it", "sub-it"),
    "Marketing": ("family-marketing", "sub-marketing"),
    "Corporate Affairs": ("family-corporate", "sub-corporate"),
}

families = sorted(filtered["Job Family"].unique().tolist())
grades = sorted(filtered["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else x, reverse=True)
subfam_map = {
    f: sorted(filtered[filtered["Job Family"] == f]["Sub Job Family"].unique().tolist())
    for f in families
}

col_sizes = [140]  # GG column
for f in families:
    for sf in subfam_map[f]:
        width = max(180, len(sf) * 8)
        col_sizes.append(width)
grid_template = f"grid-template-columns: {' '.join(str(x)+'px' for x in col_sizes)};"

# ===========================================================
# CONSTRUÇÃO DO MAPA
# ===========================================================
html = "<div class='map-wrapper'>"

# Cabeçalho GG mesclado
html += f"<div class='jobmap-grid' style='{grid_template}; z-index:70;'>"
html += "<div class='grade-header'><span>GG</span></div>"
for f in families:
    fam_class, sub_class = color_map.get(f, ("family-corporate", "sub-corporate"))
    span = len(subfam_map[f])
    html += f"<div class='header-family {fam_class}' style='grid-column: span {span};'>{f}</div>"
html += "</div>"

# Subfamílias
html += f"<div class='jobmap-grid' style='{grid_template}; z-index:60;'>"
html += "<div class='grade-cell'></div>"
for f in families:
    fam_class, sub_class = color_map.get(f, ("family-corporate", "sub-corporate"))
    for sf in subfam_map[f]:
        html += f"<div class='header-subfamily {sub_class}'>{sf}</div>"
html += "</div>"

# Linhas de cargos
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
