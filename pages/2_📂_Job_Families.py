import streamlit as st
import pandas as pd
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Job Families",
    page_icon="📂",
    layout="wide"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
<style>
    .jf-description-card {
        background-color: #f8fafc;
        border-left: 5px solid #3b82f6;
        padding: 25px;
        border-radius: 8px;
        margin-top: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .jf-label {
        font-weight: 600;
        color: #64748b;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .jf-text {
        color: #1e293b;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-top: 10px;
    }
    .stSelectbox label {
        font-weight: bold;
        color: #1e3a8a;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÃO PARA CARREGAR DADOS ---
@st.cache_data(ttl="1h")
def load_job_family_data():
    # Tenta carregar do caminho padrão do repositório
    file_path = "data/Job Family.xlsx"
    
    if not os.path.exists(file_path):
        st.error(f"❌ Arquivo não encontrado: `{file_path}`. Verifique se a pasta 'data' está na raiz do projeto.")
        return pd.DataFrame() # Retorna DataFrame vazio em caso de erro
        
    try:
        df = pd.read_excel(file_path)
        # Normaliza os nomes das colunas para evitar erros com espaços extras
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")
        return pd.DataFrame()

# --- CARREGAMENTO DOS DADOS ---
df = load_job_family_data()

# Verificação básica se as colunas necessárias existem
required_columns = ["Job Family", "Sub Job Family", "Sub Job Family Description"]
data_loaded = not df.empty and all(col in df.columns for col in required_columns)

if not data_loaded and not df.empty:
     st.warning(f"⚠️ As colunas esperadas não foram encontradas no Excel. Colunas disponíveis: {', '.join(df.columns)}")

# ==============================================================================
# SEÇÃO 1: INTRODUÇÃO (Texto Fixo)
# ==============================================================================
st.title("Famílias de Cargos (Job Families)")
st.markdown(
    "Bem-vindo à nossa estrutura de Job Families. Aqui explicamos como organizamos as diferentes "
    "áreas de especialização dentro da empresa, garantindo clareza sobre carreiras e desenvolvimentos."
)

with st.container():
    col_analogy_icon, col_analogy_text = st.columns([1, 5])
    with col_analogy_icon:
        st.markdown("# 🧭")
    with col_analogy_text:
        st.subheader("O que é uma \"Job Family\"?")
        st.markdown("""
        Imagine que nossa empresa é uma **grande cidade**. Uma Job Family é como um **bairro** dessa cidade.
        Dentro de um bairro, você tem várias casas e prédios diferentes (os Cargos), mas todos compartilham a mesma região, infraestrutura e propósito geral. 
        """)

st.markdown("### Por que dividimos assim?")
c1, c2, c3 = st.columns(3)
with c1:
    st.info("**🛣️ Clareza de Carreira**\n\nFacilita entender para onde você pode crescer na sua especialização.")
with c2:
    st.info("**⚖️ Equidade**\n\nGarante que funções similares sejam tratadas de forma justa.")
with c3:
    st.info("**🧠 Desenvolvimento**\n\nPermite treinamentos específicos para cada \"bairro\".")

st.divider()

# ==============================================================================
# SEÇÃO 2: EXPLORADOR DE FAMÍLIAS (Dados do Excel)
# ==============================================================================
st.header("📂 Conheça Nossas Famílias")

if data_loaded:
    # --- SELETORES EM CASCATA ---
    col_sel1, col_sel2 = st.columns(2)

    with col_sel1:
        # 1. Lista de Famílias Únicas
        familias = sorted(df["Job Family"].dropna().unique())
        selected_family = st.selectbox("1️⃣ Selecione a Família (Job Family):", options=familias, index=None, placeholder="Escolha uma opção...")

    with col_sel2:
        # 2. Lista de Sub Famílias (filtrada pela escolha anterior)
        if selected_family:
            sub_familias = sorted(df[df["Job Family"] == selected_family]["Sub Job Family"].dropna().unique())
            selected_sub_family = st.selectbox("2️⃣ Selecione a Sub-Família:", options=sub_familias, index=None, placeholder="Escolha uma opção...")
        else:
            # Se não escolheu a família ainda, mostra um seletor desabilitado ou vazio
            selected_sub_family = st.selectbox("2️⃣ Selecione a Sub-Família:", options=[], disabled=True, placeholder="Aguardando seleção da Família...")

    # --- ÁREA DE EXIBIÇÃO DO CONTEÚDO ---
    if selected_family and selected_sub_family:
        # Filtrar o DataFrame para pegar a linha exata
        item_selecionado = df[
            (df["Job Family"] == selected_family) & 
            (df["Sub Job Family"] == selected_sub_family)
        ].iloc[0]
        
        descricao = item_selecionado.get("Sub Job Family Description", "Descrição não disponível.")

        # Exibir o cartão formatado
        st.markdown(f"""
        <div class="jf-description-card">
            <div class="jf-label">📖 Descrição da Sub-Família:</div>
            <div class="jf-text">
                {descricao}
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif selected_family and not selected_sub_family:
        st.info("👆 Agora selecione uma **Sub-Família** ao lado para ver os detalhes.")
        
else:
    if df.empty:
       st.warning("Não foi possível carregar os dados para exibir o explorador.")
