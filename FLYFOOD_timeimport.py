# Universidade Federal Rural de Pernambuco
# Bacharelado em Sistemas de Informação
# Raquel Silva dos Santos
# Projeto Interdisciplinar para Sistemas de Informação II: Algoritmo de força bruta (VA1) - Flyfood
# Versão com import time (fim de comparação) e sem comentários

import time

inicio = time.time()

pontos_de_entrega = [] 

def permutacao(lista):
    if len(lista) == 0 or len(lista) == 1:
        return [lista]
    
    aux_list = []
    for indice in range(len(lista)):
        el_fixo = lista[indice]
        rest_elementos = lista[:indice] + lista[indice + 1:]
        rest_el_permutados = permutacao(rest_elementos)
        contador_indice = 0
        while contador_indice < len(rest_el_permutados):
            x = [el_fixo] + rest_el_permutados[contador_indice]
            aux_list.append(x)
            contador_indice += 1
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
    dronometros = 0
    gasto_dronometros = 0
    distancia = distancias_em_lista(rotas)
    dronometros += distancia
    resultados.append(distancia)
    # print(resultados) #Fim apenas didático
    for menor_sequencia in range(len(resultados)):
        if resultados[menor_sequencia] < resultados[gasto_dronometros]:
            gasto_dronometros = menor_sequencia
    menor_rota = ''.join(str(rotas) for rotas in permutados[gasto_dronometros])

print(f"A matriz de entrada possui {qntde} rotas possíveis. O menor percurso possui como sequência os pontos: {menor_rota} de custo {resultados[gasto_dronometros]} dronômetros.")
fim = time.time()
print(fim - inicio)
