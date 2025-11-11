import streamlit as st
import pandas as pd
import os
from pathlib import Path
from utils.ui import sidebar_logo_and_title

st.set_page_config(page_title="Job Families", page_icon="📂", layout="wide", initial_sidebar_state="expanded")

# ===========================================================
# CSS GLOBAL + SIDEBAR
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

# ===========================================================
# HEADER PADRÃO
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
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.page-header img {
    width: 48px;
    height: 48px;
}
.block-container {
    max-width: 950px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
.jf-card {
    background: white;
    border-left: 5px solid #145efc;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
}
.card-row {
    display: flex;
    justify-content: space-between;
    gap: 20px;
}
.card-row > div {
    flex: 1;
    background: #fff;
    border-radius: 10px;
    border-left: 4px solid #145efc;
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    padding: 20px;
    min-height: 150px;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/people%20employees.png" alt="icon">
    Famílias de Cargos (Job Families)
</div>
""", unsafe_allow_html=True)

# ===========================================================
# FUNÇÃO DE LEITURA
# ===========================================================
@st.cache_data(ttl="1h")
def load_data():
    path = "data/Job Family.xlsx"
    if not os.path.exists(path):
        return pd.DataFrame()
    return pd.read_excel(path)

df = load_data()

# ===========================================================
# CONTEÚDO PRINCIPAL
# ===========================================================
st.markdown("""
As **Job Families** representam grandes agrupamentos de funções que compartilham propósitos, competências e caminhos de desenvolvimento similares.
""")

st.markdown("### O que é uma Job Family?")
st.markdown("""
Pense nas **Job Families** como grandes **bairros organizacionais**.  
Dentro de cada bairro, existem casas diferentes (os cargos), mas todos compartilham o mesmo propósito e estrutura.
""")

st.markdown("""
### Por que dividimos assim?
""")

st.markdown("""
<div class="card-row">
    <div><b>🛣️ Clareza de Carreira</b><br>Facilita entender para onde você pode crescer.</div>
    <div><b>⚖️ Equidade</b><br>Garante tratamento justo entre funções similares.</div>
    <div><b>🧠 Desenvolvimento</b><br>Permite trilhas de aprendizado mais focadas.</div>
</div>
""", unsafe_allow_html=True)

st.divider()

st.header("🔍 Explorador de Famílias")

if not df.empty:
    families = sorted(df["Job Family"].dropna().unique())
    selected_family = st.selectbox("Selecione a Família:", families)

    if selected_family:
        sub_fams = sorted(df[df["Job Family"] == selected_family]["Sub Job Family"].dropna().unique())
        selected_sub = st.selectbox("Selecione a Sub-Família:", sub_fams)
        if selected_sub:
            desc = df[(df["Job Family"] == selected_family) &
                      (df["Sub Job Family"] == selected_sub)]["Sub Job Family Description"].values
            if len(desc):
                st.markdown(f"""
                <div class="jf-card">
                    <b>📘 Descrição da Sub-Família:</b><br>{desc[0]}
                </div>
                """, unsafe_allow_html=True)
else:
    st.warning("Arquivo de dados não encontrado.")
