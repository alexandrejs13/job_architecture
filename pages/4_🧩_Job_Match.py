# ==============================================================
# Interface
# ==============================================================

df = load_data()
if df.empty:
    st.error("⚠️ A base está vazia ou corrompida.")
    st.stop()

model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

st.markdown("## 🧩 Job Match")
st.markdown("""
Descubra o **cargo mais compatível** com suas responsabilidades e área de atuação.  
O sistema identifica automaticamente o **nível de senioridade** e o **escopo** com base na descrição das suas atividades.
""")

c1, c2 = st.columns(2)

# Always visible picklists
families = sorted(df.loc[df["Family"].ne(""), "Family"].unique().tolist())
family_selected = c1.selectbox("Selecione a Family", [""] + families)

# Subfamily box always visible (initially empty)
if family_selected:
    subs = (
        df.loc[(df["Family"] == family_selected) & (df["Subfamily"].ne("")), "Subfamily"]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )
else:
    subs = []

subfamily_selected = c2.selectbox(
    "Selecione a Subfamily",
    [""] + subs if subs else [""],
    disabled=(not family_selected)
)

descricao = st.text_area(
    "✍️ Descreva brevemente suas atividades:",
    placeholder="Exemplo: Apoio no processamento de folha de pagamento, controle de ponto e benefícios...",
    height=120
)
