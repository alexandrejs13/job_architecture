import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from job_architecture.utils.ui import sidebar_logo_and_title


# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Career Levels & Structure",
    page_icon="📊",
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
# 3. CABEÇALHO AZUL PADRONIZADO
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
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/checkmark%20success.png" alt="icon">
    Estrutura de Níveis e Bandas de Carreira
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. CONTEÚDO INTRODUTÓRIO
# ===========================================================
st.markdown("""
A **Estrutura de Níveis** define a progressão de carreira dentro da SIG, garantindo consistência e transparência
em todas as áreas. Ela conecta os conceitos de **Job Architecture**, **Career Paths** e **Global Grades**, servindo como base
para remuneração, movimentações internas e desenvolvimento de carreira.

Cada nível representa um escopo de responsabilidade, complexidade e contribuição organizacional.  
Essa padronização ajuda a comparar posições globalmente e a manter equilíbrio entre diferentes funções.
""")

st.divider()

# ===========================================================
# 5. CARREGAMENTO DOS DADOS
# ===========================================================
@st.cache_data(ttl="1h")
def load_excel(path):
    try:
        return pd.read_excel(path)
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return pd.DataFrame()

df = load_excel("data/Level Structure.xlsx")

if df.empty:
    st.error("❌ Arquivo 'Level Structure.xlsx' não encontrado ou inválido.")
    st.stop()

# Remove a primeira coluna (índice ou código)
df = df.iloc[:, 1:] if len(df.columns) > 1 else df

# ===========================================================
# 6. VISUALIZAÇÃO DO DATAFRAME
# ===========================================================
st.subheader("Tabela de Estrutura de Níveis")
st.markdown("""
Abaixo estão as **bandas de carreira** definidas corporativamente, incluindo as descrições e níveis globais correspondentes.
""")

st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# ===========================================================
# 7. GRÁFICO MINIMALISTA — DISTRIBUIÇÃO POR BANDA
# ===========================================================
st.subheader("Distribuição por Banda de Carreira")

if "Career Band" in df.columns:
    contagem = df["Career Band"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(
        contagem.index,
        contagem.values,
        color="#145efc",
        width=0.5
    )

    # Legenda acima
    ax.set_title("Quantidade de Níveis por Banda de Carreira", fontsize=11, fontweight="bold", pad=15)

    # Remove bordas e grids verticais
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="y", linestyle="--", linewidth=0.6, color="#ccc", alpha=0.6)
    ax.grid(axis="x", visible=False)

    # Ajustes visuais minimalistas
    ax.set_facecolor("none")
    fig.patch.set_facecolor("none")
    ax.tick_params(axis="x", labelsize=10, colors="#222")
    ax.tick_params(axis="y", labelsize=9, colors="#222")
    ax.set_xlabel("")
    ax.set_ylabel("")

    # Valores acima das barras
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.2,
            f"{int(height)}",
            ha="center", va="bottom", fontsize=9, color="#222", fontweight="600"
        )

    plt.tight_layout(pad=1.2)
    st.pyplot(fig)

st.divider()

# ===========================================================
# 8. EXPLICAÇÃO FINAL
# ===========================================================
st.markdown("""
### Interpretação e Aplicação

A estrutura de níveis permite que cada colaborador compreenda onde sua posição se encontra dentro da organização.
Ela também facilita o **planejamento de sucessão**, **benchmarking salarial** e a **mobilidade de carreira** entre áreas distintas.

Os níveis não são apenas títulos hierárquicos — representam **impacto organizacional**, **complexidade das entregas**
e **autonomia esperada** em cada estágio da trajetória profissional.
""")
