st.markdown("""
<style>
.block-container {
  max-width: 1200px !important;
  min-width: 900px !important;
  margin: 0 auto !important;
  padding: 2.5rem 1.5rem 2rem 1.5rem;
  zoom: 0.9;
}

/* ===== TÍTULOS ===== */
h1 {
  text-align: left !important;
  margin-top: 0.8rem !important;
  margin-bottom: 1.4rem !important;
  font-size: 1.9rem !important;
  line-height: 1.25 !important;
  font-weight: 800 !important;
  color: #145efc !important;
}

/* ===== GRID ===== */
.ja-grid {
  display: grid;
  gap: 14px 14px;
  justify-items: stretch;
  align-items: stretch; /* garante que os filhos tenham mesma altura */
  margin: 6px 0 12px 0 !important;
}

.ja-grid.cols-1 { grid-template-columns: repeat(1, minmax(250px, 1fr)); }
.ja-grid.cols-2 { grid-template-columns: repeat(2, minmax(300px, 1fr)); }
.ja-grid.cols-3 { grid-template-columns: repeat(3, minmax(340px, 1fr)); }

/* ===== CARDS ===== */
.ja-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  background: #f9f9f9;
  padding: 10px 14px;
  border-radius: 6px;
  border-left: 3px solid #1E56E0;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  width: 100%;
  text-align: left;
  box-sizing: border-box;
  flex: 1; /* força a altura uniforme */
}

.ja-sec {
  margin: 0 !important;
  text-align: left;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.ja-sec-h {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 6px;
  margin: 0 0 3px 0 !important;
}

.ja-ic { width: 18px; text-align: center; line-height: 1; }

.ja-ttl {
  font-weight: 700;
  color: #1E56E0;
  font-size: 0.95rem;
}

/* ===== HEADER CARGO ===== */
.ja-hd {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 4px;
  margin: 0 0 6px 0;
  text-align: left;
}

.ja-hd-title {
  font-size: 1.15rem;
  font-weight: 700;
}

.ja-hd-grade {
  color: #1E56E0;
  font-weight: 700;
  font-size: 1rem;
}

/* ===== BLOCO CLASSIFICAÇÃO ===== */
.ja-class {
  background: #fff;
  border: 1px solid #e0e4f0;
  border-radius: 6px;
  padding: 8px 12px;
  width: 100%;
  text-align: left;
  box-sizing: border-box;
  min-height: 130px;
}

/* ===== PARÁGRAFOS ===== */
.ja-p {
  margin: 0 0 4px 0;
  text-align: left;
  line-height: 1.48;
}
</style>
""", unsafe_allow_html=True)
