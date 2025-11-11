st.markdown("""
<style>
/* ====== CONTAINER DOS PILARES ====== */
.pillar-container {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    justify-content: space-between;
    align-items: stretch;
    margin-top: 20px;
}

/* ====== CARTÃO ====== */
.pillar-card {
    background: #ffffff;
    border-radius: 14px;
    border-left: 6px solid #145efc;
    padding: 26px 28px;
    flex: 1;
    min-width: 280px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.pillar-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
}

/* ====== TÍTULO ====== */
.pillar-title {
    font-weight: 800;
    font-size: 1.25rem;
    color: #145efc;
    margin-bottom: 12px;
}

/* ====== TEXTO ====== */
.pillar-text {
    color: #333333;
    font-size: 1.05rem;
    line-height: 1.55;
    flex-grow: 1;
}
</style>

<!-- ====== BLOCO DOS PILARES ====== -->
<div class="pillar-container">

  <div class="pillar-card">
    <div class="pillar-title">Governança Global</div>
    <div class="pillar-text">
      Define princípios corporativos e metodologias comuns para classificação, avaliação e manutenção de cargos. 
      Garante consistência e integridade das informações em todos os níveis da organização.
    </div>
  </div>

  <div class="pillar-card">
    <div class="pillar-title">Clareza de Carreira</div>
    <div class="pillar-text">
      Proporciona visibilidade sobre caminhos de crescimento e evolução profissional, 
      facilitando a mobilidade interna e o desenvolvimento de talentos.
    </div>
  </div>

  <div class="pillar-card">
    <div class="pillar-title">Integração de Sistemas</div>
    <div class="pillar-text">
      Alinha a estrutura de cargos aos sistemas corporativos de RH e gestão, 
      assegurando que os dados fluam de forma integrada e suportem decisões estratégicas.
    </div>
  </div>

</div>
""", unsafe_allow_html=True)
