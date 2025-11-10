import streamlit as st
import base64
import os

# ==============================================================================
# 1. CONFIGURAÇÕES
# ==============================================================================
FONT_REGULAR = "assets/fonts/PPSIGFlow-Regular.ttf"
FONT_SEMIBOLD = "assets/fonts/PPSIGFlow-SemiBold.ttf"
LOGO_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"
SIG_SKY = "#145efc"
TEXT_BLACK = "#000000"
TEXT_GRAY = "#333333"

# ==============================================================================
# 2. AUXILIARES
# ==============================================================================
def get_font_base64(file_path):
    if not os.path.exists(file_path): return None
    with open(file_path, "rb") as f: data = f.read()
    return base64.b64encode(data).decode("utf-8")

# ==============================================================================
# 3. SETUP UI (VERSÃO COM CABEÇALHO FIXO ACIMA DO MENU)
# ==============================================================================
def setup_sidebar():
    # --- 1. CARREGAMENTO DE FONTES ---
    font_reg_b64 = get_font_base64(FONT_REGULAR)
    font_sb_b64 = get_font_base64(FONT_SEMIBOLD)
    font_css = ""
    if font_reg_b64 and font_sb_b64:
        font_css = f"""
        @font-face {{ font-family: 'PP SIG Flow'; src: url(data:font/ttf;base64,{font_reg_b64}) format('truetype'); font-weight: 400; font-style: normal; }}
        @font-face {{ font-family: 'PP SIG Flow'; src: url(data:font/ttf;base64,{font_sb_b64}) format('truetype'); font-weight: 700; font-style: normal; }}
        html, body, [class*="css"] {{ font-family: 'PP SIG Flow', sans-serif !important; }}
        """

    # --- 2. CSS PARA ESTILO E POSICIONAMENTO ---
    st.markdown(
        f"""
        <style>
            {font_css}
            /* Limpeza de elementos nativos do Streamlit */
            header, footer, #MainMenu, .st-emotion-cache-h5rgjs {{ display: none !important; }}

            /* OCULTA O PRIMEIRO ITEM DO MENU ('APP') - ESTÁVEL */
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{
                display: none !important;
            }}

            /* --- BARRA LATERAL TRAVADA --- */
            [data-testid="stSidebar"] {{
                min-width: 300px !important; max-width: 300px !important; width: 300px !important;
                background-color: white !important;
                border-right: 1px solid #f0f0f0;
                /* Adicione padding-top para o conteúdo do sidebar não ficar por baixo do cabeçalho */
                padding-top: 190px; /* Ajuste este valor se o cabeçalho precisar de mais ou menos espaço */
            }}
            /* Esconde alça de redimensionamento */
            div[data-testid="stSidebar"] > div:last-child {{ display: none; }}

            /* --- CABEÇALHO PERSONALIZADO FIXO NO TOPO --- */
            /* Usamos o próprio [data-testid="stSidebar"] como base para o before */
            [data-testid="stSidebar"]::before {{
                content: ""; /* Necessário para pseudo-elementos */
                position: fixed; /* Fixa o cabeçalho no topo da viewport */
                top: 0;
                left: 0; /* Alinha com a borda esquerda da tela */
                width: 300px; /* Mesma largura da sidebar */
                height: 190px; /* Altura do nosso cabeçalho */
                background-color: white; /* Fundo branco do cabeçalho */
                border-bottom: 2px solid #f0f2f6; /* Divisor */
                z-index: 9999; /* Garante que fique acima de tudo */
                /* Conteúdo do cabeçalho (logo e texto) */
                background-image: url('{LOGO_URL}');
                background-repeat: no-repeat;
                background-position: center 20px;
                background-size: 100px auto;
            }}
            /* Texto do cabeçalho "Job Architecture" */
            [data-testid="stSidebar"]::after {{
                content: "Job Architecture";
                position: fixed;
                top: 140px; /* Posição do texto abaixo do logo */
                left: 0;
                width: 300px;
                text-align: center;
                color: {TEXT_BLACK} !important;
                font-size: 1.5rem;
                font-weight: 900;
                font-family: 'PP SIG Flow', sans-serif !important;
                z-index: 10000; /* Acima do 'before' se necessário */
            }}

            /* --- ESTILO DOS LINKS DO MENU --- */
            [data-testid="stSidebarNav"] > ul {{
                padding: 0 15px !important; /* Espaçamento lateral do menu */
                margin-top: 0px !important; /* Começa logo após o padding-top da sidebar */
            }}
            
            /* Links Inativos (Base) */
            [data-testid="stSidebarNav"] a {{
                color: {TEXT_GRAY} !important;
                font-weight: 500 !important;
                padding: 10px 24px !important; /* Espaçamento interno */
                margin-bottom: 4px !important; /* Espaço entre itens */
                background-color: transparent !important; /* Garante fundo transparente */
                text-decoration: none !important;
                border-radius: 0 !important; /* Remove qualquer arredondamento de pílula */
            }}

            /* Hover (Passar o mouse) */
            [data-testid="stSidebarNav"] a:hover {{
                background-color: #f0f0f0 !important; /* Fundo cinza suave no hover (nativo) */
                color: {SIG_SKY} !important; /* Texto azul SIG no hover */
            }}
            [data-testid="stSidebarNav"] a:hover span {{
                color: {SIG_SKY} !important;
            }}

            /* ITEM ATIVO (Realce padrão do Streamlit, mas com nosso texto) */
            [data-testid="stSidebarNav"] a[aria-current="page"] {{
                background-color: #e0e0e0 !important; /* Fundo cinza padrão do ativo */
                color: {TEXT_BLACK} !important; /* Texto preto no ativo */
                font-weight: 700 !important;
            }}
            [data-testid="stSidebarNav"] a[aria-current="page"] span {{
                color: {TEXT_BLACK} !important;
                font-weight: 700 !important;
            }}


            /* --- REMOÇÃO DE EMOJIS --- */
            [data-testid="stSidebarNav"] a span:first-child {{
                display: none !important;
            }}
            [data-testid="stSidebarNav"] a span:last-child {{
                display: inline-block !important; /* Garante que o texto apareça */
            }}

        </style>
        """,
        unsafe_allow_html=True
    )

    # Nota: Este hack do JS é a última tentativa para combater o flash de emojis
    # Ele tenta remover os spans de emoji o mais cedo possível
    st.components.v1.html("""
        <script>
            function removeEmojis() {
                var links = window.parent.document.querySelectorAll('[data-testid="stSidebarNav"] a');
                links.forEach(function(link) {
                    var spans = link.querySelectorAll('span');
                    if (spans.length > 1 && spans[0].textContent.trim().length === 1 && spans[0].textContent.match(/\\p{Emoji_Presentation}/u)) {
                        spans[0].style.display = 'none';
                    }
                });
            }
            // Tenta remover na carga inicial e novamente após um pequeno atraso
            removeEmojis();
            setTimeout(removeEmojis, 50);
            setTimeout(removeEmojis, 200);
        </script>
    """, height=0, width=0)
