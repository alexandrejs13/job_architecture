import streamlit as st
import pandas as pd
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Structure Level",
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
# 3. CABEÇALHO AZUL PADRÃO
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
    max-width: 1100px !important;
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
    Structure Level
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. CONCEITO E ABORDAGEM METODOLÓGICA
# ===========================================================
st.markdown("""
## Conceito

A **estrutura de níveis (Structure Level)** é um dos componentes centrais da metodologia de **Job Architecture** e está alinhada aos princípios da **Willis Towers Watson (WTW)**.  
Seu objetivo é estabelecer uma estrutura hierárquica consistente, que permita comparar funções de forma transversal e assegurar equidade interna e competitividade externa.

Essa metodologia organiza os cargos corporativos com base em três dimensões principais:
1. **Escopo e Complexidade:** o nível de responsabilidade, autonomia e impacto sobre resultados.  
2. **Conhecimento e Experiência:** o grau de especialização técnica e amplitude de expertise exigida.  
3. **Influência e Liderança:** o alcance da atuação, seja individual, funcional ou organizacional.

A estrutura de níveis WTW é projetada para permitir comparações entre diferentes áreas funcionais e países, facilitando a governança global e a integração com sistemas de remuneração, sucessão e carreira.
""")

st.markdown("""
## Estrutura Hierárquica

Cada nível representa um conjunto de responsabilidades e requisitos distintos, normalmente agrupados em **faixas de carreira (Career Bands)** e **níveis globais (Global Grades)**.  
Essas categorias descrevem a progressão natural de desenvolvimento profissional, desde posições técnicas e operacionais até cargos de liderança executiva.

| Nível | Características Gerais |
|-------|--------------------------|
| **Entry / Foundation** | Foco na execução e aprendizado; supervisão direta; escopo limitado. |
| **Intermediate / Professional** | Aplicação de conhecimento técnico; autonomia moderada; foco em resultados operacionais. |
| **Senior Professional** | Atuação como especialista ou mentor; influência dentro da área; complexidade ampliada. |
| **Lead / Expert** | Responsável por projetos complexos ou liderança técnica; orientação estratégica limitada. |
| **Manager** | Gestão de equipes e recursos; tomada de decisão sobre processos e resultados. |
| **Director** | Direção de unidades organizacionais; foco em estratégia funcional e integração entre áreas. |
| **Executive** | Responsabilidade global ou corporativa; formulação de estratégias e políticas organizacionais. |
""")

st.divider()

# ===========================================================
# 5. CARREGAMENTO DO ARQUIVO EXCEL
# ===========================================================
file_path = Path("data/Level Structure.xlsx")

@st.cache_data
def load_level_structure(path):
    try:
        df = pd.read_excel(path)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar o arquivo: {e}")
        return pd.DataFrame()

if not file_path.exists():
    st.error(f"❌ Arquivo não encontrado: `{file_path}`")
    st.stop()

df = load_level_structure(file_path)

if df.empty:
    st.warning("⚠️ O arquivo foi encontrado, mas está vazio ou em formato inválido.")
    st.stop()

# ===========================================================
# 6. EXIBIÇÃO DA ESTRUTURA DE NÍVEIS
# ===========================================================
st.subheader("Tabela de Estrutura de Níveis")

st.dataframe(
    df.style.set_properties(**{
        "background-color": "white",
        "color": "#222",
        "border-color": "#ddd",
    }),
    use_container_width=True
)

# ===========================================================
# 7. ANÁLISE DE DISTRIBUIÇÃO (OPCIONAL)
# ===========================================================
if "Career Band" in df.columns:
    st.divider()
    st.subheader("Distribuição de Níveis por Career Band")

    counts = df["Career Band"].value_counts().reset_index()
    counts.columns = ["Career Band", "Quantidade"]

    st.bar_chart(data=counts.set_index("Career Band"))
