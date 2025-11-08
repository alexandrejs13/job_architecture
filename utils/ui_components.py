import streamlit as st

def section(title):
    st.markdown(f"<h2 style='color:#1E56E0'>{title}</h2>", unsafe_allow_html=True)

def card(title, desc=""):
    st.markdown(
        f"<div class='card'><h4>{title}</h4><p style='color:#555'>{desc}</p></div>",
        unsafe_allow_html=True
    )
