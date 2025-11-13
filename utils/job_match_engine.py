import pandas as pd
from pathlib import Path

PROFILE_PATH = Path("job_architecture/data/Job Profile.xlsx")


def load_profiles():
    """Carrega o catálogo completo de cargos."""
    return pd.read_excel(PROFILE_PATH)


def find_best_job_profile(career_band, career_level, survey_grade):
    """
    Procura no Job Profile.xlsx o cargo mais compatível.
    """

    df = load_profiles()

    df_match = df[
        (df["CareerBand"] == career_band) &
        (df["CareerLevel"] == career_level) &
        (df["Grade"] == survey_grade)
    ]

    if df_match.empty:
        df_match = df[
            (df["CareerBand"] == career_band) &
            (df["CareerLevel"] == career_level)
        ]

    if df_match.empty:
        df_match = df[df["CareerBand"] == career_band]

    if df_match.empty:
        return None

    return df_match.iloc[0].to_dict()
