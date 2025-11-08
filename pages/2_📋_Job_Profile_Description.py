import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section

data = load_data()
section("📋 Job Profile Description")

if "job_profile" not in data:
    st.error("Job Profile.csv não encontrado em /data")
else:
    df = data["job_profile"]

    # === FILTROS PRINCIPAIS ===
    families = sorted(df["Job Family"].dropna().unique())
    fam = st.selectbox("Selecione a Família:", families)

    filtered = df[df["Job Family"] == fam]
    subs = sorted(filtered["Sub Job Family"].dropna().unique())
    sub = st.selectbox("Selecione a Subfamília:", subs)

    # Mostra todos os cargos da subfamília selecionada
    sub_df = filtered[filtered["Sub Job Family"] == sub]
    profiles = sorted(sub_df["Job Profile"].dropna().unique())
    profile = st.selectbox("Selecione o Cargo:", profiles)

    # === DADOS DO CARGO ===
    row = sub_df[sub_df["Job Profile"] == profile].iloc[0]

    st.markdown("---")
    st.markdown(f"## 🧾 {row['Job Profile']}")
    st.write(f"**Família:** {row['Job Family']}")
    st.write(f"**Subfamília:** {row['Sub Job Family']}")
    st.write(f"**Carreira:** {row['Career Path']}")
    st.write(f"**Nível Global:** {row['Global Grade']}")
    st.write(f"**Função:** {row['Function Code']}")
    st.write(f"**Disciplina:** {row['Discipline Code']}")
    st.write(f"**Código Completo:** {row['Full Job Code']}")

    st.markdown("---")

    # === DESCRIÇÕES E TEXTOS DETALHADOS ===
    description_sections = [
        ("Sub Job Family Description", "🧭 Sub Job Family Description"),
        ("Job Profile Description", "🧠 Job Profile Description"),
        ("Role Description", "🎯 Role Description"),
        ("Grade Differentiation", "🏅 Grade Differentiation"),
        ("Specific parameters / KPIs", "📊 Specific Parameters / KPIs"),
        ("Competency", "💡 Competency"),
        ("Qualifications", "🎓 Qualifications")
    ]

    for col, title in description_sections:
        if col in row and str(row[col]).strip() and str(row[col]).lower() != "nan":
            st.markdown(f"### {title}")
            st.markdown(f"<div style='background-color:#f9f9f9; padding:10px; border-radius:8px;'>{row[col]}</div>", unsafe_allow_html=True)
            st.markdown("---")

    # === OUTRAS POSIÇÕES RELACIONADAS ===
    st.markdown("### 📋 Outras posições relacionadas")
    st.dataframe(sub_df, use_container_width=True)
