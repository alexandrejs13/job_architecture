import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section

data = load_data()
section("📋 Job Profile Description")

if "job_profile" not in data:
    st.error("Job Profile.csv não encontrado em /data")
else:
    df = data["job_profile"]

    # === LINHA DE FILTROS PRINCIPAIS (com tamanhos personalizados) ===
    col1, col2, col3 = st.columns([1, 1.8, 0.8])  # Subfamília mais larga, trilha menor

    with col1:
        families = sorted(df["Job Family"].dropna().unique())
        fam = st.selectbox("Família", families, key="fam_select")

    filtered = df[df["Job Family"] == fam]

    with col2:
        subs = sorted(filtered["Sub Job Family"].dropna().unique())
        sub = st.selectbox("Subfamília", subs, key="sub_select")

    sub_df = filtered[filtered["Sub Job Family"] == sub]

    with col3:
        career_options = sorted(sub_df["Career Path"].dropna().unique())
        career = st.selectbox("Trilha de Carreira", career_options, key="career_select")

    career_df = sub_df[sub_df["Career Path"] == career]

    # === CSS para mostrar texto completo e ajustar largura dos cards ===
    st.markdown(
        """
        <style>
        /* Permite visualizar o texto completo dentro dos selectboxes após a seleção */
        div[data-baseweb="select"] > div {
            white-space: normal !important;
            height: auto !important;
            min-height: 38px;
        }
        div[data-baseweb="select"] span {
            white-space: normal !important;
        }

        /* Ajusta os cards descritivos para largura do conteúdo */
        .description-card {
            background-color: #f9f9f9;
            padding: 10px 14px;
            border-radius: 8px;
            border-left: 4px solid #1E56E0;
            font-size: 0.9rem;
            line-height: 1.5;
            display: inline-block; /* <-- largura se ajusta ao conteúdo */
            max-width: 95%;
            margin-bottom: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # === SELETOR DE CARGOS (MULTISELECT) ===
    st.markdown("<div style='margin-top:-10px'></div>", unsafe_allow_html=True)

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

    if selected_labels:
        st.markdown("---")
        st.markdown("### 🧾 Comparativo de Cargos Selecionados")

        cols = st.columns(len(selected_labels))

        for idx, label in enumerate(selected_labels):
            with cols[idx]:
                selected_row = career_df_sorted.iloc[pick_options.index(label)]

                # --- Cabeçalho do Cargo ---
                st.markdown(f"#### {selected_row['Job Profile']}")
                st.markdown(
                    f"<p style='color:#1E56E0; font-weight:bold;'>GG {selected_row['Global Grade']}</p>",
                    unsafe_allow_html=True
                )

                # --- Bloco de Classificação ---
                st.markdown(
                    f"""
                    <div style='background-color:#ffffff; padding:10px; border-radius:8px; border:1px solid #e0e4f0; display:inline-block;'>
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

                # --- Seções descritivas ---
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
                    if (
                        col_name in selected_row
                        and str(selected_row[col_name]).strip()
                        and str(selected_row[col_name]).lower() != "nan"
                    ):
                        st.markdown(f"**{title}**")
                        st.markdown(
                            f"<div class='description-card'>{selected_row[col_name]}</div>",
                            unsafe_allow_html=True
                        )
