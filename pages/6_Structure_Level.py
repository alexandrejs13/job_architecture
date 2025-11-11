# ===========================================================
# 6_STRUCTURE_LEVEL.PY — VISUALIZAÇÃO DE ESTRUTURA DE NÍVEIS
# ===========================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Structure Level",
    page_icon="🏗️",
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
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.page-header img {
    width: 54px;
    height: 54px;
}
.block-container {
    max-width: 1300px !important;
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
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/process.png" alt="icon">
    Estrutura de Níveis (Structure Level)
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. FUNÇÃO PARA CARREGAR OS DADOS
# ===========================================================
@st.cache_data(ttl="1h")
def load_data():
    path = Path("data/Level Structure.xlsx")
    if not path.exists():
        st.error("❌ Arquivo 'Level Structure.xlsx' não encontrado na pasta data/.")
        return pd.DataFrame()
    try:
        df = pd.read_excel(path)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# ===========================================================
# 5. CONTEÚDO PRINCIPAL — TABELA
# ===========================================================
st.markdown("""
Abaixo você pode visualizar a **estrutura de níveis corporativa (Global Grades e Career Bands)**, 
utilizada para padronizar a arquitetura de cargos da SIG.
""")

# Remove o índice numérico (coluna à esquerda)
st.dataframe(df.reset_index(drop=True), use_container_width=True)

st.divider()

# ===========================================================
# 6. VISUALIZAÇÃO GRÁFICA — DISTRIBUIÇÃO DE NÍVEIS
# ===========================================================
st.markdown("### 📊 Distribuição de Níveis por Career Band")

if "Career Band" in df.columns:
    contagem = df["Career Band"].value_counts().reset_index()
    contagem.columns = ["Career Band", "Quantidade"]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(contagem["Career Band"], contagem["Quantidade"], color="#145efc")
    ax.set_xlabel("Career Band", fontsize=11)
    ax.set_ylabel("Quantidade de Níveis", fontsize=11)
    ax.set_title("Distribuição de Estrutura de Níveis", fontsize=14, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    st.pyplot(fig, use_container_width=True)
else:
    st.warning("Coluna 'Career Band' não encontrada no arquivo Excel.")

st.divider()

# ===========================================================
# 7. INSIGHTS ADICIONAIS
# ===========================================================
st.markdown("""
### 💡 Interpretação
- **Career Band** representa o agrupamento hierárquico principal (ex.: Operational, Professional, Leadership).  
- **Global Grade** é o código numérico do nível global, usado para alinhamento interno.  
- Essa estrutura facilita análises comparativas de cargos, transições de carreira e políticas de remuneração.
""")
