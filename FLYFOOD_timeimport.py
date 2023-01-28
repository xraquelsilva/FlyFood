# Universidade Federal Rural de Pernambuco
# Bacharelado em Sistemas de Informação
# Raquel Silva dos Santos
# Projeto Interdisciplinar para Sistemas de Informação II: Algoritmo de força bruta (VA1) - Flyfood
# Versão com import time (fim de comparação) e sem comentários

import time

inicio = time.time()

pontos_de_entrega = []

def permutacao(matriz):
    matriz_auxiliar = []
    if len(matriz) == 0 or len(matriz) == 1:
        return [matriz]
    else:
        for index, elemento in enumerate(matriz): 
            el_seguinte = matriz[:index] + matriz[index+1:]
            for p in permutacao(el_seguinte):
                matriz_auxiliar.append([elemento] + p)
        return matriz_auxiliar

def fat(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n*fat(n-1)

entrada = open("matrix.txt", 'r')

i, j = [int(x) for x in entrada.readline().split()]

coordenadas = {}

for l in range(i):
    linha = entrada.readline().split()
    for c in range(j):
        if linha[c] != '0':
            pontos_de_entrega.append(linha[c])
            coordenadas[linha[c]] = (l, c)

entrada.close() 

# print(coordenadas) #Fim apenas didádico

pontos_de_entrega.remove('R')

# print (pontos_de_entrega) #Fim apenas didádico

qntde = fat(len(pontos_de_entrega))

permutados = list(permutacao(pontos_de_entrega))

def distancias_em_lista(rotas):
    distancias = []
    for dronometros in range(len(rotas)-1):
        dij = 0
        dij += abs(coordenadas[rotas[dronometros]][0] - coordenadas[rotas[dronometros+1]][0]) + abs(coordenadas[rotas[dronometros]][1] - coordenadas[rotas[dronometros+1]][1])
        distancias.append(dij)
    return sum(distancias)

resultados = []
for rotas in permutados:
    rotas.insert(0, 'R')
    rotas.append('R')
    dronometros = 0
    gasto_dronometros = 0
    distancia = distancias_em_lista(rotas)
    dronometros += distancia
    resultados.append(distancia)
    # print(resultados) #Fim apenas didático
    for menor_dist in range(len(resultados)):
        if resultados[menor_dist] < resultados[gasto_dronometros]:
            gasto_dronometros = menor_dist #Atualização do valor
        menor_rota = ''
        for rotas in permutados[gasto_dronometros]:
            menor_rota += str(rotas)

print(f"A matriz de entrada possui {qntde} rotas possíveis. O menor percurso possui como sequência os pontos: {menor_rota} de custo {resultados[gasto_dronometros]} dronômetros.")

fim = time.time()
print(fim - inicio)
