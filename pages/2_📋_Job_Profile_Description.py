# ===========================================================
# Renderização das seções comparativas (com validação dinâmica)
# ===========================================================

# Lista base de seções
SECTIONS = [
    ("🧭", "Sub Job Family Description", lambda r: safe_get(r, "Sub Job Family Description")),
    ("🧠", "Job Profile Description",   lambda r: safe_get(r, "Job Profile Description")),
    ("🎯", "Role Description",          lambda r: safe_get(r, "Role Description")),
    ("🏅", "Grade Differentiator",      lambda r: safe_get(r, [
        "Grade Differentiator",
        "Grade Differentiation",
        "Grade Differentiatior",
        " Grade Differentiator",
        "Grade Differentiator ",
        "Grade Differentiators"
    ])),
    ("📊", "KPIs / Specific Parameters", lambda r: safe_get(r, ["Specific parameters KPIs", "Specific parameters / KPIs"])),
    ("🎓", "Qualifications",            lambda r: safe_get(r, "Qualifications")),
]

# Adiciona Competencies só se existir alguma coluna correspondente
competency_cols = [c for c in df.columns if c.strip().lower().startswith("competency")]
if competency_cols:
    SECTIONS.extend([
        ("💡", "Competency 1", lambda r: safe_get(r, "Competency 1")),
        ("💡", "Competency 2", lambda r: safe_get(r, "Competency 2")),
        ("💡", "Competency 3", lambda r: safe_get(r, "Competency 3")),
    ])

# Renderização final (somente se houver conteúdo real)
for emoji, title, getter in SECTIONS:
    # Verifica se pelo menos uma linha tem conteúdo
    has_content = any(getter(r) and getter(r).strip() not in ["", "-", "nan", "NaN", "None"] for r in rows if r is not None)
    if not has_content:
        continue  # pula a seção se todos os cargos estão vazios

    html_cells = []
    for r in rows:
        if r is None:
            html_cells.append("<div></div>")
        else:
            raw = getter(r)
            html_cells.append("<div>" + cell_card(emoji, title, format_paragraphs(raw)) + "</div>")
    st.markdown(f"<div class='{grid_class}'>" + "".join(html_cells) + "</div>", unsafe_allow_html=True)
