# -*- coding: utf-8 -*-
# utils/ui.py

import streamlit as st
from pathlib import Path

def sidebar_logo_and_title(
    logo_path: str,
    active_page: str,
    menu_items,
    icons_path: str = "assets/icons",
    pilula_color: str = "#145efc",
    sidebar_bg: str = "#f2efeb",
    text_color: str = "#000000",
):
    """
    Renderiza a sidebar unificada SIG com:
    - Logo
    - Título Job Architecture
    - Menu com ícones em formato pílula
    """

    # CSS da sidebar SIG (sand, texto preto, pílula azul)
    st.markdown(f"""
    <style>
        /* Fundo da sidebar */
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
        }}

        /* Remove padding interno exagerado da sidebar */
        section[data-testid="stSidebar"] > div:first-child {{
            padding-top: 0.5rem;
        }}

        /* Container do logo */
        .sig-sidebar-logo-container {{
            text-align: center;
            padding: 12px 8px 4px 8px;
        }}

        .sig-sidebar-logo-container img {{
            max-width: 150px;
        }}

        /* Título principal */
        .sig-sidebar-title {{
            text-align: center;
            font-weight: 700;
            font-size: 18px;
            margin-bottom: 12px;
            color: {text_color};
        }}

        /* Linha separadora */
        .sig-sidebar-separator {{
            border-bottom: 1px solid #d1c8bd;
            margin: 0 8px 12px 8px;
        }}

        /* Itens de menu (pílulas) */
        .sig-menu-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 10px;
            border-radius: 999px;
            margin: 4px 6px;
            cursor: pointer;
            font-size: 14px;
            text-decoration: none;
            color: {text_color};
        }}

        .sig-menu-item:hover {{
            background-color: rgba(20, 94, 252, 0.10);
        }}

        .sig-menu-item-active {{
            background-color: {pilula_color};
            color: #ffffff !important;
        }}

        .sig-menu-item img {{
            width: 20px;
            height: 20px;
        }}
    </style>
    """, unsafe_allow_html=True)

    # SIDEBAR
    with st.sidebar:
        # Logo
        logo_full_path = Path(logo_path)
        if logo_full_path.exists():
            st.markdown(
                f"""
                <div class="sig-sidebar-logo-container">
                    <img src="{logo_full_path.as_posix()}">
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.write("SIG")

        # Título
        st.markdown(
            f'<div class="sig-sidebar-title">Job Architecture</div>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="sig-sidebar-separator"></div>', unsafe_allow_html=True)

        # MENU
        for label, icon_file, target_page in menu_items:
            icon_path = Path(icons_path) / icon_file
            is_active = (label == active_page)

            img_html = ""
            if icon_path.exists():
                img_html = f'<img src="{icon_path.as_posix()}">'

            # classe de seleção
            item_class = "sig-menu-item"
            if is_active:
                item_class += " sig-menu-item-active"

            # Renderiza como link "fake" (texto clicável, mas navegação é pelo próprio Streamlit menu)
            # Aqui usamos apenas como indicação visual; a navegação entre páginas continua pelo menu nativo.
            st.markdown(
                f"""
                <div class="{item_class}">
                    {img_html}
                    <span>{label}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
