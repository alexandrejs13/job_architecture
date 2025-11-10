import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Job Families",
    page_icon="📂",
    layout="wide" # Layout wide para melhor aproveitamento horizontal profissional
)

# --- ESTILOS PERSONALIZADOS (CSS) ---
# Pequenos ajustes para elevar o visual padrão do Streamlit
st.markdown("""
<style>
    /* Destaque sutil para o cartão da família selecionada */
    .jf-header-selected {
        background: linear-gradient(to right, #f8fafc, #f1f5f9);
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #3b82f6; /* Azul profissional */
        margin-bottom: 25px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .jf-motto-text {
        color: #64748b; /* Cinza ardósia para texto secundário */
        font-style: italic;
        margin-top: 8px;
        font-size: 1.1em;
    }
    /* Ajuste de tipografia para os benefícios */
    .benefit-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- DADOS DAS FAMÍLIAS ---
JOB_FAMILIES = {
    "tech": {
        "title": "Tecnologia & Engenharia",
        "icon": "💻",
        "motto": "Construindo o motor digital da nossa inovação.",
        "mission": "Responsável por desenhar, desenvolver e manter nossos produtos digitais, garantindo escalabilidade, segurança e alta performance.",
        "activities": ["Desenvolvimento Frontend/Backend", "DevOps & Infraestrutura Cloud", "QA e Testes Automatizados", "Arquitetura de Software", "Ciência de Dados e IA"],
        "profile": "Profissionais com forte raciocínio lógico, apaixonados por código e resolução de problemas complexos."
    },
    "growth": {
        "title": "Vendas & Marketing (Growth)",
        "icon": "🚀",
        "motto": "A voz da empresa no mercado e o acelerador do crescimento.",
        "mission": "Focada em entender as necessidades do mercado, comunicar nosso valor e garantir que nossa solução chegue aos clientes certos.",
        "activities": ["Prospecção e qualificação (SDR/BDR)", "Vendas e Fechamento (Account Executives)", "Marketing Digital e Performance", "Branding e Comunicação"],
        "profile": "Pessoas comunicativas, orientadas a dados e resultados, com alta resiliência e visão estratégica."
    },
    "ops": {
        "title": "Operações & CX",
        "icon": "⚙️",
        "motto": "A excelência invisível que faz tudo funcionar.",
        "mission": "Garantem que nossos processos internos e a jornada do cliente ocorram sem atrito, com máxima eficiência e qualidade.",
        "activities": ["Customer Success (CS)", "Suporte Técnico", "Operações de Vendas (RevOps)", "Implementação/Onboarding"],
        "profile": "Profissionais organizados, empáticos, ágeis na resolução de crises e obcecados por eficiência."
    },
    "ga": {
        "title": "Pessoas & Finanças (G&A)",
        "icon": "🏛️",
        "motto": "A fundação sólida que sustenta nossa cultura e negócios.",
        "mission": "Viabilizam a operação garantindo saúde financeira, segurança jurídica e o desenvolvimento dos nossos talentos.",
        "activities": ["People & Culture (RH)", "Financeiro e Contabilidade", "Jurídico e Compliance", "Facilities e TI Interno"],
        "profile": "Pessoas analíticas, éticas, discretas e com alto senso de responsabilidade organizacional."
    }
}

# ==============================================================================
# SEÇÃO 1: INTRODUÇÃO E CONTEXTO (O "Porquê")
# ==============================================================================

# Cabeçalho Principal
st.title("Famílias de Cargos (Job Families)")
st.markdown(
    "Bem-vindo à nossa estrutura de Job Families. Aqui explicamos como organizamos as diferentes "
    "áreas de especialização dentro da empresa, garantindo clareza sobre carreiras e desenvolvimentos."
)

st.add_rows = st.container() # Espaçador virtual

# Bloco da Analogia (Usando um container para destaque visual)
with st.container():
    col_analogy_icon, col_analogy_text = st.columns([1, 5])
    with col_analogy_icon:
        st.markdown("# 🧭")
    with col_analogy_text:
        st.subheader("O que é uma \"Job Family\"?")
        st.markdown("""
        Imagine que nossa empresa é uma **grande cidade**. Uma Job Family é como um **bairro** dessa cidade.
        
        Dentro de um bairro, você tem várias casas e prédios diferentes (os Cargos), mas todos compartilham a mesma região, infraestrutura e propósito geral. 
        Não importa se você é um *Arquiteto Sênior* ou um *Engenheiro Júnior*; se ambos trabalham na construção do nosso produto, vocês "moram" no mesmo bairro.
        """)

# Bloco de Benefícios (Usando colunas para um layout profissional horizontal)
st.markdown("### Por que dividimos assim?")
col_ben1, col_ben2, col_ben3 = st.columns(3)

with col_ben1:
    with st.container(border=True): # Container com borda para parecer um "card"
        st.markdown("#### 🛣️ Clareza de Carreira")
        st.caption("Facilita entender para onde você pode crescer verticalmente ou horizontalmente dentro da sua área de especialização.")

with col_ben2:
    with st.container(border=True):
        st.markdown("#### ⚖️ Equidade")
        st.caption("Nos ajuda a garantir que funções com complexidade similar sejam tratadas de forma justa em termos de benefícios e remuneração.")

with col_ben3:
    with st.container(border=True):
        st.markdown("#### 🧠 Desenvolvimento")
        st.caption("Permite criar trilhas de treinamento e avaliações de desempenho específicas para as necessidades reais de cada \"bairro\".")

st.divider()

# ==============================================================================
# SEÇÃO 2: EXPLORADOR INTERATIVO
# ==============================================================================

st.header("📂 Conheça Nossas Famílias")
st.markdown("Explore os detalhes de cada bairro da nossa cidade corporativa.")

# Preparação do Seletor
opcoes_formatadas = {f"{dados['icon']}  {dados['title']}": chave for chave, dados in JOB_FAMILIES.items()}
chaves_ordenadas = list(opcoes_formatadas.keys())

# Layout do seletor centralizado ou com largura controlada
col_sel1, col_sel2 = st.columns([2, 1])
with col_sel1:
    familia_selecionada = st.selectbox(
        "Selecione uma família para visualizar:",
        ["-- Escolha uma opção --"] + chaves_ordenadas,
        label_visibility="collapsed", # Esconde o label padrão para um visual mais limpo
        index=0
    )

# Exibição Condicional do Conteúdo
if familia_selecionada != "-- Escolha uma opção --":
    chave_real = opcoes_formatadas[familia_selecionada]
    info = JOB_FAMILIES[chave_real]

    # --- CARTÃO DE DETALHES (Design Profissional) ---
    st.markdown("---") # Separador sutil

    # Cabeçalho do Cartão com CSS customizado
    st.markdown(f"""
    <div class="jf-header-selected">
        <h2 style="margin:0; color: #1e293b;">{info['icon']} {info['title']}</h2>
        <div class="jf-motto-text">"{info['motto']}"</div>
    </div>
    """, unsafe_allow_html=True)

    # Corpo do Cartão dividido em duas colunas principais
    col_main, col_side = st.columns([2, 1], gap="large")

    with col_main:
        st.subheader("🎯 Nossa Missão")
        st.write(info['mission'])

        st.subheader("🛠️ O que fazemos aqui")
        # Usando markdown para uma lista mais compacta e bonita
        for atividade in info['activities']:
            st.markdown(f"🔹 {atividade}")

    with col_side:
        # Sidebar interna para o perfil, destacada com uma cor de fundo sutil
        with st.container(border=True):
            st.markdown("### 👥 Perfil Típico")
            st.write(info['profile'])
            st.caption("*Este perfil é uma referência comportamental comum, não uma regra rígida.*")

else:
    # Estado Vazio (Call to Action)
    st.info("👆 Utilize o menu acima para selecionar uma família e descobrir seus detalhes.")
