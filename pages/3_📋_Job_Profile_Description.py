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
.block-container { max-width: 95% !important; }
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
# 3. FUNÇÃO DE CARREGAMENTO DE DADOS
# ==============================================================================
@st.cache_data
def load_job_profile_df():
    # -----------------------------------------------------------
    # 👇 TENTE CARREGAR SEU ARQUIVO AQUI
    # Se o seu arquivo se chama "Base_Cargos.xlsx", mude abaixo:
    # -----------------------------------------------------------
    file_name = "data.xlsx" 
    
    try:
        return pd.read_excel(file_name)
    except Exception:
        # Se der erro ou não achar o arquivo, usa estes dados de teste para não quebrar o app
        return pd.DataFrame({
            "Job Family": ["Tech", "Finance"],
            "Sub Job Family": ["Software Engineering", "Accounting"],
            "Career Path": ["Professional", "Professional"],
            "Global Grade": ["10", "11"],
            "Job Profile": ["Developer Example", "Accountant Example"],
            "Full Job Code": ["T-SE-P3", "F-AC-P3"],
            "Function Code": ["TEC", "FIN"],
            "Discipline Code": ["SWE", "ACC"],
            "Sub Job Family Description": ["Desc Família Tech...", "Desc Família Finança..."],
            "Job Profile Description": ["Faz código...", "Faz contas..."],
            "Career Band Description": ["Nível Pleno...", "Nível Sênior..."],
            "Role Description": ["- Codar\n- Testar", "- Balanços\n- Auditoria"],
            "Grade Differentiator": ["Escopo médio...", "Escopo grande..."],
            "Qualifications": ["Superior completo", "Pós-graduação"]
        })

def safe_get(row, key, default="-"):
    val = row.get(key, default)
    return str(val).strip() if not pd.isna(val) and str(val).strip() != "" else default

def format_paragraphs(text):
    if not text or str(text).strip() in ["-", "nan", "None"]: return "-"
    parts = re.split(r"\n+|•|\r", str(text).strip())
    return "".join(f"<p class='jp-p'>• {html.escape(p.strip())}</p>" for p in parts if len(p.strip()) > 1)

# ==============================================================================
# 4. LÓGICA DA PÁGINA
# ==============================================================================
df = load_job_profile_df()
section("📋 Job Profile Description")

if df is not
