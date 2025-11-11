# ===========================================================
# 7_DETALHE_ARQUITETURA.PY — PADRONIZADO COM SIDEBAR GLOBAL
# ===========================================================

import streamlit as st
import pandas as pd
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO GERAL
# ===========================================================
st.set_page_config(
    page_title="Detalhe da Arquitetura",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. CSS GLOBAL E SIDEBAR UNIFICADA
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

# ===========================================================
# 3. CABEÇALHO PADRÃO
# ===========================================================
st.markdown("""
<style>
.page-header {
    background-color: #145efc;
    color: white;
    font-weight: 750;
    font-size: 1.45rem;
    border-radius: 12px;
    padding: 22px 36px;
    display: flex;
    align-items: center;
    gap: 18px;
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.page-header img {
    width: 54px;
    height: 54px;
}
.block-container {
    max-width: 1200px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/process.png" alt="icon">
    Documentação e Detalhe da Arquitetura
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. FUNÇÃO DE CARREGAMENTO DE DADOS
# ===========================================================
@st.cache_data
def process_uploaded_data(uploaded_file):
    """Lê o arquivo carregado pelo usuário e faz a limpeza."""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, delimiter=',')
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            st.error("Formato de arquivo não suportado. Use CSV, XLS ou XLSX.")
            return pd.DataFrame()

        df.columns = df.columns.str.strip().str.replace(' ', '_')

        if 'Generic_Job_Profile' in df.columns:
            df = df[df['Generic_Job_Profile'].notna()]

        return df

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
        return pd.DataFrame()

# ===========================================================
# 5. ÁREA DE UPLOAD
# ===========================================================
with st.sidebar:
    st.subheader("📂 Carregar Arquivo de Dados")
    uploaded_file = st.file_uploader(
        "Arraste ou clique para carregar o arquivo 'Job Profile.xlsx' ou CSV",
        type=["csv", "xlsx", "xls"],
        help="O arquivo será processado e usado no dashboard."
    )

# ===========================================================
# 6. TRATAMENTO E EXIBIÇÃO DE DADOS
# ===========================================================
df_full = pd.DataFrame()
if uploaded_file is not None:
    df_full = process_uploaded_data(uploaded_file)
    st.sidebar.success("✅ Dados carregados com sucesso!")
else:
    st.warning("⚠️ **Atenção:** Use o menu lateral para carregar o arquivo 'Job Profile.xlsx' ou CSV.")
    st.stop()

if not df_full.empty:
    st.success(f"Arquivo processado com {len(df_full):,} registros.")
    
    # Filtros
    familias = sorted(df_full["Job_Family"].dropna().unique()) if "Job_Family" in df_full.columns else []
    subs = sorted(df_full["Sub_Job_Family"].dropna().unique()) if "Sub_Job_Family" in df_full.columns else []
    
    col1, col2 = st.columns(2)
    with col1:
        fam = st.selectbox("Família (Job Family):", ["Selecione..."] + familias)
    with col2:
        subfam = st.selectbox("Sub-Família (Sub Job Family):", ["Selecione..."] + subs)
    
    filtered = df_full.copy()
    if fam != "Selecione...":
        filtered = filtered[filtered["Job_Family"] == fam]
    if subfam != "Selecione...":
        filtered = filtered[filtered["Sub_Job_Family"] == subfam]

    st.markdown("---")
    st.subheader("📘 Visualização dos Dados")
    st.dataframe(filtered, use_container_width=True)

    if not filtered.empty:
        st.download_button(
            "📥 Baixar dados filtrados (CSV)",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name=f"detalhe_arquitetura_{fam or 'todas'}.csv",
            mime="text/csv"
        )
else:
    st.info("Aguardando carregamento do arquivo para exibição dos dados.")
