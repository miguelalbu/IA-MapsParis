# Função para identificar as linhas pelas quais uma estação passa
def linhas_estacoes(estacao, linhas_metro):
    return [linha for linha, estacoes in linhas_metro.items() if estacao in estacoes]