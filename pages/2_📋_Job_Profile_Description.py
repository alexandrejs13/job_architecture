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

    sub_df = filtered[filtered["Sub Job Family"] == sub]
    career_options = sorted(sub_df["Career Path"].dropna().unique())
    career = st.selectbox("Selecione a Trilha de Carreira:", career_options)

    career_df = sub_df[sub_df["Career Path"] == career]

    # === LISTA DE CARGOS ===
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
        st.info("Selecione até 3 cargos para comparar lado a lado.")
    else:
        st.markdown("---")
        st.markdown(f"### 🧾 Comparativo de Cargos — {career} ({sub})")

        # === GERA COLUNAS PARA CADA CARGO ===
        cols = st.columns(len(selected_labels))

        for idx, label in enumerate(selected_labels):
            with cols[idx]:
                selected_row = career_df_sorted.iloc[pick_options.index(label)]

                # --- Cabeçalho do Cargo ---
                st.markdown(f"#### {selected_row['Job Profile']}")
                st.markdown(f"<p style='color:#1E56E0; font-weight:bold;'>GG {selected_row['Global Grade']}</p>", unsafe_allow_html=True)

                # --- Dados estruturais ---
                st.markdown(
                    f"""
                    <div style='background-color:#ffffff; padding:10px; border-radius:8px; border:1px solid #e0e4f0;'>
                    <b>Família:</b> {selected_row['Job Family']}<br>
                    <b>Subfamília:</b> {selected_row['Sub Job Family']}<br>
                    <b>Carreira:</b> {selected_row['Career Path']}<br>
                    <b>Função:</b> {selected_row['Function Code']}<br>
                    <b>Disciplina:</b> {selected_row['Discipline Code']}<br>
                    <b>Código:</b> {selected_row['Full Job Code']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("<br>", unsafe_allow_html=True)

                # --- Blocos descritivos ---
                description_sections = [
                    ("Sub Job Family Description", "🧭 Sub Job Family Description"),
                    ("Job Profile Description", "🧠 Job Profile Description"),
                    ("Role Description", "🎯 Role Description"),
                    ("Grade Differentiation", "🏅 Grade Differentiation"),
                    ("Specific parameters / KPIs", "📊 KPIs / Specific Parameters"),
                    ("Competency", "💡 Competency"),
                    ("Qualifications", "🎓 Qualifications")
                ]

                for col_name, title in description_sections:
                    if col_name in selected_row and str(selected_row[col_name]).strip() and str(selected_row[col_name]).lower() != "nan":
                        st.markdown(f"**{title}**")
                        st.markdown(
                            f"""
                            <div style='background-color:#f9f9f9; padding:10px; border-radius:8px;
                                        border-left:4px solid #1E56E0; font-size:0.9rem; line-height:1.5;
                                        margin-bottom:12px;'>
                                {selected_row[col_name]}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
