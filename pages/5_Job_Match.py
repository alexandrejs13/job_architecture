# -*- coding: utf-8 -*-
# pages/5_🧩_Job_Match.py

import streamlit as st
import pandas as pd
import numpy as np
import html
import json
import re
import os
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from utils.data_loader import load_excel_data
from utils.ui_components import lock_sidebar
from utils.ui import setup_sidebar
from pathlib import Path

# ===========================================================
# 1. CONFIGURAÇÃO DE PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="🧩 Job Match", page_icon="✅")

# ===========================================================
# 2. CSS GLOBAL E SIDEBAR
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

setup_sidebar()
lock_sidebar()

# ===========================================================
# 3. ESTILO VISUAL
# ===========================================================
st.markdown("""
<style>
.page-header {
    background-color: #145efc;
    color: white;
    font-weight: 750;
    font-size: 1.35rem;
    border-radius: 12px;
    padding: 22px 36px;
    display: flex;
    align-items: center;
    gap: 18px;
    width: 100%;
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.page-header img { width: 48px; height: 48px; }
h1 { display: none !important; }
.block-container { max-width: 95% !important; padding-left: 1rem !important; padding-right: 1rem !important; }
.stTextArea textarea {font-size: 16px !important;}
.comparison-grid { display: grid; gap: 20px; margin-top: 20px; }
.grid-cell { background: #fff; border: 1px solid #e0e0e0; padding: 15px; display: flex; flex-direction: column; }
.header-cell { background: #f8f9fa; border-radius: 12px 12px 0 0; border-bottom: none; }
.fjc-title { font-size: 18px; font-weight: 800; color: #2c3e50; margin-bottom: 10px; min-height: 50px; }
.fjc-gg-row { display: flex; justify-content: space-between; align-items: center; }
.fjc-gg { color: #145efc; font-weight: 700; }
.fjc-score { color: white; font-weight: 700; padding: 4px 10px; border-radius: 12px; font-size: 0.9rem; }
.meta-cell { border-top: 1px solid #eee; border-bottom: 1px solid #eee; font-size: 0.85rem; color: #555; min-height: 120px; }
.meta-row { margin-bottom: 5px; }
.section-cell { border-left-width: 5px; border-left-style: solid; border-top: none; background: #fdfdfd; }
.section-title { font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; color: #333; display: flex; align-items: center; gap: 5px;}
.section-content { color: #444; font-size: 0.9rem; line-height: 1.5; white-space: pre-wrap; }
.footer-cell { height: 10px; border-top: none; border-radius: 0 0 12px 12px; background: #fff; }
.ai-insight-box { background-color: #eef6fc; border-left: 5px solid #145efc; padding: 15px 20px; border-radius: 8px; margin: 20px 0; color: #2c3e50; }
.ai-insight-title { font-weight: 800; color: #145efc; display: flex; align-items: center; gap: 8px; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/checkmark%20success.png" alt="icon">
  Job Match - Análise Semântica de Cargo
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. CARGA OTIMIZADA DE MODELO E DADOS
# ===========================================================
@st.cache_resource(hash_funcs={SentenceTransformer: id})
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

@st.cache_data(show_spinner=False)
def load_wtw_data():
    try:
        with open("data/wtw_job_match.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

@st.cache_data(show_spinner=False)
def prepare_data():
    data = load_excel_data()
    df_jobs = data.get("job_profile", pd.DataFrame()).fillna("")
    df_levels = data.get("level_structure", pd.DataFrame()).fillna("")

    if not df_jobs.empty:
        df_jobs.columns = df_jobs.columns.str.strip()
        needed = ["Job Family","Sub Job Family","Job Profile","Role Description","Grade Differentiator",
                  "Qualifications","Global Grade","Career Path","Sub Job Family Description","Job Profile Description",
                  "Career Band Description","Function","Discipline","Full Job Code","KPIs / Specific Parameters"]
        for c in needed:
            if c not in df_jobs.columns: df_jobs[c] = "-"

    df_jobs["Global Grade Num"] = pd.to_numeric(
        df_jobs["Global Grade"].astype(str).str.replace(r"\.0$","",regex=True),
        errors='coerce').fillna(0).astype(int)
    df_jobs["Global Grade"] = df_jobs["Global Grade Num"].astype(str)

    if "Global Grade" in df_levels.columns:
        df_levels["Global Grade"] = df_levels["Global Grade"].astype(str).str.replace(r"\.0$","",regex=True).str.strip()

    df_jobs["Rich_Text"] = (
        "Job Profile: " + df_jobs["Job Profile"] + ". " +
        "Role Description: " + df_jobs["Role Description"] + ". " +
        "Grade Differentiator: " + df_jobs["Grade Differentiator"] + ". " +
        "Qualifications: " + df_jobs["Qualifications"]
    )
    return df_jobs, df_levels

@st.cache_data(show_spinner=False)
def get_embeddings(df_jobs):
    cache_file = Path("data/_cached_embeddings.npy")
    if cache_file.exists():
        return np.load(cache_file)
    model = load_model()
    emb = model.encode(df_jobs["Rich_Text"].tolist(), show_progress_bar=False, batch_size=32)
    np.save(cache_file, emb)
    return emb

try:
    df, df_levels = prepare_data()
    job_embeddings = get_embeddings(df)
    wtw_data = load_wtw_data()
    model = load_model()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# ===========================================================
# 5. LÓGICA DE MATCHING
# ===========================================================
LEVEL_GG_MAPPING = {
    "W1":[1,2,3,4,5],"W2":[5,6,7,8],"W3":[7,8,9,10],
    "U1":[4,5,6,7],"U2":[6,7,8,9],"U3":[8,9,10,11],
    "P1":[8,9,10],"P2":[10,11,12],"P3":[12,13,14],"P4":[14,15,16,17],
    "M1":[11,12,13,14],"M2":[14,15,16],"M3":[16,17,18,19],
    "E1":[18,19,20,21],"E2":[21,22,23,24,25]
}

def detect_level_from_text(text, wtw_db):
    if not wtw_db or not text: return None,None,None,[]
    text_lower = text.lower()
    best_score,best_band,best_level,best_key,kw=[] ,None,None,None,[]
    for band_key,band_info in wtw_db.get("career_bands",{}).items():
        for lvl_key,lvl_info in band_info.get("levels",{}).items():
            score=0; matches=[]
            for kw_ in lvl_info.get("core_keywords",[]):
                if re.search(r'\b'+re.escape(kw_.lower())+r'\b',text_lower):
                    score+=3; matches.append(kw_)
            for ukw in lvl_info.get("user_keywords",[]):
                if ukw.lower() in text_lower:
                    score+=1; matches.append(ukw)
            if score>best_score:
                best_score, best_band, best_level, best_key, kw = score, band_info, lvl_info, lvl_key, list(set(matches))
    return best_band,best_level,best_key,kw

# ===========================================================
# 6. INTERFACE DE USUÁRIO
# ===========================================================
st.markdown("Encontre o cargo ideal com base na descrição completa das responsabilidades.")

c1,c2 = st.columns(2)
with c1:
    families = sorted(df["Job Family"].unique())
    selected_family = st.selectbox("📂 Família (Obrigatório)", ["Selecione..."] + families)
with c2:
    subfamilies = sorted(df[df["Job Family"]==selected_family]["Sub Job Family"].unique()) if selected_family!="Selecione..." else []
    selected_subfamily = st.selectbox("📂 Subfamília (Obrigatório)", ["Selecione..."] + subfamilies)

desc_input = st.text_area("📋 Cole aqui a descrição detalhada da posição (Mínimo 50 palavras):",
                          height=200, placeholder="Descreva as principais responsabilidades, escopo de atuação, nível de autonomia...")
word_count = len(desc_input.strip().split())
st.caption(f"Contagem de palavras: {word_count} / 50")

if st.button("🔍 Analisar Aderência", type="primary", use_container_width=True):
    if selected_family=="Selecione..." or selected_subfamily=="Selecione..." or word_count<50:
        st.warning("⚠️ Para uma análise precisa, selecione Família, Subfamília e insira uma descrição com pelo menos 50 palavras.")
        st.stop()

    mask = (df["Job Family"]==selected_family)&(df["Sub Job Family"]==selected_subfamily)
    band,level,key,kws = detect_level_from_text(desc_input, wtw_data)
    allowed=[]
    if key and key in LEVEL_GG_MAPPING:
        allowed=LEVEL_GG_MAPPING[key]
        mask&=df["Global Grade Num"].isin(allowed)
        kw_fmt=", ".join([f"'{k}'" for k in kws[:3]])
        st.markdown(f"""
        <div class="ai-insight-box">
            <div class="ai-insight-title">🤖 Análise Semântica de Nível</div>
            Com base na sua descrição, identificamos características de um nível
            <strong>{level['label']}</strong> (Carreira: {band['label']}).<br>
            <small>Filtrando resultados para Grades coerentes: {min(allowed)} a {max(allowed)}. Termos detectados: {kw_fmt}...</small>
        </div>
        """, unsafe_allow_html=True)

    if not mask.any():
        st.error("Não foram encontrados cargos compatíveis com os filtros e o nível detectado.")
        st.stop()

    filt_idx = df[mask].index
    filt_emb = job_embeddings[filt_idx]
    query_emb = model.encode([desc_input], show_progress_bar=False)
    sims = cosine_similarity(query_emb, filt_emb)[0]
    results = df.loc[filt_idx].copy()
    results["similarity"] = sims
    top3 = results.sort_values("similarity", ascending=False).head(3)

    st.markdown("---")
    st.subheader("🏆 Cargos Mais Compatíveis")

    if len(top3)<1:
        st.warning("Nenhum resultado encontrado."); st.stop()

    cards=[]
    for _,r in top3.iterrows():
        score=r["similarity"]*100
        color="#28a745" if score>85 else "#1E56E0" if score>75 else "#fd7e14" if score>60 else "#dc3545"
        lvl_name=""
        gg=str(r["Global Grade"]).strip()
        if not df_levels.empty and "Global Grade" in df_levels.columns and "Level Name" in df_levels.columns:
            m=df_levels[df_levels["Global Grade"].astype(str).str.strip()==gg]
            if not m.empty: lvl_name=f"• {m['Level Name'].iloc[0]}"
        cards.append({"row":r,"score_fmt":f"{score:.1f}%","score_bg":color,"lvl":lvl_name})

    grid_style=f"grid-template-columns: repeat({len(cards)},1fr);"
    html_out=f'<div class="comparison-grid" style="{grid_style}">'
    for c in cards:
        html_out+=f"""
        <div class="grid-cell header-cell">
            <div class="fjc-title">{html.escape(c['row']['Job Profile'])}</div>
            <div class="fjc-gg-row">
                <div class="fjc-gg">GG {c['row']['Global Grade']} {c['lvl']}</div>
                <div class="fjc-score" style="background-color:{c['score_bg']};">{c['score_fmt']} Match</div>
            </div>
        </div>"""
    for c in cards:
        d=c['row']
        html_out+=f"""
        <div class="grid-cell meta-cell">
            <div class="meta-row"><strong>Família:</strong> {html.escape(str(d.get('Job Family','-')))}</div>
            <div class="meta-row"><strong>Subfamília:</strong> {html.escape(str(d.get('Sub Job Family','-')))}</div>
            <div class="meta-row"><strong>Carreira:</strong> {html.escape(str(d.get('Career Path','-')))}</div>
            <div class="meta-row"><strong>Cód:</strong> {html.escape(str(d.get('Full Job Code','-')))}</div>
        </div>"""
    sections=[
        ("🧭 Sub Job Family Description","Sub Job Family Description","#95a5a6"),
        ("🧠 Job Profile Description","Job Profile Description","#e91e63"),
        ("🏛️ Career Band Description","Career Band Description","#673ab7"),
        ("🎯 Role Description","Role Description","#145efc"),
        ("🏅 Grade Differentiator","Grade Differentiator","#ff9800"),
        ("🎓 Qualifications","Qualifications","#009688")
    ]
    for title,field,color in sections:
        for c in cards:
            content=str(c['row'].get(field,'-'))
            if field=="Qualifications" and (len(content)<2 or content.lower()=='nan'):
                html_out+='<div class="grid-cell section-cell" style="border-left-color:transparent; background:transparent; border:none;"></div>'
            else:
                html_out+=f"""
                <div class="grid-cell section-cell" style="border-left-color:{color};">
                    <div class="section-title" style="color:{color};">{title}</div>
                    <div class="section-content">{html.escape(content)}</div>
                </div>"""
    for _ in cards:
        html_out+='<div class="grid-cell footer-cell"></div>'
    html_out+='</div>'
    st.markdown(html_out, unsafe_allow_html=True)
    if top3.iloc[0]["similarity"]<0.6:
        st.info("💡 Aderência moderada. Tente refinar sua descrição.")
