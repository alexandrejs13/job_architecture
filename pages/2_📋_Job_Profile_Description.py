# -*- coding: utf-8 -*-
# pages/2_📋_Job_Profile_Description.py

import streamlit as st
import pandas as pd
import re
import html
from utils.data_loader import load_job_profile_df
from utils.ui_components import section, lock_sidebar

# ===========================================================
# CONFIGURAÇÃO DE PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="📋 Job Profile Description")
lock_sidebar()

# ===========================================================
# CSS COMPLETO (ALINHADO COM O JOB MATCH)
# ===========================================================
st.markdown("""
<style>
:root {
  --blue: #145efc;
  --gray-line: #e0e0e0;
  --gray-bg: #f8f9fa;
  --dark-gray: #2c3e50;
}

.block-container {
    max-width: 95% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* REMOVIDO: .topbar que criava a linha e o padding extra */

h1 {
    color: var(--blue);
    font-weight: 900 !important;
    font-size: 1.9rem !important;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 0 !important;
    padding-top: 15px; /* Adicionado um padding top para compensar a remoção do topbar */
    margin-bottom: 25px !important; /* Mantém o espaçamento inferior */
}

/* GRID DE COMPARAÇÃO DINÂMICO */
.comparison-grid {
    display: grid;
    gap: 25px; /* Espaço entre colunas */
    margin-top: 20px;
}

/* CÉLULAS DO GRID */
.grid-cell {
    background: #fff;
    border: 1px solid var(--gray-line);
    padding: 20px;
    display: flex;
    flex-direction: column;
}

/* CABEÇALHO (TÍTULO E GG) */
.header-cell {
    background: var(--gray-bg);
    border-radius: 12px 12px 0 0;
    border-bottom: none;
    min-height: 100px;
    justify-content: center;
}
.jp-title { font-size: 22px; font-weight: 800; color: var(--dark-gray); line-height: 1.2; margin-bottom: 8px; }
.jp-gg { color: var(--blue); font-weight: 700; font-size: 1.1rem; }

/* METADADOS (CLASSIFICAÇÃO) */
.meta-cell {
    background: #fff;
    border-top: 1px solid var(--gray-line);
    border-bottom: 1px solid var(--gray-line);
    font-size: 0.9rem;
    color: #555;
    gap: 8px;
    padding: 15px 20px;
}
.meta-row { display: flex; flex-wrap: wrap; gap: 15px; }
.meta-item strong { color: #333; font-weight: 700; }

/* SEÇÕES DE CONTEÚDO */
.section-cell {
    border-left-width: 5px;
    border-left-style: solid;
    border-top: none;
    background: #fdfdfd;
    padding: 15px 20px;
}
.section-title {
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-content {
    color: #333;
    line-height: 1.6;
    font-size: 0.95rem;
}
/* Formatação dos parágrafos internos */
.jp-p { margin: 0 0 8px 0; }

/* RODAPÉ */
.footer-cell {
    height: 15px;
    border-top: none;
    border-radius: 0 0 12px 12px;
    background: #fff;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# FUNÇÕES AUXILIARES
# ===========================================================
def safe_get(row, key, default="-"):
    val = row.get(key, "")
    return str(val).strip() if val and str(val).lower() != "nan" else default

def format_paragraphs(text):
    if not text or text == "-": return "-"
    parts = re.split(r"\n+|•|\r", text.strip())
    return "".join(f"<p class='jp-p'>• {html.escape(p.strip())}</p>" for p in parts if len(p.strip()) > 1)

# ===========================================================
# DADOS E FILTROS
# ===========================================================
df = load_job_profile_df()

# REMOVIDO O DIV TOPBAR QUE ENVOLVIA A SECTION
section("📋 Job Profile Description")

# --- FILTROS EM 3 COLUNAS ---
c1, c2, c3 = st.columns([1.2, 1.5, 1])
with c1:
    families = sorted(df["Job Family"].dropna().unique())
    fam = st.selectbox("📂 Família", families)
    filtered = df[df["Job Family"] == fam]

with c2:
    subs = sorted(filtered["Sub Job Family"].dropna().unique())
    sub = st.selectbox("📂 Subfamília", subs)
    sub_df = filtered[filtered["Sub Job Family"] == sub]

with c3:
    careers = sorted(sub_df["Career Path"].dropna().unique())
    career = st.selectbox("🛤️ Trilha de Carreira", careers)
    career_df = sub_df[sub_df["Career Path"] == career]

# --- MULTISELECT DE CARGOS ---
career_df_sorted = career_df.sort_values(by="Global Grade", ascending=False)
career_df_sorted["Option Label"] = career_df_sorted.apply(
    lambda x: f"GG{int(float(x['Global Grade']))} — {x['Job Profile']}" if str(x['Global Grade']).replace('.0','').isdigit() else x['Job Profile'], 
    axis=1
)

selected_labels = st.multiselect(
    "📌 Selecione até 3 cargos para visualizar/comparar:",
    options=career_df_sorted["Option Label"].tolist(),
    max_selections=3
)

# ===========================================================
# RENDERIZAÇÃO DINÂMICA
# ===========================================================
if selected_labels:
    selected_rows = []
    for label in selected_labels:
        row = career_df_sorted[career_df_sorted["Option Label"] == label].iloc[0]
        selected_rows.append(row)

    num_cols = len(selected_rows)
    grid_style = f"grid-template-columns: repeat({num_cols}, 1fr);"
    
    grid_html = f'<div class="comparison-grid" style="{grid_style}">'

    # --- 1. LINHA DE CABEÇALHO ---
    for row in selected_rows:
        gg = safe_get(row, 'Global Grade').replace('.0', '')
        grid_html += f"""
        <div class="grid-cell header-cell">
            <div class="jp-title">{html.escape(row['Job Profile'])}</div>
            <div class="jp-gg">Global Grade {gg}</div>
        </div>"""

    # --- 2. LINHA DE METADADOS ---
    for row in selected_rows:
        grid_html += f"""
        <div class="grid-cell meta-cell">
            <div class="meta-row">
                <div class="meta-item"><strong>Família:</strong> {html.escape(safe_get(row, 'Job Family'))}</div>
                <div class="meta-item"><strong>Subfamília:</strong> {html.escape(safe_get(row, 'Sub Job Family'))}</div>
            </div>
            <div class="meta-row">
                <div class="meta-item"><strong>Carreira:</strong> {html.escape(safe_get(row, 'Career Path'))}</div>
                <div class="meta-item"><strong>Cód:</strong> {html.escape(safe_get(row, 'Full Job Code'))}</div>
            </div>
            <div class="meta-row">
                 <div class="meta-item"><strong>Função:</strong> {html.escape(safe_get(row, 'Function Code'))}</div>
                 <div class="meta-item"><strong>Disciplina:</strong> {html.escape(safe_get(row, 'Discipline Code'))}</div>
            </div>
        </div>"""

    # --- 3. SEÇÕES DE CONTEÚDO (ALINHADAS) ---
    sections = [
        ("🧭", "Sub Job Family Description", "Sub Job Family Description", "#95a5a6"),
        ("🧠", "Job Profile Description", "Job Profile Description", "#e91e63"),
        ("🏛️", "Career Band Description", "Career Band Description", "#673ab7"),
        ("🎯", "Role Description", "Role Description", "#1E56E0"),
        ("🏅", "Grade Differentiator", "Grade Differentiator", "#ff9800"),
        ("🎓", "Qualifications", "Qualifications", "#009688")
    ]

    for emoji, title, col_name, color in sections:
        for row in selected_rows:
            raw_text = safe_get(row, col_name)
            formatted_text = format_paragraphs(raw_text) if raw_text != "-" else "-"
            
            grid_html += f"""
            <div class="grid-cell section-cell" style="border-left-color: {color};">
                <div class="section-title" style="color: {color};">
                    <span>{emoji}</span> {title}
                </div>
                <div class="section-content">{formatted_text}</div>
            </div>"""

    # --- 4. RODAPÉ (FECHAMENTO) ---
    for _ in selected_rows:
        grid_html += '<div class="grid-cell footer-cell"></div>'

    grid_html += '</div>' # Fim do Grid

    st.markdown(grid_html, unsafe_allow_html=True)

else:
    st.info("👆 Utilize os filtros acima e selecione um ou mais cargos para visualizar.")
