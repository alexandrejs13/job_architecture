import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Job Families", page_icon="📂")

# --- CSS OPCIONAL PARA O CABEÇALHO DO CARTÃO ---
st.markdown("""
<style>
    .jf-header {
        background-color: #f0f7ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #2563eb;
        margin-bottom: 20px;
    }
    .jf-motto {
        font-style: italic;
        color: #555;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- DADOS (Baseados no seu exemplo anterior) ---
JOB_FAMILIES = {
    "tech": {
        "title": "Tecnologia & Engenharia",
        "icon": "💻",
        "motto": "Construindo o motor digital da nossa inovação.",
        "mission": "Responsável por desenhar, desenvolver e manter nossos produtos digitais, garantindo escalabilidade, segurança e alta performance.",
        "activities": ["Desenvolvimento Frontend/Backend", "DevOps & Infraestrutura Cloud", "QA e Testes Automatizados", "Arquitetura de Software"],
        "profile": "Profissionais com forte raciocínio lógico, apaixonados por código e resolução de problemas complexos."
    },
    "growth": {
        "title": "Vendas & Marketing (Growth)",
        "icon": "🚀",
        "motto": "A voz da empresa no mercado e o acelerador do crescimento.",
        "mission": "Focada em entender as necessidades do mercado, comunicar nosso valor e garantir que nossa solução chegue aos clientes certos.",
        "activities": ["Prospecção e qualificação de leads (SDR/BDR)", "Gestão do ciclo de vendas (Closers)", "Marketing Digital e Branding", "Customer Success e Expansão"],
        "profile": "Pessoas comunicativas, orientadas a metas, com alta resiliência e visão estratégica de negócios."
    },
    "ops": {
        "title": "Operações & Suporte",
        "icon": "⚙️",
        "motto": "A excelência invisível que faz tudo funcionar.",
        "mission": "Garantem que nossos processos internos e entregas ao cliente ocorram sem atrito, com máxima eficiência e qualidade.",
        "activities": ["Suporte Técnico ao Cliente (N1/N2)", "Gestão e otimização de processos", "Onboarding de novos clientes", "Logística e Facilities"],
        "profile": "Profissionais organizados, ágeis na resolução de crises imediatas e obcecados por eficiência."
    },
    "ga": {
        "title": "Pessoas & Finanças (G&A)",
        "icon": "🏛️",
        "motto": "A fundação sólida que sustenta nossa cultura e negócios.",
        "mission": "Garantem a saúde financeira, a segurança jurídica e o desenvolvimento e bem-estar dos nossos talentos.",
        "activities": ["Recrutamento e Seleção (Talent Acquisition)", "Planejamento Financeiro e Controladoria", "Jurídico e Compliance", "Administração de Pessoal"],
        "profile": "Pessoas analíticas, éticas, discretas e com alto senso de responsabilidade organizacional."
    }
}

# --- INTERFACE DO USUÁRIO ---
st.title("📂 Conheça Nossas Job Families")
st.markdown("Explore as áreas de especialização da empresa. Selecione uma família abaixo para entender seu propósito e escopo.")

# Criar opções legíveis para o seletor
opcoes_display = {f"{info['icon']} {info['title']}": key for key, info in JOB_FAMILIES.items()}
lista_opcoes = ["-- Selecione uma área --"] + list(opcoes_display.keys())

# Seletor
selecao = st.selectbox("Qual área você deseja explorar?", lista_opcoes)

st.divider()

# Lógica de Exibição
if selecao != "-- Selecione uma área --":
    # Recuperar os dados da chave selecionada
    chave = opcoes_display[selecao]
    dados = JOB_FAMILIES[chave]

    # Exibir Cabeçalho Estilizado
    st.markdown(f"""
    <div class="jf-header">
        <h2 style="margin:0; color: #1e3a8a;">{dados['icon']} {dados['title']}</h2>
        <p class="jf-motto">"{dados['motto']}"</p>
    </div>
    """, unsafe_allow_html=True)

    # Colunas para dividir o conteúdo
    col_esq, col_dir = st.columns([7, 3])

    with col_esq:
        st.subheader("🎯 Nossa Missão")
        st.write(dados['mission'])
        
        st.subheader("🛠️ O que fazemos")
        for atividade in dados['activities']:
            st.markdown(f"- {atividade}")

    with col_dir:
        # Caixa lateral para o perfil
        with st.container(border=True):
            st.subheader("👥 Quem somos")
            st.write(dados['profile'])

else:
    # Estado vazio inicial
    st.info("👆 Aguardando seleção no menu acima...")
