import streamlit as st
import pandas as pd
import os
# Importa a função visual global
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
# 2. APLICA O VISUAL GLOBAL (SIDEBAR, CORES ETC)
# ===========================================================
sidebar_logo_and_title()

# ===========================================================
# 3. ESTILOS CSS (INCLUINDO CABEÇALHO AZUL)
# ===========================================================
st.markdown("""
<style>
/* ===== CABEÇALHO PADRONIZADO ===== */
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
/* Corpo centralizado */
.block-container {
    max-width: 900px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
/* Fundo da aplicação */
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
/* ===== ESTILOS ORIGINAIS DA PÁGINA ===== */
.jf-description-card {
    background-color: #ffffff;
    border-left: 5px solid #145efc;
    padding: 25px;
    border-radius: 8px;
    margin-top: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
.jf-label {
    font-weight: 700;
    color: #145efc;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}
.jf-text {
    color: #333333;
    font-size: 1.1rem;
    line-height: 1.6;
}
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

if not data_loaded and not df.empty:
    st.warning(f"⚠️ Colunas esperadas não encontradas. Disponíveis: {', '.join(df.columns)}")

# ===========================================================
# 5. CONTEÚDO PRINCIPAL
# ===========================================================
st.markdown("""
Bem-vindo à nossa estrutura de **Job Families**.  
Aqui explicamos como organizamos as diferentes áreas de especialização dentro da empresa, garantindo clareza sobre **carreiras, mobilidade e desenvolvimento**.
""")

with st.container():
    col_analogy_icon, col_analogy_text = st.columns([1, 15])
    with col_analogy_icon:
        st.markdown("## 🧭")
    with col_analogy_text:
        st.subheader("O que é uma \"Job Family\"?")
        st.markdown("""
        Imagine que nossa empresa é uma **grande cidade**.  
        Uma Job Family é como um **bairro** dessa cidade.  
        Dentro de um bairro, você tem várias casas e prédios diferentes (os Cargos),  
        mas todos compartilham a mesma região, infraestrutura e propósito geral.
        """)

st.markdown("### Por que dividimos assim?")
c1, c2, c3 = st.columns(3)
with c1:
    st.success("**🛣️ Clareza de Carreira**\n\nFacilita entender para onde você pode crescer na sua especialização.")
with c2:
    st.info("**⚖️ Equidade**\n\nGarante que funções similares sejam tratadas de forma justa.")
with c3:
    st.warning("**🧠 Desenvolvimento**\n\nPermite treinamentos específicos para cada 'bairro'.")

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
    if df.empty:
        st.warning("Não foi possível carregar os dados para exibir o explorador.")
