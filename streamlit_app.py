# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path
import base64

# =========================================================
# CONFIG PAGE
# =========================================================
st.set_page_config(
    page_title="SIG Job Architecture",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# LOAD CSS (GLOBAL)
# =========================================================
assets_path = Path(__file__).parent / "assets"

for css_file in ["fonts.css", "theme.css", "layout.css", "menu.css"]:
    css_path = assets_path / css_file
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# =========================================================
# LOAD LOGO
# =========================================================
logo_path = assets_path / "SIG_Logo_RGB_Black.png"
if logo_path.exists():
    with open(logo_path, "rb") as f:
        encoded_logo = base64.b64encode(f.read()).decode()
    logo_html = f'<img src="data:image/png;base64,{encoded_logo}" class="top-logo">'
else:
    logo_html = ""

# =========================================================
# TOP NAVIGATION MENU
# =========================================================
menu_items = {
    "Job Architecture": "1_Job_Architecture.py",
    "Job Families": "2_Job_Families.py",
    "Job Profile Description": "3_Job_Profile_Description.py",
    "Job Maps": "4_Job_Maps.py",
    "Job Match (GGS)": "5_Job_Match.py",
    "Structure Level": "6_Structure_Level.py",
    "Dashboard": "7_Dashboard.py"
}

selected_page = st.session_state.get("selected_page", "Job Architecture")

def switch(page_name):
    st.session_state.selected_page = page_name
    st.switch_page("pages/" + menu_items[page_name])

# =========================================================
# RENDER NAV BAR
# =========================================================
nav_html = f"""
<div class="top-nav">
    <div class="nav-left">{logo_html}</div>
    <input type="checkbox" id="menu-toggle"/>
    <label for="menu-toggle" class="hamburger">&#9776;</label>

    <ul class="nav-menu">
"""
for item in menu_items:
    active_class = "active-link" if item == selected_page else ""
    nav_html += f'<li><a class="{active_class}" href="#" onclick="window.parent.postMessage({{"page":"{item}"}}, \'*\')">{item}</a></li>'

nav_html += "</ul></div>"

st.markdown(nav_html, unsafe_allow_html=True)

# =========================================================
# JS – Intercept clicks and call Streamlit switch_page()
# =========================================================
st.markdown("""
<script>
window.addEventListener("message", (event) => {
    if (event.data.page) {
        const page = event.data.page;
        window.location.href = "?page=" + page;
    }
});
</script>
""", unsafe_allow_html=True)

# =========================================================
# ROUTE HANDLER
# =========================================================
query_params = st.experimental_get_query_params()
if "page" in query_params:
    target = query_params["page"][0]
    if target in menu_items:
        switch(target)

# =========================================================
# DEFAULT HOME PAGE CONTENT
# =========================================================
st.write("")
st.write("### Bem-vindo ao Sistema de Job Architecture SIG")  
st.info("Use o menu superior para navegar entre os módulos.")
