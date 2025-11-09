import streamlit as st
import pandas as pd
from utils.data_loader import load_job_profile_df

# ===========================================================
# CONFIG
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")

# Alturas fixas dos cabeçalhos (família e subfamília)
FAM_H = 46   # px
SUB_H = 64   # px
GG_COL_W = 140  # px (coluna GG)

# ===========================================================
# CSS – cabeçalhos fixos, coluna GG fixa e cores suaves
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
  overflow: auto;          /* único container com scroll */
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
  padding: 10px 12px;                /* respiro nas células */
  line-height: 1.3;
  overflow-wrap: break-word;         /* quebra sem cortar */
  word-break: break-word;
}}

/* ===== Coluna GG (preta, texto branco) ===== */
.gg-merged {{
  position: sticky;
  left: 0;
  top: 0;                            /* ocupa as DUAS linhas */
  height: calc(var(--famH) + var(--subH));
  width: var(--ggw);
  background: #000;
  color: #fff;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  border-right: 2px solid #fff;
}}
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
/* um traço suave à direita da coluna fixa */
.grade-cell::after {{
  content: "";
  position: absolute;
  right: -1px;
  top: 0;
  height: 100%;
  width: 1px;
  background: rgba(0,0,0,0.08);
}}

/* ===== Linha 1: FAMÍLIA (fixa) ===== */
.header-family {{
  position: sticky;
  top: 0;
  height: var(--famH);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;               /* texto branco em tom escuro */
  font-weight: 700;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
  z-index: 80;
  padding: 0 10px;
}}

/* ===== Linha 2: SUBFAMÍLIA (fixa) ===== */
.header-subfamily {{
  position: sticky;
  top: var(--famH);
  height: var(--subH);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
  z-index: 70;
  padding: 6px 10px;
}}

/* ===== Células de cargos ===== */
.job-card {{
  background: #fafafa;
  border-left: 4px solid #A4B8F5;
  border-radius: 8px;
  padding: 10px 12px;
  margin: 8px 6px;           /* respiro entre cards */
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
  margin-bottom: 4px;         /* título do cargo em negrito */
}}
.job-card span {{
  font-size: 0.8rem;
  color: #555;                /* Management/Professional sem negrito */
  font-weight: 500;
}}
.job-card:hover {{ background: #f5f7ff; }}

/* zebra sutil nas linhas */
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

# Colunas necessárias
req = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade", "Full Job Code"]
missing = [c for c in req if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes no Excel: {', '.join(missing)}")
    st.stop()

df = df.dropna(subset=["Job Family", "Sub Job Family", "Job Profile", "Global Grade"]).copy()
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
# CORES — únicas por família (HSL), sub = tom mais claro
# ===========================================================
families = sorted(filtered["Job Family"].unique().tolist())

def hsl(i, n, sat=52, light=32):
    # distribui tons no círculo HSL sem repetir
    hue = int((360 / max(n,1)) * i) % 360
    return f"hsl({hue}, {sat}%, {light}%)"

fam_color = {}
sub_color = {}
for i, fam in enumerate(families):
    dark = hsl(i, len(families), sat=55, light=30)   # família: mais escuro
    light = hsl(i, len(families), sat=55, light=85)  # subfamília: mais claro
    fam_color[fam] = dark
    sub_color[fam] = light

grades = sorted(
    filtered["Global Grade"].unique(),
    key=lambda x: int(x) if str(x).isdigit() else x,
    reverse=True
)

subfam_map = {
    f: sorted(filtered[filtered["Job Family"] == f]["Sub Job Family"].dropna().unique().tolist())
    for f in families
}

# Monta largura de colunas: GG + uma por subfamília ajustada ao texto
col_sizes = [GG_COL_W]
for f in families:
    for sf in subfam_map[f]:
        width = max(180, min(360, 14 * max(len(sf), 12)))  # ajusta ao título com folga
        col_sizes.append(width)
grid_template = "grid-template-columns: " + " ".join(f"{w}px" for w in col_sizes) + ";"

# ===========================================================
# HTML
# ===========================================================
html = "<div class='map-wrapper'>"

# LINHA 1 — Famílias + GG mesclado (A1+A2)
html += f"<div class='jobmap-grid' style='{grid_template}; z-index: 90;'>"
# GG mesclado vertical (A1+A2)
html += "<div class='gg-merged'>GG</div>"
for f in families:
    span = len(subfam_map[f])
    bg = fam_color[f]
    html += f"<div class='header-family' style='background:{bg}; grid-column: span {span};'>{f}</div>"
html += "</div>"

# LINHA 2 — Subfamílias (com placeholder invisível na 1ª coluna para alinhar)
html += f"<div class='jobmap-grid' style='{grid_template}; z-index: 80;'>"
# Placeholder alinhador da coluna GG (não exibe, só ocupa o slot)
html += "<div style='position:sticky; left:0; top:var(--famH); height:var(--subH); width:var(--ggw); background:#000; color:#000; z-index: 0; border: none;'></div>"
for f in families:
    for sf in subfam_map[f]:
        bg = sub_color[f]
        html += f"<div class='header-subfamily' style='background:{bg};'>{sf}</div>"
html += "</div>"

# DEMAIS LINHAS — grades + cards
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
