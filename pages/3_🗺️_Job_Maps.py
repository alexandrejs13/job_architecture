import re
import os
import math
import unicodedata
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path

# ───────────────────────────────────────────────
# CONFIG
# ───────────────────────────────────────────────
st.set_page_config(page_title="Job Match", layout="wide")
PRIMARY = "#1f6feb"

# ───────────────────────────────────────────────
# FUNÇÕES UTILITÁRIAS
# ───────────────────────────────────────────────
def norm(s: str) -> str:
    s = str(s or "")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"\s+", " ", s.strip())
    return s

def keyify(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", norm(s).lower())

STOP = set("""
a o os as um uma de do da das dos e ou para por com sem sobre entre em no na nos nas ao aos à às
the and of to in on at for from with without as by into within about over under up down out off per
que se sua seu seus suas mais menos muito pouco ja não sim
""".split())

def tokenize(text: str):
    text = norm(text).lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    return [t for t in tokens if t not in STOP and len(t) > 1]

# ───────────────────────────────────────────────
# MAPEAMENTO DE COLUNAS
# ───────────────────────────────────────────────
TARGETS = {
    "Family": {"family", "jobfamily"},
    "Subfamily": {"subfamily", "subjobfamily", "subjob", "subfamilia"},
    "Job Title": {"jobtitle", "jobprofile", "job", "title"},
    "Grade": {"grade", "gg", "globalgrade", "globalgradegg"},
    "Sub Job Family Description": {"subjobfamilydescription", "subfamilydescription"},
    "Job Profile Description": {"jobprofiledescription", "jobdescription"},
    "Role Description": {"roledescription", "roles", "role"},
    "Grade Differentiator": {"gradedifferentiator", "gradediffs", "gradediff"},
    "KPIs / Specific Parameters": {"kpis", "kpispecificparameters", "parameters", "specificparameters"},
    "Qualifications": {"qualifications", "qualification", "education"},
    "Function": {"function", "funcao"},
    "Discipline": {"discipline", "disciplina"},
    "Code": {"code", "codigo", "jobcode"},
}

def build_column_map(cols):
    k2orig = {keyify(c): c for c in cols}
    mapping = {}
    for target, aliases in TARGETS.items():
        for a in aliases:
            if a in k2orig:
                mapping[target] = k2orig[a]
                break
    return mapping

# ───────────────────────────────────────────────
# CARREGAMENTO DO CSV (ROBUSTO)
# ───────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    base_path = Path(__file__).parent
    candidates = [
        base_path / "data" / "Job Profile.csv",
        base_path / "Job Profile.csv",
        base_path.parent / "data" / "Job Profile.csv",
    ]
    df = None
    for path in candidates:
        if path.exists():
            for sep in [",", ";"]:
                for enc in ["utf-8", "utf-8-sig", "latin-1"]:
                    try:
                        df = pd.read_csv(path, sep=sep, encoding=enc, engine="python")
                        break
                    except Exception:
                        continue
                if df is not None:
                    break
        if df is not None:
            break

    if df is None:
        raise FileNotFoundError(
            "❌ Não encontrei o arquivo 'Job Profile.csv'. "
            "Coloque-o na pasta 'data' ou na raiz do app."
        )

    cmap = build_column_map(list(df.columns))
    needed = ["Family", "Subfamily", "Job Title", "Grade"]
    missing = [n for n in needed if n not in cmap]
    if missing:
        raise KeyError(f"Coluna(s) ausente(s) na base: {', '.join(missing)}")

    ren = {v: k for k, v in cmap.items()}
    df = df.rename(columns=ren)

    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].astype(str).map(norm)

    for c in [
        "Role Description",
        "Grade Differentiator",
        "KPIs / Specific Parameters",
        "Qualifications",
        "Sub Job Family Description",
        "Job Profile Description",
    ]:
        if c not in df.columns:
            df[c] = ""

    def fix_grade(g):
        g = norm(g)
        if not g:
            return ""
        m = re.search(r"(\d+)", g)
        return f"GG {m.group(1)}" if m else g

    df["Grade"] = df["Grade"].map(fix_grade)

    df["Match_Text"] = (
        df["Role Description"].fillna("")
        + " "
        + df["Grade Differentiator"].fillna("")
        + " "
        + df["KPIs / Specific Parameters"].fillna("")
        + " "
        + df["Qualifications"].fillna("")
    ).map(norm)

    return df

# ───────────────────────────────────────────────
# FUNÇÕES DE MATCH E SIMILARIDADE
# ───────────────────────────────────────────────
def text_to_vec(text, vocab):
    tokens = tokenize(text)
    vec = np.zeros(len(vocab), dtype=float)
    for t in tokens:
        if t in vocab:
            vec[vocab[t]] += 1.0
    n = np.linalg.norm(vec)
    if n > 0:
        vec /= n
    return vec

def cosine(a, b):
    d = float(np.dot(a, b))
    return max(0.0, min(1.0, d))

def infer_grade_band(text):
    t = norm(text).lower()
    if re.search(r"\b(estagi|assistente|junior|jr)\b", t):
        return "low"
    if re.search(r"\b(gerent|manager|coordenador|supervisor|sr|senior)\b", t):
        return "high"
    return "mid"

def grade_band_from_grade(grade_str):
    m = re.search(r"(\d+)", grade_str or "")
    if not m:
        return "mid"
    g = int(m.group(1))
    if g <= 6:
        return "low"
    if g >= 11:
        return "high"
    return "mid"

def band_compatible(user_band, job_band):
    if user_band == "low":
        return job_band in {"low", "mid"}
    if user_band == "mid":
        return job_band in {"low", "mid", "high"}
    return job_band in {"mid", "high"}

# ───────────────────────────────────────────────
# INTERFACE
# ───────────────────────────────────────────────
st.markdown(
    f"""
<h1 style="margin-bottom:0">🧩 Job Match</h1>
<p style="color:#666;margin-top:.25rem">
Encontre automaticamente o cargo mais compatível com base na <b>Family</b>, <b>Subfamily</b> e na sua descrição detalhada de atividades.
</p>
""",
    unsafe_allow_html=True,
)

try:
    df = load_data()
except Exception as e:
    st.error(str(e))
    st.stop()

families = sorted([f for f in df["Family"].dropna().unique() if f])
col1, col2 = st.columns([1, 1])
with col1:
    family = st.selectbox("Selecione a Family", ["—"] + families, index=0)
sub_options = []
if family and family != "—":
    sub_options = sorted(df.loc[df["Family"] == family, "Subfamily"].dropna().unique())
with col2:
    subfamily = st.selectbox(
        "Selecione a Subfamily",
        ["—"] + sub_options if sub_options else ["—"],
        index=0,
        disabled=(family == "—"),
    )

st.markdown("**✍️ Descreva brevemente suas atividades:**", unsafe_allow_html=True)
placeholder = (
    "Exemplo (≥ 50 palavras): Executo rotinas de departamento pessoal, com foco em admissão, "
    "lançamento de ponto, fechamento de folha, conferência de encargos (INSS/FGTS/IRRF), "
    "emissão de guias, atendimento a colaboradores e apoio em benefícios. "
    "Experiência de 2 anos como assistente, reportando a analista sênior, seguindo políticas internas "
    "e legislação trabalhista. Faço conciliações simples, controles em planilhas e organização de documentos."
)
desc = st.text_area("", value="", height=140, placeholder=placeholder)
go = st.button("🔎 Identificar Cargo", type="primary")

def word_count(s: str) -> int:
    return len(re.findall(r"\w+", s or ""))

if go:
    if family == "—":
        st.warning("Selecione uma **Family**.")
        st.stop()
    if subfamily == "—":
        st.warning("Selecione uma **Subfamily**.")
        st.stop()
    if word_count(desc) < 50:
        st.warning("Descreva com **pelo menos 50 palavras** para um match preciso.")
        st.stop()

    base = df[(df["Family"] == family) & (df["Subfamily"] == subfamily)].copy()
    if base.empty:
        st.info("Não encontrei cargos nessa combinação de Family/Subfamily.")
        st.stop()

    vocab = {}
    for txt in base["Match_Text"]:
        for tok in tokenize(txt):
            if tok not in vocab:
                vocab[tok] = len(vocab)
    if not vocab:
        st.error("Base insuficiente para pontuar esta Subfamily.")
        st.stop()

    user_vec = text_to_vec(desc, vocab)
    user_band = infer_grade_band(desc)

    scores = []
    for i, row in base.iterrows():
        job_vec = text_to_vec(row["Match_Text"], vocab)
        sim = cosine(user_vec, job_vec)
        jb = grade_band_from_grade(row.get("Grade", ""))
        if not band_compatible(user_band, jb):
            sim *= 0.55
        scores.append((i, sim))

    scores.sort(key=lambda x: x[1], reverse=True)
    top = scores[:3]

    st.markdown("### 🎯 Cargos mais compatíveis:")
    for idx, (i, sc) in enumerate(top, start=1):
        r = base.loc[i]
        gg = r.get("Grade", "")
        title = r.get("Job Title", "")

        with st.container(border=True):
            c1, c2 = st.columns([0.8, 0.2])
            with c1:
                st.markdown(
                    f"<div style='font-size:1.1rem;font-weight:700;color:{PRIMARY}'>{gg} — {title}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='color:#666'>{r.get('Family','')} | {r.get('Subfamily','')}</div>",
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f"<div style='text-align:right;color:#555'>Similaridade: <b>{round(sc*100,1)}%</b></div>",
                    unsafe_allow_html=True,
                )

            with st.expander("📋 Ver detalhes"):
                st.markdown(
                    f"""
**{title}**  
{gg}  

**Família:** {r.get('Family','')}  
**Subfamília:** {r.get('Subfamily','')}  
**Carreira:** {r.get('Career','')}  
**Função:** {r.get('Function','')}  
**Disciplina:** {r.get('Discipline','')}  
**Código:** {r.get('Code','')}
""",
                )

                def section(label, col, icon=""):
                    text = r.get(col, "")
                    if not text or text == "nan":
                        return
                    st.markdown(f"**{icon}{label}**")
                    if "•" in text or "●" in text:
                        for b in re.split(r"[•●]\s*", text):
                            if b.strip():
                                st.markdown(f"- {b.strip()}")
                    else:
                        st.write(text)

                section("Sub Job Family Description", "Sub Job Family Description", "🧭 ")
                section("Job Profile Description", "Job Profile Description", "🧠 ")
                section("Role Description", "Role Description", "🎯 ")
                section("Grade Differentiator", "Grade Differentiator", "🏅 ")
                section("KPIs / Specific Parameters", "KPIs / Specific Parameters", "📊 ")
                section("Qualifications", "Qualifications", "🎓 ")
