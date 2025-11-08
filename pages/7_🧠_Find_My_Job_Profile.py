st.markdown("---")
st.subheader("🎯 Cargos mais compatíveis:")

compare_labels = []
for i, score in results:
    row = df.iloc[i]
    label = f"{row.get('Job Profile','-')} (GG {row.get('Global Grade','')})"
    compare_labels.append(label)

    with st.container(border=True):
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
            f"<div><span style='font-weight:700;color:#1E56E0;font-size:1rem;'>{row.get('Job Profile','-')}</span><br>"
            f"<span style='color:#333;'>Similaridade: <b>{score*100:.1f}%</b></span></div>"
            f"</div>", unsafe_allow_html=True
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
