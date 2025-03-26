import heapq
from collections import deque
# from funcoes import linhas_estacoes
import json

# Velocidade do trem (30 km/h) e baldeação (4 minutos = 0,0666 horas)
TREM_VELOCIDADE = 30
TROCA_LINHA = 4 / 60

# Importando dados do JSON
def carregar_dados_json(arquivo="metro.json"):
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f);


dados_metro = carregar_dados_json()

linhas_metro = dados_metro["linhas_metro"]
distancias_reais = {}

for chave, valor in dados_metro["distancias_reais"].items():
    e1, e2 = chave.split("-")
    distancias_reais[(e1, e2)] = valor
    distancias_reais[(e2, e1)] = valor

# Tornando o grafo bidirecional
for (a, b), dist in list(distancias_reais.items()):
    distancias_reais[(b, a)] = dist

# Função para identificar as linhas de uma estação
def linhas_estacao(estacao):
    return [linha for linha, estacoes in linhas_metro.items() if estacao in estacoes]

# Função que converte distância em tempo
def tempo_viagem(dist_km):
    return dist_km / TREM_VELOCIDADE


# Busca cega (largura), sem considerar tempo
def busca_cega(origem, destino):
    fila = deque()
    fila.append((origem, [origem]))
    visitados = set()

    while fila:
        atual, caminho = fila.popleft()

        if atual == destino:
            return caminho

        visitados.add(atual)

        for (e1, e2), _ in distancias_reais.items():
            if e1 == atual and e2 not in visitados and e2 not in caminho:
                fila.append((e2, caminho + [e2]))

    return None

# Busca heurística (best-first) que calcula o menor tempo, considerando trocas de linha
def busca_heuristica(origem, linha_origem, destino):
    fila = []
    heapq.heappush(fila, (0, origem, linha_origem, []))
    visitados = set()

    while fila:
        tempo_acumulado, atual, linha_atual, caminho = heapq.heappop(fila)

        if (atual, linha_atual) in visitados:
            continue
        visitados.add((atual, linha_atual))

        caminho = caminho + [(atual, linha_atual)]

        if atual == destino:
            return caminho, tempo_acumulado

        for (e1, e2), dist in distancias_reais.items():
            if e1 == atual:
                for prox_linha in linhas_estacao(e2):
                    troca = TROCA_LINHA if prox_linha != linha_atual else 0
                    tempo_total = tempo_acumulado + tempo_viagem(dist) + troca
                    heapq.heappush(fila, (tempo_total, e2, prox_linha, caminho))

    return None, float('inf')

# Interface principal
if __name__ == "__main__":
    origem = input("Digite a estação de origem (ex: E1): ").strip().upper()
    linha_origem = input("Digite a linha em que está (azul, amarela, vermelha, verde): ").strip().lower()
    destino = input("Digite a estação de destino (ex: E14): ").strip().upper()

    print("\nRESULTADO DA BUSCA CEGA:")
    caminho_cego = busca_cega(origem, destino)
    if caminho_cego:
        print(f"Caminho encontrado (não otimizado): {' -> '.join(caminho_cego)}")
    else:
        print("Caminho não encontrado.")

    print("\nRESULTADO DA BUSCA HEURÍSTICA:")
    caminho_heuristico, tempo_heuristico = busca_heuristica(origem, linha_origem, destino)
    if caminho_heuristico:
    #    print("Melhor caminho com tempos e trocas:")
        for i in range(len(caminho_heuristico) - 1):
            atual_est, atual_linha = caminho_heuristico[i]
            prox_est, prox_linha = caminho_heuristico[i + 1]
            troca = " (TROCA DE LINHA)" if atual_linha != prox_linha else ""
            print(f"{atual_est} ({atual_linha}) -> {prox_est} ({prox_linha}){troca}")
        print(f"Tempo estimado: {tempo_heuristico * 60:.2f} minutos")
    else:
        print("Caminho não encontrado.")