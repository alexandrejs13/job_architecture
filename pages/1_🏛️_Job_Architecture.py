import streamlit as st
from utils.ui import sidebar_logo_and_title, header

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(page_title="Job Architecture", layout="wide")

# ===========================================================
# 2. APLICA ESTILOS GLOBAIS E HEADER PADRÃO
# ===========================================================
with open("assets/header.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()
header("Job Architecture", "assets/icons/governance.png")

# ===========================================================
# 3. CONTEÚDO PRINCIPAL
# ===========================================================

st.markdown("""
<style>
.block-container {
  max-width: 1400px !important;
  padding: 2rem 2rem;
}
h1 {
  font-size: 2.2rem !important;
  font-weight: 600;
  color: #000;
  border-bottom: 2px solid #d0d0d0;
  padding-bottom: 10px;
}
h2 {
  font-size: 1.6rem !important;
  color: #000;
  margin-top: 2.5rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid #d0d0d0;
  padding-bottom: 5px;
}
h3 {
  font-weight: 600;
  font-size: 1.3rem !important;
  color: #333;
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}
p, li {
  font-size: 1.05rem;
  line-height: 1.6;
  color: #222;
}
div[data-testid="stAlert"] {
    border: 1px solid #145efc;
    background-color: #e8f0fe;
    border-radius: 8px;
}
div[data-testid="stAlert"] p {
    color: #001f5c;
    font-size: 1.05rem;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# 4. CONTEÚDO DA PÁGINA
# ===========================================================

st.markdown("## Introdução")
st.markdown("""
A **Job Architecture (JA)** é a estrutura fundamental de P&C na SIG que organiza e nivela os cargos em toda a organização.
Ela serve como base para processos críticos de pessoas, garantindo consistência, clareza e equidade global.
""")

st.markdown("## O que é a nossa Job Architecture?")
st.markdown("""
A arquitetura é composta por quatro elementos principais:

1. **Famílias de Cargos (Job Families):** Grandes grupos funcionais.
2. **Sub-Famílias (Sub-Job Families):** Especializações dentro das famílias.
3. **Níveis de Carreira (Career Levels):** Definem a senioridade e o foco do papel (Gestão, Especialista, Projetos, etc.).
4. **Perfis Genéricos (Generic Profiles):** Descrições padronizadas que servem de base para cada função.
""")

st.markdown("## Por que é importante?")
st.markdown("""
A Job Architecture não trata apenas de títulos, mas também de **gestão estratégica de talentos**:

- **Caminhos de Carreira Claros:** Crescimento na SIG vai além da gestão. Reconhecemos a evolução técnica e funcional.
- **Benchmarking e Remuneração Justa:** O código do cargo conecta nossa estrutura a dados de mercado para garantir justiça e equidade salarial.
- **Desenvolvimento de Talentos:** Permite identificar próximos passos e oportunidades de crescimento dentro e fora da área atual.
""")

st.markdown("## Princípios de Mapeamento")
st.markdown("""
Siga estas diretrizes ao criar ou revisar posições:

1. **Foco no Conteúdo, Não na Pessoa:** O mapeamento baseia-se nas tarefas e responsabilidades, não no desempenho individual.
2. **Regra dos 50%:** Uma posição deve se alinhar a um perfil genérico que cubra pelo menos metade de suas responsabilidades.
3. **Independência Hierárquica:** Agrupa cargos de natureza semelhante, independentemente da estrutura de reporte.
""")

st.markdown("## Quando agir?")
st.markdown("""
- **Nova Posição:** Sempre requer novo mapeamento e criação de Job Code antes do recrutamento.  
- **Substituição:** Se o conteúdo do trabalho for igual, o mapeamento pode ser mantido. Mudanças significativas de escopo exigem novo mapeamento.
""")

st.markdown("## Governança e Ferramentas")
st.markdown("""
A diretiva de JA, as ferramentas e os formulários de aprovação estão disponíveis no SharePoint de Global Compensation & Benefits.  
Alterações de nível de carreira ou família requerem aprovações específicas, variando do HRBP local até o GEB/CEO.
""")

st.info("""
**Ponto de Atenção:**  
O Perfil Genérico não substitui a Job Description.  
Ao mapear no SAP, o cargo herda automaticamente as características do perfil (grade, qualificações, responsabilidades).
""")
