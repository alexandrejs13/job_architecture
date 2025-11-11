import streamlit as st
import pandas as pd
import re
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
# 3. HEADER PADRONIZADO
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
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.page-header img { width: 48px; height: 48px; }

[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
.block-container {
    max-width: 1000px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/process.png" alt="icon">
    Estrutura de Níveis (Structure Level)
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. EXPLICAÇÃO TÉCNICA (PADRÃO WTW)
# ===========================================================
st.markdown("""
## Conceito  
A **Estrutura de Níveis (Structure Level)** define a progressão de carreira e a diferenciação entre cargos com base em **responsabilidade, complexidade, impacto e escopo**.  
É uma abordagem alinhada às metodologias da **Willis Towers Watson (WTW)** para garantir consistência global e equidade interna.

## Princípios-Chave  
- **Amplitude de Impacto:** mede o alcance das decisões (local, regional ou global).  
- **Complexidade:** avalia o grau de autonomia e análise exigido.  
- **Influência:** relaciona-se ao nível de responsabilidade e tomada de decisão.  
- **Conhecimento Técnico e Liderança:** definem a senioridade e contribuição esperada.  

A estrutura possibilita uma **comparação objetiva** entre funções, servindo como base para remuneração, sucessão e desenvolvimento de carreira.
""")

# ===========================================================
# 5. CARREGAMENTO DE DADOS
# ===========================================================
file_path = Path("data/Level Structure.xlsx")
if not file_path.exists():
    st.error("❌ Arquivo `Level Structure.xlsx` não encontrado na pasta `data`.")
    st.stop()

try:
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
except Exception as e:
    st.error(f"Erro ao carregar o arquivo Excel: {e}")
    st.stop()

# ===========================================================
# 6. LIMPEZA E EXIBIÇÃO DA TABELA
# ===========================================================
# Remove colunas automáticas de índice
drop_cols = [col for col in df.columns if re.match(r'^(Unnamed|index|ID)$', str(col), flags=re.IGNORECASE)]
df_display = df.drop(columns=drop_cols, errors="ignore")

st.divider()
st.subheader("Tabela de Estrutura de Níveis")

st.dataframe(
    df_display.style.set_properties(**{
        "background-color": "white",
        "color": "#222",
        "border-color": "#ddd",
    }),
    use_container_width=True
)

# ===========================================================
# 7. GRÁFICO ESTÁTICO DE DISTRIBUIÇÃO
# ===========================================================
if "Career Band" in df.columns:
    st.divider()
    st.subheader("Distribuição de Níveis por Career Band")

    counts = df["Career Band"].value_counts().reset_index()
    counts.columns = ["Career Band", "Quantidade"]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(counts["Career Band"], counts["Quantidade"], color="#145efc", edgecolor="#0f3eb8")
    ax.set_xlabel("Career Band", fontsize=11, fontweight="bold")
    ax.set_ylabel("Quantidade de Níveis", fontsize=11)
    ax.set_title("Distribuição de Estrutura de Níveis", fontsize=13, fontweight="bold", pad=12)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    plt.xticks(rotation=45, ha="right")

    st.pyplot(fig, use_container_width=False)

# ===========================================================
# 8. RESUMO FINAL
# ===========================================================
st.markdown("""
### Conclusão  
A estrutura de níveis fornece uma visão integrada das **camadas de contribuição organizacional**, permitindo  
o alinhamento entre **avaliação de cargos, planos de carreira e práticas salariais**.  
Essa metodologia garante **coerência global** e **transparência interna**, pilares fundamentais do modelo de Job Architecture da SIG.
""")
