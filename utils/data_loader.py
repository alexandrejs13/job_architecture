import os
import pandas as pd

# ===========================================================
# Funções auxiliares para leitura de Excel
# ===========================================================
def _read_xlsx(filename: str) -> pd.DataFrame:
    """
    Lê um arquivo Excel da pasta /data independentemente do local de execução.
    """
    base = os.path.join(os.path.dirname(__file__), "..", "data")
    path = os.path.join(base, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    df = pd.read_excel(path)
    df.columns = [str(c).strip() for c in df.columns]
    return df

def load_job_profile_df() -> pd.DataFrame:
    """Carrega a base principal Job Profile.xlsx"""
    return _read_xlsx("Job Profile.xlsx")

def load_job_map_df() -> pd.DataFrame:
    """Usa a mesma base do Job Profile.xlsx para o mapa"""
    return _read_xlsx("Job Profile.xlsx")

def load_level_structure_df() -> pd.DataFrame:
    """Carrega Level Structure.xlsx"""
    return _read_xlsx("Level Structure.xlsx")
