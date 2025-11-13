# -*- coding: utf-8 -*-
# pages/5_🧩_Job_Match.py

import streamlit as st
import pandas as pd
import html
import json
from pathlib import Path
import re
import numpy as np
# Importações de ML e data_loader omitidas por brevidade, mas devem ser mantidas
# from sklearn.metrics.pairwise import cosine_similarity
# from sentence_transformers import SentenceTransformer
# from utils.data_loader import load_excel_data
# from utils.ui_components import lock_sidebar
# from utils.ui import setup_sidebar

# ... (Resto do código de configuração e carregamento de dados omitido por brevidade) ...

# ===========================================================
# 3. FUNÇÕES AUXILIARES E CARREGAMENTO DE DADOS E MODELO
# ===========================================================
# (Mantendo as funções load_json_rules, load_data, etc. intactas)
# ...

# Simulação das funções load_data e load_json_rules para evitar NameError
# No ambiente real, estas funções devem ser carregadas de 'utils'
@st.cache_data
def load_json_rules():
    path = Path("wtw_match_rules.json") 
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"thresholds": {"weak_match": 0.50}, "wtw_reporting_limits": {"Coordenador": 12, "Gerente": 16}} 
# --- Fim da simulação ---

df, df_levels = pd.DataFrame({'job_family': ['Finance'], 'sub_job_family': ['Accounting'], 'global_grade': ['10'], 'global_grade_num': [10], 'career_path': ['Analista Sênior'], 'job_profile': ['Analista Contábil Sênior']}), pd.DataFrame()
model = None
JOB_RULES = load_json_rules()

GG_LIMITS_MAP = JOB_RULES.get("wtw_reporting_limits", {})


# ===========================================================
# 4. FUNÇÃO DE CÁLCULO DE MATCH BASEADO EM PARÂMETROS
# (Esta função será totalmente nova e focará no score de proximidade do nível)
# ===========================================================
# Funções calculate_structured_match (mantida do último exemplo estruturado)
# ... (código da calculate_structured_match do último exemplo deve ser mantido aqui) ...
def calculate_structured_match(df_filtered, params):
    # Apenas o esqueleto da função de cálculo para manter o fluxo
    if df_filtered.empty:
        return pd.DataFrame()

    # Mapeamento de Nível para um Score Numérico (1 a 3)
    knowledge_map = {"Rotinas/Procedimentos Definidos (Banda U/W)": 1, "Conhecimento de Conceitos e Princípios (Banda P/T)": 2, "Domínio Amplo e Integrado da Disciplina (Banda P/M Sênior)": 3}
    
    # Exemplo simples de inferência de GG (GG Inferido é baseado no conhecimento, o mais crucial)
    target_score_num = knowledge_map.get(params['knowledge_level'], 1) 
    inferred_gg = 8 + ((target_score_num - 1) / 2) * 5 # Mapeia 1-3 para 8-13 (Junior/Pleno)

    df_filtered['target_gg_normalized'] = inferred_gg / 25
    df_filtered['gg_normalized'] = df_filtered['global_grade_num'] / 25
    
    df_filtered['similarity'] = np.exp(-((df_filtered['gg_normalized'] - df_filtered['target_gg_normalized'])**2) / 0.05)
    
    # Ajuste por Liderança/IC (muito simplificado para esta demonstração)
    if not params['is_manager']:
        df_filtered.loc[df_filtered['career_path'].str.contains('manager|coordenador|supervisor', case=False, na=False), 'similarity'] *= 0.5
    
    df_filtered['similarity'] = np.clip(df_filtered['similarity'] / df_filtered['similarity'].max() if df_filtered['similarity'].max() > 0 else 0, 0, 1)

    return df_filtered.sort_values("similarity", ascending=False)
# ===========================================================

# ===========================================================
# 5. CAMPOS DE ENTRADA E LÓGICA DINÂMICA
# ===========================================================
st.markdown("### 🔧 Parâmetros Hierárquicos e Organizacionais")

c1, c2, c3 = st.columns(3)
with c1:
    families = sorted(df["job_family"].unique())
    selected_family = st.selectbox("📂 Família (Função) *", ["Selecione..."] + families)
with c2:
    subfamilies = sorted(df[df["job_family"] == selected_family]["sub_job_family"].unique()) if selected_family != "Selecione..." else []
    selected_subfamily = st.selectbox("📂 Subfamília (Disciplina) *", ["Selecione..."] + subfamilies)
with c3:
    superior = st.selectbox("📋 Cargo ao qual reporta (Filtro Rígido) *", [
        "Selecione...", "Supervisor", "Coordenador", "Gerente", "Diretor", "Vice-presidente", "Presidente / CEO"
    ])

# --- Lógica de Banding Dinâmico (Executivo, Gerência, ou IC) ---
st.markdown("---")
st.markdown("#### Fatores de Graduação (GGS): Nível de Complexidade")

# A ABA DE PERGUNTAS VAI MUDAR CONFORME A HIERARQUIA SELECIONADA
if superior in ["Diretor", "Vice-presidente", "Presidente / CEO"]:
    # ----------------------------------------------------
    # PERGUNTAS EXECUTIVAS (Foco em Estratégia e Impacto)
    # ----------------------------------------------------
    st.markdown("##### Nível Executivo Detectado: Foco em Estratégia e Liderança de Múltiplas Funções.")
    col1, col2 = st.columns(2)
    with col1:
        # Pergunta 1: Estratégia/Business Strategy (EX)
        is_exec_team = st.selectbox("1. Ocupa posição no Comitê Executivo (Strategic Impact)?", ["Sim", "Não"])
    with col2:
        # Pergunta 2: Leadership/Multiple Functions
        exec_scope = st.selectbox("2. Liderança Funcional:", [
            "Head de Função Crítica/Múltiplas Funções",
            "Head de Função Grande ou Chave",
            "Head de Subfunção/Contribui para a Estratégia Funcional"
        ])

    # Default para M/IC se não for Executivo
    is_manager = is_exec_team == "Sim"
    leadership_scope = "Responsabilidade Total de Supervisão (M1/M2)" if is_manager else "Nenhuma responsabilidade de gestão"
    knowledge_level = "Domínio Amplo e Integrado da Disciplina (Banda P/M Sênior)"
    problem_level = "Julgamento Complexo, Análise de Múltiplas Fontes (Banda P/M)"
    impact_scope = "Função/Organização (Ex: Vice-Presidência)"
    business_expertise = "Conhecimento da Indústria/Competidores"
    interpersonal_skills = "Influência Estratégica/Negociação Externa Sênior"
    proficiency_level = "Especialista/Guru (P5/P6): Alto nível de competência reconhecida."
    
elif superior in ["Supervisor", "Coordenador", "Gerente"]:
    # ----------------------------------------------------
    # PERGUNTAS GERENCIAIS/PROFISSIONAIS (Foco em Proficiência e Gestão)
    # ----------------------------------------------------
    st.markdown("##### Nível de Gerência/Profissional Detectado: Foco em Proficiência (P) ou Gestão Operacional (M).")
    
    col1, col2 = st.columns(2)

    with col1:
        # Fator 3: Tipo de Contribuição (M vs IC)
        is_manager_input = st.radio("1. Possui Responsabilidade Formal de Gestão?", ["Não (IC)", "Sim (Gestor de Pessoas)"])
        is_manager = is_manager_input == "Sim (Gestor de Pessoas)"
        
        # Fator 1: Profundidade do Conhecimento Funcional
        knowledge_level = st.selectbox(
            "2. Profundidade do Conhecimento Funcional (Qualificação):",
            ["Rotinas/Procedimentos Definidos (Banda U/W): Não exige diploma universitário.", 
             "Conhecimento de Conceitos e Princípios (Banda P/T): Exige diploma ou experiência equivalente.", 
             "Domínio Amplo e Integrado da Disciplina (Banda P/M Sênior): Conhecimento de teorias complexas."]
        )
        
        # Fator 2: Solução de Problemas / Julgamento
        problem_level = st.selectbox(
            "3. Complexidade na Solução de Problemas (Julgamento):",
            ["Seguir Regras Simples (Julgamento básico)", 
             "Julgamento baseado em Prática e Experiência",
             "Julgamento Complexo, Análise de Múltiplas Fontes (Banda P/M)"]
        )
    
    with col2:
        # Fator 8: Nível de Proficiência (Experience Proxy)
        proficiency_level = st.selectbox(
            "4. Nível de Proficiência/Experiência Esperado:",
            ["Nível de Entrada/Inicial (P1): Nível de entrada, sob supervisão.", 
             "Nível Intermediário/Pleno (P2): Exige mais competência que P1.", 
             "Nível de Carreira/Sênior (P3/P4): Exige competência significativamente maior.",
             "Especialista/Guru (P5/P6): Alto nível de competência reconhecida."]
        )
        
        # Fator 5: Amplitude do Impacto Organizacional
        impact_scope = st.selectbox(
            "5. Área de Impacto:",
            ["Restrito ao próprio Time",
             "Área/Subfunção (Ex: Contabilidade)",
             "Função/Organização (Ex: Vice-Presidência)"]
        )
        
        # Fator 7: Habilidades Interpessoais
        interpersonal_skills = st.selectbox(
            "6. Nível de Comunicação/Influência:",
            ["Boas Maneiras/Troca de Info simples", 
             "Exige Tato e Diplomacia/Negociação Interna", 
             "Influência Estratégica/Negociação Externa Sênior"]
        )
        
    # Variáveis default para o cálculo, mesmo que não perguntadas diretamente
    leadership_scope = "Responsabilidade Total de Supervisão (M1/M2)" if is_manager else "Orientação/Treinamento de Juniores (IC)"
    business_expertise = "Integração com a Subfunção/Função" 
    
else:
    # ----------------------------------------------------
    # PERGUNTAS DE APOIO/ENTRADA (W/U/T)
    # ----------------------------------------------------
    st.markdown("##### Nível de Apoio/Entrada Detectado: Foco em Tarefas e Procedimentos Definidos.")
    
    col1, col2 = st.columns(2)
    with col1:
        # Fator 1: Conhecimento Funcional (Banda W/U)
        knowledge_level = st.selectbox(
            "1. Qualificação Requerida:",
            ["Tipicamente não exige diploma universitário (Banda W)", 
             "Pode exigir treinamento vocacional/experiência equivalente (Banda U/T)"]
        )
        # Fator 2: Solução de Problemas
        problem_level = st.selectbox(
            "2. Complexidade na Solução de Problemas:",
            ["Seguir Regras Simples (Julgamento básico)", 
             "Julgamento baseado em Prática e Experiência"]
        )
    with col2:
        # Fator 5: Amplitude do Impacto Organizacional
        impact_scope = st.selectbox(
            "3. Área de Impacto:",
            ["Restrito ao próprio Cargo",
             "Restrito ao próprio Time"]
        )
        # Fator 4: Escopo de Liderança (Quase sempre nenhuma)
        leadership_scope = st.selectbox(
            "4. Responsabilidade de Liderança:",
            ["Nenhuma responsabilidade de gestão", 
             "Orientação/Treinamento de Juniores (IC)"]
        )
        
    # Variáveis default para o cálculo
    is_manager = False
    proficiency_level = "Nível de Entrada/Inicial (P1)"
    business_expertise = "Restrito ao Time/Área"
    interpersonal_skills = "Boas Maneiras/Troca de Info simples"


# ===========================================================
# 6. EXECUÇÃO DE ANÁLISE (FILTRAGEM E MATCHING ESTRUTURADO)
# ===========================================================

if st.button("🔍 Analisar Aderência", type="primary", use_container_width=True):

    # 6.1. Validação de Inputs Essenciais
    required_inputs = [selected_family, selected_subfamily, superior]
    if "Selecione..." in required_inputs:
        st.warning("⚠️ Os campos Família, Subfamília e Cargo de Reporte são obrigatórios.")
        st.stop()
        
    # 6.2. Determinar o GG Máximo Permitido (Filtro Rígido Hierárquico)
    max_gg_allowed = GG_LIMITS_MAP.get(superior, 99) 
    
    # CORREÇÃO CRÍTICA DO BUG DE LEITURA: Força o limite para 12 se for Coordenador/Supervisor, ignorando o 99.
    if superior in ["Coordenador", "Supervisor"] and max_gg_allowed == 99:
        max_gg_allowed = 12 # Limite correto para Coordenador/Supervisor (GG < 12)
        
    # 6.3. Coleta de Parâmetros de Match
    # Nota: Usamos as variáveis definidas dinamicamente acima
    match_params = {
        'knowledge_level': knowledge_level,
        'problem_level': problem_level,
        'leadership_scope': leadership_scope,
        'impact_scope': impact_scope,
        'is_manager': is_manager,
        'business_expertise': business_expertise,
        'interpersonal_skills': interpersonal_skills,
        'proficiency_level': proficiency_level
    }

    # 6.4. Aplicação do Filtro Rígido (Arquitetura e Hierarquia)
    mask = (df["job_family"] == selected_family) & \
           (df["sub_job_family"] == selected_subfamily) & \
           (df["global_grade_num"] < max_gg_allowed)
    
    filtered_df = df[mask].copy()

    if filtered_df.empty:
        st.error(f"Nenhum cargo encontrado que satisfaça os filtros de Arquitetura ({selected_family}/{selected_subfamily}) e Hierarquia (GG < {max_gg_allowed}).")
        st.stop()
    
    # 6.5. Cálculo da Pontuação de Aderência (Match Estruturado)
    results_df = calculate_structured_match(filtered_df, match_params)
    
    # 6.6. Exibição dos Top 3 Resultados
    top3 = results_df.head(3)

    # --- Guardrail de Coerência Simples ---
    if top3.empty or top3.iloc[0]["similarity"] < JOB_RULES.get("thresholds", {}).get("weak_match", 0.50):
        best_score = top3.iloc[0]["similarity"] if not top3.empty else 0.0
        threshold_weak = JOB_RULES.get("thresholds", {}).get("weak_match", 0.50)
        score_to_display = float(best_score * 100)
        
        st.markdown(f"""
        <div class="custom-error-box">
            <div class="custom-error-title">❌ Alerta: Coerência de Fatores Baixa</div>
            A pontuação do melhor cargo compatível ({score_to_display:.1f}%) está abaixo do limite de Match Fraco ({threshold_weak*100:.0f}%).
            <br>
            **Ação Necessária:** Ajuste os Fatores de Graduação (GGS) para refletir um nível de complexidade que encontre aderência na sua base de dados.
        </div>
        """, unsafe_allow_html=True)
        st.stop()
        
    # --- Inferência do GG Mais Provável (Para Insight) ---
    inferred_gg_for_display = results_df.iloc[0]["global_grade"]
    
    # --- Insight Box (Adaptação para o novo modelo) ---
    st.markdown(f"""
    <div class="ai-insight-box">
        <div class="ai-insight-title">📊 Análise de Aderência Estruturada (GGS)</div>
        **Filtros Rígidos:** Família, Disciplina e Hierarquia (GG < **{max_gg_allowed}**).<br>
        **Global Grade Mais Provável (GG):** **{inferred_gg_for_display}** (Este é o resultado do match de maior pontuação).<br>
        **Aderência:** Ranqueado pela proximidade das suas respostas aos Fatores de Graduação (GGS).
    </div>
    """, unsafe_allow_html=True)


    # ===========================================================
    # 7. GRID FINAL (EXIBIÇÃO DOS CARGOS)
    # ===========================================================
    
    st.markdown("---")
    st.header("🏆 Cargos Mais Compatíveis")

    cards_data = []
    
    for _, row in top3.iterrows():
        lvl_name = ""
        gg_val = str(row["global_grade"]).strip() 
        
        if not df_levels.empty and "global_grade" in df_levels.columns and "level_name" in df_levels.columns:
            match = df_levels[df_levels["global_grade"].astype(str).str.strip() == gg_val]
            if not match.empty:
                lvl_name = f"• {match['level_name'].iloc[0]}"
        cards_data.append({
            "row": row,
            "score_fmt": f"{row['similarity']*100:.1f}%",
            "score_bg": "#145efc",
            "lvl": lvl_name
        })

    num_results = len(cards_data)
    grid_style = f"grid-template-columns: repeat({num_results}, 1fr);"
    grid_html = f'<div class="comparison-grid" style="{grid_style}">'

    # Lógica de renderização completa do grid (simplificada para o contexto)
    sections_config = [
        ("🧭 Sub Job Family Description", "sub_job_family_description", "#95a5a6"),
        ("🧠 Job Profile Description", "job_profile_description", "#e91e63"),
        ("🏛️ Career Band Description", "career_band_description", "#673ab7"),
    ]

    # 1. Cabeçalho
    for card in cards_data:
        d = card['row']
        grid_html += f"""
        <div class="grid-cell header-cell">
            <div class="fjc-title">{html.escape(d.get('job_profile', '-'))}</div>
            <div class="fjc-gg-row">
                <div class="fjc-gg">GG {d.get('global_grade', '-')} {card['lvl']}</div>
                <div class="fjc-score">{card['score_fmt']} Match</div>
            </div>
        </div>
        <div class="grid-cell meta-cell">
            <div class="meta-row"><strong>Família:</strong> {html.escape(d.get('job_family', '-'))}</div>
            <div class="meta-row"><strong>Subfamília:</strong> {html.escape(d.get('sub_job_family', '-'))}</div>
            <div class="meta-row"><strong>Carreira:</strong> {html.escape(d.get('career_path', '-'))}</div>
        </div>
        """

    # 2. Seções de Conteúdo (Exibindo 3 das seções de descrição)
    for title, field, color in sections_config:
        for card in cards_data:
            content = str(card['row'].get(field, '')).strip()
            if content.lower() in ('nan', '-'):
                content = ''
            
            grid_html += f"""
            <div class="grid-cell section-cell" style="border-left-color: {color};">
                <div class="section-title" style="color: {color};">{title}</div>
                <div class="section-content">{html.escape(content)}</div>
            </div>"""
    
    # 3. Rodapé
    for _ in cards_data:
        grid_html += '<div class="grid-cell footer-cell"></div>'

    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)
