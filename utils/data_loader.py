import pandas as pd
import os
from typing import Dict, Optional, List

# -----------------------------------------------------------
# Helpers de normalização
# -----------------------------------------------------------
def _slug(s: str) -> str:
    return (
        str(s)
        .strip()
        .lower()
        .replace("\n", " ")
        .replace("\r", " ")
        .replace("  ", " ")
    )

def _find_first_present(cols: List[str], candidates: List[str]) -> Optional[str]:
    """
    Retorna o nome da coluna real do dataframe que corresponde ao primeiro
    candidato presente (comparação case-insensitive e ignorando espaços extras).
    """
    norm = {_slug(c): c for c in cols}
    for cand in candidates:
        key = _slug(cand)
        if key in norm:
            return norm[key]
    return None

def _rename_using_synonyms(df: pd.DataFrame, synonym_map: Dict[str, List[str]]) -> pd.DataFrame:
    """
    synonym_map: { "NomePadrao": ["Possível nome 1", "Possível nome 2", ...] }
    Faz rename das colunas presentes para "NomePadrao".
    """
    present = {}
    cols = list(df.columns)
    for standard, cands in synonym_map.items():
        found = _find_first_present(cols, cands)
        if found:
            present[found] = standard
    if present:
        df = df.rename(columns=present)
    return df

# -----------------------------------------------------------
# Loader principal
# -----------------------------------------------------------
def load_excel_tables() -> Dict[str, pd.DataFrame]:
    """
    Lê e normaliza:
      - data/Job Profile.xlsx
      - data/Level Structure.xlsx
    Retorna um dict com chaves 'job_profile' e 'level_structure' quando disponíveis.
    """
    data: Dict[str, pd.DataFrame] = {}

    # ---------------- Job Profile.xlsx ----------------
    jp_path = os.path.join("data", "Job Profile.xlsx")
    if os.path.exists(jp_path):
        jp = pd.read_excel(jp_path)

        # Mapa de sinônimos -> nome padrão
        jp_syn = {
            # chaves essenciais de arquitetura
            "Job Family": ["Job Family", "Family"],
            "Sub Job Family": ["Sub Job Family", "Subfamily", "Sub Family", "Job Subfamily", "Sub Job-Family"],
            "Career Path": ["Career Path", "Path", "Carreira"],
            "Global Grade": ["Global Grade", "Grade", "GG"],
            "Full Job Code": ["Full Job Code", "Job Code", "Code", "Código", "Full Code"],
            "Job Profile": ["Job Profile", "Job Title", "Title", "Profile", "Local Job Title"],

            # descrições (seus apontamentos de colunas P / Q / V / Y / AA)
            "Sub Job Family Description": [
                "Sub Job Family Description",
                "Subfamily Description",
                "Sub Job Family Desc",
                "Sub Family Description",
            ],
            "Job Profile Description": [
                "Job Profile Description",
                "Job Description",
                "Profile Description",
                "Job Profile Desc",
            ],
            "Role Description": [
                "Role Description",
                "Role Summary",
                "Responsibilities",
                "Role Overview",
            ],
            "Grade Differentiator": [
                "Grade Differentiator",
                "Grade Differentiation",
                "Grade Differentiators",
            ],
            "Qualifications": [
                "Qualifications",
                "Education/Experience",
                "Minimum Qualifications",
                "Qualificações",
            ],

            # extras (se existirem no seu arquivo)
            "Function Code": ["Function Code", "Function", "Função"],
            "Discipline Code": ["Discipline Code", "Discipline", "Disciplina"],
        }

        jp = _rename_using_synonyms(jp, jp_syn)

        # Garante tipos e limpeza básica
        if "Global Grade" in jp.columns:
            jp["Global Grade"] = jp["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True)

        # remove linhas totalmente vazias
        jp = jp.dropna(how="all")
        data["job_profile"] = jp

    # ---------------- Level Structure.xlsx ----------------
    ls_path = os.path.join("data", "Level Structure.xlsx")
    if os.path.exists(ls_path):
        ls = pd.read_excel(ls_path)

        ls_syn = {
            "Career Path": ["Career Path", "Path", "Carreira"],
            "Structure Level": ["Structure Level", "Level", "Nível", "Job Level"],
            "Level Name": ["Level Name", "Name", "Nome do Nível", "Level Title"],
            "Level Description": ["Level Description", "Description", "Descrição"],
            "Global Grade": ["Global Grade", "Grade", "GG"],
        }
        ls = _rename_using_synonyms(ls, ls_syn)
        if "Global Grade" in ls.columns:
            ls["Global Grade"] = ls["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True)
        ls = ls.dropna(how="all")
        data["level_structure"] = ls

    return data
