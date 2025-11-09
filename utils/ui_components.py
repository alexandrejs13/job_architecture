# utils/ui_components.py
import streamlit as st

BASE_CSS = """
<style>
/* Largura estável, sem “amassar” o conteúdo */
.block-container {
  max-width: 1700px !important;
  min-width: 1200px !important;
  margin: 0 auto !important;
}

/* Títulos */
h1, .ja-h1 {
  color: #1E56E0 !important;
  font-weight: 800 !important;
  font-size: 1.8rem !important;
  margin: 0 0 1rem 0 !important;
  display: flex; align-items: center; gap: 8px;
}

/* Cards padrões */
.ja-card {
  background: #fafafa; border-left: 4px solid #1E56E0; border-radius: 8px;
  padding: 10px 12px; box-shadow: 0 1px 3px rgba(0,0,0,.05);
}
.ja-card-title {
  font-weight: 700; color: #1E56E0; margin-bottom: 6px;
}

/* Grid generoso */
.ja-grid { display: grid; gap: 12px; }
.ja-grid.cols-2 { grid-template-columns: 1fr 1fr; }
.ja-grid.cols-3 { grid-template-columns: 1fr 1fr 1fr; }

/* Job Map específico */
.map-wrapper {
  overflow-x: auto; overflow-y: hidden;
  border-top: 3px solid #1E56E0; border-bottom: 3px solid #1E56E0;
  background: #fff; padding-bottom: 1rem; white-space: nowrap;
}
.jobmap-grid {
  display: grid; border-collapse: collapse; font-size: .85rem; text-align: center;
  width: max-content; position: relative; z-index: 0;
}
.jobmap-grid > div {
  border: 1px solid #ddd; box-sizing: border-box;
}
.header-family {
  font-weight: 800; color: #fff; padding: 10px; border-right: 2px solid #fff;
  white-space: normal; font-size: 1rem; display: flex; align-items: center; justify-content: center;
}
.header-subfamily {
  font-weight: 700; background: #f0f2ff; padding: 8px; white-space: normal; font-size: .95rem;
  display: flex; align-items: center; justify-content: center;
}
.grade-header {
  font-weight: 800; font-size: .95rem; background: #1E56E0; color: #fff; padding: 8px;
  border-right: 2px solid #fff; display: flex; align-items: center; justify-content: center;
  position: sticky; top: 0; left: 0; z-index: 40 !important;
}
.grade-cell {
  font-weight: 700; background: #eef3ff; border-right: 2px solid #1E56E0; padding: 6px 8px;
  position: sticky; left: 0; z-index: 30 !important; display: flex; align-items: center; justify-content: center;
}
.grade-cell::after { content: ""; position: absolute; right: 0; top: 0; height: 100%; width: 2px; background: rgba(0,0,0,0.05); }
.job-card {
  background: #fafafa; border-left: 4px solid #1E56E0; border-radius: 6px; padding: 5px 8px; margin: 3px 0;
  text-align: left; font-size: .82rem; box-shadow: 0 1px 2px rgba(0,0,0,.05); white-space: normal;
}
.job-card span { display: block; font-size: .75rem; color: #555; }
.job-card:hover { background: #f0f5ff; }
.grade-row:nth-child(even) { background: #fcfcfc; }

/* Responsividade leve (apenas reduz tamanho geral) */
@media (max-width: 1500px) { .block-container { zoom: 0.9; } }
@media (max-width: 1200px) { .block-container { zoom: 0.85; } }
</style>
"""

def inject_base_css():
    st.markdown(BASE_CSS, unsafe_allow_html=True)

def page_title(text_with_emoji: str):
    st.markdown(f"<div class='ja-h1'>{text_with_emoji}</div>", unsafe_allow_html=True)
