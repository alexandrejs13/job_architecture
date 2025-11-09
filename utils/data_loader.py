# utils/data_loader.py
import pandas as pd
from functools import lru_cache

RAW_URL = "https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/data/Job%20Profile.csv"

PREFERRED_COLS = [
    "Job Family","Sub Job Family","Job Profile","Function Code","Discipline Code",
    "Career Path","Global Grade","SIG Full Title","Full Job Code","Career Level",
    "Sub Job Family Description","Job Profile Description","Role Description",
    "Grade Differentiator","Qualifications","Specific parameters KPIs","Photo"
]

def _try_read(url_or_path):
    """Tenta variações robustas de leitura."""
    # 1) tenta ; (o seu arquivo costuma estar assim)
    for sep in [";", ",", "\t", "|"]:
        for enc in ["utf-8", "latin-1"]:
            try:
                df = pd.read_csv(url_or_path, sep=sep, encoding=enc, engine="python", dtype=str, quoting=3)
                if df.shape[1] >= 8:
                    return df
            except Exception:
                pass
    # fallback: deixa o erro aparecer de verdade
    return pd.read_csv(url_or_path, sep=";", encoding="utf-8", engine="python", dtype=str, quoting=3)

def _normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    # mantém as colunas originais; apenas retira espaços/breaklines das células
    df = df.copy()
    for c in df.columns:
        df[c] = df[c].astype(str).str.replace("\r", " ").str.replace("\n", " ").str.strip()
    # assegura colunas críticas (se faltar, cria vazia)
    for col in PREFERRED_COLS:
        if col not in df.columns:
            df[col] = ""
    # padroniza campo de grade
    if "Global Grade" in df.columns:
        df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    return df

@lru_cache(maxsize=1)
def load_job_profile():
    """Lê SEMPRE do GitHub raw e normaliza (cache local em memória)."""
    df = _try_read(RAW_URL)
    df = _normalize_df(df)
    # linhas válidas mínimas
    df = df[df["Job Family"].str.len() > 0]
    df = df[df["Job Profile"].str.len() > 0]
    return df
