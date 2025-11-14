# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path

# ==============================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================
# CARREGAR CSS GLOBAL (fonts, theme, menu)
# ==============================================
assets_path = Path(__file__).parents[1] / "assets"

css_files = ["fonts.css", "theme.css", "menu.css"]
for css_name in css_files:
    css_path = assets_path / css_name
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==============================================
# TÍTULO PRINCIPAL COM ÍCONE (2 cm ~ 70 px)
# ==============================================
st.markdown(
    """
    <div style="display:flex; align-items:center; gap:18px; margin-bottom:24px;">
        <img src="https://raw.githubusercontent.com/alexandrejs13/job_architecture/main/assets/icons/governance.png"
             style="width:70px; height:70px;">
        <h1 class="page-main-title">Job Architecture</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================
# INTRODUÇÃO
# ==============================================
st.markdown(
    """
    <p>
    A <strong>Job Architecture (JA)</strong> é o modelo corporativo que estrutura de forma integrada todas as posições da organização,
    definindo agrupamento de funções, níveis de responsabilidade, critérios de progressão e diferenciais de complexidade.
    </p>

    <p>
    Baseada na metodologia global da <strong>Willis Towers Watson (WTW)</strong>, a JA garante
    <strong>equidade interna, consistência organizacional e comparabilidade externa</strong>, 
    sustentando decisões estratégicas sobre estrutura, remuneração, carreira e sucessão.
    </p>

    <p>
    Mais do que um catálogo de cargos, trata-se de uma 
    <strong>infraestrutura de governança</strong> que conecta o desenho organizacional à gestão de talentos,
    assegurando práticas claras, coerentes e orientadas por propósito.
    </p>
    """,
    unsafe_allow_html=True,
)

# ==============================================
# PILARES ESTRUTURANTES (3 CARDS)
# ==============================================
st.markdown('<div class="section-title">Pilares Estruturantes</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="sig-card">
            <h3 style="font-family:'PPSIGFlow'; font-weight:600; font-size:16px; color:#145efc; margin-top:0;">
                Governança Global
            </h3>
            <p>
                Regras universais que asseguram comparabilidade entre países e funções,
                garantindo integridade organizacional.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="sig-card">
            <h3 style="font-family:'PPSIGFlow'; font-weight:600; font-size:16px; color:#145efc; margin-top:0;">
                Clareza de Carreira
            </h3>
            <p>
                Estrutura que define bandas e grades, orientando diferenciação de níveis, 
                progressão e mobilidade.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="sig-card">
            <h3 style="font-family:'PPSIGFlow'; font-weight:600; font-size:16px; color:#145efc; margin-top:0;">
                Integração de Sistemas
            </h3>
            <p>
                Base estruturada para performance, remuneração, sucessão e benchmarking global.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==============================================
# ESTRUTURA DA ARQUITETURA – TABELA
# ==============================================
st.markdown('<div class="section-title">Estrutura da Arquitetura</div>', unsafe_allow_html=True)

st.markdown(
    """
    <p>
    A arquitetura é composta por cinco elementos integrados, formando um modelo padronizado e comparável globalmente:
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <table>
        <thead>
            <tr>
                <th>Elemento</th>
                <th>Propósito</th>
                <th>Exemplo</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Job Family</strong></td>
                <td>Agrupa funções com competências similares e natureza de trabalho comum.</td>
                <td>Finanças, Engenharia, RH</td>
            </tr>
            <tr>
                <td><strong>Sub-Job Family</strong></td>
                <td>Distingue especializações técnicas dentro de cada Job Family.</td>
                <td>Contabilidade, Engenharia de Processo</td>
            </tr>
            <tr>
                <td><strong>Career Band</strong></td>
                <td>Representa o nível hierárquico e escopo de influência.</td>
                <td>Profissional, Gerencial, Executivo</td>
            </tr>
            <tr>
                <td><strong>Global Grade</strong></td>
                <td>Diferencia complexidade e contribuição entre os níveis.</td>
                <td>GG07, GG09, GG12</td>
            </tr>
            <tr>
                <td><strong>Generic Profile</strong></td>
                <td>Descrição corporativa de referência do nível.</td>
                <td>“Finance Specialist”, “HR Manager”</td>
            </tr>
        </tbody>
    </table>
    """,
    unsafe_allow_html=True,
)

# ==============================================
# IMPORTÂNCIA ESTRATÉGICA
# ==============================================
st.markdown('<div class="section-title">Importância Estratégica</div>', unsafe_allow_html=True)

st.markdown(
    """
    <p>
    A <strong>Job Architecture</strong> é o alicerce das práticas de gestão de pessoas e governança corporativa.
    Ela fornece uma linguagem comum para estruturar, comparar e avaliar cargos, promovendo decisões justas e sustentáveis.
    </p>

    <p>
    Com base em critérios consistentes de complexidade e contribuição, o modelo da WTW permite 
    <strong>equidade interna, benchmarking de mercado e mapeamento de carreiras</strong> de forma padronizada.
    </p>

    <p>
    Ao integrar estrutura organizacional, remuneração e desenvolvimento, a JA fortalece a conexão entre 
    <strong>estratégia de negócios, desempenho organizacional e evolução profissional</strong>,
    garantindo coerência global e meritocracia.
    </p>
    """,
    unsafe_allow_html=True,
)
