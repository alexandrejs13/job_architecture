st.markdown("---")
st.subheader("🎯 Cargos mais compatíveis:")

# Ordenar resultados por Global Grade (maior → menor)
results_sorted = sorted(
    [(i, sims[i]) for i in idx[:top_n]],
    key=lambda x: float(df.iloc[x[0]].get("Global Grade", 0) or 0),
    reverse=True
)

compare_labels = []
for i, score in results_sorted:
    row = df.iloc[i]
    grade = str(row.get("Global Grade", "")).strip()
    job = row.get("Job Profile", "-").strip()
    compare_labels.append(f"{job} (GG {grade})")

    # CARD ELEGANTE UNIFICADO
    st.markdown(
        f"""
        <div style="
            background:#fff;
            border:1px solid #e4e8f4;
            border-left:6px solid #1E56E0;
            border-radius:12px;
            padding:18px 22px;
            margin-bottom:14px;
            box-shadow:0 1px 3px rgba(0,0,0,0.05);
        ">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <span style="font-weight:700;color:#1E56E0;font-size:1.05rem;">
                    GG {grade} — {job}
                </span>
                <span style="color:#333;font-size:0.95rem;">
                    Similaridade: <b>{score*100:.1f}%</b>
                </span>
            </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("📋 Ver detalhes"):
        st.markdown(f"**Família:** {row.get('Job Family','')}")
        st.markdown(f"**Subfamília:** {row.get('Sub Job Family','')}")
        st.markdown(f"**Carreira:** {row.get('Career Path','')}")
        st.markdown(f"**Função:** {row.get('Function Code','')}")
        st.markdown(f"**Disciplina:** {row.get('Discipline Code','')}")
        st.markdown(f"**Código:** {row.get('Full Job Code','')}")

        st.markdown("### 🧭 Sub Job Family Description")
        st.write(row.get("Sub Job Family Description","-") or "-")

        st.markdown("### 🧠 Job Profile Description")
        st.write(row.get("Job Profile Description","-") or "-")

        st.markdown("### 🎯 Role Description")
        st.write(row.get("Role Description","-") or "-")

        st.markdown("### 🏅 Grade Differentiator")
        gd = row.get("Grade Differentiator","") or row.get("Grade Differentiatior","") or "-"
        st.write(gd)

        st.markdown("### 📊 KPIs / Specific Parameters")
        kp = row.get("Specific parameters KPIs","") or row.get("Specific parameters / KPIs","") or "-"
        st.write(kp)

        st.markdown("### 🎓 Qualifications")
        st.write(row.get("Qualifications","-") or "-")

    st.markdown("</div>", unsafe_allow_html=True)
