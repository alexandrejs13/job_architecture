st.markdown("""
<style>

/* ====== CONTAINER CENTRAL ====== */
.block-container {
  max-width: 1200px !important;
  min-width: 900px !important;
  margin: 0 auto !important;
  padding: 2.5rem 1.5rem 2rem 1.5rem; /* mais espaço no topo */
  zoom: 0.9;
}

/* ====== ESCALA RESPONSIVA ====== */
html, body, [class*="css"] {
  font-size: calc(13px + 0.18vw) !important;
}

/* ====== TÍTULO DA PÁGINA ====== */
h1 {
  text-align: left !important;
  margin-top: 0.8rem !important;
  margin-bottom: 1.4rem !important;
  line-height: 1.25 !important;
  overflow-wrap: break-word !important;
  white-space: normal !important;
  word-break: break-word !important;
  font-size: 1.9rem !important;
}
h2, h3 {
  text-align: left !important;
  margin-top: 1rem !important;
  margin-bottom: 1.1rem !important;
}

/* ====== SIDEBAR ====== */
[data-testid="stSidebar"][aria-expanded="true"]{
  width: 300px !important;
  min-width: 300px !important;
  max-width: 300px !important;
}
[data-testid="stSidebarCollapsedControl"]{
  width: 300px !important;
}

/* ====== TEXTOS ====== */
.ja-p {
  margin: 0 0 4px 0;
  text-align: left;
  line-height: 1.48;
}

/* ====== TÍTULOS DE CARGO ====== */
.ja-hd {
  display:flex;
  flex-direction:column;
  align-items:flex-start;
  justify-content:flex-start;
  gap:4px;
  margin:0 0 6px 0;
  text-align:left;
}
.ja-hd-title {
  font-size:1.15rem;
  font-weight:700;
}
.ja-hd-grade {
  color:#1E56E0;
  font-weight:700;
  font-size:1rem;
}

/* ====== CLASSE DE CARGO ====== */
.ja-class {
  background:#fff;
  border:1px solid #e0e4f0;
  border-radius:6px;
  padding:8px 12px;
  width:100%;
  text-align:left;
  box-sizing:border-box;
  min-height:130px;
}

/* ====== SEÇÕES ====== */
.ja-sec { margin: 0 !important; text-align:left; }
.ja-sec-h {
  display:flex;
  align-items:center;
  justify-content:flex-start;
  gap:6px;
  margin:0 0 3px 0 !important;
}
.ja-ic { width:18px; text-align:center; line-height:1; }
.ja-ttl {
  font-weight:700;
  color:#1E56E0;
  font-size:0.95rem;
}
.ja-card {
  background:#f9f9f9;
  padding:10px 14px;
  border-radius:6px;
  border-left:3px solid #1E56E0;
  box-shadow:0 1px 2px rgba(0,0,0,0.05);
  width:100%;
  text-align:left;
  display:block;
  min-height:120px;
  box-sizing:border-box;
}

/* ====== GRID ====== */
.ja-grid {
  display:grid;
  gap:14px 14px;
  justify-items:stretch;
  align-items:start;
  margin:6px 0 12px 0 !important;
}
.ja-grid.cols-1 { grid-template-columns: repeat(1, minmax(250px, 1fr)); }
.ja-grid.cols-2 { grid-template-columns: repeat(2, minmax(300px, 1fr)); }
.ja-grid.cols-3 { grid-template-columns: repeat(3, minmax(340px, 1fr)); }

/* ====== MULTISELECT ====== */
.compare-box { margin-top:-14px; }
.compare-box .compare-label {
  margin:4px 0 5px 0;
  font-weight:600;
  color:#2b2d42;
  font-size:0.85rem;
}
div[data-baseweb="tag"] span {
  white-space: normal !important;
  word-break: break-word !important;
  line-height: 1.15 !important;
  font-weight: 600 !important;
  font-size: 0.82rem !important;
}
div[data-baseweb="select"] > div {
  min-height:38px !important;
  height:auto !important;
}
</style>
""", unsafe_allow_html=True)
