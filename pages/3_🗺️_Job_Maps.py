import streamlit as st
import pandas as pd
import io
import base64

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")

st.markdown("""
<style>
/* Layout base */
.block-container {
  max-width: 1500px !important;
  min-width: 1500px !important;
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

/* Grade visual */
.jobmap-container {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  width: 100%;
  overflow-x: auto;
  border-top: 3px solid #1E56E0;
  border-bottom: 3px solid #1E56E0;
  padding: 10px 0;
}

.jobmap-row {
  display: grid;
  gap: 8px;
  padding: 4px 0;
  align-items: start;
}

.jobmap-header {
  font-weight: 800;
  background: #1E56E0;
  color: white;
  text-align: center;
  padding: 6px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.jobmap-grade {
  font-weight: 700;
  background: #f2f4ff;
  border-right: 3px solid #1E56E0;
  padding: 4px 8px;
  text-align: center;
}

.job-card {
  background: #f9f9f9;
  border-left: 4px solid #1E56E0;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 0.85rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  min-height: 40px;
  word-wrap: break-word;
}
.job-card:hover {
  background: #eef3ff;
}

/* Responsividade */
@media (max-width: 1300px) {
  .block-container { zoom: 0.9; }
}
@media (max-width: 1100px) {
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

# Limpeza
df = df.dropna(subset=["Job Family", "Sub Job Family", "Job Profile", "Global Grade"])
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True)

# ===========================================================
# FILTROS
# ===========================================================
st.markdown("<h1>🗺️ Job Map</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([2,2])
with col1:
    fam_opts = ["Todas"] + sorted(df["Job Family"].dropna().unique().tolist())
    selected_family = st.selectbox("Família", fam_opts)
with col2:
    path_opts = ["Todas"] + sorted(df["Career Path"].dropna().unique().tolist())
    selected_path = st.selectbox("Trilha de Carreira", path_opts)

# Aplicar filtros
filtered = df.copy()
if selected_family != "Todas":
    filtered = filtered[filtered["Job Family"] == selected_family]
if selected_path != "Todas":
    filtered = filtered[filtered["Career Path"] == selected_path]

# ===========================================================
# CONSTRUÇÃO DO MAPA VISUAL
# ===========================================================
st.markdown("---")

if filtered.empty:
    st.warning("Nenhum cargo encontrado com os filtros selecionados.")
else:
    # Obter grades e famílias
    grades = sorted(filtered["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else x)
    subfamilies = filtered.groupby(["Job Family", "Sub Job Family"]).ngroup()
    families = filtered["Job Family"].unique().tolist()

    st.markdown(f"### 📊 Mapa de Cargos ({len(filtered)} cargos)")

    fam_groups = filtered.groupby("Job Family")
    for fam, fam_df in fam_groups:
        st.markdown(f"#### 🏢 {fam}")
        subfams = sorted(fam_df["Sub Job Family"].dropna().unique().tolist())

        # Cabeçalho
        cols_css = f"grid-template-columns: 80px repeat({len(subfams)}, 1fr);"
        st.markdown(f"<div class='jobmap-container'>", unsafe_allow_html=True)
        header_html = "<div class='jobmap-row' style='" + cols_css + "'>" + \
                      "<div></div>" + "".join([f"<div class='jobmap-header'>{sf}</div>" for sf in subfams]) + \
                      "</div>"
        st.markdown(header_html, unsafe_allow_html=True)

        # Linhas por Grade
        for g in sorted(fam_df["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else x):
            row_html = f"<div class='jobmap-row' style='{cols_css}'>"
            row_html += f"<div class='jobmap-grade'>GG {g}</div>"
            for sf in subfams:
                cell_df = fam_df[(fam_df["Sub Job Family"] == sf) & (fam_df["Global Grade"] == g)]
                if not cell_df.empty:
                    cards = "".join([
                        f"<div class='job-card' title='{r['Full Job Code']} ({r['Career Path']})'>{r['Job Profile']}</div>"
                        for _, r in cell_df.iterrows()
                    ])
                    row_html += f"<div>{cards}</div>"
                else:
                    row_html += "<div></div>"
            row_html += "</div>"
            st.markdown(row_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ===========================================================
# EXPORTAR PARA EXCEL
# ===========================================================
def gerar_excel(dframe):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Aba consolidada
        dframe.to_excel(writer, index=False, sheet_name="Job Map Consolidado")
        # Uma aba por família
        for fam, fam_df in dframe.groupby("Job Family"):
            fam_df.to_excel(writer, index=False, sheet_name=fam[:30])
    return output.getvalue()

st.markdown("---")
excel_data = gerar_excel(filtered)
b64 = base64.b64encode(excel_data).decode()
href = f'<a href="data:application/octet-stream;base64,{b64}" download="Job_Map.xlsx" class="stDownloadButton">📤 Baixar Job Map em Excel</a>'
st.markdown(href, unsafe_allow_html=True)
