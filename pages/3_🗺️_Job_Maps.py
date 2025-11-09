import streamlit as st
import pandas as pd
import re
import unicodedata
from pathlib import Path

# ───────────────────────────────────────────────────────────
# Configurações da página
# ───────────────────────────────────────────────────────────
st.set_page_config(page_title="Job Maps", layout="wide")
PRIMARY = "#1f6feb"

def normalize(s: str) -> str:
    s = str(s or "")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s.strip())

@st.cache_data(show_spinner=False)
def load_data():
    base = Path(__file__).parent
    path = base / "data" / "Job Profile.csv"
    if not path.exists():
        path = base.parent / "data" / "Job Profile.csv"
    if not path.exists():
        raise FileNotFoundError("Arquivo 'data/Job Profile.csv' não encontrado.")
    # tenta distintos separadores, com fallback
    for sep in [",", ";", "\t"]:
        try:
            df = pd.read_csv(path, sep=sep, encoding="utf-8", engine="python")
            if df.shape[1] >= 4:
                break
        except Exception:
            try:
                df = pd.read_csv(path, sep=sep, encoding="latin-1", engine="python")
                if df.shape[1] >= 4:
                    break
            except Exception:
                df = None
    if df is None:
        raise ValueError("Falha ao ler 'Job Profile.csv' — verifique formatação ou codificação.")
    # normaliza colunas
    df.columns = [normalize(c) for c in df.columns]
    return df

df = load_data()

# listas de filtros
families = sorted(df["job family"].dropna().unique()) if "job family" in df.columns else []
col1, col2 = st.columns([1, 1])
with col1:
    family = st.selectbox("Selecione a Family", ["—"] + families)
subfamilies = []
if family != "—":
    subfamilies = sorted(df[df["job family"] == family]["sub job family"].dropna().unique()) if "sub job family" in df.columns else []
with col2:
    subfamily = st.selectbox("Selecione a Subfamily", ["—"] + subfamilies if subfamilies else ["—"], index=0)

if family == "—":
    st.info("Selecione uma Family para visualizar o mapa.")
    st.stop()

base = df[df["job family"] == family]
if subfamily != "—":
    base = base[base["sub job family"] == subfamily]

if base.empty:
    st.warning("Nenhum cargo encontrado nessa Family/Subfamily.")
    st.stop()

st.markdown("### 📊 Estrutura de Cargos")
for _, row in base.iterrows():
    title = row.get("job profile", "")
    grade = row.get("grade", "")
    st.markdown(f"<div style='font-size:1.2rem;font-weight:700;color:{PRIMARY}'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#555'>Grade: {grade} | Subfamily: {row.get('sub job family','')}</div>", unsafe_allow_html=True)
    for field_label, icon in [
        ("Role Description", "🎯"),
        ("Grade Differentiator", "🏅"),
        ("KPIs / Specific Parameters", "📊"),
        ("Qualifications", "🎓"),
    ]:
        fld = normalize(row.get(field_label.lower(), "") if field_label.lower() in row.index else row.get(field_label, ""))
        if fld.strip():
            st.markdown(f"**{icon} {field_label}**")
            bullets = re.split(r"[•●]\s*", fld)
            for b in bullets:
                if b.strip():
                    st.markdown(f"- {b.strip()}")
    st.divider()

st.markdown("---")
st.markdown(f"<p style='color:#666'>Total de cargos exibidos: <b>{len(base)}</b></p>", unsafe_allow_html=True)
