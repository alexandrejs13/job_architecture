# ===========================================================
# 2_JOB_FAMILIES.PY — ALINHADO COM O LAYOUT DA PÁGINA 1
# ===========================================================

import streamlit as st
import pandas as pd
import os
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Families",
    page_icon="📂",
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
# 3. CABEÇALHO AZUL PADRONIZADO
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
/* Títulos com tamanhos padronizados à página 1 */
h2 {
    font-weight: 700 !important;
    color: #000000 !important;
    font-size: 1.35rem !important;
    margin-top: 25px !important;
    margin-bottom: 12px !important;
}
h3 {
    font-weight: 700 !important;
    color: #000000 !important;
    font-size: 1.15rem !important;
}
/* Cards nivelados com altura fixa e layout consistente */
.card-container {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    margin-top: 20px;
}
.info-card {
    flex: 1;
    background-color: #ffffff;
    border-radius: 10px;
    padding: 18px;
    height: 160px; /* mesma altura para todos */
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    border-left: 5px solid transparent;
}
.info-card h4 {
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 8px;
}
.card-green { border-left-color: #4CAF50; background-color: #e8f5e9; }
.card-blue { border-left-color: #2196F3; background-color: #e3f2fd; }
.card-yellow { border-left-color: #f9a825; background-color: #fff8e1; }
.info-card p { font-size: 0.95rem; color: #333; line-height: 1.4; }

/* Caixa informativa refinada */
.stAlert {
    background-color: #eef3ff !important;
    border-left: 4px solid #145efc !important;
    color: #000 !important;
    border-radius: 6px;
}

/* Ajustes no seletor */
.stSelectbox label p {
    font-weight: 700 !important;
    color: #333333 !important;
    font-size: 1rem !important;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/people%20employees.png" alt="icon">
    Famílias de Cargos (Job Families)
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. FUNÇÕES E DADOS
# ===========================================================
@st.cache_data(ttl="1h")
def load_job_family_data():
    """Carrega os dados do Excel de Job Families."""
    file_path = "data/Job Family.xlsx"
    if not os.path.exists(file_path):
        st.error(f"❌ Arquivo não encontrado: `{file_path}`.")
        return pd.DataFrame()
    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")
        return pd.DataFrame()

df = load_job_family_data()
required_columns = ["Job Family", "Sub Job Family", "Sub Job Family Description"]
data_loaded = not df.empty and all(col in df.columns for col in required_columns)

# ===========================================================
# 5. CONTEÚDO PRINCIPAL
# ===========================================================
st.markdown("""
## Introdução  
A **Job Family** representa uma área funcional ampla que agrupa papéis relacionados dentro da organização.  
Ela promove **clareza, consistência e alinhamento global** sobre carreiras e especializações.
""")

st.markdown("""
## O que é uma Job Family?
Imagine que nossa empresa é uma **grande cidade**.  
Uma Job Family é como um **bairro** dessa cidade.  
Dentro de um bairro, você tem várias casas e prédios diferentes (os Cargos),  
mas todos compartilham a mesma região, infraestrutura e propósito geral.
""")

st.markdown("## Por que dividimos assim?")
st.markdown("""
<div class="card-container">
    <div class="info-card card-green">
        <h4>🛣️ Clareza de Carreira</h4>
        <p>Facilita entender para onde você pode crescer na sua especialização.</p>
    </div>
    <div class="info-card card-blue">
        <h4>⚖️ Equidade</h4>
        <p>Garante que funções similares sejam tratadas de forma justa.</p>
    </div>
    <div class="info-card card-yellow">
        <h4>🧠 Desenvolvimento</h4>
        <p>Permite treinamentos específicos para cada “bairro”.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ===========================================================
# 6. EXPLORADOR DE FAMÍLIAS
# ===========================================================
st.header("🔍 Explorador de Famílias")

if data_loaded:
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        familias = sorted(df["Job Family"].dropna().unique())
        selected_family = st.selectbox(
            "1️⃣ Selecione a Família (Job Family):",
            options=familias,
            index=None,
            placeholder="Escolha uma opção..."
        )

    with col_sel2:
        if selected_family:
            sub_familias = sorted(df[df["Job Family"] == selected_family]["Sub Job Family"].dropna().unique())
            selected_sub_family = st.selectbox(
                "2️⃣ Selecione a Sub-Família:",
                options=sub_familias,
                index=None,
                placeholder="Escolha uma opção..."
            )
        else:
            selected_sub_family = st.selectbox(
                "2️⃣ Selecione a Sub-Família:",
                options=[],
                disabled=True,
                placeholder="Aguardando seleção da Família..."
            )

    if selected_family and selected_sub_family:
        item = df[(df["Job Family"] == selected_family) & (df["Sub Job Family"] == selected_sub_family)].iloc[0]
        descricao = item.get("Sub Job Family Description", "Descrição não disponível.")

        st.markdown(f"""
        <div class="jf-description-card">
            <div class="jf-label">📖 Descrição da Sub-Família</div>
            <div class="jf-text">{descricao}</div>
        </div>
        """, unsafe_allow_html=True)
    elif selected_family and not selected_sub_family:
        st.info("👆 Selecione uma **Sub-Família** para ver os detalhes.")
else:
    st.warning("⚠️ Não foi possível carregar os dados para exibir o explorador.")
