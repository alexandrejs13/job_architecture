import streamlit as st

def setup_sidebar():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "Job Architecture";
                display: flex; align-items: center; justify-content: center;
                font-size: 1.5rem; font-weight: bold; padding: 20px 0;
                border-bottom: 2px solid #f0f2f6; margin-bottom: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def section(title):
    st.markdown(f"# {title}")
    st.markdown("---")
