import streamlit as st
import pandas as pd
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Profile Description",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. CSS GLOBAL E SIDEBAR
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

# ===========================================================
# 3. CABEÇALHO PADRÃO
# ===========================================================
st.markdown("""
<style>
.page-header {
    background-color: #145efc;
    color: white;
    font-weight: 750;
    font-size: 1.4rem;
    border-radius: 12px;
    padding: 22px 36px;
    display: flex;
    align-items: center;
    gap: 18px;
    width: 100%;
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.page-header img {
    width: 52px;
    height: 52px;
}
.block-container {
    max-width: 1100px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
/* GRID DE COMPARAÇÃO */
.jp-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 25px;
    margin-top: 25px;
}
.jp-card {
    background: #ffffff;
    border-radius: 10px;
    border-left: 6px solid #145efc;
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    padding: 20px;
}
.jp-card h4 {
    color: #145efc;
    font-weight: 750;
    margin-bottom: 6px;
}
.jp-meta {
    color: #333;
    font-size: 0.95rem;
    margin-bottom: 10px;
}
.jp-section {
    border-left: 5px solid var(--color);
    background-color: #fafafa;
    padding: 15px 18px;
    border-radius: 8px;
    margin-top: 14px;
}
.jp-section-title {
    font-weight: 700;
    font-size: 1rem;
    color: var(--color);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.jp-section-content {
    font-size: 0.94rem;
    line-height: 1.55;
    color: #333;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/business%20review%20clipboard.png" alt="icon">
    Job Profile Description
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. FUNÇÃO DE CARGA DE DADOS
# ===========================================================
@st.cache_data(ttl="1h")
def load_job_profile_data():
    file_path = "data/Job Profile.xlsx"
    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        for col in df.select_dtypes(include="object"):
            df[col] = df[col].astype(str).fillna("").str.strip()
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = load_job_profile_data()

# ===========================================================
# 5. CONTEÚDO PRINCIPAL
# ===========================================================
if df.empty:
    st.warning("⚠️ Base de dados não encontrada ou vazia.")
else:
    st.markdown("""
    Compare até **3 perfis de cargo** lado a lado.  
    As seções abaixo mostram descrições completas, níveis de carreira e qualificações.
    """)

    families = sorted(df["Job Family"].dropna().unique())
    col1, col2, col3 = st.columns(3)

    with col1:
        family = st.selectbox("1️⃣ Família:", families, index=None, placeholder="Selecione...")
    with col2:
        subfamilies = sorted(df[df["Job Family"] == family]["Sub Job Family"].dropna().unique()) if family else []
        sub_family = st.selectbox("2️⃣ Sub-Família:", subfamilies, index=None, placeholder="Selecione...")
    with col3:
        paths = sorted(df[df["Sub Job Family"] == sub_family]["Career Path"].dropna().unique()) if sub_family else []
        path = st.selectbox("3️⃣ Trilha:", paths, index=None, placeholder="Selecione...")

    if family and sub_family and path:
        filtered = df[
            (df["Job Family"] == family)
            & (df["Sub Job Family"] == sub_family)
            & (df["Career Path"] == path)
        ]

        profiles = sorted(filtered["Job Profile"].dropna().unique())
        selected_profiles = st.multiselect(
            "Selecione até 3 perfis de cargo para comparar:",
            options=profiles,
            max_selections=3
        )

        if selected_profiles:
            st.markdown('<div class="jp-grid">', unsafe_allow_html=True)
            for profile in selected_profiles:
                item = filtered[filtered["Job Profile"] == profile].iloc[0]

                def section_html(color, icon, title, content):
                    if not content or content.strip() == "":
                        content = "-"
                    content = content.replace("\n", "<br>")
                    return f"""
                    <div class="jp-section" style="--color:{color}">
                        <div class="jp-section-title">{icon} {title}</div>
                        <div class="jp-section-content">{content}</div>
                    </div>
                    """

                st.markdown(f"""
                <div class="jp-card">
                    <h4>{item.get('Job Profile', '-')}</h4>
                    <div class="jp-meta"><b>Global Grade:</b> {item.get('Global Grade', '-')}</div>
                    <div class="jp-meta"><b>Career Band:</b> {item.get('Career Band', '-')}</div>
                    {section_html("#95a5a6", "🏘️", "Sub Job Family Description", item.get("Sub Job Family Description", "-"))}
                    {section_html("#e91e63", "🧠", "Job Profile Description", item.get("Job Profile Description", "-"))}
                    {section_html("#673ab7", "🏛️", "Career Band Description", item.get("Career Band Description", "-"))}
                    {section_html("#1E56E0", "🎯", "Role Description", item.get("Role Description", "-"))}
                    {section_html("#ff9800", "🏅", "Grade Differentiator", item.get("Grade Differentiator", "-"))}
                    {section_html("#009688", "🎓", "Qualifications", item.get("Qualifications", "-"))}
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("👆 Selecione até **3 perfis** para visualizar a comparação detalhada.")
    else:
        st.info("Selecione as opções acima para exibir os perfis.")
