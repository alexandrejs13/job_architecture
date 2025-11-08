import streamlit as st
import pandas as pd
import io, base64, random

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")

st.markdown("""
<style>
.block-container {
  max-width: 1700px !important;
  min-width: 1700px !important;
  margin: 0 auto !important;
}

/* Header */
h1 {
  color: #1E56E0 !important;
  font-weight: 800 !important;
  font-size: 1.8rem !important;
  margin-bottom: 1rem !important;
  display: flex; align-items: center; gap: 8px;
}

/* Selectors */
div[data-baseweb="select"] > div {
  min-height: 44px !important;
  font-weight: 600 !important;
}

/* Scroll principal */
.map-wrapper {
  overflow-x: auto;
  overflow-y: hidden;
  border-top: 3px solid #1E56E0;
  border-bottom: 3px solid #1E56E0;
  background: #fff;
  padding-bottom: 1rem;
  white-space: nowrap;
}

/* GRID COMPLETO */
.jobmap-grid {
  display: grid;
  border-collapse: collapse;
  font-size: 0.85rem;
  text-align: center;
  width: max-content;
}

/* ====== NOVO GRID VISUAL ====== */
.jobmap-grid > div {
  border: 1px solid #ddd;
  box-sizing: border-box;
}

/* Cabeçalhos */
.header-family {
  font-weight: 800;
  color: #fff;
  padding: 6px 4px;
  text-align: center;
  border-right: 2px solid #fff;
  white-space: normal;
}
.header-subfamily {
  font-weight: 700;
  background: #f0f2ff;
  padding: 6px;
  white-space: normal;
}

/* Grade fixa à esquerda */
.grade-cell {
  font-weight: 700;
  background: #eef3ff;
  border-right: 2px solid #1E56E0;
  padding: 6px 8px;
  position: sticky;
  left: 0;
  z-index: 3;
}

/* Card */
.job-card {
  background: #fafafa;
  border-left: 4px solid #1E56E0;
  border-radius: 6px;
  padding: 5px 8px;
  margin: 3px 0;
  text-align: left;
  font-size: 0.82rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  white-space: normal;
}
.job-card span {
  display: block;
  font-size: 0.75rem;
  color: #555;
}
.job-card:hover {
  background: #f0f5ff;
}

/* Zebra rows */
.grade-row:nth-child(even) {
  background: #fcfcfc;
}

/* Responsividade */
@media (max-width: 1500px) {
  .block-container { zoom: 0.9; }
}
@media (max-width: 1200px) {
  .block-container { zoom: 0.8; }
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# CARREGAR DADOS
# ===========================================================
from utils.data_loader import load_data
data = load_data()

if "job_profile" not in data:
    st.error("⚠️ Arquivo 'Job Profile.csv' não encontrado.")
    st.stop()

df = data["job_profile"]

required_cols = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade", "Full Job Code"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes no CSV: {', '.join(missing)}")
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
# CORES AUTOMÁTICAS POR FAMÍLIA
# ===========================================================
families = sorted(filtered["Job Family"].unique().tolist())
random.seed(10)
palette = [
    "#1E56E0", "#00796B", "#9C27B0", "#E65100", "#5D4037", "#0288D1",
    "#558B2F", "#8E24AA", "#F9A825", "#6D4C41", "#0097A7"
]
fam_colors = {f: palette[i % len(palette)] for i, f in enumerate(families)}

# ===========================================================
# GERAÇÃO DO MAPA HORIZONTAL
# ===========================================================
grades = sorted(filtered["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else x)
subfam_map = {f: sorted(filtered[filtered["Job Family"] == f]["Sub Job Family"].unique().tolist()) for f in families}

st.markdown("---")
st.markdown("### 📊 Mapa de Cargos Completo (Corporativo)")

# Montar grid com cabeçalho duplo (Family / SubFamily)
col_sizes = [80]  # primeira coluna (GG)
for f in families:
    col_sizes += [140 for _ in subfam_map[f]]
grid_template = f"grid-template-columns: {' '.join(str(x)+'px' for x in col_sizes)};"

html = "<div class='map-wrapper'>"

# Cabeçalho 1 (Família)
html += f"<div class='jobmap-grid' style='{grid_template}'>"
html += "<div style='background:#fff;'></div>"
for f in families:
    span = len(subfam_map[f])
    color = fam_colors[f]
    html += f"<div class='header-family' style='grid-column: span {span}; background:{color};'>{f}</div>"
html += "</div>"

# Cabeçalho 2 (Sub Family)
html += f"<div class='jobmap-grid' style='{grid_template}'>"
html += "<div style='background:#fff;'></div>"
for f in families:
    for sf in subfam_map[f]:
        html += f"<div class='header-subfamily'>{sf}</div>"
html += "</div>"

# Linhas de Grades
for g in grades:
    html += f"<div class='jobmap-grid grade-row' style='{grid_template}'>"
    html += f"<div class='grade-cell'>GG {g}</div>"
    for f in families:
        fam_df = filtered[filtered["Job Family"] == f]
        for sf in subfam_map[f]:
            cell_df = fam_df[(fam_df["Sub Job Family"] == sf) & (fam_df["Global Grade"] == g)]
            if not cell_df.empty:
                cards = "".join([
                    f"<div class='job-card' title='{r['Full Job Code']}'><b>{r['Job Profile']}</b><span>{r['Career Path']}</span></div>"
                    for _, r in cell_df.iterrows()
                ])
                html += f"<div>{cards}</div>"
            else:
                html += "<div></div>"
    html += "</div>"

html += "</div>"  # fecha wrapper

st.markdown(html, unsafe_allow_html=True)

# ===========================================================
# EXPORTAR PARA EXCEL
# ===========================================================
def gerar_excel(dframe):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        dframe.to_excel(writer, index=False, sheet_name="Job Map Consolidado")
        for fam, fam_df in dframe.groupby("Job Family"):
            fam_df.to_excel(writer, index=False, sheet_name=fam[:30])
    return output.getvalue()

st.markdown("---")
excel_data = gerar_excel(filtered)
b64 = base64.b64encode(excel_data).decode()
href = f'<a href="data:application/octet-stream;base64,{b64}" download="Job_Map_Corporativo.xlsx" class="stDownloadButton">📤 Baixar Job Map Corporativo (Excel)</a>'
st.markdown(href, unsafe_allow_html=True)
