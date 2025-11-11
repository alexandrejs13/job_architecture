import streamlit as st
from utils.ui import sidebar_logo_and_title
from pathlib import Path

st.set_page_config(page_title="Structure Level", layout="wide", initial_sidebar_state="expanded")

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
    max-width: 900px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
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

st.markdown("""
## Conceito  
Os **Structure Levels** definem a progressão de carreira dentro de cada família de cargos, refletindo responsabilidades e escopo.

## Níveis Típicos  
1. Entry  
2. Intermediate  
3. Senior  
4. Lead  
5. Manager  
6. Director  
7. Executive

## Importância  
Permitem uma avaliação justa e comparável entre funções, suportando decisões de remuneração e sucessão.
""")
