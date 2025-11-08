# 🧩 Job Match — Trecho seguro corrigido para carregamento da base
# (Substitui integralmente o bloco load_data anterior)

import streamlit as st
import pandas as pd
import csv

@st.cache_data(show_spinner=False)
def load_data():
    path = "data/Job Profile.csv"

    try:
        df = pd.read_csv(
            path,
            sep=",",
            engine="python",
            dtype=str,
            quotechar='"',
            escapechar="\\",
            quoting=csv.QUOTE_MINIMAL,
            on_bad_lines="skip",
        )
    except Exception:
        df = pd.read_csv(
            path,
            sep=";",
            engine="python",
            dtype=str,
            quotechar='"',
            escapechar="\\",
            quoting=csv.QUOTE_MINIMAL,
            on_bad_lines="skip",
        )

    df = df.fillna("")

    # 🔍 Detecta automaticamente Family/Subfamily
    colunas_lower = {c.lower().strip(): c for c in df.columns}

    family_col = next(
        (colunas_lower[n] for n in ["family", "job family", "job_family"] if n in colunas_lower),
        None
    )
    subfamily_col = next(
        (colunas_lower[n] for n in ["subfamily", "sub-family", "sub family", "job sub-family", "job_subfamily"] if n in colunas_lower),
        None
    )

    # Renomeia para nomes padronizados
    if family_col:
        df.rename(columns={family_col: "Family"}, inplace=True)
    else:
        df["Family"] = ""

    if subfamily_col:
        df.rename(columns={subfamily_col: "Subfamily"}, inplace=True)
    else:
        df["Subfamily"] = ""

    df["Family"] = df["Family"].str.strip().str.title()
    df["Subfamily"] = df["Subfamily"].str.strip().str.title()

    # Garante colunas obrigatórias
    for col in [
        "Job Title", "Grade", "Sub Job Family Description", "Job Profile Description",
        "Role Description", "Grade Differentiator", "KPIs/Specific Parameters", "Qualifications"
    ]:
        if col not in df.columns:
            df[col] = ""

    # Texto unificado para embeddings
    df["Merged_Text"] = (
        "Job Title: " + df["Job Title"] +
        " | Family: " + df["Family"] +
        " | Subfamily: " + df["Subfamily"] +
        " | Grade: " + df["Grade"] +
        " | Job Profile Description: " + df["Job Profile Description"] +
        " | Role Description: " + df["Role Description"] +
        " | Grade Differentiator: " + df["Grade Differentiator"] +
        " | KPIs: " + df["KPIs/Specific Parameters"]
    )

    return df
