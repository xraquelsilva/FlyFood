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

#Função de menor valor
def minimo(lista): 
    menor_custo = float('inf')
    for item in lista:
        try:
            valor = int(item)
            if valor < menor_custo:
                menor_custo = valor
        except:
            pass
    return menor_custo
  
#Cálculo da distância
for rotas in permutados:
    #Gasto atual do percurso, acúmulo, todas as distâncias
    dronometros = 0
    dronometros_gastos = 0
    distancias = []

    for dronometros in range(len(rotas)-1):
            di = abs(coordenadas[rotas[dronometros]][0] - coordenadas[rotas[dronometros+1]][0])
            dj = abs(coordenadas[rotas[dronometros]][1] - coordenadas[rotas[dronometros+1]][1])
            dij = di + dj
            dronometros_gastos =+ dij
            dronometros += 1
            distancias.append(dronometros)
            distancia = sum(distancias)
    
    if dronometros_gastos < distancia:
        menor_custo = distancia

# print(distancia) #Fim apenas didádico

print(f'O menor percurso possui como sequência os pontos: {str(rotas)[1:-1]} de custo {menor_custo}')
