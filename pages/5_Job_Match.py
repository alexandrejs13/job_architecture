    # ===========================================================
    # 7. RENDERIZAÇÃO VISUAL (formato original restaurado e indentação corrigida)
    # ===========================================================
    st.markdown("---")
    st.subheader("🏆 Cargos Mais Compatíveis")

    if len(top3) < 1:
        st.warning("Nenhum resultado encontrado.")
        st.stop()

    cards_data = []
    for _, row in top3.iterrows():
        score_val = float(row["similarity"]) * 100
        score_bg = (
            "#28a745" if score_val > 85
            else "#1E56E0" if score_val > 75
            else "#fd7e14" if score_val > 60
            else "#dc3545"
        )
        lvl_name = ""
        gg_val = str(row["Global Grade"]).strip()
        if not df_levels.empty and "Global Grade" in df_levels.columns and "Level Name" in df_levels.columns:
            match = df_levels[df_levels["Global Grade"].astype(str).str.strip() == gg_val]
            if not match.empty:
                lvl_name = f"• {match['Level Name'].iloc[0]}"
        cards_data.append({
            "row": row,
            "score_fmt": f"{score_val:.1f}%",
            "score_bg": score_bg,
            "lvl": lvl_name
        })

    num_results = len(cards_data)
    grid_style = f"grid-template-columns: repeat({num_results}, 1fr);"
    grid_html = f'<div class="comparison-grid" style="{grid_style}">'

    # Cabeçalho
    for card in cards_data:
        grid_html += f"""
        <div class="grid-cell header-cell">
            <div class="fjc-title">{html.escape(card['row']['Job Profile'])}</div>
            <div class="fjc-gg-row">
                <div class="fjc-gg">GG {card['row']['Global Grade']} {card['lvl']}</div>
                <div class="fjc-score" style="background-color:{card['score_bg']};">{card['score_fmt']} Match</div>
            </div>
        </div>"""

    # Metadados
    for card in cards_data:
        d = card["row"]
        grid_html += f"""
        <div class="grid-cell meta-cell">
            <div class="meta-row"><strong>Família:</strong> {html.escape(str(d.get('Job Family','-')))}</div>
            <div class="meta-row"><strong>Subfamília:</strong> {html.escape(str(d.get('Sub Job Family','-')))}</div>
            <div class="meta-row"><strong>Carreira:</strong> {html.escape(str(d.get('Career Path','-')))}</div>
            <div class="meta-row"><strong>Cód:</strong> {html.escape(str(d.get('Full Job Code','-')))}</div>
        </div>"""

    # Seções coloridas — restauradas com alinhamento fixo
    sections_config = [
        ("🧭 Sub Job Family Description", "Sub Job Family Description", "#95a5a6"),
        ("🧠 Job Profile Description", "Job Profile Description", "#e91e63"),
        ("🏛️ Career Band Description", "Career Band Description", "#673ab7"),
        ("🎯 Role Description", "Role Description", "#145efc"),
        ("🏅 Grade Differentiator", "Grade Differentiator", "#ff9800"),
        ("🎓 Qualifications", "Qualifications", "#009688")
    ]

    for title, field, color in sections_config:
        for card in cards_data:
            content = str(card["row"].get(field, "-"))
            if field == "Qualifications" and (len(content) < 2 or content.lower() == "nan"):
                grid_html += '<div class="grid-cell section-cell" style="border-left-color: transparent; background: transparent; border: none;"></div>'
            else:
                grid_html += f"""
                <div class="grid-cell section-cell" style="border-left-color:{color};">
                    <div class="section-title" style="color:{color};">{title}</div>
                    <div class="section-content">{html.escape(content)}</div>
                </div>"""

    # Rodapé
    for _ in cards_data:
        grid_html += '<div class="grid-cell footer-cell"></div>'

    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)

    if float(top3.iloc[0]["similarity"]) < 0.6:
        st.info("💡 Aderência moderada. Tente refinar sua descrição.")
