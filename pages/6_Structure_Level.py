# ===========================================================
# 6_STRUCTURE_LEVEL.PY — PADRONIZADO COM HEADER, TEXTO E GRÁFICO MINIMALISTA
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
# 2. CSS GLOBAL E SIDEBAR
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
    max-width: 900px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 30px 0;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/process.png" alt="icon">
    Estrutura de Níveis (Structure Level)
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. CARREGAMENTO DE DADOS
# ===========================================================
@st.cache_data(ttl="1h")
def load_level_data():
    path = Path("data/Level Structure.xlsx")
    if not path.exists():
        st.error("❌ Arquivo 'Level Structure.xlsx' não encontrado na pasta `data/`.")
        return pd.DataFrame()
    try:
        df = pd.read_excel(path)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")
        return pd.DataFrame()

df = load_level_data()
if df.empty:
    st.stop()

# ===========================================================
# 5. CONTEÚDO TEXTUAL
# ===========================================================
st.markdown("""
A **estrutura de níveis (Structure Level)** é o alicerce da **Job Architecture da SIG**.  
Ela organiza os cargos em **faixas hierárquicas globais (Global Grades)** e **bandas de carreira (Career Bands)**, 
garantindo coerência e comparabilidade entre funções em diferentes áreas e regiões.

Cada nível reflete **escopo de responsabilidade**, **complexidade** e **impacto organizacional**.  
Essa padronização é essencial para manter **equidade interna**, **governança global** e **clareza de progressão de carreira**.
""")

st.divider()

# ===========================================================
# 6. TABELA DE ESTRUTURA
# ===========================================================
st.subheader("📘 Estrutura Detalhada de Níveis")

st.markdown("""
Abaixo, a tabela apresenta a **descrição completa dos níveis globais (Global Grades)**, 
com suas respectivas bandas de carreira e escopos.
""")

# Remove índice e exibe tabela limpa
st.dataframe(df.reset_index(drop=True), use_container_width=True)

st.divider()

# ===========================================================
# 7. VISUALIZAÇÃO MINIMALISTA
# ===========================================================
st.subheader("📊 Distribuição por Banda de Carreira")

if "Career Band" in df.columns:
    contagem = df["Career Band"].value_counts().reset_index()
    contagem.columns = ["Career Band", "Quantidade"]

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(
        contagem["Career Band"],
        contagem["Quantidade"],
        color="#145efc",
        edgecolor="#0e46c2",
        width=0.6
    )

    ax.set_facecolor("#f5f3f0")
    fig.patch.set_facecolor("#f5f3f0")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#cccccc")
    ax.spines["bottom"].set_color("#cccccc")
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5)
    ax.set_ylabel("Número de Níveis", fontsize=10, labelpad=10)
    ax.set_xlabel("Career Band", fontsize=10, labelpad=6)
    ax.set_title("Distribuição da Estrutura de Níveis", fontsize=13, fontweight="bold", pad=10)

    # Adiciona valores sobre as barras
    for bar in bars:
        yval = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            yval + 0.2,
            int(yval),
            ha="center",
            va="bottom",
            fontsize=9,
            color="#333"
        )

    st.pyplot(fig, use_container_width=True)
else:
    st.warning("Coluna 'Career Band' não encontrada no arquivo Excel.")

st.divider()

# ===========================================================
# 8. CONCLUSÃO
# ===========================================================
st.markdown("""
### 💡 Interpretação
- A **Career Band** representa o agrupamento macro de carreira (ex.: *Operational*, *Professional*, *Leadership*).  
- O **Global Grade** indica o nível global, usado como referência para estrutura, remuneração e mobilidade.  
- A combinação entre ambos define **consistência global** e **equidade entre funções** dentro da SIG.
""")
