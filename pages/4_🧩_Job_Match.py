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

    # 🔍 Detecta automaticamente colunas de Family/Subfamily
    colunas_lower = {c.lower(): c for c in df.columns}

    family_col = None
    for nome in ["family", "job family", "job_family"]:
        if nome in colunas_lower:
            family_col = colunas_lower[nome]
            break

    subfamily_col = None
    for nome in ["subfamily", "sub-family", "sub family", "job sub-family", "job_subfamily"]:
        if nome in colunas_lower:
            subfamily_col = colunas_lower[nome]
            break

    # Se não encontrar, cria vazio
    if not family_col:
        df["Family"] = ""
    else:
        df.rename(columns={family_col: "Family"}, inplace=True)

    if not subfamily_col:
        df["Subfamily"] = ""
    else:
        df.rename(columns={subfamily_col: "Subfamily"}, inplace=True)

    # Normaliza capitalização
    df["Family"] = df["Family"].str.strip().str.title()
    df["Subfamily"] = df["Subfamily"].str.strip().str.title()

    # Garante que demais colunas existam
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
