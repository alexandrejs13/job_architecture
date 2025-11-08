import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section
from utils.search_engine import find_best_match

data = load_data()
section("🧠 Find My Job Profile")

if "job_profile" not in data:
    st.error("Job Profile.csv não encontrado em /data")
else:
    text = st.text_area(
        "Descreva as atividades do cargo:",
        placeholder="Exemplo: responsável pelo fechamento da folha de pagamento, controle de encargos e gestão de equipe..."
    )
    
    if st.button("Encontrar perfil correspondente"):
        with st.spinner("Analisando descrição..."):
            result, score = find_best_match(text, data["job_profile"])
        
        if result is None:
            st.warning("Nenhum resultado encontrado.")
        else:
            st.success(f"Cargo sugerido: **{result['Job Profile']}** ({score*100:.1f}% de similaridade)")
            st.dataframe(result.to_frame().T, use_container_width=True)
