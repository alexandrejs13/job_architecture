import streamlit as st
from utils.ggs_factors import load_ggs_factors, filter_levels_by_supervisor, map_factors_to_level
from utils.job_match_engine import find_best_job_profile
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Job Match", layout="wide", initial_sidebar_state="expanded")

# --- Título ---
st.markdown("""
<h1 style='color:#145efc; font-weight:700;'>🔍 Job Match</h1>
""", unsafe_allow_html=True)

# ============================
# PARÂMETROS ORGANIZACIONAIS
# ============================

family_file = Path("job_architecture/data/Job Family.xlsx")
df_family = pd.read_excel(family_file)

col1, col2, col3 = st.columns(3)

familia = col1.selectbox("Família (Função)", sorted(df_family["Family"].unique()))
subfamilia = col2.selectbox("Subfamília (Disciplina)", sorted(df_family["SubFamily"].unique()))
superior = col3.selectbox("Cargo ao qual reporta (Filtro Rígido)", [
    "Supervisor",
    "Coordenador",
    "Gerente",
    "Diretor",
    "Vice-presidente",
    "Presidente / CEO"
])

allowed_levels = filter_levels_by_supervisor(superior)

# ============================
# FATORES GGS - ACCORDION
# ============================

st.markdown("## 🧠 Fatores de Complexidade (GGS)")

factors_json = load_ggs_factors()

factor_selection = {}

for factor_key, factor_data in factors_json.items():

    with st.expander(f"**{factor_data['label']}** – {factor_data['description_short']}"):

        levels = factor_data["levels"]

        level_titles = {k: v["title"] for k, v in levels.items()}

        selected_key = st.selectbox(
            f"Selecione uma opção para {factor_data['label']}",
            options=list(level_titles.keys()),
            format_func=lambda x: level_titles[x]
        )

        selected_info = levels[selected_key]

        factor_selection[factor_key] = {
            "selected": selected_key,
            "career_band": selected_info["career_band"],
            "career_level": selected_info["career_level
