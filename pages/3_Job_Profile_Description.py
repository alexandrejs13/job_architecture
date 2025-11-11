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
# 2. CSS GLOBAL
# ===========================================================
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

sidebar_logo_and_title()

# ===========================================================
# 3. CABEÇALHO PADRONIZADO
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
.page-header img { width: 48px; height: 48px; }

.block-container {
    max-width: 900px !important; /* largura máxima igual às outras páginas */
    padding-left: 40px !important;
    padding-right: 40px !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
}

/* Cartões de perfil */
.job-card {
    background:white;
    border-left:5px solid #145efc;
    padding:20px;
    border-radius:10px;
    box-shadow:0 4px 8px rgba(0,0,0,0.05);
}
.job-card h4 {
    color:#145efc;
    margin-bottom:8px;
}
.job-card .meta {
    background:#fff;
    border-top:1px solid #e0e0e0;
    border-bottom:1px solid #e0e0e0;
    font-size:.9rem;
    color:#555;
    padding:12px 16px;
    margin-top:10px;
}
.job-card .desc {
    margin-top:12px;
    color:#333;
    line-height:1.6;
    font-size:.95rem;
}
</style>

<div class="page-header">
    <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/business%20review%20clipboard.png" alt="icon">
    Job Profile Description
</div>
""", unsafe_allow_html=True)

# ===========================================================
# 4. CARREGAMENTO DE DADOS
# ===========================================================
@st.cache_data(ttl="1h")
def load_job_profiles():
    """Lê o arquivo Excel de Job Profiles."""
    try:
        df = pd.read_excel("data/Job Profile.xlsx")
        for c in df.select_dtypes(include="object"):
            df[c] = df[c].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = load_job_profiles()

# ===========================================================
# 5. CONTEÚDO PRINCIPAL
# ===========================================================
if not df.empty:
    families = sorted(df["Job Family"].dropna().unique())
    col1, col2, col3 = st.columns(3)

    with col1:
        fam = st.selectbox("Família:", families)

    with col2:
        subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].dropna().unique())
        sub = st.selectbox("Subfamília:", subs)

    with col3:
        paths = sorted(df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique())
        path = st.selectbox("Trilha:", paths)

    # Filtra conforme seleção
    filtered = df[
        (df["Job Family"] == fam)
        & (df["Sub Job Family"] == sub)
        & (df["Career Path"] == path)
    ]

    profiles = sorted(filtered["Job Profile"].dropna().unique())
    selected = st.multiselect("Selecione até 3 perfis:", profiles, max_selections=3)

    def format_desc(value):
        """Mantém HTML e quebras de linha da descrição."""
        if pd.isna(value) or not str(value).strip():
            return "-"
        text = str(value).strip()
        # se tiver tags HTML, mantém; caso contrário, converte \n em <br>
        if any(tag in text.lower() for tag in ["<p", "<br", "<ul", "<ol", "<li", "<b", "<i", "<div>"]):
            return text
        return text.replace("\r\n", "<br>").replace("\n", "<br>")

    # =======================================================
    # 6. GRID DE COMPARAÇÃO
    # =======================================================
    if selected:
        cols = len(selected)
        grid_html = f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:25px;">'

        for s in selected:
            item = filtered[filtered["Job Profile"] == s]
            if item.empty:
                continue
            row = item.iloc[0]

            title = row.get("Job Profile", "-")
            gg = row.get("Global Grade", "-")
            desc = format_desc(row.get("Job Profile Description", "-"))
            family = row.get("Job Family", "-")
            sub_family = row.get("Sub Job Family", "-")
            path_name = row.get("Career Path", "-")
            level = row.get("Career Level", "-")

            meta_html = f"""
                <div class="meta">
                    <b>Família:</b> {family} •
                    <b>Subfamília:</b> {sub_family} •
                    <b>Trilha:</b> {path_name} •
                    <b>Nível:</b> {level}
                </div>
            """

            grid_html += f"""
            <div class="job-card">
                <h4>{title}</h4>
                <p><b>Global Grade:</b> {gg}</p>
                {meta_html}
                <div class="desc"><b>Descrição:</b><br>{desc}</div>
            </div>
            """

        grid_html += "</div>"
        st.markdown(grid_html, unsafe_allow_html=True)
    else:
        st.info("👆 Selecione até 3 cargos para comparar.")
else:
    st.warning("⚠️ Base de dados não encontrada ou vazia.")
