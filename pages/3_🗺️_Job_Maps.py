import streamlit as st
import pandas as pd
import re
import unicodedata

# ───────────────────────────────────────────────
# CONFIG
# ───────────────────────────────────────────────
st.set_page_config(page_title="Job Maps", layout="wide")

PRIMARY = "#1f6feb"
BG = "#f8f9fc"

# ───────────────────────────────────────────────
# FUNÇÕES
# ───────────────────────────────────────────────
def norm(s):
    """Remove acentos e espaços extras"""
    s = str(s or "")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s.strip())

@st.cache_data
def load_data():
    for path in ["data/Job Profile.csv", "Job Profile.csv"]:
        try:
            df = pd.read_csv(path, sep=";", encoding="utf-8", engine="python")
            break
        except Exception:
            try:
                df = pd.read_csv(path, sep=",", encoding="utf-8", engine="python")
                break
            except Exception:
                df = None
    if df is None:
        st.error("Não foi possível carregar o arquivo `Job Profile.csv`. Coloque-o na pasta `/data`.")
        st.stop()

    df.columns = [norm(c) for c in df.columns]
    if "job family" not in df.columns or "sub job family" not in df.columns:
        st.error("O arquivo deve conter as colunas **Job Family** e **Sub Job Family**.")
        st.stop()

    df["job family"] = df["job family"].astype(str)
    df["sub job family"] = df["sub job family"].astype(str)
    df["job profile"] = df.get("job profile", "")
    df["grade"] = df.get("grade", "")
    return df

# ───────────────────────────────────────────────
# INTERFACE
# ───────────────────────────────────────────────
st.markdown(
    f"""
    <h1 style="margin-bottom:0">🗺️ Job Maps</h1>
    <p style="color:#666;margin-top:.25rem">
    Visualize a estrutura de cargos e suas relações hierárquicas dentro da organização.
    </p>
    """,
    unsafe_allow_html=True,
)

df = load_data()

families = sorted(df["job family"].dropna().unique())
col1, col2 = st.columns([1, 1])
with col1:
    family = st.selectbox("Selecione a Family", ["—"] + families, index=0)
with col2:
    subfamilies = (
        sorted(df[df["job family"] == family]["sub job family"].dropna().unique())
        if family != "—"
        else []
    )
    subfamily = st.selectbox(
        "Selecione a Subfamily", ["—"] + subfamilies if subfamilies else ["—"], index=0
    )

if family == "—":
    st.info("Selecione uma Family para começar.")
    st.stop()

base = df[df["job family"] == family]
if subfamily != "—":
    base = base[base["sub job family"] == subfamily]

if base.empty:
    st.warning("Nenhum cargo encontrado para essa combinação.")
    st.stop()

# ───────────────────────────────────────────────
# TABELA DE CARGOS
# ───────────────────────────────────────────────
st.markdown("### 📊 Estrutura de Cargos")

for _, row in base.iterrows():
    with st.container(border=True):
        st.markdown(
            f"<div style='font-size:1.1rem;font-weight:700;color:{PRIMARY}'>{row.get('job profile','')}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='color:#555'>Grade: {row.get('grade','')} | Subfamily: {row.get('sub job family','')}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<hr style='margin:0.5rem 0;'>", unsafe_allow_html=True)

        for section, icon in [
            ("role description", "🎯"),
            ("grade differentiator", "🏅"),
            ("kpis / specific parameters", "📊"),
            ("qualifications", "🎓"),
        ]:
            content = row.get(section, "")
            if isinstance(content, str) and content.strip():
                st.markdown(f"**{icon} {section.title()}**")
                bullets = re.split(r"[•●]\s*", content)
                for b in bullets:
                    if b.strip():
                        st.markdown(f"- {b.strip()}")

        st.markdown(
            "<div style='height:0.8rem;border-bottom:1px solid #e5e5e5;'></div>",
            unsafe_allow_html=True,
        )

# ───────────────────────────────────────────────
# RESUMO
# ───────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f"<p style='color:#666'>Total de cargos exibidos: <b>{len(base)}</b></p>",
    unsafe_allow_html=True,
)
