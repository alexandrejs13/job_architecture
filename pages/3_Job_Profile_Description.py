import streamlit as st
import pandas as pd
import re
import html
from utils.ui import setup_sidebar, section

# ==============================================================================
# 1. CONFIGURAÇÃO INICIAL
# ==============================================================================
st.set_page_config(page_title="Job Profile Description", page_icon="📋", layout="wide")
setup_sidebar()

# ==============================================================================
# 2. CSS ESPECÍFICO DA PÁGINA
# ==============================================================================
st.markdown("""
<style>
:root {
--blue: #145efc;
--gray-line: #e0e0e0;
--gray-bg: #f8f9fa;
--dark-gray: #2c3e50;
}

/* Estilo para garantir que o contêiner não fique muito apertado */
.block-container { max-width: 95% !important; }

/* Estilos do grid de comparação */
.comparison-grid { display: grid; gap: 25px; margin-top: 20px; }
.grid-cell { background: #fff; border: 1px solid var(--gray-line); padding: 20px; display: flex; flex-direction: column; }
.header-cell { background: var(--gray-bg); border-radius: 12px 12px 0 0; border-bottom: none; min-height: 100px; justify-content: center; }
.jp-title { font-size: 22px; font-weight: 800; color: var(--dark-gray); line-height: 1.2; margin-bottom: 8px; }
.jp-gg { color: var(--blue); font-weight: 700; font-size: 1.1rem; }

.meta-cell { background: #fff; border-top: 1px solid var(--gray-line); border-bottom: 1px solid var(--gray-line); font-size: 0.9rem; color: #555; gap: 8px; padding: 15px 20px; }
.meta-row { display: flex; flex-wrap: wrap; gap: 15px; }
.meta-item strong { color: #333; font-weight: 700; }

.section-cell { border-left-width: 5px; border-left-style: solid; border-top: none; background: #fdfdfd; padding: 15px 20px; }
.section-title { font-weight: 700; font-size: 1rem; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
.section-content { color: #333; line-height: 1.6; font-size: 0.95rem; }
.jp-p { margin: 0 0 8px 0; }
.footer-cell { height: 15px; border-top: none; border-radius: 0 0 12px 12px; background: #fff; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. FUNÇÕES AUXILIARES E CARREGAMENTO DE DADOS
# ==============================================================================
@st.cache_data
def load_job_profile_df():
    # --- CORREÇÃO DO CAMINHO DO ARQUIVO ---
    file_path = "data/Job Profile.xlsx"
    try:
        # Tenta carregar o arquivo Excel real do caminho correto
        df = pd.read_excel(file_path)
        # Opcional: converte todas as colunas de texto para string para garantir filtros corretos
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).str.strip()
        return df
    except Exception as e:
        # Mensagem de erro se o arquivo não for encontrado ou tiver problemas de leitura
        st.error(f"Erro Crítico: Não foi possível carregar o arquivo {file_path}. Detalhe: {e}")
        # Retorna um DataFrame vazio para evitar que o app quebre
        return pd.DataFrame()

def safe_get(row, key, default="-"):
    """Retorna o valor da célula de forma segura, tratando NaNs e Strings vazias."""
    val = row.get(key, default)
    if pd.isna(val) or str(val).strip() == "":
        return default
    return html.escape(str(val)).replace("\n", "<br>")

# ==============================================================================
# 4. CONTEÚDO PRINCIPAL
# ==============================================================================
df = load_job_profile_df()
if df.empty:
    st.warning("⚠️ Não foi possível carregar o arquivo de perfis de cargo.")
else:
    families = sorted(df["Job Family"].dropna().unique())
    col1, col2, col3 = st.columns(3)

    with col1:
        fam = st.selectbox("Família (Job Family):", families)
    with col2:
        subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].dropna().unique())
        sub = st.selectbox("Sub-Família:", subs)
    with col3:
        paths = sorted(df[df["Sub Job Family"] == sub]["Career Path"].dropna().unique())
        path = st.selectbox("Trilha de Carreira:", paths)

    filtered = df[
        (df["Job Family"] == fam)
        & (df["Sub Job Family"] == sub)
        & (df["Career Path"] == path)
    ]

    profiles = sorted(filtered["Job Profile"].unique())
    selected_profiles = st.multiselect(
        "Selecione até 3 perfis de cargo para comparar:",
        options=profiles,
        max_selections=3
    )

    if selected_profiles:
        st.markdown('<div class="comparison-grid">', unsafe_allow_html=True)
        for profile in selected_profiles:
            row = filtered[filtered["Job Profile"] == profile].iloc[0]
            st.markdown(f"""
            <div class="grid-cell">
                <div class="header-cell">
                    <div class="jp-title">{safe_get(row, 'Job Profile')}</div>
                    <div class="jp-gg">Global Grade: {safe_get(row, 'Global Grade')}</div>
                </div>
                <div class="meta-cell">
                    <div class="meta-row">
                        <div class="meta-item"><strong>Career Band:</strong> {safe_get(row, 'Career Band')}</div>
                        <div class="meta-item"><strong>Career Path:</strong> {safe_get(row, 'Career Path')}</div>
                        <div class="meta-item"><strong>Sub Job Family:</strong> {safe_get(row, 'Sub Job Family')}</div>
                    </div>
                </div>

                <div class="section-cell" style="border-color:#145efc">
                    <div class="section-title">📘 Job Profile Description</div>
                    <div class="section-content">{safe_get(row, 'Job Profile Description')}</div>
                </div>

                <div class="section-cell" style="border-color:#673ab7">
                    <div class="section-title">🏛️ Career Band Description</div>
                    <div class="section-content">{safe_get(row, 'Career Band Description')}</div>
                </div>

                <div class="section-cell" style="border-color:#1e56e0">
                    <div class="section-title">🎯 Role Description</div>
                    <div class="section-content">{safe_get(row, 'Role Description')}</div>
                </div>

                <div class="section-cell" style="border-color:#ff9800">
                    <div class="section-title">🏅 Grade Differentiator</div>
                    <div class="section-content">{safe_get(row, 'Grade Differentiator')}</div>
                </div>

                <div class="section-cell" style="border-color:#009688">
                    <div class="section-title">🎓 Qualifications</div>
                    <div class="section-content">{safe_get(row, 'Qualifications')}</div>
                </div>

                <div class="footer-cell"></div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("👆 Selecione até **3 perfis de cargo** para comparar.")
