import streamlit as st
from utils.ui_components import section
# Importa nossa nova função de visual global
from utils.ui import setup_sidebar

# ===========================================================
# CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(layout="wide", page_title="🏛️ Job Architecture")

# --- APLICA O VISUAL GLOBAL (BARRA LATERAL PRETA + LOGO) ---
# Isso deve vir logo após o set_page_config
setup_sidebar()

# ===========================================================
# ESTILOS DA PÁGINA (Conteúdo Principal)
# ===========================================================
# Mantive seus estilos originais para o conteúdo principal,
# pois eles não conflitam com a nossa sidebar.
st.markdown("""
<style>
.block-container {
  max-width: 1400px !important;
  padding: 2rem 2rem;
}
h1 { /* Título principal da 'section' */
  color: #1E56E0;
  font-weight: 800;
  font-size: 2.2rem !important;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
}
h2 { /* Subtítulos principais (##) */
  color: #1E56E0;
  font-weight: 700;
  font-size: 1.8rem !important;
  margin-top: 2.5rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 5px;
}
h3 { /* Subtítulos secundários (###) */
  font-weight: 600;
  font-size: 1.3rem !important;
  color: #333;
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}
p, li { /* Texto principal e itens de lista */
  font-size: 1.05rem;
  line-height: 1.6;
  color: #222;
}
/* Estiliza o st.info como um callout */
div[data-testid="stAlert"] {
    border: 1px solid #1E56E0;
    background-color: #f0f5ff;
    border-radius: 8px;
}
div[data-testid="stAlert"] p { /* Garante que o texto dentro do alerta também seja estilizado */
    color: #001f5c;
    font-size: 1.05rem;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# TÍTULO E CONTEÚDO
# ===========================================================

section("🏛️ Job Architecture")

st.markdown("""
A Job Architecture (JA) é a estrutura fundamental de P&C na SIG, que organiza e nivela os cargos em toda a organização. Ela serve como base para processos críticos de pessoas, garantindo consistência e clareza.
""")

st.markdown("## O que é a nossa Job Architecture?")
st.markdown("""
### Os 4 Elementos Chave:
* **Famílias de Cargos (Job Families):** Grandes grupos funcionais.
* **Sub-Famílias (Sub-Job Families):** Especializações dentro das famílias.
* **Níveis de Carreira (Career Levels):** Definem a senioridade e o foco do papel (ex: Gestão, Especialista, Projetos).
* **Perfis Genéricos (Generic Profiles):** Descrições padronizadas que servem de base para cada função.
""")

st.markdown("## Por que é importante?")
st.markdown("""
A Job Architecture não é apenas sobre títulos; ela habilita:
* **Caminhos de Carreira Claros:** Crescimento na SIG não se limita à gestão. Valorizamos e recompensamos a experiência funcional especializada através de bandas de carreira dedicadas (Especialista, Projetos, Vendas, Operações).
* **Benchmarking e Remuneração Justa:** O código do cargo (Job Code) liga nossa estrutura aos dados de mercado, garantindo análises salariais justas e equidade de gênero.
* **Desenvolvimento de Talento:** Facilita a identificação de próximos passos e oportunidades de desenvolvimento dentro e fora da função atual.
""")

st.markdown("## Princípios de Mapeamento: Instruções Essenciais")
st.markdown("""
Ao criar ou revisar uma posição, siga estas regras de ouro para garantir o mapeamento correto:
1.  **Foco no Conteúdo, Não na Pessoa:** O mapeamento baseia-se nas tarefas e responsabilidades do cargo, não nas habilidades ou desempenho do ocupante atual.
2.  **A Regra dos 50%:** Uma posição deve ser mapeada para um Perfil Genérico que cubra a maioria (pelo menos 50%) de suas tarefas e atividades.
3.  **Independência Hierárquica:** A arquitetura agrupa posições similares por natureza, independentemente de a quem reportam ou em que região estão.
""")

st.markdown("## Quando é necessário agir?")
st.markdown("""
* **Nova Posição:** Sempre requer um novo mapeamento e criação de Job Code antes do início do recrutamento.
* **Substituição (New Hire):** Se o conteúdo do trabalho permanece o mesmo, nenhum novo mapeamento é necessário. Se o escopo mudar significativamente (equipe, responsabilidades, requisitos), um novo mapeamento é exigido.
""")

st.markdown("## Governança e Ferramentas")
st.markdown("""
A Diretiva de JA, a ferramenta de Job Architecture e os formulários de aprovação estão disponíveis no SharePoint de Global Compensation & Benefits. Alterações de nível de carreira ou família exigem aprovações específicas (do HRBP local ao GEB/CEO, dependendo da senioridade do cargo).
""")

st.info("""
**Ponto de Atenção:** O Perfil Genérico não substitui a Descrição do Cargo (Job Description). Ao mapear a posição no SAP, ela herda automaticamente as características do perfil (grade, qualificações necessárias).
""")
