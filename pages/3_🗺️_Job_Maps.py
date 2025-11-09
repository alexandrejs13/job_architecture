import streamlit as st
import random
from utils.data_loader import load_job_profile_df

st.set_page_config(layout="wide", page_title="🗺️ Job Map")

st.markdown("""
<style>
.block-container { max-width: 1700px !important; margin: 0 auto !important; }
h1 { color: #1E56E0; font-weight: 800; font-size: 1.8rem !important; }
</style>
""", unsafe_allow_html=True)

df = load_job_profile_df()

required_cols = ["Job Family", "Sub Job Family", "Job Profile", "Career Path", "Global Grade", "Full Job Code"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Colunas ausentes no Excel: {', '.join(missing)}")
    st.stop()

df = df.dropna(subset=required_cols)
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\\.0$", "", regex=True)

st.markdown("## 🗺️ Job Map")

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

families = sorted(filtered["Job Family"].unique().tolist())
random.seed(10)
palette = ["#1E56E0", "#00796B", "#9C27B0", "#E65100", "#5D4037", "#0288D1", "#558B2F"]
fam_colors = {f: palette[i % len(palette)] for i, f in enumerate(families)}

grades = sorted(filtered["Global Grade"].unique(), key=lambda x: int(x) if x.isdigit() else x, reverse=True)
subfam_map = {f: sorted(filtered[filtered["Job Family"] == f]["Sub Job Family"].unique().tolist()) for f in families}

html = "<div style='overflow-x:auto; white-space:nowrap;'>"
html += "<table style='border-collapse:collapse; font-size:0.85rem;'>"

html += "<tr><th style='background:#1E56E0;color:white;'>GG</th>"
for f in families:
    span = len(subfam_map[f])
    html += f"<th colspan='{span}' style='background:{fam_colors[f]};color:white;'>{f}</th>"
html += "</tr><tr><th></th>"
for f in families:
    for sf in subfam_map[f]:
        html += f"<th style='background:#eef3ff'>{sf}</th>"
html += "</tr>"

for g in grades:
    html += f"<tr><td style='background:#eef3ff;font-weight:700;'>GG {g}</td>"
    for f in families:
        fam_df = filtered[filtered["Job Family"] == f]
        for sf in subfam_map[f]:
            cell_df = fam_df[(fam_df["Sub Job Family"] == sf) & (fam_df["Global Grade"] == g)]
            if not cell_df.empty:
                cards = "".join([f"<div style='margin:2px;padding:4px;border-left:3px solid #1E56E0;'>{r['Job Profile']}<br><small>{r['Career Path']}</small></div>" for _, r in cell_df.iterrows()])
                html += f"<td>{cards}</td>"
            else:
                html += "<td></td>"
    html += "</tr>"
html += "</table></div>"

st.markdown(html, unsafe_allow_html=True)
