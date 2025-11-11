# ===========================================================
# 6_STRUCTURE_LEVEL.PY — VISÃO DE NÍVEIS E BANDAS DE CARREIRA
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
Abaixo, você pode visualizar os níveis de carreira definidos corporativamente,
incluindo as **descrições de banda** e **níveis globais (Global Grades)** correspondentes.
""")

st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# ===========================================================
# 7. GRÁFICO MINIMALISTA — DISTRIBUIÇÃO POR BANDA
# ===========================================================
st.subheader("Distribuição por Banda de Carreira")

if "Career Path" in df.columns:
    contagem = df["Career Path"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(6, 3.5))

    # Barras azul SIG minimalistas
    ax.bar(
        contagem.index,
        contagem.values,
        color="#145efc",
        edgecolor="none",
        width=0.5,
    )

    # Remover molduras e grades excessivas
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(axis="y", linestyle="--", linewidth=0.5, color="#ddd", alpha=0.6)

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(axis="x", labelrotation=0, colors="#222", labelsize=10)
    ax.tick_params(axis="y", colors="#222", labelsize=9)
    ax.set_facecolor("none")
    fig.patch.set_facecolor("none")

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
