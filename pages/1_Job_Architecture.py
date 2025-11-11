# ===========================================================
# 5. PILARES DA ARQUITETURA (AJUSTADOS E ALINHADOS)
# ===========================================================
st.markdown("""
<style>
.pillar-row {
    display: flex;
    justify-content: space-between;
    align-items: stretch;
    gap: 20px;
    flex-wrap: wrap;
    margin-top: 10px;
}
.pillar-card {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    background-color: #ffffff;
    border-left: 5px solid #145efc;
    border-radius: 10px;
    padding: 22px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    min-height: 280px;
    transition: all 0.2s ease-in-out;
}
.pillar-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.08);
}
.pillar-title {
    font-weight: 700;
    color: #145efc;
    font-size: 1.05rem;
    margin-bottom: 6px;
}
.pillar-text {
    color: #333333;
    font-size: 0.98rem;
    line-height: 1.6;
    flex-grow: 1;
}
</style>

<div class="section-title">Pilares Estruturantes</div>

<div class="pillar-row">

    <div class="pillar-card">
        <div class="pillar-title">Governança Global</div>
        <div class="pillar-text">
            Define princípios, critérios e regras universais para a criação, atualização e manutenção dos cargos, 
            garantindo comparabilidade entre países, funções e níveis organizacionais.  
            Essa governança assegura que toda posição seja avaliada de acordo com padrões globais e práticas de mercado reconhecidas.
        </div>
    </div>

    <div class="pillar-card">
        <div class="pillar-title">Clareza de Carreira</div>
        <div class="pillar-text">
            Cada cargo é vinculado a um <strong>Career Band</strong> e <strong>Global Grade</strong>, refletindo o escopo de atuação, 
            o grau de autonomia e a natureza da contribuição.  
            Essa estrutura fornece visibilidade sobre oportunidades de progressão, diferenciação de níveis e mobilidade lateral entre áreas.
        </div>
    </div>

    <div class="pillar-card">
        <div class="pillar-title">Integração de Sistemas</div>
        <div class="pillar-text">
            A Job Architecture serve como base única de referência para os principais processos de 
            <strong>Remuneração, Performance Management, Talent Review</strong> e 
            <strong>Benchmarking de Mercado</strong>.  
            Isso garante que as decisões de pessoas estejam ancoradas em um modelo técnico e sustentável.
        </div>
    </div>

</div>
""", unsafe_allow_html=True)
