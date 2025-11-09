# -*- coding: utf-8 -*-
# pages/3_🗺️_Job_Maps.py

import io
import math
import pandas as pd
import streamlit as st
from utils.data_loader import load_excel_data
from utils.ui_components import section, lock_sidebar
import streamlit.components.v1 as components

# ===========================================================
# CONFIGURAÇÃO DE PÁGINA (primeiro comando)
# ===========================================================
st.set_page_config(layout="wide", page_title="🗺️ Job Map")
lock_sidebar()

# ===========================================================
# CSS GLOBAL (cores, layout e correções “linha fantasma”)
# ===========================================================
st.markdown("""
<style>
:root{
  --blue:#145efc;
  --grid:#d8dbe2;
  --grid-light:#eef1f5;
  --gg-w:160px;
  --hdr-h1:48px;  /* altura Família */
  --hdr-h2:46px;  /* altura Subfamília */
  --card-pad:10px;
}

/* container padrão com as mesmas margens das outras páginas */
.block-container{
  max-width:1750px !important;
  margin:0 auto !important;
  padding:0 18px 18px 18px !important;
}

/* Título + filtros fixos no topo */
.topbar{
  position:sticky; top:0; z-index:999;
  background:#fff; padding:10px 0 8px 0;
  border-bottom:2px solid var(--blue);
}
h1{ color:var(--blue); font-weight:900; font-size:1.9rem; margin:0 0 8px 0; display:flex; gap:8px; align-items:center;}

/* =================== MAPA =================== */
.map-shell{ position:relative; }
#mapbox{
  height:78vh; background:#fff;
  border-top:3px solid var(--blue);
  border-bottom:3px solid var(--blue);
  overflow:auto;
}

/* GRID principal */
.map-grid{
  display:grid; width:max-content;
  border-right:1px solid var(--grid);
  border-bottom:1px solid var(--grid);
  font-size:.88rem;
}

/* célula base */
.map-grid > div{ box-sizing:border-box; }

/* ===== CABEÇALHOS ===== */
/* Família (linha 1) */
.hdr-family{
  height:var(--hdr-h1);
  position:sticky; top:0; z-index:70;
  display:flex; align-items:center; justify-content:center;
  font-weight:800; color:#fff; padding:0 12px; text-align:center;
  border-right:1px solid #fff;
  /* sem linha fantasma: borda inferior branca coincide com subfamília */
  border-bottom:0;
}

/* Subfamília (linha 2) */
.hdr-sub{
  height:var(--hdr-h2);
  position:sticky; top:var(--hdr-h1); z-index:69;
  display:flex; align-items:center; justify-content:center;
  font-weight:600; color:#2d3139; padding:0 12px; text-align:center;
  background:#f5f6f8;
  border-right:1px solid var(--grid);
  /* elimina “linha fantasma”: zero gap */
  margin-top:0; border-top:0;
}

/* ===== COLUNA GG ===== */
.gg-hdr{
  width:var(--gg-w);
  height:calc(var(--hdr-h1) + var(--hdr-h2));
  position:sticky; top:0; left:0; z-index:80;
  display:flex; align-items:center; justify-content:center;
  background:#000; color:#fff; font-weight:900; font-size:1.05rem;
  border-right:2px solid #fff;
}
.gg-cell{
  width:var(--gg-w);
  position:sticky; left:0; z-index:60;
  display:flex; align-items:center; justify-content:center;
  background:#000; color:#fff; font-weight:700;
  border-right:2px solid #fff;
  border-top:1px solid #fff; /* grade branco entre GGs */
}

/* ===== CÉLULA de conteúdo ===== */
.cell{
  min-height:80px;
  background:#fff;
  border-top:1px solid var(--grid);
  border-right:1px solid var(--grid);
  padding:6px;
}

/* Card de job */
.job{
  background:#f9fafc; border-left:4px solid var(--blue);
  border-radius:8px; padding:var(--card-pad);
  margin:6px 4px; box-shadow:0 1px 2px rgba(0,0,0,.06);
  word-wrap:break-word; overflow-wrap:break-word; white-space:normal;
}
.job b{ display:block; line-height:1.3; margin-bottom:2px; }
.job span{ display:block; color:#4c566a; font-size:.8rem; }

/* ===== TOOLBAR ===== */
.toolbar{
  position:sticky; top:8px; z-index:1000; float:right;
  display:flex; gap:8px; justify-content:flex-end; margin-top:-42px;
}
.tbtn{
  border:1px solid #e4e7ee; background:#fff; border-radius:12px;
  padding:8px 10px; cursor:pointer; box-shadow:0 1px 2px rgba(0,0,0,.06);
  display:flex; gap:8px; align-items:center;
}
.tbtn:hover{ background:#f5f6f9; }
.tbtn input{ border:none; outline:none; width:180px; }

/* ===== FULLSCREEN helpers ===== */
:fullscreen #mapbox{ height:100vh; }
</style>
""", unsafe_allow_html=True)

# ===========================================================
# DADOS
# ===========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

req = ["Job Family","Sub Job Family","Job Profile","Career Path","Global Grade"]
miss = [c for c in req if c not in df.columns]
if miss:
    st.error(f"Colunas ausentes no Excel: {', '.join(miss)}")
    st.stop()

df = df.dropna(subset=["Job Family","Sub Job Family","Job Profile","Global Grade"]).copy()
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$","",regex=True)

# ===========================================================
# ORDEM DE FAMÍLIAS + CORES (elegantes, sem gritaria)
# ===========================================================
families_order = [
    "Top Executive/General Management",
    "Corporate Affairs/Communications",
    "Legal & Internal Audit",
    "Finance",
    "IT",
    "People & Culture",
    "Sales",
    "Marketing",
    "Technical Services",
    "Research & Development",
    "Technical Engineering",
    "Operations",
    "Supply Chain & Logistics",
    "Quality Management",
    "Facility & Administrative Services",
]

# paleta escura (famílias) – tons neutros diferentes
fam_dark = [
    "#616a72","#6b645d","#5e6f73","#676c5c","#5e6277",
    "#6f6068","#596b5f","#6a6660","#5f6a7a","#6b5e72",
    "#655f6e","#6a6e67","#6b6767","#5f6e73","#6a655d"
]
# claro (subfamílias): mesma família -> tom correspondente e ~+60% luminosidade
fam_light = [
    "#e9ecef","#eeeae6","#ecf1f3","#eef1ea","#eceff8",
    "#f0edf1","#eaf0ec","#efefed","#eef1f6","#efeef2",
    "#eeedf1","#eff1ee","#f1efef","#eef1f3","#efeeec"
]

# famílias presentes no dado, respeitando ordem desejada
familias = [f for f in families_order if f in df["Job Family"].unique()]
fam2dark = {f:fam_dark[i % len(fam_dark)] for i,f in enumerate(familias)}
fam2light= {f:fam_light[i % len(fam_light)] for i,f in enumerate(familias)}

# subfamílias por família
submap = {f: sorted(df[df["Job Family"]==f]["Sub Job Family"].dropna().unique().tolist())
          for f in familias}

# grades (GG) desc
grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x) if str(x).isdigit() else 999, reverse=True)

# ===========================================================
# TÍTULO + FILTROS FIXOS
# ===========================================================
st.markdown("<div class='topbar'>", unsafe_allow_html=True)
section("🗺️ Job Map")
c1,c2 = st.columns([2,2])
with c1:
    fam_sel = st.selectbox("Família", ["Todas"]+familias, index=0)
with c2:
    paths = ["Todas"]+sorted(df["Career Path"].dropna().unique().tolist())
    path_sel = st.selectbox("Trilha de Carreira", paths, index=0)
st.markdown("</div>", unsafe_allow_html=True)

# aplica filtros
work = df.copy()
if fam_sel!="Todas":
    work = work[work["Job Family"]==fam_sel]
if path_sel!="Todas":
    work = work[work["Career Path"]==path_sel]
if work.empty:
    st.warning("Nenhum cargo encontrado com os filtros selecionados.")
    st.stop()

# famílias e subfamílias do recorte atual (mantendo ordem global)
fam_now = [f for f in familias if f in work["Job Family"].unique()]
sub_now = {f: [sf for sf in submap[f] if sf in work[work["Job Family"]==f]["Sub Job Family"].unique()]
           for f in fam_now}

# ===========================================================
# COLUNAS (largura auto com teto)
# ===========================================================
def col_width(texts):
    mx = max([len(str(t)) for t in texts]) if texts else 14
    px = min(max(220, mx*8 + 60), 420)
    return f"{px}px"

colspec = ["var(--gg-w)"]
for f in fam_now:
    for sf in sub_now[f]:
        txts = [sf] + work[(work["Job Family"]==f)&(work["Sub Job Family"]==sf)]["Job Profile"].tolist()
        colspec.append(col_width(txts))
grid_style = f"grid-template-columns: {' '.join(colspec)};"

# ===========================================================
# CSV para download (toolbar)
# ===========================================================
buf = io.StringIO()
work[["Job Family","Sub Job Family","Job Profile","Career Path","Global Grade"]].to_csv(buf, index=False)
csv_bytes = buf.getvalue().encode("utf-8")

# ===========================================================
# TOOLBAR (zoom, busca, fullscreen, download)
# – Zoom e Fullscreen via JS em components (seguro)
# ===========================================================
toolbar_html = """
<div class="toolbar">
  <div class="tbtn" onclick="zoomMap(1)">➕ Zoom</div>
  <div class="tbtn" onclick="zoomMap(-1)">➖ Zoom</div>
  <div class="tbtn"><span>🔎</span><input id="q" placeholder="Localizar..."/></div>
  <div class="tbtn" onclick="toggleFS()">⛶ Tela cheia</div>
</div>
<script>
let scale=1.0;
function zoomMap(delta){
  scale = Math.min(1.6, Math.max(0.6, scale + (delta>0?0.1:-0.1)));
  const el = window.parent.document.getElementById('mapbox');
  if(el){ el.style.transform = 'scale('+scale+')'; el.style.transformOrigin='top left'; }
}
function toggleFS(){
  const root = window.parent.document.documentElement;
  const box = window.parent.document.getElementById('mapbox');
  if(!document.fullscreenElement){ box.requestFullscreen && box.requestFullscreen(); }
  else{ document.exitFullscreen && document.exitFullscreen(); }
}
window.addEventListener('message', (ev)=>{
  if(ev.data && ev.data.type==='SEARCH'){
    const term = (ev.data.q||'').toLowerCase();
    const cards = window.parent.document.querySelectorAll('.job');
    let first=null;
    cards.forEach(c=>{
      const txt=c.innerText.toLowerCase();
      if(term && txt.includes(term)){ c.style.outline='2px solid #145efc'; if(!first){ first=c; } }
      else{ c.style.outline='none'; }
    });
    if(first){
      first.scrollIntoView({behavior:'smooth',block:'center',inline:'center'});
    }
  }
});
</script>
"""
# render toolbar (componente em branco, só p/ carregar JS)
components.html(toolbar_html, height=10)

# input de busca ligado ao JS (enviando postMessage)
q = st.text_input("", key="___hidden_search", placeholder="", label_visibility="hidden")
if q:
    components.html(f"<script>window.parent.postMessage({{type:'SEARCH', q:{q!r}}}, '*');</script>", height=0)

# botão de download (mantém o estilo visual da toolbar – usa nativo st)
dl_col = st.columns([0.84,0.16])[1]
with dl_col:
    st.download_button("⬇️ Baixar CSV do recorte", data=csv_bytes,
                       file_name="job_map_recorte.csv", mime="text/csv", use_container_width=True)

# ===========================================================
# GRID (HTML)
# ===========================================================
html = [f"<div class='map-shell'><div id='mapbox'><div class='map-grid' style='{grid_style}'>"]

# Linha 1 – GG (mesclado 2 linhas) + Famílias
html.append("<div class='gg-hdr'>GG</div>")
for f in fam_now:
    span = len(sub_now[f])
    html.append(f"<div class='hdr-family' style='grid-column: span {span}; background:{fam2dark[f]};'>{f}</div>")

# Linha 2 – Subfamílias (sem linha fantasma)
for f in fam_now:
    for sf in sub_now[f]:
        html.append(f"<div class='hdr-sub' style='background:{fam2light[f]};'>{sf}</div>")

# Demais linhas – GG + células com cards
for g in grades:
    html.append(f"<div class='gg-cell'>GG {g}</div>")
    for f in fam_now:
        cut_f = work[work["Job Family"]==f]
        for sf in sub_now[f]:
            cut = cut_f[(cut_f["Sub Job Family"]==sf) & (cut_f["Global Grade"]==g)]
            if cut.empty:
                html.append("<div class='cell'></div>")
            else:
                cards = "".join(
                    f"<div class='job'><b>{r['Job Profile']}</b><span>{r['Career Path']}</span></div>"
                    for _,r in cut.iterrows()
                )
                html.append(f"<div class='cell'>{cards}</div>")

html.append("</div></div></div>")
st.markdown("".join(html), unsafe_allow_html=True)
