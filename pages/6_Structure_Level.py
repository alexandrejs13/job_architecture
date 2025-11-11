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
# 4. CONTEÚDO EXPLICATIVO
# ===========================================================
st.markdown("""
## 📘 Conceito  
Os **Structure Levels** definem a progressão de carreira dentro de cada família de cargos, refletindo **responsabilidades, complexidade e escopo**.

## 🔢 Níveis Típicos  
1. Entry  
2. Intermediate  
3. Senior  
4. Lead  
5. Manager  
6. Director  
7. Executive  

## 🎯 Importância  
Essa estrutura permite uma avaliação **justa e comparável** entre funções, apoiando decisões de **remuneração, promoção e sucessão**.
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
# 6. EXIBIÇÃO DA TABELA
# ===========================================================
st.subheader("📊 Estrutura de Níveis (Level Structure)")

st.dataframe(
    df.style.set_properties(**{
        "background-color": "white",
        "color": "#222",
        "border-color": "#ddd",
    }),
    use_container_width=True
)

# ===========================================================
# 7. INSIGHT VISUAL OPCIONAL (contagem por banda)
# ===========================================================
if "Career Band" in df.columns:
    st.divider()
    st.subheader("📈 Distribuição de Níveis por Career Band")

    counts = df["Career Band"].value_counts().reset_index()
    counts.columns = ["Career Band", "Quantidade"]

    st.bar_chart(data=counts.set_index("Career Band"))
