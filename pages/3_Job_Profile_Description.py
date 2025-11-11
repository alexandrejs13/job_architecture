import streamlit as st
import pandas as pd
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ===========================================================
# 1. CONFIGURAÇÃO INICIAL
# ===========================================================
st.set_page_config(
    page_title="Job Profile Description",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================================================
# 2. CSS GLOBAL E SIDEBAR UNIFICADA
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
    font-size: 1.35rem;
    border-radius: 12px;
    padding: 22px 36px;
    display: flex;
    align-items: center;
    gap: 18px;
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 40px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.page-header img {
    width: 48px;
    height: 48px;
}
.block-container {
    max-width: 950px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}
.job-card {
    background: white;
    border-left: 5px solid #145efc;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
}
.job-card h4 {
    color: #145efc;
    margin-bottom: 10px;
}
.job-card p {
    font-size: 0.95rem;
    color: #333;
    margin-bottom: 8px;
}
.job-card strong {
    color: #000;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/business%20review%20clipboard.png" alt="icon">
    Job Profile Description
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. FUNÇÕES AUXILIARES E CARREGAMENTO DE DADOS
# ===========================================================
@st.cache_data(ttl="1h")
def load_job_profile_data():
    file_path = "data/Job Profile.xlsx"
    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        for col in df.select_dtypes(include="object"):
            df[col] = df[col].astype(str).str.strip()
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
    Explore e compare até **3 perfis de cargo** simultaneamente para visualizar diferenças de descrição, carreira e qualificações.
    """)

    families = sorted(df["Job Family"].dropna().unique())
    col1, col2, col3 = st.columns(3)
    with col1:
        family = st.selectbox("1️⃣ Selecione a Família:", families)
    with col2:
        subfamilies = sorted(df[df["Job Family"] == family]["Sub Job Family"].dropna().unique())
        sub_family = st.selectbox("2️⃣ Selecione a Sub-Família:", subfamilies)
    with col3:
        paths = sorted(df[df["Sub Job Family"] == sub_family]["Career Path"].dropna().unique())
        path = st.selectbox("3️⃣ Selecione a Trilha:", paths)

    # Filtro principal
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

    # ===========================================================
    # 6. EXIBIÇÃO DOS RESULTADOS — COMPARAÇÃO
    # ===========================================================
    if selected_profiles:
        st.divider()
        st.subheader("📊 Comparação de Perfis")

        cols = len(selected_profiles)
        st.markdown(f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:25px;">', unsafe_allow_html=True)

        for profile in selected_profiles:
            item = filtered[filtered["Job Profile"] == profile].iloc[0]
            st.markdown(f"""
            <div class="job-card">
                <h4>{item.get("Job Profile", "-")}</h4>
                <p><strong>Global Grade:</strong> {item.get("Global Grade", "-")}</p>
                <p><strong>Career Band:</strong> {item.get("Career Band", "-")}</p>
                <p><strong>Job Family:</strong> {item.get("Job Family", "-")}</p>
                <p><strong>Sub Job Family:</strong> {item.get("Sub Job Family", "-")}</p>
                <hr style="border: none; border-top: 1px solid #eee; margin: 10px 0;">
                <p><strong>Descrição do Perfil:</strong></p>
                <p>{item.get("Job Profile Description", "-")}</p>
                <p><strong>Career Band Description:</strong></p>
                <p>{item.get("Career Band Description", "-")}</p>
                <p><strong>Role Description:</strong></p>
                <p>{item.get("Role Description", "-")}</p>
                <p><strong>Grade Differentiator:</strong></p>
                <p>{item.get("Grade Differentiator", "-")}</p>
                <p><strong>Qualifications:</strong></p>
                <p>{item.get("Qualifications", "-")}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("👆 Selecione até **3 perfis** para exibir a comparação detalhada.")
