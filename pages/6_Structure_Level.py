import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
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
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.page-header img {
    width: 48px;
    height: 48px;
}
.block-container {
    max-width: 1000px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
h2 {
    font-weight: 700 !important;
    color: #000 !important;
    font-size: 1.35rem !important;
    margin-top: 25px !important;
    margin-bottom: 12px !important;
}
h3 {
    font-weight: 700 !important;
    color: #000 !important;
    font-size: 1.15rem !important;
}
.stAlert {
    background-color: #eef3ff !important;
    border-left: 4px solid #145efc !important;
    color: #000 !important;
    border-radius: 6px;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/process.png" alt="icon">
    Structure Level
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 3. CONCEITO E EXPLICAÇÃO PROFISSIONAL
# ===========================================================
st.markdown("""
## Conceito  
Os **Structure Levels** fazem parte da metodologia de **Job Architecture** proposta pela **Willis Towers Watson (WTW)**, 
servindo como uma estrutura padronizada para alinhar **níveis de complexidade, escopo e responsabilidade** em toda a organização.

## Estrutura Hierárquica  
Cada posição é classificada dentro de uma hierarquia global de níveis — também chamada de **Career Framework** — 
que garante coerência entre diferentes áreas, subsidiárias e regiões.  
Os níveis são definidos com base em critérios como:
- Impacto e escopo das decisões tomadas.  
- Grau de autonomia e complexidade das atividades.  
- Natureza da liderança exercida (individual ou de equipe).  
- Conhecimento técnico e comportamental exigido.  

## Importância Estratégica  
Essa padronização:
- Facilita comparações salariais e equidade interna.  
- Dá suporte à mobilidade de carreira (lateral e vertical).  
- Serve como base para **remuneração, sucessão e desenvolvimento** de talentos.  

## Estrutura Global Típica
A metodologia da WTW divide os níveis de carreira de forma crescente em escopo e responsabilidade:
1. **Entry** – Início de carreira, foco em execução.  
2. **Intermediate** – Profissional com experiência, executa com supervisão limitada.  
3. **Senior** – Atua de forma autônoma e influencia decisões.  
4. **Lead** – Especialista técnico ou líder funcional.  
5. **Manager** – Gestão de pessoas e processos.  
6. **Director** – Responsável por área estratégica e resultados amplos.  
7. **Executive** – Alta liderança e responsabilidade corporativa.  
""")

# ===========================================================
# 4. LEITURA DOS DADOS
# ===========================================================
@st.cache_data(ttl="1h")
def load_data():
    try:
        df = pd.read_excel("data/Level Structure.xlsx")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar arquivo: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("Não foi possível carregar o arquivo `Level Structure.xlsx`. Verifique se o arquivo está no diretório `/data`.")
    st.stop()

# ===========================================================
# 5. EXIBIÇÃO DA TABELA
# ===========================================================
st.divider()
st.subheader("Tabela de Estrutura de Níveis")

# Remove colunas numéricas ou não relevantes (ex: index, Unnamed)
drop_cols = [col for col in df.columns if re.match(r'^(Unnamed|index|ID)$', str(col), flags=re.IGNORECASE)]
df_display = df.drop(columns=drop_cols, errors="ignore")

st.dataframe(
    df_display.style.set_properties(**{
        "background-color": "white",
        "color": "#222",
        "border-color": "#ddd",
    }),
    use_container_width=True
)

# ===========================================================
# 6. GRÁFICO ESTÁTICO DE DISTRIBUIÇÃO
# ===========================================================
if "Career Band" in df.columns:
    st.divider()
    st.subheader("Distribuição de Estrutura de Níveis por Career Band")

    counts = df["Career Band"].value_counts().reset_index()
    counts.columns = ["Career Band", "Quantidade"]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(counts["Career Band"], counts["Quantidade"], color="#145efc", alpha=0.9)

    ax.set_xlabel("Career Band", fontsize=11, fontweight="bold")
    ax.set_ylabel("Quantidade de Níveis", fontsize=11)
    ax.set_title("Distribuição dos Níveis de Estrutura", fontsize=13, fontweight="bold", pad=12)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    plt.xticks(rotation=45, ha="right")

    # Rótulos de valor acima das barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.2, f'{int(height)}', 
                ha='center', va='bottom', fontsize=9, color="#000")

    st.pyplot(fig, use_container_width=False)

# ===========================================================
# 7. CONCLUSÃO
# ===========================================================
st.divider()
st.markdown("""
### Conclusão  
O framework de **Structure Levels** permite que a organização mantenha uma linguagem única sobre 
**posições, senioridade e responsabilidades**, em linha com as práticas de **Job Architecture** e os princípios da **Willis Towers Watson**.  
Ele é a base para análises consistentes de remuneração, desempenho e evolução de carreira global.
""")
