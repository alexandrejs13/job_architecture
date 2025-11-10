import streamlit as st
import os

# ==============================================================================
# 1. CONFIGURAÇÕES
# ==============================================================================
LOGO_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Blue.png"

# --- CORES DA PALETA SIG ---
SIG_SKY = "#145efc"     # Azul Principal (Pantone 2387 C)
TEXT_BLACK = "#000000"  # Preto Puro para Títulos

# ==============================================================================
# 2. SETUP UI (CSS GLOBAL DEFINITIVO)
# ==============================================================================
def setup_sidebar():
    st.markdown(
        f"""
        <style>
            /* Oculta elementos nativos */
            header, footer, #MainMenu, .st-emotion-cache-h5rgjs {{ visibility: hidden !important; }}
            [data-testid="stSidebarNav"] > ul:first-child > li:first-child {{ display: none !important; }}

            /* Sidebar Travada */
            [data-testid="stSidebar"] {{
                min-width: 300px !important; max-width: 300px !important; width: 300px !important;
                background-color: white !important; border-right: 1px solid #f0f0f0 !important;
            }}
            div[data-testid="stSidebar"] > div:last-child {{ display: none !important; }}

            /* Cabeçalho */
            [data-testid="stSidebarNav"]::before {{
                content: "Job Architecture"; display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
                height: 180px; background-image: url('{LOGO_URL}'); background-repeat: no-repeat; background-position: center 10px; background-size: 100px auto;
                color: {TEXT_BLACK} !important; font-size: 1.5rem; font-weight: 900; padding-bottom: 40px; margin-bottom: 20px; border-bottom: 2px solid #f0f2f6;
            }}

            /* --- MENU DE NAVEGAÇÃO --- */
            [data-testid="stSidebarNav"] > ul {{ padding: 0 15px !important; }}

            /* Reset dos Links */
            [data-
