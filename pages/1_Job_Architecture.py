# -*- coding: utf-8 -*-
# pages/1_Job_Architecture.py

import streamlit as st
from pathlib import Path
from utils.ui import sidebar_logo_and_title

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar SIG com logo
sidebar_logo_and_title("assets/SIG_Logo_RGB_Black.png")

# ==========================================================
# TÍTULO SIG
# ==========================================================

st.markdown("""
<div class="sig-title">
    <img src="assets/icons/governance.png">
    <span>Job Architecture — Fundamentos e Governança</span>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# CONTEÚDO 1 — CONCEITO CENTRAL (CONTEÚDO ORIGINAL)
# ==========================================================

st.markdown("""
<div class="sig-card">
<div style="text-align: justify;">

A <strong>Job Architecture (JA)</strong> é o modelo corporativo que estrutura de forma integrada todas as posições da organização, 
definindo a lógica de agrupamento de funções, níveis de responsabilidade, critérios de progressão e diferenciais de complexidade.

Baseada na metodologia global da <strong>Willis Towers Watson (WTW)</strong>, a Job Architecture fornece um framework que garante 
<strong>equidade interna, consistência organizacional e comparabilidade externa</strong>, sustentando decisões estratégicas sobre 
estrutura, remuneração, carreira e sucessão.

Mais do que um catálogo de cargos, trata-se de uma <strong>infraestrutura de governança</strong> que conecta o desenho organizacional 
à gestão de talentos, assegurando que as práticas de gestão de pessoas sejam <strong>claras, coerentes e orientadas por propósito.</strong>

</div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# CONTEÚDO 2 — PILARES (CONTEÚDO ORIGINAL + SIG CARDS)
# ==========================================================

st.markdown("""
<div class="sig-card">
    <h3>Pilares Estruturantes</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="sig-card">
        <strong style="color:#145efc; font-size:1.1rem;">Governança Global</strong>
        <p>
        Define princípios, critérios e regras universais para a criação, atualização e manutenção dos cargos, garantindo comparabilidade entre países, funções e níveis organizacionais.  
        Essa governança assegura que toda posição seja avaliada de acordo com padrões globais e práticas de mercado reconhecidas.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="sig-card">
        <strong style="color:#145efc; font-size:1.1rem;">Clareza de Carreira</strong>
        <p>
        Cada cargo é vinculado a um <strong>Career Band</strong> e <strong>Global Grade</strong>, refletindo o escopo de atuação, 
        o grau de autonomia e a natureza da contribuição.  
        Essa estrutura fornece visibilidade sobre oportunidades de progressão, diferenciação de níveis e mobilidade lateral.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="sig-card">
        <strong style="color:#145efc; font-size:1.1rem;">Integração de Sistemas</strong>
        <p>
        A Job Architecture serve como base única para processos de <strong>Remuneração, Performance, Talent Review e Benchmarking</strong>.  
        Garante decisões integradas e sustentadas por critérios globais.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# CONTEÚDO 3 — ESTRUTURA DA ARQUITETURA (TABELA ORIGINAL)
# ==========================================================

st.markdown("""
<div class="sig-card">
    <h3>Estrutura da Arquitetura</h3>

    A arquitetura é composta por cinco elementos integrados, formando um modelo organizacional padronizado e comparável globalmente:

    <br><br>

    <table style="width:100%; border-collapse: collapse;">
        <tr>
            <th style="border-bottom:2px solid #145efc; text-align:left; padding:8px;">Elemento</th>
            <th style="border-bottom:2px solid #145efc; text-align:left; padding:8px;">Propósito</th>
            <th style="border-bottom:2px solid #145efc; text-align:left; padding:8px;">Exemplo</th>
        </tr>

        <tr>
            <td style="padding:8px;"><strong>Job Family</strong></td>
            <td style="padding:8px;">Agrupa funções com competências similares e natureza de trabalho comum.</td>
            <td style="padding:8px;">Finanças, Engenharia, RH</td>
        </tr>

        <tr>
            <td style="padding:8px;"><strong>Sub-Job Family</strong></td>
            <td style="padding:8px;">Distingue especializações técnicas dentro de cada Job Family.</td>
            <td style="padding:8px;">Contabilidade, Engenharia de Processo</td>
        </tr>

        <tr>
            <td style="padding:8px;"><strong>Career Band</strong></td>
            <td style="padding:8px;">Representa o nível hierárquico e o escopo de influência.</td>
            <td style="padding:8px;">Profissional, Gerencial, Executivo</td>
        </tr>

        <tr>
            <td style="padding:8px;"><strong>Global Grade</strong></td>
            <td style="padding:8px;">Diferencia complexidade e contribuição entre níveis.</td>
            <td style="padding:8px;">GG07, GG09, GG12</td>
        </tr>

        <tr>
            <td style="padding:8px;"><strong>Generic Profile</strong></td>
            <td style="padding:8px;">Descrição corporativa de referência do nível.</td>
            <td style="padding:8px;">“Finance Specialist”, “HR Manager”</td>
        </tr>
    </table>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# CONTEÚDO 4 — IMPORTÂNCIA ESTRATÉGICA (ORIGINAL)
# ==========================================================

st.markdown("""
<div class="sig-card">
    <h3>Importância Estratégica</h3>

    <p>
    A <strong>Job Architecture</strong> é o alicerce das práticas de <strong>Gestão de Pessoas e Governança Corporativa</strong>.  
    Ela fornece uma linguagem comum para estruturar, comparar e avaliar cargos, promovendo decisões justas e sustentáveis.
    </p>

    <p>
    Com base em critérios consistentes de complexidade e contribuição, o modelo da WTW permite <strong>equidade interna, benchmarking de mercado e mapeamento de carreiras</strong> de forma padronizada.
    </p>

    <p>
    Ao integrar estrutura organizacional, remuneração e desenvolvimento, a Job Architecture fortalece a conexão entre <strong>estratégia de negócios, desempenho organizacional e evolução profissional</strong>, garantindo coerência global e meritocracia.
    </p>

</div>
""", unsafe_allow_html=True)
