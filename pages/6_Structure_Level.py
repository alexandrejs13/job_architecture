import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
# 3. CABEÇALHO PADRÃO
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
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
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
        return pd.read_excel(path)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# ===========================================================
# 5. CONTEÚDO CONCEITUAL
# ===========================================================
st.markdown("""
### Estrutura Detalhada de Níveis

A **estrutura de níveis globais** é o alicerce que define como os cargos se organizam dentro das **trilhas de carreira da SIG**.  
Ela traz **consistência, transparência e mobilidade** entre áreas, permitindo que colaboradores compreendam claramente o escopo e impacto de cada posição.

Cada nível reflete uma combinação de **responsabilidade, complexidade e contribuição organizacional**, alinhada às práticas de mercado e à governança corporativa.
""")

# ===========================================================
# 6. TABELA DE NÍVEIS (SEM COLUNA DE ÍNDICE)
# ===========================================================
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# ===========================================================
# 7. VISUALIZAÇÃO GRÁFICA MINIMALISTA
# ===========================================================
st.markdown("""
### Distribuição por Banda de Carreira

O gráfico abaixo ilustra como os diferentes níveis se distribuem nas **trilhas de carreira**, destacando a proporção e progressão das bandas globais.
""")

if "Career Path" in df.columns and "Global Grade" in df.columns:
    summary = df.groupby("Career Path")["Global Grade"].count().reset_index()

    # estilo visual refinado e harmônico com a identidade SIG
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(7, 3))
    sns.barplot(
        data=summary,
        x="Career Path",
        y="Global Grade",
        color="#145efc",
        ax=ax
    )

    ax.set_xlabel("")
    ax.set_ylabel("Quantidade de Níveis", fontsize=10, labelpad=8)
    ax.set_title("Distribuição dos Níveis por Trilha de Carreira", fontsize=12, fontweight="bold", pad=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()

    st.pyplot(fig)
else:
    st.warning("As colunas 'Career Path' e 'Global Grade' não foram encontradas.")

st.divider()

# ===========================================================
# 8. CONCLUSÃO
# ===========================================================
st.markdown("""
### Interpretação

A **Estrutura de Níveis** é fundamental para manter coerência entre as funções e permitir comparabilidade entre países, áreas e grades de complexidade.  
Ela orienta decisões de **remuneração, progressão e desenho organizacional**, reforçando a meritocracia e a clareza de expectativas em toda a organização.
""")
