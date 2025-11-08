import re
import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section

# -----------------------------
# Funções utilitárias
# -----------------------------
def safe_get(row, keys, default=""):
    """Retorna o primeiro campo válido na lista de possíveis nomes de coluna."""
    for k in keys:
        for col in row.index:
            if col.strip().lower() == k.strip().lower():
                val = str(row[col]).strip()
                if val and val.lower() != "nan":
                    return val
    return default

def format_paragraphs(text):
    """Formata blocos de texto em parágrafos separados por linha."""
    if not text:
        return "-"
    parts = re.split(r'\n+|•|\r', text.strip())
    return "".join(
        f"<p style='margin:0 0 6px 0; text-align:justify;'>{p.strip()}</p>"
        for p in parts if len(p.strip()) > 2
    )

# -----------------------------
# Página principal
# -----------------------------
data = load_data()
section("📋 Job Profile Description")

if "job_profile" not in data:
    st.error("Job Profile.csv não encontrado em /data")
else:
    df = data["job_profile"]

    # ===== CSS visual =====
    st.markdown("""
        <style>
        .compare-box { margin-top: -18px; }
        .compare-box .compare-label { margin: 4px 0 6px 0; font-weight: 600; color: #2b2d42; }
        div[data-baseweb="tag"] span {
            white-space: normal !important;
            word-break: break-word !important;
            line-height: 1.25 !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
        }
        div[data-baseweb="select"] > div { min-height: 44px !important; height: auto !important; }
        .description-card {
            background-color: #f9f9f9;
            padding: 10px 14px;
            border-radius: 8px;
            border-left: 4px solid #1E56E0;
            font-size: 0.9rem;
            line-height: 1.5;
            display: inline-block;
            width: 100%;
            margin-bottom: 14px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .title-section {
            font-weight: 700;
            color: #1E56E0;
            margin-top: 10px;
            margin-bottom: 4px;
            text-align: left;
        }
        </style>
    """, unsafe_allow_html=True)

    # ===== FILTROS =====
    col1, col2, col3 = st.columns([1.2, 2.2, 1])
    with col1:
        families = sorted(df["Job Family"].dropna().unique())
        fam = st.selectbox("Família", families)
    filtered = df[df["Job Family"] == fam]

    with col2:
        subs = sorted(filtered["Sub Job Family"].dropna().unique())
        sub = st.selectbox("Subfamília", subs)
    sub_df = filtered[filtered["Sub Job Family"] == sub]

    with col3:
        careers = sorted(sub_df["Career Path"].dropna().unique())
        career = st.selectbox("Trilha de Carreira", careers)
    career_df = sub_df[sub_df["Career Path"] == career]

    # ===== MULTISELECT =====
    def format_profile(row):
        g = row.get("Global Grade", "")
        p = row.get("Job Profile", "")
        return f"GG{int(g)} — {p}" if str(g).isdigit() else p

    career_df_sorted = career_df.sort_values(by="Global Grade", ascending=False)
    pick_options = career_df_sorted.apply(format_profile, axis=1).tolist()

    st.markdown('<div class="compare-box">', unsafe_allow_html=True)
    st.markdown('<div class="compare-label">Selecione até 3 cargos para comparar:</div>', unsafe_allow_html=True)
    selected_labels = st.multiselect("", options=pick_options, max_selections=3, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # ===== RESULTADO =====
    if selected_labels:
        st.markdown("---")
        st.markdown("### 🧾 Comparativo de Cargos Selecionados")

        cols = st.columns(len(selected_labels))
        for idx, label in enumerate(selected_labels):
            with cols[idx]:
                parts = re.split(r"\s*[–—-]\s*", label)
                label_grade = parts[0].replace("GG", "").strip() if parts else ""
                label_title = parts[1].strip() if len(parts) > 1 else label.strip()

                selected_row_df = career_df_sorted[
                    career_df_sorted["Job Profile"].str.strip().str.lower() == label_title.lower()
                ]
                if label_grade:
                    selected_row_df = selected_row_df[
                        selected_row_df["Global Grade"].astype(str).str.strip() == label_grade
                    ]
                if selected_row_df.empty:
                    st.warning(f"Cargo não encontrado: {label}")
                    continue

                row = selected_row_df.iloc[0]

                # Cabeçalho
                st.markdown(f"#### {row['Job Profile']}")
                st.markdown(
                    f"<p style='color:#1E56E0; font-weight:bold;'>GG {row['Global Grade']}</p>",
                    unsafe_allow_html=True
                )

                # Classificação
                st.markdown(f"""
                    <div style='background-color:#ffffff; padding:10px; border-radius:8px;
                    border:1px solid #e0e4f0; display:inline-block; width:100%;'>
                        <b>Família:</b> {row['Job Family']}<br>
                        <b>Subfamília:</b> {row['Sub Job Family']}<br>
                        <b>Carreira:</b> {row['Career Path']}<br>
                        <b>Função:</b> {row['Function Code']}<br>
                        <b>Disciplina:</b> {row['Discipline Code']}<br>
                        <b>Código:</b> {row['Full Job Code']}
                    </div>
                """, unsafe_allow_html=True)

                # Seções, incluindo a detecção automática do Grade Differentiator (com erros)
                sections = [
                    ("Sub Job Family Description", "🧭 Sub Job Family Description"),
                    ("Job Profile Description", "🧠 Job Profile Description"),
                    ("Role Description", "🎯 Role Description"),
                    (["Grade Differentiator", "Grade Differentiation", "Grade Differentiatior", "Grade Differentiators", " Grade Differentiator", "Grade Differentiator "], "🏅 Grade Differentiator"),
                    ("Specific parameters KPIs", "📊 KPIs / Specific Parameters"),
                    ("Competency 1", "💡 Competency 1"),
                    ("Competency 2", "💡 Competency 2"),
                    ("Competency 3", "💡 Competency 3"),
                    ("Qualifications", "🎓 Qualifications")
                ]

                for key, title in sections:
                    val = safe_get(row, key if isinstance(key, list) else [key])
                    if val:
                        formatted = format_paragraphs(val)
                        st.markdown(f"<div class='title-section'>{title}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='description-card'>{formatted}</div>", unsafe_allow_html=True)
