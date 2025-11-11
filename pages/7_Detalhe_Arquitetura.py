# pages/7_Detalhe_Arquitetura.py

import streamlit as st
import pandas as pd
from utils.ui import section 

st.set_page_config(page_title="Página 7 - Detalhe da Arquitetura", layout="wide")

# --- DEFINIÇÃO DO ARQUIVO CARREGADO ---
# Usamos o nome do arquivo enviado no chat anterior (Geralmente o Streamlit lida com o ID)
FILE_ID = "Job Profile.xlsx - Job Profile.csv"

# --- FUNÇÃO DE CARREGAMENTO DE DADOS (Reutilizando a lógica anterior) ---
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path, delimiter=',')
        df.columns = df.columns.str.replace(' ', '_')
        return df
    except Exception:
        return pd.DataFrame()

df_full = load_data(FILE_ID)

# --- TÍTULO DA PÁGINA ---
section("📄 Documentação e Detalhe da Arquitetura (Página 7)")

if not df_full.empty:
    
    # --- 1. SEÇÃO DE DOCUMENTAÇÃO (O que se imaginava perceber) ---
    st.subheader("1. Conceitos Chave da Arquitetura")
    
    col_conceito_1, col_conceito_2, col_conceito_3 = st.columns(3)
    
    with col_conceito_1:
        st.info("**Job Family (Família de Cargos)**")
        st.write("Agrupamento principal de cargos com função e propósito similares, independente do nível de senioridade (ex: **Tecnologia**, **Finanças**).")
        st.markdown(f"**Total de Famílias:** **`{df_full['Job_Family'].nunique()}`**")

    with col_conceito_2:
        st.info("**Sub Job Family (Subfamília)**")
        st.write("Sub-segmentação dentro da Família, que define a especialidade ou disciplina (ex: Tech - **Desenvolvimento**, Finanças - **Controladoria**).")
        st.markdown(f"**Total de Subfamílias:** **`{df_full['Sub_Job_Family'].nunique()}`**")

    with col_conceito_3:
        st.info("**Global Grade (Nível)**")
        st.write("O nível vertical que define o valor e a hierarquia do cargo. Essencial para a banda salarial e progressão de carreira (ex: **L5**, **M3**).")
        st.markdown(f"**Total de Níveis:** **`{df_full['Global_Grade'].nunique()}`**")

    st.markdown("---")

    # --- 2. FERRAMENTA DE CONSULTA/BUSCA ---
    st.subheader("2. Tabela de Consulta e Detalhamento de Cargos")
    st.caption("Use os filtros para localizar cargos específicos ou visualizar os detalhes de cada Job Profile.")

    # Colunas para filtros
    col_filtro_1, col_filtro_2, col_filtro_3 = st.columns(3)
    
    # Filtros
    family_select = col_filtro_1.multiselect(
        "Filtrar por Job Family:",
        options=df_full['Job_Family'].unique(),
        default=df_full['Job_Family'].unique()[:3] # Seleciona os 3 primeiros como padrão
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
        # Busca em Título e no Código de Função
        df_filtered = df_filtered[
            df_filtered['Generic_Job_Profile'].str.contains(search_term, case=False) |
            df_filtered['Function_Code'].str.contains(search_term, case=False)
        ]

    st.write(f"Cargos encontrados: **{len(df_filtered)}** de **{len(df_full)}**")
    
    # --- Tabela Interativa de Detalhes ---
    st.dataframe(
        df_filtered.reset_index(drop=True), 
        use_container_width=True, 
        height=500
    )

    # --- 3. DOWNLOAD DA VISÃO FILTRADA ---
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download da Tabela Filtrada (.CSV)",
        data=csv,
        file_name='Detalhe_Arquitetura_Filtrada.csv',
        mime='text/csv',
    )
    
else:
    st.error("Não foi possível carregar a tabela completa para a página de Detalhes.")
