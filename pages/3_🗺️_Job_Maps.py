import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section, card

data = load_data()
section("🗺️ Job Maps")

df = data.get("map") or data.get("map_2") or None
if df is None:
    st.error("Nenhum arquivo 'Map.csv' ou 'Map 2.csv' encontrado em /data")
else:
    # Normaliza colunas para evitar erros de capitalização
    df.columns = [c.strip() for c in df.columns]

    if "Job Family" not in df.columns:
        st.error("A coluna 'Job Family' não foi encontrada no dataset.")
    else:
        families = sorted(df["Job Family"].dropna().unique())
        fam = st.selectbox("Família:", families)

        if "Sub Job Family" in df.columns:
            subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].dropna().unique())
            sub = st.selectbox("Subfamília:", subs)
            filtered = df[df["Sub Job Family"] == sub]
        else:
            sub = None
            filtered = df[df["Job Family"] == fam]

        cols = st.columns(3)
        for i, (_, row) in enumerate(filtered.iterrows()):
            with cols[i % 3]:
                title = row.get("SIG Full Title", row.get("Job Profile", ""))
                subtitle = f"{row.get('Career Path','')} — GG {row.get('Global Grade','')}"
                card(title, subtitle)
