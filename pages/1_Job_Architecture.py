import streamlit as st

def render():

    st.markdown("""
    <h1 class="page-title">
        <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png"
             class="page-title-icon">
        Job Architecture — Fundamentos e Governança
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p class="section-text">
    A <strong>Job Architecture (JA)</strong> é o modelo corporativo que estrutura de forma integrada todas as posições da organização,
    definindo agrupamento de funções, níveis de responsabilidade, critérios de progressão e diferenciais de complexidade.
    </p>

    <p class="section-text">
    Baseada na metodologia global da <strong>Willis Towers Watson (WTW)</strong>, a JA garante 
    <strong>equidade interna, consistência organizacional e comparabilidade externa</strong>,
    sustentando decisões estratégicas sobre estrutura, remuneração, carreira e sucessão.
    </p>
    """, unsafe_allow_html=True)

    # ======================
    # PILARES
    # ======================

    st.markdown("""<h2 class="section-title">Pilares Estruturantes</h2>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="sig-card">
            <strong>Governança Global</strong><br>
            Regras universais que asseguram comparabilidade entre países e funções.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="sig-card">
            <strong>Clareza de Carreira</strong><br>
            Estrutura que define bandas e grades, orientando progressão e mobilidade.
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="sig-card">
            <strong>Integração de Sistemas</strong><br>
            Base estruturada para performance, remuneração, sucessão e benchmarking.
        </div>
        """, unsafe_allow_html=True)

    # ======================
    # TABELA ESTRUTURA
    # ======================

    st.markdown("""<h2 class="section-title">Estrutura da Arquitetura</h2>""", unsafe_allow_html=True)

    st.markdown("""
    <table class="sig-table">
        <tr>
            <th>Elemento</th>
            <th>Propósito</th>
            <th>Exemplo</th>
        </tr>

        <tr>
            <td><strong>Job Family</strong></td>
            <td>Agrupa funções com competências similares.</td>
            <td>Finanças, Engenharia, RH</td>
        </tr>

        <tr>
            <td><strong>Sub-Job Family</strong></td>
            <td>Especializações dentro da Job Family.</td>
            <td>Contabilidade, Engenharia de Processo</td>
        </tr>

        <tr>
            <td><strong>Career Band</strong></td>
            <td>Nível hierárquico e escopo de influência.</td>
            <td>Profissional, Gerencial, Executivo</td>
        </tr>

        <tr>
            <td><strong>Global Grade</strong></td>
            <td>Diferencia complexidade entre níveis.</td>
            <td>GG07, GG09, GG12</td>
        </tr>

        <tr>
            <td><strong>Generic Profile</strong></td>
            <td>Descrição corporativa de referência.</td>
            <td>“Finance Specialist”, “HR Manager”</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

