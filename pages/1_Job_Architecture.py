import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO GERAL
# ===========================================================
st.set_page_config(
    page_title="Job Architecture",
    page_icon="🏛️",
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
    font-size: 1.4rem;
    border-radius: 12px;
    padding: 22px 36px;
    display: flex;
    align-items: center;
    gap: 18px;
    width: 100%;
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.page-header img { width: 52px; height: 52px; }
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro","Helvetica",sans-serif;
}
.block-container {
    max-width: 950px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
.info-box {
    background-color: #ffffff;
    border-left: 5px solid #145efc;
    border-radius: 8px;
    padding: 20px 26px;
    margin-bottom: 25px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
h2, h3 {
    color: #000000 !important;
    font-weight: 700 !important;
}
.table-container {
    margin-top: 15px;
    margin-bottom: 35px;
}
</style>

<div class="page-header">
  <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png" alt="icon">
  Job Architecture
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 3. CONCEITO ESTRUTURADO
# ===========================================================
st.markdown("""
A **Job Architecture** é a estrutura corporativa que organiza e classifica todas as funções da empresa, 
permitindo uma visão clara e comparável de cargos, níveis e trajetórias de carreira.  
Ela é a base para a **governança de talentos**, **equidade interna** e **consistência global**, 
alinhando a estrutura organizacional aos princípios corporativos definidos pela metodologia da **Willis Towers Watson (WTW)**.
""")

st.markdown("""
### Propósito e Valor
A arquitetura de cargos estabelece a coerência entre papéis, responsabilidades e recompensas, 
servindo como referência para decisões estratégicas em:

- Estruturação de carreiras e trilhas de desenvolvimento  
- Benchmarking de remuneração e comparabilidade global  
- Planejamento de sucessão e mobilidade interna  
- Padronização de perfis funcionais e critérios de avaliação
""")

# ===========================================================
# 4. ELEMENTOS ESTRUTURAIS
# ===========================================================
st.markdown("""
### Estrutura Conceitual da Job Architecture
Os componentes principais se conectam para garantir a padronização global e a flexibilidade local.
""")

data = {
    "Elemento": [
        "Career Band",
        "Global Grade",
        "Job Family / Subfamily",
        "Generic Profile"
    ],
    "Definição": [
        "Agrupa papéis com similar escopo e impacto organizacional (e.g. Operational, Professional, Leadership).",
        "Nível global padronizado que define a complexidade, escopo e contribuição relativa do papel.",
        "Organiza as funções em áreas de especialização e subáreas específicas.",
        "Descrição corporativa genérica usada globalmente como referência para descrições locais."
    ],
    "Aplicação": [
        "Define amplitude de responsabilidade e influência.",
        "Permite comparabilidade global e alinhamento com o mercado.",
        "Orienta mobilidade e trilhas de desenvolvimento técnico e funcional.",
        "Garante consistência nas práticas de gestão e avaliação de cargos."
    ]
}
df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True, hide_index=True)

# ===========================================================
# 5. VISUALIZAÇÃO MINIMALISTA (CAREER BAND X GLOBAL GRADE)
# ===========================================================
st.markdown("""
### Estrutura Visual Simplificada
A relação entre **Career Bands** e **Global Grades** define a progressão da complexidade de papéis dentro da organização.
""")

career_bands = ["Operational", "Professional", "Managerial", "Executive"]
grades = [range(1, 3), range(3, 6), range(6, 9), range(9, 12)]

plt.figure(figsize=(9, 3.8))
for i, (band, gr) in enumerate(zip(career_bands, grades)):
    plt.plot(list(gr), [i]*len(gr), 'o-', linewidth=3, markersize=10, label=band)

plt.yticks(range(len(career_bands)), career_bands)
plt.xlabel("Global Grade", fontsize=11)
plt.ylabel("")
plt.title("Relação entre Career Bands e Global Grades", fontsize=13, weight='bold', pad=15)
plt.legend(title="Career Band", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(axis="y", color="#ddd", linestyle="-", linewidth=0.6)
plt.grid(axis="x", linestyle="", linewidth=0)
plt.tight_layout()
st.pyplot(plt.gcf())

# ===========================================================
# 6. CONTEÚDO CONCEITUAL ADICIONAL
# ===========================================================
st.markdown("""
### Interpretação
Cada **Career Band** representa um conjunto de papéis com escopo e complexidade similares.  
Os **Global Grades** permitem granularidade dentro de cada banda, assegurando que as funções sejam avaliadas de forma justa e comparável entre regiões e unidades de negócio.

Essa estrutura é fundamental para:

- Diferenciar responsabilidades sem sobreposição de níveis;  
- Assegurar equidade e coerência entre funções equivalentes;  
- Criar uma base sólida para gestão de remuneração, mobilidade e sucessão.
""")

st.markdown("""
### Conclusão
Uma arquitetura de cargos bem desenhada é o **alicerce da governança de talentos**.  
Ela conecta estratégia organizacional, gestão de desempenho e políticas de remuneração, 
permitindo decisões consistentes, transparentes e sustentáveis.
""")
