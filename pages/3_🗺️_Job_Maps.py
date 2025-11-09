import streamlit as st
import pandas as pd
from utils.data_loader import load_excel_data
from utils.ui_components import section, lock_sidebar

# ===========================================================
# CONFIG
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")
lock_sidebar()

section("🗺️ Job Map")

# ===========================================================
# CSS
# ===========================================================
st.markdown("""
<style>
.block-container {
  max-width: 1700px !important;
  min-width: 1200px !important;
  margin: 0 auto !important;
}
h1 {
  color: #145efc;
  font-weight: 800;
  font-size: 2.1rem;
  display: flex;
  align-items: center;
  gap: .6rem;
}

/* ===== Layout principal ===== */
.map-wrap {
  overflow: auto;
  border-top: 3px solid #e9eef9;
  border-bottom: 3px solid #e9eef9;
  background: #fff;
  padding-bottom: .5rem;
}

.jmap {
  display: grid;
  width: max-content;
  font-size: .9rem;
  border-collapse: collapse;
  margin: 0;
  padding: 0;
}

/* ===== Congelamento ===== */
.sticky-top-1 { position: sticky; top: 0; z-index: 50; }
.sticky-top-2 { position: sticky; top: 48px; z-index: 49; }
.sticky-left  { position: sticky; left: 0; z-index: 60; }

/* ===== Coluna GG (preta) ===== */
.gg-head, .gg-cell {
  background: #000;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  border-right: 2px solid #fff;
}

/* ===== Cabeçalho Família ===== */
.family {
  color: #fff;
  font-weight: 800;
  letter-spacing: .2px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: .6rem .8rem;
  border: none;
  margin: 0;
  line-height: 1.2;
}

/* ===== Cabeçalho Subfamília ===== */
.subfamily {
  font-weight: 700;
  padding: .6rem .8rem;
  border: none;
  margin: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ===== Alturas fixas ===== */
.row1 { height: 48px; }
.row2 { height: 56px; }

/* ===== Corpo ===== */
.cell {
  border-right: 1px solid #eef2f9;
  border-top: 1px solid #f0f3fb;
  min-width: 170px;
}

.job-card {
  background: #fafafa;
  border-left: 4px solid #145efc;
  border-radius: 6px;
  padding: 6px 10px;
  margin: .35rem 0;
  box-shadow: 0 1px 2px rgba(0,0,0,.04);
  line-height: 1.25;
}
.job-card b {
  display: block;
  font-size: .92rem;
}
.job-card span {
  display: block;
  font-size: .8rem;
  color: #555;
}

.cell-inner {
  padding: .25rem .4rem;
}

/* ===== Remove qualquer gap entre grids ===== */
.no-gap { margin: 0; padding: 0; border: none; }

</style>
""", unsafe_allow_html=True)

# ===========================================================
# DADOS
# ===========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame()).copy()

if df.empty:
    st.error("⚠️ Não encontrei **data/Job Profile.xlsx**.")
    st.stop()

cols = ["Job Family","Sub Job Family","Job Profile","Career Path","Global Grade"]
for c in cols:
    if c not in df.columns:
        st.error(f"Falta a coluna: {c}")
        st.stop()

df = df.dropna(subset=["Job Family","Sub Job Family","Job Profile","Global Grade"])
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\\.0$","",regex=True)

# ===========================================================
# FILTROS
# ===========================================================
col1, col2 = st.columns(2)
with col1:
    fam = st.selectbox("Família", ["Todas"] + sorted(df["Job Family"].unique()))
with col2:
    path = st.selectbox("Trilha de Carreira", ["Todas"] + sorted(df["Career Path"].dropna().unique()))

f = df.copy()
if fam != "Todas":
    f = f[f["Job Family"] == fam]
if path != "Todas":
    f = f[f["Career Path"] == path]

if f.empty:
    st.info("Nenhum resultado com os filtros selecionados.")
    st.stop()

# ===========================================================
# PALETA DISTINTA — 20 cores únicas
# ===========================================================
def generate_palette(n: int):
    import colorsys
    hues = [i / n for i in range(n)]
    palette = []
    for h in hues:
        r,g,b = colorsys.hsv_to_rgb(h, 0.55, 0.55)
        palette.append('#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255)))
    return palette

def lighten(hex_color, factor=0.45):
    import colorsys
    h = hex_color.lstrip('#')
    r,g,b = [int(h[i:i+2],16)/255 for i in (0,2,4)]
    h,l,s = colorsys.rgb_to_hls(r,g,b)
    l = min(1, l + (1-l)*factor)
    r,g,b = colorsys.hls_to_rgb(h,l,s)
    return '#%02x%02x%02x' % (int(r*255),int(g*255),int(b*255))

families = sorted(f["Job Family"].unique().tolist())
fam_colors = dict(zip(families, generate_palette(len(families))))
sub_colors = {fam: lighten(color) for fam, color in fam_colors.items()}

sub_map = {fam: sorted(f[f["Job Family"]==fam]["Sub Job Family"].unique().tolist()) for fam in families}
grades = sorted(f["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else x, reverse=True)

col_sizes = [140]
for fam in families:
    col_sizes += [180 for _ in sub_map[fam]]
grid_template = "grid-template-columns: " + " ".join(f"{c}px" for c in col_sizes) + ";"

# ===========================================================
# HTML — FAMÍLIA + SUBFAMÍLIA FUNDIDAS
# ===========================================================
html = []
html.append("<div class='map-wrap'>")

# LINHA 1 — GG + Famílias
html.append(f"<div class='jmap row1 sticky-top-1 no-gap' style='{grid_template}'>")
html.append("<div class='gg-head sticky-left'>GG</div>")
for fam in families:
    span = len(sub_map[fam])
    html.append(f"<div class='family' style='background:{fam_colors[fam]}; grid-column: span {span};'>{fam}</div>")
html.append("</div>")

# LINHA 2 — Subfamílias (sem linha branca intermediária)
html.append(f"<div class='jmap row2 sticky-top-2 no-gap' style='{grid_template}'>")
html.append("<div class='gg-head sticky-left' style='background:#000;'></div>")
for fam in families:
    for sub in sub_map[fam]:
        html.append(f"<div class='subfamily' style='background:{sub_colors[fam]};'>{sub}</div>")
html.append("</div>")

# LINHAS DE CARGOS
for g in grades:
    html.append(f"<div class='jmap no-gap' style='{grid_template}'>")
    html.append(f"<div class='gg-cell sticky-left cell'><div class='cell-inner'><b>GG {g}</b></div></div>")
    for fam in families:
        fam_df = f[f["Job Family"]==fam]
        for sub in sub_map[fam]:
            cell_df = fam_df[(fam_df["Sub Job Family"]==sub) & (fam_df["Global Grade"]==g)]
            if cell_df.empty:
                html.append("<div class='cell'><div class='cell-inner'></div></div>")
            else:
                cards = "".join(
                    f"<div class='job-card'><b>{r['Job Profile']}</b><span>{r['Career Path']}</span></div>"
                    for _,r in cell_df.iterrows()
                )
                html.append(f"<div class='cell'><div class='cell-inner'>{cards}</div></div>")
    html.append("</div>")

html.append("</div>")
st.markdown("".join(html), unsafe_allow_html=True)
