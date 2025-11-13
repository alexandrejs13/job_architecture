import streamlit as st
import pandas as pd
import os
from pathlib import Path
from job_architecture.utils.ui import sidebar_logo_and_title

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
As **Job Families** são pilares fundamentais da arquitetura de cargos e constituem agrupamentos estratégicos de funções que compartilham um propósito organizacional comum, naturezas de trabalho semelhantes e conjuntos de competências correlacionadas.

Essa classificação segue a metodologia global da **Willis Towers Watson (WTW)**, que estrutura os cargos de forma lógica e comparável, permitindo análises consistentes de remuneração, mobilidade e progressão de carreira.
""")

st.markdown("### O que é uma Job Family?")
st.markdown("""
Uma **Job Family** representa uma **área funcional ou disciplina profissional** dentro da organização.  
Ela agrupa posições que possuem **conhecimento técnico similar**, **natureza de contribuição análoga** e **propósitos de negócio interligados**.

Por exemplo, dentro da Job Family “Finanças”, podem existir cargos voltados a Contabilidade, Tesouraria, Planejamento e Análise Financeira, todos conectados pela mesma base funcional.
""")

st.markdown("### Estrutura Hierárquica e Subdivisões")
st.markdown("""
As **Sub Job Families** detalham as especializações técnicas ou funcionais existentes dentro de uma Job Family.  
Elas oferecem uma visão mais granular, permitindo distinguir, por exemplo, áreas como **Remuneração e Benefícios** ou **Folha de Pagamento** dentro da Job Family de Recursos Humanos.

Esse nível de detalhamento apoia a **consistência interna**, **precisão na avaliação de cargos** e **clareza na mobilidade lateral**.
""")

st.markdown("### Benefícios da Estruturação por Famílias de Cargos")
st.markdown("""
<div class="card-row">
    <div><b>🛣️ Clareza de Carreira</b><br>Define caminhos de desenvolvimento estruturados, com visibilidade das possibilidades de crescimento vertical e lateral dentro de uma mesma disciplina profissional.</div>
    <div><b>⚖️ Equidade Interna</b><br>Promove consistência nas comparações de cargos, assegurando que funções de complexidade semelhante recebam tratamento justo em termos de reconhecimento e recompensas.</div>
    <div><b>🧠 Desenvolvimento Estratégico</b><br>Permite a construção de trilhas de capacitação e planos de sucessão alinhados às competências críticas de cada família funcional.</div>
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
