# ===========================================================
# 4. DADOS
# ===========================================================
@st.cache_data
def load_and_prepare_data():
    try:
        # Carrega a tabela de estrutura de níveis usando a função do usuário
        df_levels = load_level_structure_df()
    except NameError:
        st.error("Erro: A função `load_level_structure_df()` não foi encontrada.")
        return pd.DataFrame(), {}
        
    # Carrega a tabela de perfil de cargo para obter o Career Band Description (Contexto de Carreira)
    data = load_excel_data() # Supondo que esta função carregue todos os dados excel
    df_jobs = data.get("job_profile", pd.DataFrame())
    
    if df_levels.empty: return df_levels, {}
    
    # --- INÍCIO DA CORREÇÃO DE KEYERROR ---
    if not df_jobs.empty:
        # 1. Limpa nomes de colunas (remove espaços extras)
        df_jobs.columns = df_jobs.columns.str.strip()
        
        # 2. Garante que colunas essenciais para o mapeamento existam
        job_cols_needed = ["Career Band", "Career Band Description"]
        for col in job_cols_needed:
            if col not in df_jobs.columns:
                # Se a coluna estiver faltando, cria-a com valor '-'
                df_jobs[col] = '-'
            # Limpa valores da coluna
            df_jobs[col] = df_jobs[col].astype(str).str.strip()
            
        # 3. Mapear Descrição da Faixa de Carreira (Contexto da Coluna)
        # Este passo agora só é executado após garantir que 'Career Band' existe.
        career_bands_desc = df_jobs.set_index('Career Band')['Career Band Description'].dropna().drop_duplicates().to_dict()
    else:
        career_bands_desc = {}
    # --- FIM DA CORREÇÃO DE KEYERROR ---
    
    # Limpeza de colunas do df_levels
    required_level_cols = ["Career Band", "Level Key", "Level Name", "Global Grade", "Level Description"]
    for col in required_level_cols:
        if col not in df_levels.columns: df_levels[col] = "-"
        df_levels[col] = df_levels[col].astype(str).str.strip()

    return df_levels, career_bands_desc
# Fim da função load_and_prepare_data
