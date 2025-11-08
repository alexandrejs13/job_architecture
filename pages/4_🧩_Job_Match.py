import re
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer, util

# ===========================================================
# ⚙️ Configuração da página
# ===========================================================
st.set_page_config(page_title="🧩 Job Match", layout="wide")

# ===========================================================
# 🧠 Cache de carregamento do modelo
# ===========================================================
@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer("paraphrase-MiniLM-L6-v2")

model = load_model()

# ===========================================================
# 📂 Carrega a base de dados de cargos
# ===========================================================
@st.cache_data(show_spinner=True)
def load_data():
    df = pd.read_csv("data/Job_Profile.csv")
    df.columns = [c.strip().title().replace("_", " ") for c in df.columns]

    # Padroniza colunas principais
    rename_map = {
        "Job Family": "Family",
        "Sub Job Family": "Subfamily",
        "Career Path": "Career Path",
        "Job Profile": "Job Profile",
        "Global Grade": "Grade",
    }
    df.rename(columns=rename_map, inplace=True)

    # Limpa valores nulos
    for c in ["Family", "Subfamily", "Job Profile", "Grade"]:
        df[c] = df.get(c, "").astype(str).fillna("").str.strip().str.title()

    # Concatena colunas para criar campo de busca semântico
    def safe_concat(row):
        cols = [
            "Job Profile Description",
            "Role Description",
            "Grade Differentiator",
            "Kpis / Specific Parameters",
            "Qualifications",
        ]
        text = " ".join(str(row[c]) for c in cols if c in row and pd.notna(row[c]))
        return re.sub(r"\s+", " ", text).strip()

    df["Merged_Text"] = df.apply(safe_concat, axis=1)
    df["Embedding"] = df["Merged_Text"].apply(lambda x: model.encode(x, convert_to_tensor=True))

    return df

df = load_data()

# ===========================================================
# 🎨 CSS customizado
# ===========================================================
st.markdown("""
<style>
.block-container {
  max-width: 1600px;
  margin: 0 auto;
}
h1 { font-size: 1.8rem; margin-bottom: 0.5rem; }
.ja-card {
  background: #f9f9f9;
  padding: 12px 16px;
  border-radius: 10px;
  border-left: 4px solid #1E56E0;
  margin-bottom: 16px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.ja-hd { display:flex; align-items:baseline; gap:10px; margin-bottom:8px; }
.ja-hd-title { font-size:1.1rem; font-weight:700; }
.ja-hd-grade { color:#1E56E0; font-weight:700; }
.ja-p { margin: 0 0 6px 0; text-align: justify; }
.ja-sec { margin-top: 8px; }
.ja-sec-h { font-weight:700; color:#1E56E0; margin-bottom:4px; }
button[title="View fullscreen"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ===========================================================
# 🧭 Cabeçalho
# ===========================================================
st.markdown("## 🧩 Job Match")
st.markdown("Identifique automaticamente o cargo mais compatível com base na descrição de suas atividades e nível de atuação.")

# ===========================================================
# 🔍 Seletores de filtros
# ===========================================================
col1, col2 = st.columns(2)
with col1:
    families = sorted(df["Family"].dropna().unique())
    selected_family = st.selectbox("Família", [""] + families, index=0)

with col2:
    subfamilies = []
    if selected_family:
        subfamilies = sorted(df[df["Family"] == selected_family]["Subfamily"].dropna().unique())
    selected_subfamily = st.selectbox("Subfamília", [""] + subfamilies, index=0)

# ===========================================================
# 📝 Campo de descrição
# ===========================================================
descricao = st.text_area(
    "✍️ Descreva brevemente suas atividades:",
    placeholder=(
        "Exemplo: Atuo como analista de remuneração, responsável por conduzir estudos salariais, elaborar políticas de benefícios "
        "e apoiar revisões de estrutura organizacional. Tenho 6 anos de experiência em RH corporativo, graduação em Administração "
        "e MBA em Gestão de Pessoas. Coordeno processos de meritocracia e indicadores de performance em ambiente multinacional."
    ),
    height=160
)

# ===========================================================
# 🚦 Validações iniciais
# ===========================================================
if st.button("🔎 Encontrar Job Profile", use_container_width=True):
    if not selected_family or not selected_subfamily:
        st.warning("⚠️ Selecione a **Família** e **Subfamília** antes de prosseguir.")
        st.stop()

    if len(descricao.split()) < 50:
        st.warning("""
        ⚠️ Descreva suas atividades com mais detalhes (mínimo de **50 palavras**).  
        Inclua informações como: responsabilidades principais, tempo de experiência, nível de autonomia, escopo da função e formação acadêmica.
        """)
        st.stop()

    st.info("🔄 Buscando correspondência mais precisa...")

    # Filtro da base pela family e subfamily
    df_filtered = df[(df["Family"] == selected_family) & (df["Subfamily"] == selected_subfamily)]

    if df_filtered.empty:
        st.error("Nenhum cargo encontrado para a combinação selecionada.")
        st.stop()

    # Calcula embedding da descrição
    query_embedding = model.encode(descricao, convert_to_tensor=True)
    df_filtered["Similarity"] = df_filtered["Embedding"].apply(lambda emb: float(util.cos_sim(query_embedding, emb)))

    best_row = df_filtered.sort_values(by="Similarity", ascending=False).iloc[0]
    sim_score = best_row["Similarity"] * 100

    st.success(f"✅ Cargo mais compatível encontrado ({sim_score:.1f}% de similaridade):")

    # ===========================================================
    # 🧱 Estrutura visual (mesmo formato do Job Profile Description)
    # ===========================================================
    def section(emoji, title, text):
        return f"""
        <div class='ja-sec'>
          <div class='ja-sec-h'>{emoji} {title}</div>
          <div class='ja-card'><div class='ja-p'>{re.sub(r'\\n+', '<br>', str(text))}</div></div>
        </div>
        """

    st.markdown(f"""
    <div class='ja-card'>
      <div class='ja-hd'>
        <div class='ja-hd-title'>{best_row["Job Profile"]}</div>
        <div class='ja-hd-grade'>GG {best_row["Grade"]}</div>
      </div>
      <div class='ja-p'>
        <b>Família:</b> {best_row["Family"]}<br>
        <b>Subfamília:</b> {best_row["Subfamily"]}<br>
        <b>Carreira:</b> {best_row["Career Path"]}<br>
        <b>Código:</b> {best_row["Full Job Code"] if "Full Job Code" in best_row else "-"}
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(section("🧭", "Sub Job Family Description", best_row.get("Sub Job Family Description", "")), unsafe_allow_html=True)
    st.markdown(section("🧠", "Job Profile Description", best_row.get("Job Profile Description", "")), unsafe_allow_html=True)
    st.markdown(section("🎯", "Role Description", best_row.get("Role Description", "")), unsafe_allow_html=True)
    st.markdown(section("🏅", "Grade Differentiator", best_row.get("Grade Differentiator", "")), unsafe_allow_html=True)
    st.markdown(section("📊", "KPIs / Specific Parameters", best_row.get("Kpis / Specific Parameters", "")), unsafe_allow_html=True)
    st.markdown(section("🎓", "Qualifications", best_row.get("Qualifications", "")), unsafe_allow_html=True)
