import re
import difflib
import streamlit as st
from utils.data_loader import load_data
from utils.ui_components import section

# -----------------------------
# Utilidades
# -----------------------------
def safe_get(row, keys, default=""):
    """Retorna o primeiro campo existente na ordem de keys."""
    for k in keys:
        if k in row and str(row[k]).strip() and str(row[k]).strip().lower() != "nan":
            return str(row[k])
    return default

def grade_int(x):
    try:
        return int(str(x).strip())
    except:
        return None

def bulletify(text):
    """Transforma parágrafos ou frases longas em bullets."""
    if not text:
        return "-"
    parts = re.split(r"[•\-–—]\s*|\n", text.strip())
    clean = [p.strip() for p in parts if len(p.strip()) > 3]
    return "<ul>" + "".join(f"<li>{p}</li>" for p in clean) + "</ul>"

def analyze_grade_signals(row):
    text = " ".join([
        safe_get(row, ["Role Description"]),
        safe_get(row, ["Grade Differentiation", "Grade Differentiator"]),
        safe_get(row, ["Competency"]),
        safe_get(row, ["Qualifications"]),
        safe_get(row, ["Job Profile Description"])
    ]).lower()
    score = 0
    signals = {
        "liderança": 3, "gestão de equipe": 2, "coordena": 2, "autonomia": 2,
        "estratégico": 3, "tático": 2, "operacional": 1, "regional": 2, "global": 3,
        "budget": 2, "orçamento": 2, "p&l": 3, "governança": 3, "políticas": 2
    }
    for k, v in signals.items():
        if k in text:
            score += v
    if len(text) > 800:
        score += 1
    return score

def executive_delta_summary(rows):
    """Gera um resumo executivo claro do porquê as grades diferem."""
    if not rows:
        return ""
    rows_sorted = sorted(rows, key=lambda r: grade_int(r.get("Global Grade")))
    enriched = []
    for r in rows_sorted:
        g = grade_int(r.get("Global Grade"))
        score = analyze_grade_signals(r)
        enriched.append({
            "grade": g,
            "title": r.get("Job Profile", ""),
            "score": score,
            "role": safe_get(r, ["Role Description"]),
            "diff": safe_get(r, ["Grade Differentiation", "Grade Differentiator"]),
            "comp": safe_get(r, ["Competency"])
        })

    bullets = []
    for i, item in enumerate(enriched):
        lane = []
        text = (item["role"] + " " + item["diff"] + " " + item["comp"]).lower()
        if "lider" in text or "gest" in text or "people" in text:
            lane.append("liderança de pessoas ou gestão de equipe")
        if any(k in text for k in ["estratég", "polític", "governança"]):
            lane.append("atuação estratégica e definição de diretrizes")
        if any(k in text for k in ["regional", "global", "corporativo"]):
            lane.append("escopo ampliado (regional/global)")
        if any(k in text for k in ["budget", "p&l", "orçamento"]):
            lane.append("responsabilidade financeira e orçamentária")
        if any(k in text for k in ["portfólio", "transformação", "programa"]):
            lane.append("gestão de programas e transformação organizacional")
        lane_txt = "; ".join(dict.fromkeys(lane)) if lane else "escopo e responsabilidades proporcionais ao nível"
        bullets.append(f"- **GG{item['grade']} – {item['title']}**: {lane_txt} (sinais de senioridade: {item['score']}).")

    comp_lines = []
    for a, b in zip(enriched, enriched[1:]):
        if b["score"] > a["score"]:
            comp_lines.append(
                f"- **Progressão GG{a['grade']} → GG{b['grade']}**: amplia **escopo** (local → regional/global), "
                f"**autonomia** (tático → estratégico), **liderança** (individual → gestão de times) "
                f"e **impacto** (operações → políticas e programas)."
            )

    summary = "#### 🔍 Resumo executivo das diferenças de grade\n"
    summary += "Os perfis evidenciam progressão consistente de **escopo**, **autonomia**, **liderança**, **complexidade** e **impacto**.\n\n"
    summary += "\n".join(bullets)
    if comp_lines:
        summary += "\n\n" + "\n".join(comp_lines)
    return summary

# -----------------------------
# Página principal
# -----------------------------
data = load_data()
section("📋 Job Profile Description")

if "job_profile" not in data:
    st.error("Job Profile.csv não encontrado em /data")
else:
    df = data["job_profile"]

    st.markdown(
        """
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
            margin-bottom: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

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
        selected_data = []

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
                selected_row = selected_row_df.iloc[0]
                selected_data.append(selected_row)

                st.markdown(f"#### {selected_row['Job Profile']}")
                st.markdown(f"<p style='color:#1E56E0; font-weight:bold;'>GG {selected_row['Global Grade']}</p>", unsafe_allow_html=True)

                # Classificação
                st.markdown(
                    f"""
                    <div style='background-color:#ffffff; padding:10px; border-radius:8px; border:1px solid #e0e4f0; display:inline-block; width:100%;'>
                        <b>Família:</b> {selected_row['Job Family']}<br>
                        <b>Subfamília:</b> {selected_row['Sub Job Family']}<br>
                        <b>Carreira:</b> {selected_row['Career Path']}<br>
                        <b>Função:</b> {selected_row['Function Code']}<br>
                        <b>Disciplina:</b> {selected_row['Discipline Code']}<br>
                        <b>Código:</b> {selected_row['Full Job Code']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Seções principais
                sections = [
                    ("Sub Job Family Description", "🧭 Sub Job Family Description"),
                    ("Job Profile Description", "🧠 Job Profile Description"),
                    ("Role Description", "🎯 Role Description"),
                    ("Grade Differentiation", "🏅 Grade Differentiator"),
                    ("Specific parameters / KPIs", "📊 KPIs / Specific Parameters"),
                    ("Competency", "💡 Competency"),
                    ("Qualifications", "🎓 Qualifications")
                ]
                for key, title in sections:
                    val = safe_get(selected_row, [key])
                    if val:
                        formatted = bulletify(val) if key in ["Role Description", "Grade Differentiation"] else val
                        st.markdown(f"**{title}**")
                        st.markdown(f"<div class='description-card'>{formatted}</div>", unsafe_allow_html=True)

        # ===== Resumo executivo =====
        if len(selected_data) > 1:
            st.markdown("---")
            st.markdown(executive_delta_summary(selected_data), unsafe_allow_html=True)
