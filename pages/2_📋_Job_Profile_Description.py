import streamlit as st
from utils.load_csv import load_csv_safe

st.set_page_config(page_title="Job Profile Description", layout="wide")

st.markdown(
    """
    <h1>📘 Job Profile Description</h1>
    <p style='color:#555'>Visualize a descrição detalhada dos cargos, incluindo funções, responsabilidades e qualificações.</p>
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
    st.warning("Nenhum resultado encontrado.")
    st.stop()

for _, row in base.iterrows():
    st.divider()
    st.markdown(f"### 🧩 {row.get('Job Profile', 'Cargo sem título')}")
    st.write(f"**Grade:** {row.get('Grade', '')}")

    for label, icon in [
        ("Role Description", "🎯"),
        ("Grade Differentiator", "🏅"),
        ("KPIs / Specific Parameters", "📊"),
        ("Qualifications", "🎓"),
    ]:
        content = row.get(label, "")
        if isinstance(content, str) and content.strip():
            st.markdown(f"**{icon} {label}**")
            st.markdown(content)
