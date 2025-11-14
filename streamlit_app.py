# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path

# ============================
# CONFIG BÁSICO
# ============================
st.set_page_config(
    page_title="Job Architecture",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================
# CARREGAR CSS GLOBAL
# ============================
assets = Path("assets")

css_files = ["fonts.css", "theme.css", "menu.css"]

for css in css_files:
    css_path = assets / css
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ============================
# MENU SUPERIOR (SIG)
# ============================
st.markdown("""
<div class="top-menu">
    <div class="top-menu-left">
        <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/SIG_Logo_RGB_Black.png"
             class="sig-logo">
    </div>

    <div class="top-menu-center">
        <a class="menu-pill" href="?page=1">Job Architecture</a>
        <a class="menu-pill" href="?page=2">Job Families</a>
        <a class="menu-pill" href="?page=3">Job Profile Description</a>
        <a class="menu-pill" href="?page=4">Job Maps</a>
        <a class="menu-pill" href="?page=5">Job Match (GGS)</a>
        <a class="menu-pill" href="?page=6">Structure Level</a>
        <a class="menu-pill" href="?page=7">Dashboard</a>
    </div>
</div>
<br><br>
""", unsafe_allow_html=True)

# ============================
# REDIRECIONAMENTO
# ============================
query = st.query_params.get("page", "1")

if query == "1":
    import pages.1_Job_Architecture as page
    page.render()
