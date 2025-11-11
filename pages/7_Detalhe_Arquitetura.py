# pages/7_Detalhe_Arquitetura.py

import streamlit as st
import pandas as pd
from utils.ui import section 

st.set_page_config(page_title="Página 7 - Detalhe da Arquitetura", layout="wide")

# --- DEFINIÇÃO DO CAMINHO LOCAL DO ARQUIVO (CORRIGIDO PARA CSV) ---
LOCAL_FILE_PATH = "data/Job Profile.csv" 


# --- FUNÇÃO DE CARREGAMENTO DE DADOS (USANDO read_csv) ---
@st.cache_data
def load_data(file_path):
    """Carrega o arquivo CSV localmente e faz a limpeza."""
    try:
        # Usamos read_csv para maior compatibilidade
        df = pd.read_csv(file_path, delimiter=',') 
        
        # Garante que os cabeçalhos sejam fáceis de usar (sem espaços)
        df.columns = df.columns.str.replace(' ', '_')
        
        # Filtra linhas onde o Título do Cargo não é nulo para limpeza básica
        if 'Generic_Job_Profile' in df.columns:
            df = df[df['Generic_Job_Profile'].notna()]
        
        return df

    except FileNotFoundError:
        st.error(f"ERRO: Arquivo não encontrado! Certifique-se de que o arquivo **{file_path}** existe na sua estrutura local.")
        st.caption("Verifique o passo 1 (Preparação dos Arquivos) e 2 (Modificação no Código) da minha resposta anterior.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao processar o arquivo CSV. Detalhe: {e}")
        return pd.DataFrame()

df_full = load_data(LOCAL_FILE_PATH)

# --- INÍCIO DA EXIBIÇÃO ---

if not df_full.empty:
    
    # --- TÍTULO DA PÁGINA ---
    section("📄 Documentação e Detalhe da Arquitetura (Página 7)")

    # --- 1. SEÇÃO DE DOCUMENTAÇÃO ---
    st.subheader("1. Conceitos Chave da Arquitetura")
    
    col_conceito_1, col_conceito_2, col_conceito_3 = st.columns(3)
    
    # É CRUCIAL que os nomes das colunas aqui (Job_Family, Global_Grade, etc.)
    # correspondam aos nomes do cabeçalho do seu CSV (após a substituição de espaço por underscore)

    # Exemplo: Usando os nomes das colunas do seu arquivo:
    if 'Job_Family' in df_full.columns:
        with col_conceito_1:
            st.info("**Job Family (Família de Cargos)**")
            st.write("Agrupamento principal de cargos com função e propósito similares.")
            st.markdown(f"**Total de Famílias:** **`{df_full['Job_Family'].nunique()}`**")

    if 'Sub_Job_Family' in df_full.columns:
        with col_conceito_2:
            st.info("**Sub Job Family (Subfamília)**")
            st.write("Sub-segmentação dentro da Família, que define a especialidade.")
            st.markdown(f"**Total de Subfamílias:** **`{df_full['Sub_Job_Family'].nunique()}`**")

    if 'Global_Grade' in df_full.columns:
        with col_conceito_3:
            st.info("**Global Grade (Nível)**")
            st.write("O nível vertical que define o valor e a hierarquia do cargo.")
            st.markdown(f"**Total de Níveis:** **`{df_full['Global_Grade'].nunique()}`**")

    st.markdown("---")

    # --- 2. FERRAMENTA DE CONSULTA/BUSCA ---
    st.subheader("2. Tabela de Consulta e Detalhamento de Cargos")
    
    
    # Verificação de colunas para filtros e tabela (mantendo a segurança do código)
    if all(col in df_full.columns for col in ['Job_Family', 'Global_Grade', 'Generic_Job_Profile', 'Function_Code']):
        
        col_filtro_1, col_filtro_2, col_filtro_3 = st.columns(3)
        
        # Filtros
        family_select = col_filtro_1.multiselect(
            "Filtrar por Job Family:",
            options=df_full['Job_Family'].unique(),
            default=df_full['Job_Family'].unique()[:3] 
        )
        
        grade_select = col_filtro_2.multiselect(
            "Filtrar por Global Grade:",
            options=df_full['Global_Grade'].unique(),
            default=df_full['Global_Grade'].unique()[:3]
        )

        search_term = col_filtro_3.text_input("Buscar Cargo (Título ou Código):", "")


        # Aplica os filtros
        df_filtered = df_full[df_full['Job_Family'].isin(family_select)]
        df_filtered = df_filtered[df_filtered['Global_Grade'].isin(grade_select)]
        
        if search_term:
            df_filtered = df_filtered[
                df_filtered['Generic_Job_Profile'].str.contains(search_term, case=False, na=False) |
                df_filtered['Function_Code'].str.contains(search_term, case=False, na=False)
            ]

        st.write(f"Cargos encontrados: **{len(df_filtered)}** de **{len(df_full)}**")
        
        st.dataframe(
            df_filtered.reset_index(drop=True), 
            use_container_width=True, 
            height=500
        )
        
        # --- DOWNLOAD DA VISÃO FILTRADA ---
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download da Tabela Filtrada (.CSV)",
            data=csv,
            file_name='Detalhe_Arquitetura_Filtrada.csv',
            mime='text/csv',
        )

    else:
        st.warning("Verifique os nomes das colunas: 'Job_Family', 'Global_Grade', 'Generic_Job_Profile' e 'Function_Code' no seu arquivo CSV.")

else:
    st.error("Não foi possível carregar a tabela completa para a página de Detalhes.")
