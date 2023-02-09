# Universidade Federal Rural de Pernambuco
# Bacharelado em Sistemas de Informação
# Raquel Silva dos Santos
# Projeto Interdisciplinar para Sistemas de Informação II: Algoritmo de força bruta (VA1) - Flyfood
# Versão com import time (fim de comparação) e sem comentários

import time

inicio = time.time()

pontos_de_entrega = [] 

def permutacao(lista):
    if len(lista) <= 1:
        return [lista]
    aux_list = []
    for indice, elemento in enumerate(lista):
        restantes = lista[:indice] + lista[indice+1:]
        for p in permutacao(restantes):
            aux_list.append([elemento]+p)
    return aux_list
    
def fat(n):
    if n == 0 or n == 1:
        return 1
    return n*fat(n-1)

entrada = open("matrix.txt", 'r')

i, j = [int(x) for x in entrada.readline().split()]

coordenadas = {}

for l in range(i):
    linha = entrada.readline().split()
    for c in range(j):
        if linha[c] != 'R' and linha[c] != '0':
            pontos_de_entrega.append(linha[c])
        if linha[c] != '0':
            coordenadas[linha[c]] = (l, c)

entrada.close() 

# print(coordenadas) #Fim apenas didádico

# print (pontos_de_entrega) #Fim apenas didádico

qntde = fat(len(pontos_de_entrega))

permutados = permutacao(pontos_de_entrega)

def distancias_em_lista(lista):
    distancias = []
    for dronometros in range(len(lista)-1):
        dij = 0
        dij += abs(coordenadas[lista[dronometros]][0] - coordenadas[lista[dronometros+1]][0]) + abs(coordenadas[lista[dronometros]][1] - coordenadas[lista[dronometros+1]][1])
        distancias.append(dij)
    return sum(distancias)

resultados = []
for rotas in permutados:
    rotas.insert(0, 'R')
    rotas.append('R')
    # print(rotas) #Fim apenas didádico
    distancia = distancias_em_lista(rotas)
    resultados.append(distancia)
    # print(resultados) #Fim apenas didático
    menor_gasto = min(resultados)
    trilha_economico = resultados.index(menor_gasto)
    menor_rota = ''.join(str(rotas) for rotas in permutados[trilha_economico])

print(f"A matriz de entrada possui {qntde} rotas possíveis. O menor percurso possui como sequência os pontos: {menor_rota} de custo {resultados[gasto_dronometros]} dronômetros.")
fim = time.time()
print(fim - inicio)
