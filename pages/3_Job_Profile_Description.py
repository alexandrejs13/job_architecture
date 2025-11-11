import streamlit as st
import pandas as pd
import html
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
    max-width: 950px !important;
    padding-left: 40px !important;
    padding-right: 40px !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f5f3f0;
    color: #202020;
    font-family: "Source Sans Pro", "Helvetica", sans-serif;
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

    # Filtra dados conforme seleções
    filtered = df[
        (df["Job Family"] == fam)
        & (df["Sub Job Family"] == sub)
        & (df["Career Path"] == path)
    ]

    profiles = sorted(filtered["Job Profile"].dropna().unique())
    selected = st.multiselect("Selecione até 3 perfis:", profiles, max_selections=3)

    # =======================================================
    # 6. FUNÇÃO DE ESCAPE E FORMATAÇÃO DE TEXTO
    # =======================================================
    def safe_text(value: str) -> str:
        """Escapa HTML e preserva quebras de linha."""
        if value is None or str(value).strip() == "":
            return "-"
        s = html.escape(str(value))
        return s.replace("\n", "<br>")

    # =======================================================
    # 7. GRID DE COMPARAÇÃO
    # =======================================================
    if selected:
        cols = len(selected)
        cards_html = [
            f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:25px;">'
        ]

        for s in selected:
            item = filtered[filtered["Job Profile"] == s]
            if item.empty:
                continue

            row = item.iloc[0]

            title = safe_text(row.get("Job Profile", "-"))
            gg = safe_text(row.get("Global Grade", "-"))
            desc = safe_text(row.get("Job Profile Description", "-"))

            # Campos opcionais
            family = safe_text(row.get("Job Family", "-"))
            sub_family = safe_text(row.get("Sub Job Family", "-"))
            path_name = safe_text(row.get("Career Path", "-"))
            level = safe_text(row.get("Career Level", "-"))

            meta_items = []
            if family != "-": meta_items.append(f"<b>Família:</b> {family}")
            if sub_family != "-": meta_items.append(f"<b>Subfamília:</b> {sub_family}")
            if path_name != "-": meta_items.append(f"<b>Trilha:</b> {path_name}")
            if level != "-": meta_items.append(f"<b>Nível:</b> {level}")

            meta_html = ""
            if meta_items:
                meta_html = (
                    '<div style="background:#fff;border-top:1px solid #e0e0e0;'
                    'border-bottom:1px solid #e0e0e0;font-size:.9rem;color:#555;'
                    'padding:12px 16px;margin-top:10px;">'
                    + " &nbsp;•&nbsp; ".join(meta_items)
                    + "</div>"
                )

            card_html = f"""
            <div style="
                background:white;
                border-left:5px solid #145efc;
                padding:20px;
                border-radius:10px;
                box-shadow:0 4px 8px rgba(0,0,0,0.05);
            ">
                <h4 style="color:#145efc;margin-bottom:8px;">{title}</h4>
                <p style="margin-bottom:6px;"><b>Global Grade:</b> {gg}</p>
                {meta_html}
                <div style="margin-top:12px;color:#333;line-height:1.6;font-size:.95rem;">
                    <b>Descrição:</b><br>{desc}
                </div>
            </div>
            """
            cards_html.append(card_html)

        cards_html.append("</div>")
        st.markdown("".join(cards_html), unsafe_allow_html=True)

    else:
        st.info("👆 Selecione até 3 cargos para comparar.")
else:
    st.warning("⚠️ Base de dados não encontrada ou vazia.")
