# utils/ui.py
import streamlit as st
from pathlib import Path

# =========================================================
#   CONFIGURAÇÃO DO SIDEBAR CORPORATIVO SIG
# =========================================================

def inject_global_css():
    """Carrega o CSS global da pasta assets"""
    css_files = ["theme.css", "sidebar.css", "layout.css"]

    for css in css_files:
        css_path = Path("assets") / css
        if css_path.exists():
            with open(css_path) as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def sidebar_logo_and_title(logo_path, active_page, menu_items):
    inject_global_css()

    # SIDEBAR
    with st.sidebar:
        # LOGO
        st.markdown(
            f"""
            <div class="sig-sidebar-logo-container">
                <img src="{logo_path}" class="sig-sidebar-logo">
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Menu Title
        st.markdown(
            f"""
            <div class="sig-sidebar-title">SIG Job Architecture</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<hr class='sig-divider'>", unsafe_allow_html=True)

        # MENU ITEMS
        for label, icon_file, page_script in menu_items:
            icon_path = f"assets/icons/{icon_file}"

            is_active = label == active_page
            active_class = "active-item" if is_active else ""

            st.markdown(
                f"""
                <div class="sig-menu-item {active_class}">
                    <a href="/{page_script}" target="_self" class="sig-menu-link">
                        <img src="{icon_path}" class="sig-menu-icon">
                        {label}
                    </a>
                </div>
                """,
                unsafe_allow_html=True,
            )
