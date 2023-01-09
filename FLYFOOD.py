# Universidade Federal Rural de Pernambuco
# Bacharelado em Sistemas de Informação
# Raquel Silva dos Santos
# Projeto Interdisciplinar para Sistemas de Informação II: Algoritmo de força bruta (VA1) - Flyfood

pontos_de_entrega = []

#Função de permutação de pontos
def permutacao(matriz):
    matriz_auxiliar = [] #É uma lista auxiliar que guardará todas permutações dos elementos da matriz (pontos)
    if len(matriz) == 0 or len(matriz) == 1: #Caso base: Não há permutação a ser realizada
        return [matriz]
    else:
        for index, elemento in enumerate(matriz): #Pega cada elemento da lista e posição correspondente
            el_seguinte = matriz[:index] + matriz[index+1:] #Passa para o próximo elemento da lista
            for p in permutacao(el_seguinte):
                matriz_auxiliar.append([elemento] + p)
        return matriz_auxiliar #retorna a lista de permutações

#Leitura da entrada (arquivo)
entrada = open("matrix.txt", 'r')

#Separação de linhas e colunas
linhas, colunas = [int(x) for x in entrada.readline().split()]

#Dicionário que guarda os pontos de entrega com suas coordenadas
coordenadas = {}

#Manipulação das linhas e colunas para retirar os '0' e pegar as coordenadas dos pontos
for l in range(linhas):
    linha = entrada.readline().split()
    for c in range(colunas):
        if linha[c] != '0':
            pontos_de_entrega.append(linha[c])
            coordenadas[linha[c]] = (l, c)

#Fecha-se o arquivo de entrada
entrada.close() 

# print(coordenadas) #Fim apenas didádico

pontos_de_entrega.remove('R') #Ponto inicial não permuta

# print (pontos_de_entrega) #Fim apenas didádico

#Todas as permutações possíveis
permutados = list(permutacao(pontos_de_entrega))

#Adicionar, novamente, após permutações, o restaurante
for rotas in permutados:
    #Adicionar elemento inicial (posição 0) e de retorno (final)
    rotas.insert(0, 'R')
    rotas.append('R')
    # print(rotas) #Fim apenas didádico

def distancia_total(lista_de_pontos):
    gasto = 0
    for distancia_computada in lista_de_pontos:
        gasto += distancia_computada
    return gasto

def distancias_em_lista(rotas): #Vai pegar todas as distâncias
    distancias = []
    for dronometros in range(len(rotas)-1):
        di = abs(coordenadas[rotas[dronometros]][0] - coordenadas[rotas[dronometros+1]][0])
        dj = abs(coordenadas[rotas[dronometros]][1] - coordenadas[rotas[dronometros+1]][1])
        dij = di + dj
        distancias.append(dij)
    return distancias

resultados = []
for rotas in permutados:
    dronometros = 0
    gasto_dronometros = 0
    distancia = distancias_em_lista(rotas)
    resulto = distancia_total(distancia)
    dronometros += resulto
    resultados.append(resulto)
    for menor_dist in range(len(resultados)):
        if resultados[menor_dist] < resultados[gasto_dronometros]:
            gasto_dronometros = menor_dist
            menor_rota = ''
            for rotas in permutados[gasto_dronometros]:
                menor_rota += str(rotas)

print(f"O menor percurso possui como sequência os pontos: {menor_rota} de custo {resultados[gasto_dronometros]} dronômetros.")
