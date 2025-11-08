import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section

data = load_data()
section("📋 Job Profile Description")

if "job_profile" not in data:
    st.error("Job Profile.csv não encontrado em /data")
else:
    df = data["job_profile"]

    families = sorted(df["Job Family"].dropna().unique())
    fam = st.selectbox("Selecione a Família:", families)

    filtered = df[df["Job Family"] == fam]
    subs = sorted(filtered["Sub Job Family"].dropna().unique())
    sub = st.selectbox("Selecione a Subfamília:", subs)

    sub_df = filtered[filtered["Sub Job Family"] == sub]
    profiles = sorted(sub_df["Job Profile"].unique())
    profile = st.selectbox("Selecione o Cargo:", profiles)

    # Linha selecionada
    row = sub_df[sub_df["Job Profile"] == profile].iloc[0]

    st.markdown("---")
    st.markdown(f"## 🧾 {row['Job Profile']}")
    st.write(f"**Família:** {row['Job Family']}")
    st.write(f"**Subfamília:** {row['Sub Job Family']}")
    st.write(f"**Nível Global:** {row['Global Grade']}")
    st.write(f"**Carreira:** {row['Career Path']}")
    st.write(f"**Código Completo:** {row['Full Job Code']}")
    st.write(f"**Função:** {row['Function Code']}")
    st.write(f"**Disciplina:** {row['Discipline Code']}")

    # Descrição automática
    st.markdown("### 🧠 Descrição do Cargo")
    desc = (
        f"O cargo **{row['Job Profile']}** integra a família **{row['Job Family']}**, "
        f"atuando na subfamília **{row['Sub Job Family']}**. "
        f"Este papel tem como foco o desempenho e coordenação de atividades relacionadas a "
        f"{row['Sub Job Family'].lower()}, com nível global **{row['Global Grade']}** "
        f"e enquadramento na trilha de carreira **{row['Career Path']}**."
    )
    st.info(desc)

    st.markdown("### 📊 Outras posições relacionadas")
    st.dataframe(sub_df, use_container_width=True)
