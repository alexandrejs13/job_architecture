import pandas as pd
from pathlib import Path

def load_csv_safe(filename):
    """Carrega CSV com múltiplas tentativas de separador, encoding e tratamento de erros."""
    base_path = Path(__file__).parent
    candidates = [
        base_path / "data" / filename,
        base_path.parent / "data" / filename,
        base_path / filename,
        base_path.parent / filename,
    ]

    for path in candidates:
        if not path.exists():
            continue
        for sep in [";", ",", "\t"]:
            for enc in ["utf-8-sig", "utf-8", "latin-1"]:
                try:
                    df = pd.read_csv(
                        path,
                        sep=sep,
                        encoding=enc,
                        engine="python",
                        quotechar='"',
                        on_bad_lines="skip",
                    )
                    if len(df.columns) > 2:
                        print(f"✅ {filename} carregado com sucesso de {path}")
                        return df
                except Exception:
                    continue

    raise FileNotFoundError(f"❌ Arquivo '{filename}' não pôde ser carregado. Verifique formato ou aspas incorretas.")
