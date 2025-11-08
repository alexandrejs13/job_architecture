import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section

data = load_data()
section("📋 Job Profile Description")

if "job_profile" not in data:
    st.error("Job Profile.csv não encontrado em /data")
else:
    df = data["job_profile"]

    # === LINHA DE FILTROS PRINCIPAIS (tamanhos proporcionais) ===
    col1, col2, col3 = st.columns([1, 2, 0.8])  # Subfamília mais larga, trilha menor

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

    # === CSS: ajuste de espaçamento e chips com GG + cargo ===
    st.markdown(
        """
        <style>
        /* Reduz distância entre filtros e multiselect */
        div[data-testid="stVerticalBlock"] > div:nth-child(3) {
            margin-top: -25px !important;
        }

        /* Mostra texto completo dentro dos selects */
        div[data-baseweb="select"] > div {
            white-space: normal !important;
            height: auto !important;
            min-height: 38px;
        }
        div[data-baseweb="select"] span {
            white-space: normal !important;
        }

        /* Ajuste visual dos cards descritivos */
        .description-card {
            background-color: #f9f9f9;
            padding: 10px 14px;
            border-radius: 8px;
            border-left: 4px solid #1E56E0;
            font-size: 0.9rem;
            line-height: 1.5;
            display: inline-block;
            max-width: 95%;
            margin-bottom: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        /* Chips de seleção (GG + cargo) */
        div[data-baseweb="tag"] span {
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            text-transform: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # === MULTISELECT (com GG + cargo no texto) ===
    def format_profile(row):
        grade = row.get("Global Grade", "")
        title = row.get("Job Profile", "")
        return f"GG{int(grade)} — {title}" if str(grade).isdigit() else title

    career_df_sorted = career_df.sort_values(by="Global Grade", ascending=False)
    pick_options = career_df_sorted.apply(format_profile, axis=1).tolist()

    st.markdown("<div style='margin-top:-15px'></div>", unsafe_allow_html=True)

    selected_labels = st.multiselect(
        "Selecione até 3 cargos para comparar:",
        options=pick_options,
        max_selections=3
    )

    # === BLOCO DE RESULTADO ===
    if selected_labels:
        st.markdown("---")
        st.markdown("### 🧾 Comparativo de Cargos Selecionados")

        cols = st.columns(len(selected_labels))

        for idx, label in enumerate(selected_labels):
            with cols[idx]:
                # Localiza o cargo selecionado
                label_grade = label.split(" — ")[0].replace("GG", "").strip()
                label_title = label.split(" — ")[1].strip() if "—" in label else label
                selected_row = career_df_sorted[
                    (career_df_sorted["Job Profile"] == label_title)
                    & (career_df_sorted["Global Grade"].astype(str) == label_grade)
                ]
                if selected_row.empty:
                    continue
                selected_row = selected_row.iloc[0]

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
