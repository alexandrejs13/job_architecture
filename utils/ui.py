import streamlit as st

def setup_sidebar():
    st.markdown(
        """
        <style>
            #MainMenu, footer { visibility: hidden !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

def section(title):
    st.markdown(f"## {title}")
    st.markdown("---")
