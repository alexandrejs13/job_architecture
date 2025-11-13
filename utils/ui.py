# -*- coding: utf-8 -*-
# utils/ui.py

import streamlit as st
from pathlib import Path

def hide_streamlit_default_menu():
    """Esconde COMPLETAMENTE o menu nativo do Streamlit."""
    st.markdown("""
        <style>
            /* Remove o menu lateral nativo */
            section[data-testid="stSidebarNav"] {display: none !important;}
            .stSidebarNav {display: none !important;}
            [data-testid="stSidebarNavItems"] {display: none !important;}

            /* Remove título do menu nativo */
            .css-1vq4p4l, .css-1d391kg, .css-1oe5cao, header {visibility: hidden !important;}
        </style>
    """, unsafe_allow_html=True)


def apply_global_css():
    """Aplica o tema visual SIG em toda a aplicação."""
    st.markdown("""
    <style>

        /* Fundo BRANCO da aplicação */
        [data-testid="stAppViewContainer"] {
            background-color: white !important;
        }

        /* Sidebar Sand */
        section[data-testid="stSidebar"] {
            background-color: #f2efeb !important;
            padding-top: 10px;
        }

        /* Remove padding interno extra */
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0;
        }

        /* Estilos do menu SIG */
        .sig-menu-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 14px;
            margin: 4px 2px;
            border-radius: 999px;
            cursor: pointer;
            font-size: 15px;
            color: #000000;
            text-decoration: none;
        }

        .sig-menu-item:hover {
            background-color: rgba(20, 94, 252, 0.12);
        }

        .sig-menu-item-active {
            background-color: #145efc !important;
            color: white !important;
            font-weight: 600;
        }

        .sig-menu-item img {
            width: 22px;
            height: 22px;
        }

        /* Logo */
        .sig-logo-container {
            text-align: center;
            margin-bottom: 20px;
        }
        .sig-logo-container img {
            width: 140px;
            margin-top: 10px;
        }

        /* Título da sidebar */
        .sig-sidebar-title {
            text-align: center;
            font-size: 18px;
            margin-top: -5px;
            margin-bottom: 15px;
            font-weight: 700;
            color: #000000;
        }

    </style>
    """, unsafe_allow_html=True)


def sidebar_logo_and_title(
    logo_path,
    active_page,
    menu_items,
    icons_path="assets/icons"
):
    """Renderiza sidebar SIG e habilita navegação real com st.switch_page."""
    
    hide_streamlit_default_menu()
    apply_global_css()

    with st.sidebar:
        # Logo SIG
        logo = Path(logo_path)
        if logo.exists():
            st.markdown(
                f'<div class="sig-logo-container"><img src="{logo.as_posix()}"></div>',
                unsafe_allow_html=True
            )
        else:
            st.write("SIG")

        # Título
        st.markdown(
            '<div class="sig-sidebar-title">Job Architecture</div>',
            unsafe_allow_html=True
        )

        # MENU SIG
        for label, icon_file, target_page in menu_items:
            icon_path = Path(icons_path) / icon_file
            icon_html = f'<img src="{icon_path.as_posix()}">' if icon_path.exists() else ""

            is_active = (label == active_page)

            div_class = "sig-menu-item"
            if is_active:
                div_class += " sig-menu-item-active"

            if st.markdown(
                f"""
                <div class="{div_class}" onclick="window.location.href='/{target_page}'">
                    {icon_html}
                    {label}
                </div>
                """,
                unsafe_allow_html=True
            ):
                st.switch_page(target_page)
