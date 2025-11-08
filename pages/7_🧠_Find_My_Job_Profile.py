# ------------------ Carregar base (robusto contra CSV com vírgulas em texto) ------------------ #
import os, io, csv, glob, hashlib
import pandas as pd
import streamlit as st

def _normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
    # mapa flexível de nomes -> padrão
    cols_low = {c.lower().strip(): c for c in df.columns}
    def pick(*opts, default=None):
        for o in opts:
            if o.lower().strip() in cols_low:
                return cols_low[o.lower().strip()]
        return default

    rename = {}
    def set_alias(srcs, tgt):
        c = pick(*srcs)
        if c and c != tgt:
            rename[c] = tgt

    set_alias(["job title", "job profile", "title", "cargo"], "Job Title")
    set_alias(["global grade", "gg", "grade"], "Global Grade")
    set_alias(["family", "job family"], "Family")
    set_alias(["sub family", "sub job family", "subfamily"], "Sub Family")
    set_alias(["career track", "career path"], "Career Track")
    set_alias(["function", "function code"], "Function")
    set_alias(["job code", "full job code", "código"], "Job Code")

    set_alias(["sub job family description", "subfamily description"], "Sub Job Family Description")
    set_alias(["job profile description", "profile description"], "Job Profile Description")
    set_alias(["role description"], "Role Description")
    # variações e o seu typo “Differentiatior”
    set_alias(["grade differentiator", "grade differentiation", "grade differentiators", "grade differentiatior"], "Grade Differentiator")
    set_alias(["kpis / specific parameters", "specific parameters kpis", "specific parameters / kpis"], "KPIs / Specific Parameters")
    set_alias(["qualifications", "qualification"], "Qualifications")

    if rename:
        df = df.rename(columns=rename)
    return df

def _try_read(path: str):
    # 1) tentativa auto (Sniffer) + engine python
    try:
        with open(path, 'rb') as f:
            raw = f.read()
        for enc in ("utf-8-sig", "latin1"):
            try:
                text = raw.decode(enc, errors="replace")
                sample = "\n".join(text.splitlines()[:50])
                dialect = csv.Sniffer().sniff(sample, delimiters=[",",";","\t","|"])
                sep = dialect.delimiter
                df = pd.read_csv(io.StringIO(text), sep=sep, engine="python",
                                 quoting=csv.QUOTE_MINIMAL, quotechar='"',
                                 escapechar='\\', dtype=str, keep_default_na=False)
                return df
            except Exception:
                continue
    except Exception:
        pass

    # 2) tentativas explícitas de separador
    for enc in ("utf-8-sig", "latin1"):
        for sep in (",",";","\t","|"):
            try:
                df = pd.read_csv(path, sep=sep, engine="python",
                                 quoting=csv.QUOTE_MINIMAL, quotechar='"',
                                 escapechar='\\', dtype=str, keep_default_na=False,
                                 encoding=enc)
                return df
            except Exception:
                continue

    # 3) último recurso: tenta ler “solto” e descartar linhas problemáticas
    for enc in ("utf-8-sig", "latin1"):
        for sep in (",",";","\t","|"):
            try:
                df = pd.read_csv(path, sep=sep, engine="python",
                                 quoting=csv.QUOTE_NONE, escapechar='\\',
                                 dtype=str, keep_default_na=False,
                                 encoding=enc, on_bad_lines="skip")
                st.warning("⚠️ Algumas linhas foram ignoradas por formatação inconsistente.")
                return df
            except Exception:
                continue

    raise ValueError("Não foi possível ler o CSV com nenhum método robusto.")

def _find_csv():
    candidatos = [
        "data/Job_Profile.csv",
        "data/Job Profile.csv",
        "data/job_profile.csv",
        "data/job profile.csv",
        "data/JobProfile.csv",
        "data/JOB_PROFILE.csv",
    ]
    if not any(os.path.exists(p) for p in candidatos):
        for f in sorted(glob.glob("data/*.csv")):
            nm = os.path.basename(f).lower()
            if "job" in nm and "profile" in nm:
                candidatos.insert(0, f)
                break
    for p in candidatos:
        if os.path.exists(p):
            return p
    return None

csv_path = _find_csv()
if not csv_path:
    existentes = "\n".join(f"- {os.path.basename(x)}" for x in sorted(glob.glob("data/*.csv")))
    st.error("❌ Não encontrei um CSV de Job Profile em `data/`.\n"
             "Coloque o arquivo com nome como `Job_Profile.csv`.\n\n"
             "Arquivos vistos:\n" + (existentes or "(nenhum .csv encontrado)"))
    st.stop()

try:
    df = _try_read(csv_path)
except Exception as e:
    st.error(f"Erro ao ler `{os.path.basename(csv_path)}`: {e}")
    st.stop()

# Normaliza nomes e garante colunas principais
df = _normalize_cols(df)

obrig = ["Job Title", "Job Profile Description"]
faltando = [c for c in obrig if c not in df.columns]
if faltando:
    st.error("❌ Colunas obrigatórias ausentes: " + ", ".join(faltando) +
             "\nVerifique o cabeçalho do CSV.")
    st.stop()

st.success(f"✅ Base carregada: `{os.path.basename(csv_path)}` — {df.shape[0]} linhas, {df.shape[1]} colunas.")
