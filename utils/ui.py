import streamlit as st
import pandas as pd
from pathlib import Path
from utils.ui import setup_sidebar, section

# ===========================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ===========================================================
st.set_page_config(
    page_title="Job Profile Description",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

setup_sidebar()
section("Job Profile Description", "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/business%20review%20clipboard.png")

# ===========================================================
# 2. CSS GLOBAL
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
    color: #202020;
}
.block-container {
    max-width: 1100px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}

/* GRID DE COMPARAÇÃO */
.jp-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 25px;
    margin-top: 25px;
}
.grid-cell {
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.05);
}
.section-cell {
    border-left-width: 6px;
    border-left-style: solid;
    padding: 18px;
    border-radius: 8px;
    background: #fff;
}
.section-title {
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-content {
    font-size: 0.95rem;
    line-height: 1.6;
}
.jp-p {
    margin-bottom: 6px;
}
.footer-cell {
    height: 10px;
}
</style>
""", unsafe_allow_html=True)

# ===========================================================
# 3. FUNÇÕES E DADOS
# ===========================================================
@st.cache_data
def load_job_profiles():
    file_path = "data/Job Profile.xlsx"
    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        for col in df.select_dtypes(include='object'):
            df[col] = df[col].fillna("").astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = load_job_profiles()

# ===========================================================
# 4. INTERFACE DE FILTRO
# ===========================================================
if not df.empty:
    families = sorted(df["Job Family"].dropna().unique())
    col1, col2, col3 = st.columns(3)

    with col1:
        fam = st.selectbox("1️⃣ Selecione a Família:", families, index=None, placeholder="Escolha...")

    with col2:
        subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].dropna().unique()) if fam else []
        sub = st.selectbox("2️⃣ Sub-Família:", subs, index=None, placeholder="Escolha...")

    with col3:
        paths = sorted(df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique()) if sub else []
        path = st.selectbox("3️⃣ Trilha:", paths, index=None, placeholder="Escolha...")

    # -------------------------------------------------------
    # Seleção dos perfis
    # -------------------------------------------------------
    if fam and sub and path:
        filtered = df[
            (df["Job Family"] == fam) &
            (df["Sub Job Family"] == sub) &
            (df["Career Path"] == path)
        ]

        profiles = sorted(filtered["Job Profile"].unique())
        selected = st.multiselect(
            "Selecione até 3 perfis para comparar:",
            profiles,
            max_selections=3
        )

        # ===========================================================
        # 5. EXIBIÇÃO DAS COMPARAÇÕES
        # ===========================================================
        if selected:
            st.markdown('<div class="jp-grid">', unsafe_allow_html=True)

            for s in selected:
                item = filtered[filtered["Job Profile"] == s].iloc[0]

                # Função auxiliar
                def block(color, icon, title, content):
                    return f"""
                    <div class="grid-cell section-cell" style="border-left-color:{color};">
                        <div class="section-title" style="color:{color};"><span>{icon}</span> {title}</div>
                        <div class="section-content">{content}</div>
                    </div>
                    """

                # Blocos
                html_blocks = ""

                html_blocks += block("#95a5a6", "🧭", "Sub Job Family Description", item.get("Sub Job Family Description", "-").replace("\n", "<p class='jp-p'>• "))
                html_blocks += block("#e91e63", "🧠", "Job Profile Description", item.get("Job Profile Description", "-").replace("\n", "<p class='jp-p'>• "))
                html_blocks += block("#673ab7", "🏛️", "Career Band Description", item.get("Career Band Description", "-").replace("\n", "<p class='jp-p'>• "))
                html_blocks += block("#1E56E0", "🎯", "Role Description", item.get("Role Description", "-").replace("\n", "<p class='jp-p'>• "))
                html_blocks += block("#ff9800", "🏅", "Grade Differentiator", item.get("Grade Differentiator", "-").replace("\n", "<p class='jp-p'>• "))
                html_blocks += block("#009688", "🎓", "Qualifications", item.get("Qualifications", "-").replace("\n", "<p class='jp-p'>• "))

                st.markdown(f"""
                <div class="grid-cell" style="border-left:5px solid #145efc;">
                    <h4 style="color:#145efc;">{item['Job Profile']}</h4>
                    <p><b>Global Grade:</b> {item.get('Global Grade', '-')}</p>
                    {html_blocks}
                    <div class="footer-cell"></div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("👆 Selecione até 3 perfis para comparar.")
    else:
        st.info("Selecione os filtros acima para visualizar os perfis.")
else:
    st.warning("⚠️ Não foi possível carregar a base de dados `Job Profile.xlsx`.")
