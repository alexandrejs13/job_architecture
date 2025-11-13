# -*- coding: utf-8 -*-
"""
Arquivo principal para Streamlit Cloud.

Este arquivo garante que o pacote job_architecture seja corretamente
carregado e que o app principal (app.py) seja executado sem erros.
"""

import streamlit as st
import sys
from pathlib import Path

# ===========================================
# ADICIONA O PACOTE job_architecture AO PYTHON PATH
# ===========================================
ROOT_DIR = Path(__file__).resolve().parent / "job_architecture"
sys.path.append(str(ROOT_DIR))

# ===========================================
# IMPORTA E EXECUTA O APLICATIVO PRINCIPAL
# ===========================================
from job_architecture.app import main

if __name__ == "__main__":
    main()
