# pages/7_Detalhe_Arquitetura.py

# ... (restante dos imports)

st.set_page_config(page_title="Página 7 - Detalhe da Arquitetura", layout="wide")

# --- FUNÇÃO DE CARREGAMENTO DE DADOS COM UPLOADER ---
@st.cache_data
def process_uploaded_data(uploaded_file):
    """Lê o arquivo carregado pelo usuário e faz a limpeza."""
    try:
        # Verifica a extensão para usar o leitor correto
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, delimiter=',')
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            # Requer pip install openpyxl
            df = pd.read_excel(uploaded_file, engine='openpyxl') 
        else:
            st.error("Formato de arquivo não suportado. Use CSV, XLS ou XLSX.")
            return pd.DataFrame()

        # Garante que os cabeçalhos sejam fáceis de usar (sem espaços)
        df.columns = df.columns.str.replace(' ', '_')
        
        if 'Generic_Job_Profile' in df.columns:
            df = df[df['Generic_Job_Profile'].notna()]
        
        return df

    except Exception as e:
        st.error(f"Erro ao processar o arquivo. Verifique o formato e o separador de colunas: {e}")
        return pd.DataFrame()

# --- ÁREA DE UPLOAD E CARREGAMENTO ---
with st.sidebar:
    st.subheader("Carregar Arquivo de Dados")
    uploaded_file = st.file_uploader(
        "Arraste ou clique para carregar o 'Job Profile.xlsx' ou CSV",
        type=["csv", "xlsx", "xls"],
        help="O arquivo será processado e usado no dashboard."
    )

df_full = pd.DataFrame()
if uploaded_file is not None:
    df_full = process_uploaded_data(uploaded_file)
    st.sidebar.success("Dados carregados com sucesso!")
else:
    # Se nenhum arquivo foi carregado, exibe a mensagem no corpo da página
    section("📄 Documentação e Detalhe da Arquitetura (Página 7)")
    st.warning("⚠️ **ATENÇÃO:** Por favor, use o menu lateral para carregar o arquivo 'Job Profile.xlsx' ou CSV.")
    
# --- INÍCIO DA EXIBIÇÃO ---
if not df_full.empty:
    
    section("📄 Documentação e Detalhe da Arquitetura (Página 7)")
    # ... (O restante da sua lógica de exibição, filtros e tabela)
# ... (o restante do código continua)
