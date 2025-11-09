# 4_🧩_Job_Match.py
import re
import os
import math
import unicodedata
import numpy as np
import pandas as pd
import streamlit as st

# ────────────────────────────────────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Job Match", layout="wide")

PRIMARY = "#1f6feb"

# ────────────────────────────────────────────────────────────────────────────────
# UTIL: Normalização de texto
# ────────────────────────────────────────────────────────────────────────────────
def norm(s: str) -> str:
    s = str(s or "")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"\s+", " ", s.strip())
    return s

def keyify(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", norm(s).lower())

# Stopwords curtinhas PT/EN (só para limpar ruído)
STOP = set("""
a o os as um uma de do da das dos e ou para por com sem sobre entre em no na nos nas ao aos à às
the and of to in on at for from with without as by into within about over under up down out off per
que se sua seu seus suas suas mais menos muito pouco ja não sim
""".split())

def tokenize(text: str):
    text = norm(text).lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    return [t for t in tokens if t not in STOP and len(t) > 1]

# ────────────────────────────────────────────────────────────────────────────────
# DETECÇÃO e MAPEAMENTO de CABEÇALHOS
# ────────────────────────────────────────────────────────────────────────────────
# Alvos padronizados que o app usa internamente
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
    # Campos opcionais
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

# ────────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ────────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    candidates = [
        "Job Profile.csv",
        "data/Job Profile.csv",
        "data/Job_Profile.csv",
    ]
    last_error = None
    df = None
    for path in candidates:
        if os.path.exists(path):
            # Tenta , depois ;
            for sep in [",", ";"]:
                for enc in ["utf-8", "utf-8-sig", "latin-1"]:
                    try:
                        tmp = pd.read_csv(path, sep=sep, encoding=enc, engine="python")
                        df = tmp
                        break
                    except Exception as e:
                        last_error = e
                if df is not None:
                    break
        if df is not None:
            break
    if df is None:
        raise FileNotFoundError(
            "Não encontrei o arquivo 'Job Profile.csv'. Coloque-o na raiz do app ou em /data."
        )

    # Mapeamento de colunas
    cmap = build_column_map(list(df.columns))
    # Checa obrigatórios mínimos para UI
    needed = ["Family", "Subfamily", "Job Title", "Grade"]
    missing = [n for n in needed if n not in cmap]
    if missing:
        raise KeyError(f"Coluna(s) ausente(s) na base: {', '.join(missing)}")

    # Renomeia para padrão interno
    ren = {v: k for k, v in cmap.items()}
    df = df.rename(columns=ren)

    # Normaliza texto
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].astype(str).map(norm)

    # Campos que usaremos para MATCH
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

    # Garante Grade como "GG X"
    def fix_grade(g):
        g = norm(g)
        if not g:
            return ""
        m = re.search(r"(\d+)", g)
        return f"GG {m.group(1)}" if m else g

    df["Grade"] = df["Grade"].map(fix_grade)

    # Texto para o match SEMÂNTICO focado nos campos que realmente diferenciam
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

# ────────────────────────────────────────────────────────────────────────────────
# SCORING: TF simples + cosseno + heurística de senioridade
# ────────────────────────────────────────────────────────────────────────────────
def text_to_vec(text, vocab):
    tokens = tokenize(text)
    vec = np.zeros(len(vocab), dtype=float)
    for t in tokens:
        if t in vocab:
            vec[vocab[t]] += 1.0
    # normaliza L2
    n = np.linalg.norm(vec)
    if n > 0:
        vec /= n
    return vec

def cosine(a, b):
    d = float(np.dot(a, b))
    if d < 0:
        return 0.0
    return max(0.0, min(1.0, d))

def infer_grade_band(text):
    """Retorna ('low'|'mid'|'high') para filtrar coerência de senioridade."""
    t = norm(text).lower()
    # baixa: assistente, estagi, junior
    if re.search(r"\b(estagi|assistente|junior|jr)\b", t):
        return "low"
    # alta: gerente, manager, coordenador, supervisor, senior?
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
    # low aceita low/mid (evita high)
    if user_band == "low":
        return job_band in {"low", "mid"}
    # mid aceita tudo (mais flexível)
    if user_band == "mid":
        return job_band in {"low", "mid", "high"}
    # high evita low
    return job_band in {"mid", "high"}

# ────────────────────────────────────────────────────────────────────────────────
# UI
# ────────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
<h1 style="margin-bottom:0">🧩 Job Match</h1>
<p style="color:#666;margin-top:.25rem">
Encontre automaticamente o cargo mais compatível com base na <b>Family</b>, <b>Subfamily</b> e na sua descrição detalhada de atividades.
</p>
""",
    unsafe_allow_html=True,
)

# Carrega base com tratamento de erros
try:
    df = load_data()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()
except KeyError as e:
    st.error(str(e))
    st.stop()
except Exception as e:
    st.error(f"Falha ao carregar a base: {e}")
    st.stop()

# Picklists
families = sorted([f for f in df["Family"].dropna().unique() if f])
col_a, col_b = st.columns([1, 1])
with col_a:
    family = st.selectbox("Selecione a Family", options=["—"] + families, index=0)
# Subfamily sempre visível
sub_options = []
if family and family != "—":
    sub_options = sorted(df.loc[df["Family"] == family, "Subfamily"].dropna().unique())
with col_b:
    subfamily = st.selectbox(
        "Selecione a Subfamily",
        options=(["—"] + sub_options) if sub_options else ["—"],
        index=0,
        disabled=(family == "—"),
    )

st.markdown(
    f"""
<label style="font-weight:600">✍️ Descreva brevemente suas atividades:</label>
""",
    unsafe_allow_html=True,
)

placeholder = (
    "Exemplo (≥ 50 palavras): Executo rotinas de departamento pessoal, com foco em admissão, "
    "lançamento de ponto, fechamento de folha, conferência de encargos (INSS/FGTS/IRRF), "
    "emissão de guias, atendimento a colaboradores e apoio em benefícios. "
    "Experiência de 2 anos como assistente, reportando a analista sênior, seguindo políticas internas "
    "e legislação trabalhista. Faço conciliações simples, controles em planilhas e organização de documentos."
)

desc = st.text_area(
    "",
    value="",
    height=140,
    placeholder=placeholder,
)

go = st.button("🔎 Identificar Cargo", type="primary")

# ────────────────────────────────────────────────────────────────────────────────
# VALIDAÇÃO
# ────────────────────────────────────────────────────────────────────────────────
def word_count(s: str) -> int:
    return len(re.findall(r"\w+", s or ""))

if go:
    # Campos obrigatórios
    if family == "—":
        st.warning("Selecione uma **Family**.")
        st.stop()
    if subfamily == "—":
        st.warning("Selecione uma **Subfamily**.")
        st.stop()
    if word_count(desc) < 50:
        st.warning("Descreva com **pelo menos 50 palavras** para um match preciso.")
        st.stop()

    # Filtra a base pela família/subfamília
    base = df[(df["Family"] == family) & (df["Subfamily"] == subfamily)].copy()
    if base.empty:
        st.info("Não encontrei cargos nessa combinação de Family/Subfamily.")
        st.stop()

    # Vocab a partir dos textos de MATCH
    vocab = {}
    for txt in base["Match_Text"]:
        for tok in tokenize(txt):
            if tok not in vocab:
                vocab[tok] = len(vocab)

    if not vocab:
        st.error("Não há conteúdo suficiente (Role/KPIs/Qualifications) para pontuar nesta subfamily.")
        st.stop()

    user_vec = text_to_vec(desc, vocab)
    user_band = infer_grade_band(desc)

    # Score de similaridade + coerência de grade
    scores = []
    for i, row in base.iterrows():
        job_vec = text_to_vec(row["Match_Text"], vocab)
        sim = cosine(user_vec, job_vec)

        # Ajuste de coerência de senioridade
        jb = grade_band_from_grade(row.get("Grade", ""))
        if not band_compatible(user_band, jb):
            sim *= 0.55  # penaliza

        scores.append((i, sim))

    if not scores:
        st.info("Não consegui pontuar os cargos desta subfamily.")
        st.stop()

    scores.sort(key=lambda x: x[1], reverse=True)
    top = scores[:3]

    st.markdown(
        f"<h2 style='margin-top:1.5rem'>🎯 Cargos mais compatíveis:</h2>",
        unsafe_allow_html=True,
    )

    for rank, (idx, sc) in enumerate(top, start=1):
        r = base.loc[idx]
        gg = r.get("Grade", "")
        title = r.get("Job Title", "")

        with st.container(border=True):
            # Cabeçalho do card
            lh, rh = st.columns([0.75, 0.25])
            with lh:
                st.markdown(
                    f"<div style='font-size:1.15rem;font-weight:700;color:{PRIMARY}'>"
                    f"{gg} — {title}"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='color:#666'>{r.get('Family','')} &nbsp;|&nbsp; {r.get('Subfamily','')}</div>",
                    unsafe_allow_html=True,
                )
            with rh:
                st.markdown(
                    f"<div style='text-align:right;color:#555'>Similaridade: "
                    f"<b>{round(sc*100,1)}%</b></div>",
                    unsafe_allow_html=True,
                )

            # Detalhes com a MESMA estrutura da Job Profile Description
            with st.expander("📋 Ver detalhes", expanded=False):
                # Bloco cabeçalho igual
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
""".strip()
                )

                def section(label, text, icon=""):
                    text = r.get(text, "")
                    if not text or text == "nan":
                        return
                    st.markdown(f"**{icon}{label}**")
                    # Quebra linhas mantendo bullets quando houver "•" ou "●"
                    if "•" in text or "●" in text:
                        bullets = re.split(r"[•●]\s*", text)
                        for b in bullets:
                            b = b.strip()
                            if b:
                                st.markdown(f"- {b}")
                    else:
                        st.write(text)

                section("Sub Job Family Description", "Sub Job Family Description", icon="🧭")
                section("Job Profile Description", "Job Profile Description", icon="🧠")
                section("Role Description", "Role Description", icon="🎯")
                section("Grade Differentiator", "Grade Differentiator", icon="🏅")
                section("KPIs / Specific Parameters", "KPIs / Specific Parameters", icon="📊")
                section("Qualifications", "Qualifications", icon="🎓")
