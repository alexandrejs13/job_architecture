import streamlit as st
import pandas as pd
from utils.data_loader import load_job_profile_df

# ===========================================================
# CONFIGURAÇÃO
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")

FAM_H = 46
SUB_H = 64
GG_COL_W = 140

# ===========================================================
# CSS — 2 LINHAS FIXAS + COLUNA GG MESCLADA
# ===========================================================
st.markdown(f"""
<style>
:root {{
  --famH: {FAM_H}px;
  --subH: {SUB_H}px;
  --ggw: {GG_COL_W}px;
}}

.block-container {{
  max-width: 1750px !important;
  margin: 0 auto !important;
}}

h1 {{
  color: #1E56E0;
  font-weight: 800;
  font-size: 1.9rem;
  margin-bottom: 12px;
}}

.map-wrapper {{
  max-height: 76vh;
  overflow: auto;
  border: 1px solid #e7ebf3;
  border-radius: 10px;
  background: #fff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  position: relative;
}}

.jobmap-grid {{
  display: grid;
  border-collapse: collapse;
  text-align: center;
  width: max-content;
  font-size: 0.9rem;
}}
.jobmap-grid > div {{
  border: 1px solid #e7ebf3;
  box-sizing: border-box;
  padding: 10px 12px;
  line-height: 1.3;
  overflow-wrap: break-word;
  word-break: break-word;
}}

/* ===== Coluna GG (preta, mesclada verticalmente) ===== */
.gg-merged {{
  position: sticky;
  left: 0;
  top: 0;
  height: calc(var(--famH) + var(--subH));
  width: var(--ggw);
  background: #000;
  color: #fff;
  font-weight: 800;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  border-right: 2px solid #fff;
  border-bottom: none;
  border-top-left-radius: 6px;
}}

/* ===== Linhas fixas ===== */
.header-family {{
  position: sticky;
  top: 0;
  height: var(--famH);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 700;
  z-index: 90;
  padding: 0 10px;
  border-bottom: none;
}}

.header-subfamily {{
  position: sticky;
  top: var(--famH);
  height: var(--subH);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
  z-index: 80;
  padding: 6px 10px;
  border-top: none;
}}

/* ===== Células de cargos ===== */
.job-card {{
  background: #fafafa;
  border-left: 4px solid #A4B8F5;
  border-radius: 8px;
  padding: 10px 12px;
  margin: 8px 6px;
  text-align: left;
  font-size: 0.85rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  justify-content: center;
}}
.job-card b {{
  font-weight: 700;
  display: block;
  margin-bottom: 4px;
}}
.job-card span {{
  font-size: 0.8rem;
  color: #555;
  font-weight: 500;
}}
.job-card:hover {{ background: #f5f7ff; }}

.grade-cell {{
  position: sticky;
  left: 0;
  z-index: 60;
  background: #fff;
  color: #000;
  font-weight: 700;
  width: var(--ggw);
  border-right: 2px solid #000;
}}

.grade-row:nth-child(even) {{ background: #fcfcfc; }}
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

req = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade"]
missing = [c for c in req if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes: {', '.join(missing)}")
    st.stop()

df = df.dropna(subset=["Job Family", "Sub Job Family", "Job Profile", "Global Grade"])
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True)

# ===========================================================
# FILTROS
# ===========================================================
st.markdown("<h1>🗺️ Job Map</h1>", unsafe_allow_html=True)
c1, c2 = st.columns([2, 2])
with c1:
    fam_opts = ["Todas"] + sorted(df["Job Family"].dropna().unique().tolist())
    selected_family = st.selectbox("Família", fam_opts)
with c2:
    path_opts = ["Todas"] + sorted(df["Career Path"].dropna().unique().tolist())
    selected_path = st.selectbox("Trilha de Carreira", path_opts)

filtered = df
if selected_family != "Todas":
    filtered = filtered[filtered["Job Family"] == selected_family]
if selected_path != "Todas":
    filtered = filtered[filtered["Career Path"] == selected_path]

if filtered.empty:
    st.warning("Nenhum cargo encontrado com os filtros selecionados.")
    st.stop()

# ===========================================================
# PALETA CONTRASTANTE — sem tons próximos
# ===========================================================
families = sorted(filtered["Job Family"].unique().tolist())
palette = [
    ("#145efc", "#9cc5ff"),  # azul SIG
    ("#138D75", "#A9DFBF"),  # verde
    ("#884EA0", "#D2B4DE"),  # roxo
    ("#D68910", "#FAD7A0"),  # dourado
    ("#BA4A00", "#EDBB99"),  # laranja
    ("#2874A6", "#AED6F1"),  # azul médio
    ("#117A65", "#ABEBC6"),  # verde petróleo
    ("#633974", "#E8DAEF"),  # lilás
    ("#1B2631", "#D6DBDF"),  # grafite
    ("#78281F", "#F5B7B1")   # vermelho terroso
]

fam_color, sub_color = {}, {}
for i, fam in enumerate(families):
    dark, light = palette[i % len(palette)]
    fam_color[fam] = dark
    sub_color[fam] = light

grades = sorted(filtered["Global Grade"].unique(), key=lambda x: int(x) if str(x).isdigit() else x, reverse=True)
subfam_map = {
    f: sorted(filtered[filtered["Job Family"] == f]["Sub Job Family"].dropna().unique().tolist())
    for f in families
}

col_sizes = [GG_COL_W]
for f in families:
    for sf in subfam_map[f]:
        width = max(180, min(360, 14 * max(len(sf), 12)))
        col_sizes.append(width)
grid_template = "grid-template-columns: " + " ".join(f"{w}px" for w in col_sizes) + ";"

# ===========================================================
# HTML — AGORA SÓ 2 LINHAS FIXAS (SEM ESPAÇO BRANCO)
# ===========================================================
html = "<div class='map-wrapper'>"

# LINHA 1 — GG + FAMÍLIAS
html += f"<div class='jobmap-grid' style='{grid_template}; z-index: 90;'>"
html += "<div class='gg-merged'>GG</div>"
for f in families:
    span = len(subfam_map[f])
    bg = fam_color[f]
    html += f"<div class='header-family' style='background:{bg}; grid-column: span {span};'>{f}</div>"
html += "</div>"

# LINHA 2 — SUBFAMÍLIAS (SEM LINHA INTERMEDIÁRIA)
html += f"<div class='jobmap-grid' style='{grid_template}; z-index: 80;'>"
html += f"<div class='header-subfamily' style='background:#000; color:#fff; position:sticky; left:0;'>Subfamília</div>"
for f in families:
    for sf in subfam_map[f]:
        bg = sub_color[f]
        html += f"<div class='header-subfamily' style='background:{bg};'>{sf}</div>"
html += "</div>"

# LINHAS DE CARGOS
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
