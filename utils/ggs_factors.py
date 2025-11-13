import json
from pathlib import Path

DATA_PATH = Path("job_architecture/data/wtw_ggs_factors.json")


def load_ggs_factors():
    """Carrega os fatores GGS do JSON."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def filter_levels_by_supervisor(superior):
    """
    Aplica o filtro hierárquico rígido.
    Define quais níveis de carreira podem aparecer conforme o superior imediato.
    """

    mapping = {
        "Supervisor": ["U1", "U2", "P1", "P2"],
        "Coordenador": ["P2", "P3", "P4"],
        "Gerente": ["P3", "P4", "M1"],
        "Diretor": ["M1", "M2"],
        "Vice-presidente": ["M2", "M3"],
        "Presidente / CEO": ["EX"]
    }

    return mapping.get(superior, None)


def map_factors_to_level(selected):
    """
    Recebe seleção dos fatores GGS e retorna:
      - career_band
      - career_level
      - survey_grade_range
    """

    band_scores = {}
    level_scores = []
    survey_ranges = []

    for factor, value in selected.items():
        level = value.get("selected")
        band = value.get("career_band")
        lvl = value.get("career_level")
        sgr = value.get("survey_grade_range")

        band_scores.setdefault(band, 0)
        band_scores[band] += 1
        level_scores.append(lvl)
        survey_ranges.append(sgr)

    dominant_band = sorted(band_scores.items(), key=lambda x: x[1], reverse=True)[0][0]

    flat_grades = []
    for g in survey_ranges:
        flat_grades.extend(g)

    survey_grade = round(sum(flat_grades) / len(flat_grades))

    return {
        "career_band": dominant_band,
        "career_level": max(level_scores),
        "survey_grade": survey_grade
    }
