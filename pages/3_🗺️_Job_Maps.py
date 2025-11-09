import streamlit as st
from utils.load_csv import load_csv_safe

st.set_page_config(page_title="Job Maps", layout="wide")

st.markdown(
    """
    <h1>🗺️ Job Maps</h1>
    <p style='color:#555'>Visualize a estrutura de cargos agrupada por Family e Subfamily.</p>
    """,
    unsafe_allow_html=True,
)

try:
    df = load_csv_safe("Job Profile.csv")
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

families = sorted(df["Job Family"].dropna().unique()) if "Job Family" in df.columns else []
col1, col2 = st.columns([1, 1])
with col1:
    family = st.selectbox("Selecione a Family", ["—"] + families)
with col2:
    subfamilies = (
        sorted(df[df["Job Family"] == family]["Sub Job Family"].dropna().unique())
        if family != "—" and "Sub Job Family" in df.columns
        else []
    )
    subfamily = st.selectbox("Selecione a Subfamily", ["—"] + subfamilies)

if family == "—":
    st.info("Selecione uma Family para visualizar.")
    st.stop()

base = df[df["Job Family"] == family]
if subfamily != "—":
    base = base[base["Sub Job Family"] == subfamily]

if base.empty:
    st.warning("Nenhum cargo encontrado.")
    st.stop()

for _, row in base.iterrows():
    st.markdown(f"### {row.get('Job Profile', 'Sem título')} — {row.get('Grade', '')}")
    for label, icon in [
        ("Role Description", "🎯"),
        ("Grade Differentiator", "🏅"),
        ("KPIs / Specific Parameters", "📊"),
        ("Qualifications", "🎓"),
    ]:
        txt = row.get(label, "")
        if isinstance(txt, str) and txt.strip():
            st.markdown(f"**{icon} {label}**")
            st.write(txt)
    st.divider()
