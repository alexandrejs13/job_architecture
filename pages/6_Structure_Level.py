
# -*- coding: utf-8 -*-
# pages/6_Structure_Level.py

import streamlit as st
import pandas as pd
from pathlib import Path
# Importa a função de carregamento específica do usuário (assumindo que 'load_excel_data'
# é a fonte para df_jobs, e 'load_level_structure_df' para df_levels)
from utils.data_loader import load_level_structure_df, load_excel_data 
# Importa a nossa função de visual global
from utils.ui import setup_sidebar, sidebar_logo_and_title
import html

# ===========================================================
# 4. DADOS (FUNÇÃO DE CARREGAMENTO NO TOPO PARA EVITAR ERROS)
# ===========================================================
@st.cache_data 
def load_and_prepare_data():
    try:
        # Carrega a tabela de estrutura de níveis (df_levels)
        df_levels = load_level_structure_df()
    except NameError:
        st.error("Erro: A função `load_level_structure_df()` não foi encontrada.")
        return pd.DataFrame(), {}
        
    try:
        # Carrega a tabela de perfil de cargo para obter o Career Band Description
        data = load_excel_data()
        df_jobs = data.get("job_profile", pd.DataFrame())
    except NameError:
        st.warning("Aviso: A função `load_excel_data()` não foi encontrada. Descrições de Carreira serão limitadas.")
        df_jobs = pd.DataFrame()
    
    if df_levels.empty: return df_levels, {}
    
    # --- PROCESSAMENTO DE df_jobs PARA OBTER DESCRIÇÕES DE CARREIRA ---
    career_bands_desc = {}
    if not df_jobs.empty:
        # 1. Limpa nomes de colunas
        df_jobs.columns = df_jobs.columns.str.strip()
        
        # 2. Garante que colunas essenciais existam
        job_cols_needed = ["Career Band", "Career Band Description"]
        for col in job_cols_needed:
            if col not in df_jobs.columns:
                df_jobs[col] = '-'
            df_jobs[col] = df_jobs[col].astype(str).str.strip()
            
        # 3. Mapear Descrição da Faixa de Carreira
        if "Career Band" in df_jobs.columns and "Career Band Description" in df_jobs.columns:
             career_bands_desc = df_jobs.set_index('Career Band')['Career Band Description'].dropna().drop_duplicates().to_dict()
    
    # --- PROCESSAMENTO DE df_levels ---
    required_level_cols = ["Career Band", "Level Key", "Level Name", "Global Grade", "Level Description"]
    for col in required_level_cols:
        if col not in df_levels.columns: df_levels[col] = "-"
        df_levels[col] = df_levels[col].astype(str).str.strip()

    return df_levels, career_bands_desc

# ===========================================================
# 1. CONFIGURAÇÃO DE PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Structure Level", 
    page_icon="🪜", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. APLICA VISUAL GLOBAL E SIDEBAR
# ===========================================================
setup_sidebar()

# ===========================================================
# 3. CSS CRIATIVO (Layout de Cards e Cores para LUDICIDADE)
# ===========================================================
st.markdown("""
<style>
:root {
    --blue: #145efc;
    --bg-color: #f5f3f0;
}

/* ============ HEADER PADRÃO ============ */
.page-header {
    background-color: var(--blue);
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

/* ============ LAYOUT LÚDICO (EXPLORADOR DE NÍVEIS) ============ */
.level-explorer {
    display: flex;
    gap: 30px;
    overflow-x: auto;
    padding-bottom: 20px;
}
.career-column {
    flex-shrink: 0;
    width: 250px; 
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    min-height: 200px; 
}
.career-title {
    background-color: #333333; 
    color: white;
    font-weight: 800;
    padding: 15px 12px;
    text-align: center;
    font-size: 1.1rem;
    position: sticky; 
    top: 0;
    z-index: 10;
}
.level-list {
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.level-card {
    background: var(--bg-color);
    border: 2px solid #ddd;
    border-radius: 8px;
    padding: 10px 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    transition: all 0.2s;
    cursor: default;
}

.level-name {
    font-weight: 800;
    color: var(--blue);
    font-size: 1.2rem;
    margin-bottom: 3px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.level-grade {
    font-size: 0.9rem;
    font-weight: 700;
    color: #444;
}
.level-desc {
    font-size: 0.85rem;
    color: #555;
    margin-top: 5px;
    border-top: 1px dashed #eee;
    padding-top: 5px;
}

/* Cores de Badges baseadas no prefixo do Level Key (W, U, P, M, E) */
.badge-W { border-left: 5px solid #999; }
.badge-U { border-left: 5px solid #ff9800; } 
.badge-P { border-left: 5px solid #00bcd4; } 
.badge-M { border-left: 5px solid #4caf50; } 
.badge-E { border-left: 5px solid #f44336; } 

/* Neutraliza o h1 original */
h1 { display: none !important; }

</style>
""", unsafe_allow_html=True)

# ===========================================================
# 5. CARREGAMENTO E PROCESSAMENTO (EXECUÇÃO)
# ===========================================================
df_levels, career_bands_desc = load_and_prepare_data()

if df_levels.empty:
    st.info("Ajuste os arquivos de dados para visualizar a Estrutura de Níveis.")
    st.stop()

# ===========================================================
# 6. PRÉ-PROCESSAMENTO PARA VISUALIZAÇÃO LÚDICA
# ===========================================================

# Agrupar os dados por Faixa de Carreira (Career Band) e ordená-los
grouped_by_band = df_levels.groupby('Career Band', sort=True)

# Função para definir a classe CSS de cor para o Level Card
def get_level_class(level_key):
    if pd.isna(level_key) or level_key == '-': return 'badge-W'
    prefix = level_key[0].upper()
    if prefix in ['W', 'U', 'P', 'M', 'E']:
        return f'badge-{prefix}'
    return 'badge-W' # Default

# ===========================================================
# 7. CONTEÚDO PRINCIPAL E RENDERIZAÇÃO
# ===========================================================

# Renderiza o header padrão (Identidade Visual)
st.markdown(f"""
<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png" alt="icon">
  Estrutura de Níveis e Progressão de Carreira (Levels)
</div>
""", unsafe_allow_html=True)

st.markdown("""
### 🪜 Explorador de Progressão por Carreira
Esta visualização mostra a estrutura de níveis agrupada por **Faixa de Carreira** (*Career Band*). Use o scroll horizontal para ver todas as carreiras.
""")

# --- RENDERIZAÇÃO DO LAYOUT LÚDICO DE COLUNAS ---
st.markdown('<div class="level-explorer">', unsafe_allow_html=True)

for band, group in grouped_by_band:
    if band == '-' or band == 'NAN': continue 
    
    # 1. Ordenar os níveis dentro da carreira por Global Grade (GG) crescente
    group['GG_Num'] = pd.to_numeric(group['Global Grade'], errors='coerce').fillna(0)
    group_sorted = group.sort_values(by='GG_Num', ascending=True)
    
    # 2. Inicia a coluna da Carreira
    st.markdown(f"""
    <div class="career-column">
        <div class="career-title">{html.escape(band)}</div>
        <div class="level-list">
    """, unsafe_allow_html=True)

    # 3. Adiciona a descrição da faixa de carreira (contexto)
    desc = career_bands_desc.get(band, "Descrição da Faixa de Carreira não disponível.")
    st.markdown(f"""
        <div style="padding: 10px; background: #fdfdfd; border-bottom: 1px solid #eee; font-size: 0.8rem; color: #666; font-style: italic; border-radius: 8px 8px 0 0;">
            {html.escape(desc)}
        </div>
    """, unsafe_allow_html=True)
    
    # 4. Itera e cria os cards de nível
    for _, row in group_sorted.iterrows():
        level_key = row['Level Key']
        level_class = get_level_class(level_key)
        
        # Assume que o Level Description contém o texto explicativo
        desc_content = row['Level Description'] if row['Level Description'] != '-' else "Nenhuma descrição detalhada disponível."
        
        # HTML do Card de Nível
        st.markdown(f"""
        <div class="level-card {level_class}">
            <div class="level-name">
                <span>{html.escape(row['Level Name'])}</span>
                <span style="font-size: 0.9rem; font-weight: 700; color: #111;">{html.escape(level_key)}</span>
            </div>
            <div class="level-grade">Global Grade: {html.escape(row['Global Grade'])}</div>
            <div class="level-desc">{html.escape(desc_content)}</div>
        </div>
        """, unsafe_allow_html=True)
        
    # 5. Fecha a coluna da Carreira
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True) # Fecha .level-explorer
