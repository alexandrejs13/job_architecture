import os
import pandas as pd

def _read_xlsx(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    df = pd.read_excel(path)
    # normaliza nomes de colunas (tira espaços nas pontas)
    df.columns = [str(c).strip() for c in df.columns]
    return df

def _normalize_map(df: pd.DataFrame):
    """
    Retorna um dicionário {nome_normalizado: nome_original} para acesso tolerante.
    Normalização: lower + collapse spaces.
    """
    def norm(s): return " ".join(str(s).strip().lower().split())
    return {norm(c): c for c in df.columns}

def _ensure_columns(df: pd.DataFrame, required: list):
    """
    Verifica se 'required' existem em df (tolerante a caixa/espacos).
    Retorna um dict {canonical: actual_name} para acesso.
    """
    norm_map = _normalize_map(df)
    found = {}
    missing = []
    for col in required:
        key = " ".join(col.strip().lower().split())
        if key in norm_map:
            found[col] = norm_map[key]
        else:
            missing.append(col)
    return found, missing

def load_job_profile_df() -> pd.DataFrame:
    """
    Carrega a base principal para DESCRIÇÕES (Job Profile.xlsx).
    """
    df = _read_xlsx("data/Job Profile.xlsx")
    return df

def load_job_map_df() -> pd.DataFrame:
    """
    Carrega a base para o JOB MAP (usa Job Profile.xlsx para manter consistência).
    """
    return load_job_profile_df()

def load_level_structure_df() -> pd.DataFrame:
    """
    Carrega Level Structure.xlsx, se existir.
    """
    return _read_xlsx("data/Level Structure.xlsx")
