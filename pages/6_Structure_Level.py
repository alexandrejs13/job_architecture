import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Estrutura de Níveis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. CSS GLOBAL E HEADER
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

# ===========================================================
# 3. CABEÇALHO
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
    box-sizing: border-box;
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.page-header img {
    width: 48px;
    height: 48px;
}
.block-container {
    max-width: 900px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/checkmark%20success.png" alt="icon">
    Estrutura de Níveis
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. CARREGAMENTO DOS DADOS
# ===========================================================
@st.cache_data
def load_data():
    path = Path("data/Level Structure.xlsx")
    if not path.exists():
        st.error("❌ Arquivo 'Level Structure.xlsx' não encontrado.")
        return pd.DataFrame()
    try:
        df = pd.read_excel(path)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# ===========================================================
# 5. CONTEÚDO EXPLICATIVO
# ===========================================================
st.markdown("""
### Estrutura Detalhada de Níveis
Abaixo, a tabela apresenta a **descrição completa dos níveis globais** da SIG, com suas respectivas trilhas de carreira e escopos.
""")

# Remove o índice (coluna numérica automática)
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# ===========================================================
# 6. GRÁFICO MINIMALISTA DE DISTRIBUIÇÃO
# ===========================================================
st.markdown("""
### Distribuição por Banda de Carreira
A visualização abaixo mostra a distribuição dos níveis por **trilhas de carreira**, evidenciando a proporção entre os diferentes grupos.
""")

if "Career Path" in df.columns and "Global Grade" in df.columns:
    summary = df.groupby("Career Path")["Global Grade"].count().reset_index()

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(summary["Career Path"], summary["Global Grade"], width=0.5)
    ax.set_xlabel("")
    ax.set_ylabel("Quantidade de Níveis", fontsize=10)
    ax.set_title("", fontsize=12, weight="bold")
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("As colunas 'Career Path' e 'Global Grade' não foram encontradas.")
