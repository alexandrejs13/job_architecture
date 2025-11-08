import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section

data = load_data()
section("📋 Job Profile Description")

if "job_profile" not in data:
    st.error("Job Profile.csv não encontrado em /data")
else:
    df = data["job_profile"]

    # === SELEÇÃO DE FAMÍLIA ===
    families = sorted(df["Job Family"].dropna().unique())
    fam = st.selectbox("Selecione a Família:", families)

    filtered = df[df["Job Family"] == fam]
    subs = sorted(filtered["Sub Job Family"].dropna().unique())
    sub = st.selectbox("Selecione a Subfamília:", subs)

    sub_df = filtered[filtered["Sub Job Family"] == sub]

    # === SELEÇÃO DE CARREIRA ===
    career_options = sorted(sub_df["Career Path"].dropna().unique())
    career = st.selectbox("Selecione a Trilha de Carreira:", career_options)

    career_df = sub_df[sub_df["Career Path"] == career]

    # === LISTA DE CARGOS (MULTISELECT) ===
    def format_profile(row):
        grade = row.get("Global Grade", "")
        title = row.get("Job Profile", "")
        diff = f" — GG{int(grade)}" if str(grade).strip() and str(grade).isdigit() else ""
        return f"{title}{diff}"

    career_df_sorted = career_df.sort_values(by="Global Grade", ascending=False)
    pick_options = career_df_sorted.apply(format_profile, axis=1).tolist()

    selected_labels = st.multiselect(
        "Selecione até 3 cargos para comparar:",
        options=pick_options,
        max_selections=3
    )

    if not selected_labels:
        st.info("Selecione até 3 cargos para visualizar suas descrições detalhadas.")
    else:
        st.markdown("---")
        st.markdown(f"### 🧾 Comparativo de Cargos — {career} ({sub})")

        for label in selected_labels:
            selected_row = career_df_sorted.iloc[pick_options.index(label)]

            st.markdown(f"## {selected_row['Job Profile']} — GG {selected_row['Global Grade']}")
            st.write(f"**Família:** {selected_row['Job Family']}")
            st.write(f"**Subfamília:** {selected_row['Sub Job Family']}")
            st.write(f"**Trilha de Carreira:** {selected_row['Career Path']}")
            st.write(f"**Função:** {selected_row['Function Code']}")
            st.write(f"**Disciplina:** {selected_row['Discipline Code']}")
            st.write(f"**Código Completo:** {selected_row['Full Job Code']}")

            st.markdown("---")

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
                if col in selected_row and str(selected_row[col]).strip() and str(selected_row[col]).lower() != "nan":
                    html_block = f"""
<div style='
    background-color:#f9f9f9;
    padding:12px;
    border-radius:8px;
    border-left:4px solid #1E56E0;
    margin-bottom:10px;
    line-height:1.6;
    white-space:pre-wrap;'>
<b>{title}</b><br>{selected_row[col]}
</div>
"""
                    st.markdown(html_block, unsafe_allow_html=True)

            st.markdown("---")
