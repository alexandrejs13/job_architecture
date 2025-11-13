import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório job_architecture ao PATH
PROJECT_ROOT = Path(__file__).resolve().parent / "job_architecture"
sys.path.append(str(PROJECT_ROOT))

# Executa o app principal
from job_architecture.app import main

if __name__ == "__main__":
    main()
