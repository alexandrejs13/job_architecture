# ===========================================================
# Renderização comparativa (corrigido)
# ===========================================================
if selected_labels:
    st.markdown("---")
    st.markdown("### 🧾 Comparativo de Cargos Selecionados")

    rows = []
    for label in selected_labels:
        parts = re.split(r"\s*[–—-]\s*", label)
        label_grade = parts[0].replace("GG", "").strip() if parts else ""
        label_title = parts[1].strip() if len(parts) > 1 else label.strip()
        sel = career_df_sorted[
            career_df_sorted["Job Profile"].str.strip().str.lower() == label_title.lower()
        ]
        if label_grade:
            sel = sel[sel["Global Grade"].astype(str).str.strip() == label_grade]
        rows.append(sel.iloc[0] if not sel.empty else None)

    n = len(rows)
    grid_class = f"ja-grid cols-{n}"

    # Cabeçalhos
    html_cells = [f"<div>{header_badge(r['Job Profile'], r['Global Grade'])}</div>" if r is not None else "<div></div>" for r in rows]
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

    # Classificação
    html_cells = [f"<div>{class_box(r)}</div>" if r is not None else "<div></div>" for r in rows]
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)

    # Seções principais (com reconhecimento ampliado de nomes de colunas)
    SECTIONS = [
        ("🧭", "Sub Job Family Description", lambda r: safe_get(r, ["Sub Job Family Description", "Sub-Job Family Description"])),
        ("🧠", "Job Profile Description",   lambda r: safe_get(r, ["Job Profile Description", "Job Description", "Profile Description"])),
        ("🎯", "Role Description",          lambda r: safe_get(r, ["Role Description", "Primary Responsibilities", "Responsibilities", "Key Responsibilities"])),
        ("🏅", "Grade Differentiator",      lambda r: safe_get(r, [
            "Grade Differentiator", "Grade Differentiation",
            "Grade Differentiatior", "Grade Differentiators",
            "Level Differentiator"
        ])),
        ("📊", "KPIs / Specific Parameters", lambda r: safe_get(r, [
            "KPIs / Specific Parameters", "Specific Parameters / KPIs", "Key KPIs", "Performance Indicators", "KPIs"
        ])),
        ("🎓", "Qualifications",            lambda r: safe_get(r, [
            "Qualifications", "Required Qualifications", "Education", "Academic Background"
        ])),
    ]

    for emoji, title, getter in SECTIONS:
        html_cells = []
        for r in rows:
            if r is None:
                html_cells.append("<div></div>")
            else:
                raw = getter(r)
                html_cells.append("<div>" + cell_card(emoji, title, format_paragraphs(raw)) + "</div>")
        st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)
