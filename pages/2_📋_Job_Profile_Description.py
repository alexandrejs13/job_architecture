# utils/data_loader.py
from __future__ import annotations
import csv
import io
import re
from pathlib import Path
from typing import Dict, Tuple, List

import pandas as pd
import streamlit as st


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _read_csv_robust(path: Path) -> Tuple[pd.DataFrame, List[int], str]:
    """
    Lê um CSV tentando separadores e configurações seguras.
    Retorna (df, linhas_inconsistentes, separador_detectado)
    """
    raw = path.read_text(encoding="utf-8", errors="replace")
    # normaliza quebras de linha "estranhas"
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")

    candidates = [",", ";", "\t", "|"]
    last_err = None
    detected_sep = ","

    for sep in candidates:
        try:
            df = pd.read_csv(
                io.StringIO(raw),
                sep=sep,
                engine="python",
                dtype=str,
                quotechar='"',
                escapechar="\\",
                skipinitialspace=True,
                keep_default_na=False,
            )
            # heurística mínima: precisa ter ao menos 5 colunas
            if df.shape[1] >= 5:
                detected_sep = sep
                break
        except Exception as e:
            last_err = e
            df = None  # noqa

    if df is None:
        # fallback auto-sniff
        df = pd.read_csv(
            io.StringIO(raw),
            sep=None,               # autodetect
            engine="python",
            dtype=str,
            quotechar='"',
            escapechar="\\",
            skipinitialspace=True,
            keep_default_na=False,
        )

    # strip de colunas e normalizações
    df.columns = [c.strip() for c in df.columns]

    # mapeia variações comuns de nomes
    col_map = {
        "grade differentiatior": "Grade Differentiator",
        "grade differentiator": "Grade Differentiator",
        "grade differentiation": "Grade Differentiator",
        "specific parameters kpis": "Specific parameters KPIs",
        "specific parameters / kpis": "Specific parameters KPIs",
    }
    fixed = {}
    for c in df.columns:
        key = c.strip().lower()
        fixed[c] = col_map.get(key, c)
    df.rename(columns=fixed, inplace=True)

    # diagnostica linhas com contagem de campos diferente do cabeçalho
    # (usa o mesmo separador detectado e regras de aspas)
    bad_rows: List[int] = []
    try:
        reader = csv.reader(io.StringIO(raw), delimiter=detected_sep, quotechar='"', escapechar="\\")
        rows = list(reader)
        if rows:
            header_len = len(rows[0])
            for idx, r in enumerate(rows[1:], start=2):  # 1-based + header
                if len(r) != header_len:
                    bad_rows.append(idx)
    except Exception:
        # se algo der errado no diagnóstico, apenas ignore
        pass

    # padroniza espaços em branco em todas as células
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return df, bad_rows, detected_sep


def load_data() -> Dict[str, pd.DataFrame]:
    """
    Carrega todos os arquivos necessários do app.
    Mostra alertas amigáveis no Streamlit se encontrar problemas.
    """
    datasets = {}
    problems = []

    files = {
        "job_profile": "Job Profile.csv",
        "job_family": "Job Family.csv",
        "sub_job_family": "Sub Job Family.csv",
        "map": "Map.csv",
        "map2": "Map 2.csv",
        "levels": "Level Structure.csv",
        "glossary": "Glossary.csv",
    }

    for key, fname in files.items():
        path = DATA_DIR / fname
        if not path.exists():
            problems.append(f"Arquivo ausente: {fname}")
            continue

        try:
            df, bad_rows, sep = _read_csv_robust(path)
            datasets[key] = df

            if bad_rows:
                # mostra apenas as 10 primeiras linhas com problema para não poluir
                preview = ", ".join(map(str, bad_rows[:10]))
                more = "" if len(bad_rows) <= 10 else f" … (+{len(bad_rows)-10} linhas)"
                st.warning(
                    f"**{fname}** carregado com separador **{repr(sep)}**, "
                    f"mas há linhas com contagem de campos diferente do cabeçalho: "
                    f"{preview}{more}. Verifique vírgulas não protegidas por aspas."
                )

        except Exception as e:
            problems.append(f"Erro ao carregar {fname}: {e}")

    if problems:
        st.error("Ocorreram problemas ao carregar os dados:\n- " + "\n- ".join(problems))

    return datasets
