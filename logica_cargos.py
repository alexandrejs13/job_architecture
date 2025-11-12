# logica_cargos.py

# --- Mapeamento Global Grade (GG) Mínimo por Nível Hierárquico ---
# IMPORTANTE: Estes GGs são exemplos e DEVEM ser ajustados para refletir a
# tabela de Global Grade real utilizada pela sua empresa na família Finance/Accounting.
NIVEIS_HIERARQUICOS = {
    "ASSISTANT": 1,
    "ANALISTA_JUNIOR": 6,
    "ANALISTA_PLENO": 9,
    "ANALISTA_SENIOR": 12,
    "SUPERVISOR": 14,  # GG Mínimo para um Supervisor (Ponto de Corte)
    "COORDENADOR": 15,
    "MANAGER": 18
}

def filtrar_cargos_por_hierarquia(cargo_de_reporte: str, lista_cargos_sugeridos: list) -> list:
    """
    Filtra a lista de cargos sugeridos para garantir que o GG do cargo
    seja estritamente menor que o GG do cargo para o qual ele reporta.

    A regra é: Cargo sugerido.GG < Cargo de Reporte.GG Mínimo.

    Args:
        cargo_de_reporte: O cargo reportado pelo usuário (ex: 'Supervisor').
                          Será normalizado e comparado com as chaves em NIVEIS_HIERARQUICOS.
        lista_cargos_sugeridos: Lista de dicionários, cada um contendo
                                {'titulo': str, 'gg': int}.

    Returns:
        Uma nova lista contendo apenas os cargos aderentes à regra hierárquica.
    """
    
    # 1. Normalizar e buscar o GG mínimo do cargo de reporte
    # A normalização é necessária para lidar com variações de escrita (ex: 'supervisor' vs 'SUPERVISOR')
    cargo_normalizado = cargo_de_reporte.upper().replace(" ", "_").replace("/", "_")

    # Tenta encontrar o GG do cargo reportado no mapa de NÍVEIS
    gg_minimo_reporte = NIVEIS_HIERARQUICOS.get(cargo_normalizado)
    
    if gg_minimo_reporte is None:
        # Se não encontrar o GG de reporte, retorna a lista original com um aviso.
        print(f"AVISO (Hierarquia): Cargo de reporte '{cargo_de_reporte}' não mapeado em NIVEIS_HIERARQUICOS. Retornando lista original.")
        return lista_cargos_sugeridos
        
    # 2. Aplicar a regra de filtragem (GG < GG de Reporte)
    cargos_aderentes = []
    
    for cargo in lista_cargos_sugeridos:
        # Verifica se o 'gg' existe e se é um número inteiro
        if isinstance(cargo.get("gg"), int):
            
            # Condição de Ouro: O Global Grade do cargo sugerido deve ser MENOR que o do Reporte
            if cargo["gg"] < gg_minimo_reporte:
                cargos_aderentes.append(cargo)
            
    return cargos_aderentes

# --- Exemplo de Uso (Para Teste) ---
if __name__ == '__main__':
    # Simulação dos resultados brutos do GGS 4.2
    resultados_brutos = [
        {"titulo": "Supervisor Accounting", "gg": 14},
        {"titulo": "Manager Accounting", "gg": 18},
        {"titulo": "Analyst Senior Accounting", "gg": 12},
        {"titulo": "Analyst Pleno Accounting", "gg": 10},
        {"titulo": "Assistant / Analyst Accounting", "gg": 6}
    ]

    # Teste com 'Supervisor'
    cargo_reportado_supervisor = "Supervisor" 
    cargos_filtrados_supervisor = filtrar_cargos_por_hierarquia(
        cargo_de_reporte=cargo_reportado_supervisor,
        lista_cargos_sugeridos=resultados_brutos
    )

    print(f"--- Teste: Reporta a {cargo_reportado_supervisor} (GG Mínimo {NIVEIS_HIERARQUICOS['SUPERVISOR']}) ---")
    for cargo in cargos_filtrados_supervisor:
        print(f"✅ Título: {cargo['titulo']} | GG: {cargo['gg']}")
    
    print("\n" + "="*50 + "\n")

    # Teste com 'Analista Sênior' (exemplo de reporte mais baixo)
    cargo_reportado_senior = "Analista Senior"
    cargos_filtrados_senior = filtrar_cargos_por_hierarquia(
        cargo_de_reporte=cargo_reportado_senior,
        lista_cargos_sugeridos=resultados_brutos
    )
    
    print(f"--- Teste: Reporta a {cargo_reportado_senior} (GG Mínimo {NIVEIS_HIERARQUICOS['ANALISTA_SENIOR']}) ---")
    for cargo in cargos_filtrados_senior:
        print(f"✅ Título: {cargo['titulo']} | GG: {cargo['gg']}")
