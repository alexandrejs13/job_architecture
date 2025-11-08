# =========================
# ESTILO dos cards de matches
# =========================
st.markdown("""
<style>
.match-card{
  background:#fafafa;border:1px solid #e8edf5;border-radius:12px;
  padding:14px 16px;margin:12px 0;box-shadow:0 1px 2px rgba(0,0,0,.03);
  border-left:6px solid #2F6FEB;
}
.match-head{display:flex;align-items:center;justify-content:space-between;gap:12px;}
.match-title{font-weight:800;font-size:1.05rem;color:#1b2b52;}
.match-gg{display:inline-block;background:#eef3ff;color:#2F6FEB;font-weight:800;
  padding:4px 8px;border-radius:999px;margin-right:8px;}
.match-sim{color:#506079;font-weight:700;white-space:nowrap;}
</style>
""", unsafe_allow_html=True)


def _fmt(text: str) -> str:
    if not text or str(text).strip().lower() in ("nan", "none"):
        return "-"
    # quebra em parágrafos por linhas/pontos médios ou bullets existentes
    import re
    parts = re.split(r"\n+|•|\r", str(text).strip())
    return "".join(f"<p style='margin:0 0 6px 0'>{p.strip()}</p>" for p in parts if len(p.strip())>0)


def _class_box(r) -> str:
    return f"""
    <div style="background:#fff;border:1px solid #e8edf5;border-radius:8px;padding:10px;line-height:1.35">
      <b>Família:</b> {r.get('Job Family','-')}<br>
      <b>Subfamília:</b> {r.get('Sub Job Family','-')}<br>
      <b>Carreira:</b> {r.get('Career Path','-')}<br>
      <b>Função:</b> {r.get('Function Code','-')}<br>
      <b>Disciplina:</b> {r.get('Discipline Code','-')}<br>
      <b>Código:</b> {r.get('Full Job Code','-')}
    </div>
    """


def render_match_card(r, sim_pct: float):
    gg = str(r.get("Global Grade","")).strip()
    gg_badge = f"<span class='match-gg'>GG {gg}</span>" if gg else ""
    title = f"{gg_badge}<span>{r.get('Job Profile','(sem título)')}</span>"

    with st.container():
        st.markdown("<div class='match-card'>", unsafe_allow_html=True)

        # Cabeçalho do card (tudo no mesmo container)
        left, right = st.columns([1,0.22])
        with left:
            st.markdown(f"<div class='match-head'><div class='match-title'>{title}</div></div>", unsafe_allow_html=True)
        with right:
            st.markdown(f"<div class='match-sim'>Similaridade: {sim_pct:.1f}%</div>", unsafe_allow_html=True)

        # Detalhes dentro do mesmo card (expander)
        with st.expander("📋 Ver detalhes", expanded=False):
            st.markdown(_class_box(r), unsafe_allow_html=True)

            st.markdown("**🧭 Sub Job Family Description**")
            st.markdown(_fmt(r.get("Sub Job Family Description","-")), unsafe_allow_html=True)

            st.markdown("**🧠 Job Profile Description**")
            st.markdown(_fmt(r.get("Job Profile Description","-")), unsafe_allow_html=True)

            st.markdown("**🎯 Role Description**")
            st.markdown(_fmt(r.get("Role Description","-")), unsafe_allow_html=True)

            # aceita colunas com grafias diferentes no CSV
            grade_text = (r.get("Grade Differentiator") or r.get("Grade Differentiatior") 
                          or r.get("Grade Differentiation") or "-")
            st.markdown("**🥇 Grade Differentiator**")
            st.markdown(_fmt(grade_text), unsafe_allow_html=True)

            st.markdown("**🎓 Qualifications**")
            st.markdown(_fmt(r.get("Qualifications","-")), unsafe_allow_html=True)

            st.markdown("**📊 KPIs / Specific Parameters**")
            st.markdown(_fmt(r.get("Specific parameters KPIs") or r.get("Specific parameters / KPIs") or "-"),
                        unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# =========================
# RENDERIZAÇÃO DOS RESULTADOS
# (substitua o seu loop atual por este)
# =========================
# matches_top já deve estar ordenado do MAIOR pro MENOR (similaridade desc).
# Caso precise garantir:
matches_top = sorted(matches_top, key=lambda x: x["score"], reverse=True)

for m in matches_top:
    row = m["row"]          # pandas.Series ou dict com as colunas do CSV
    score = m["score"]*100  # converte para %
    # se vier Series, converter para dict p/ .get funcionar bem:
    r = row.to_dict() if hasattr(row, "to_dict") else row
    render_match_card(r, score)
