# Universidade Federal Rural de Pernambuco
# Bacharelado em Sistemas de Informação
# Raquel Silva dos Santos
# Projeto Interdisciplinar para Sistemas de Informação II: Algoritmo de força bruta (VA1) - Flyfood

pontos_de_entrega = [] #Lista que guardará os pontos de entrega

#Função de permutação de pontos
def permutacao(matriz):
    matriz_auxiliar = [] #É uma lista auxiliar que guardará todas permutações dos elementos da matriz (pontos)
    #Caso base: Não há permutação a ser realizada
    if len(matriz) == 0 or len(matriz) == 1:
        return [matriz]
    #Passo recursivo:
    else:
        for index, elemento in enumerate(matriz): #Pega cada elemento da lista e posição correspondente
            el_seguinte = matriz[:index] + matriz[index+1:] #Passa para o próximo elemento da lista
            for p in permutacao(el_seguinte): #O último elemento é considerado com p
                matriz_auxiliar.append([elemento] + p) #P é adicionado com o elemento anterior em diferente índice
        return matriz_auxiliar #retorna a lista de permutações

#Função fatorial para Pn = n!
def fat(n):
    if n == 0 or n == 1: #Casos bases
        return 1
    else:
        return n*fat(n-1) #Retorna quantidade de rotas possíveis

#Leitura da entrada (arquivo)
entrada = open("matrix.txt", 'r')

#Separação do número de linhas e colunas (Matriz ij)
i, j = [int(x) for x in entrada.readline().split()]

#Dicionário que guarda os pontos de entrega com suas coordenadas
coordenadas = {}

#Manipulação das linhas e colunas para retirar os '0' e pegar as coordenadas dos pontos
for l in range(i):
    linha = entrada.readline().split()
    for c in range(j):
        if linha[c] != '0':
            pontos_de_entrega.append(linha[c])
            coordenadas[linha[c]] = (l, c)

#Fecha-se o arquivo de entrada
entrada.close() 

# print(coordenadas) #Fim apenas didádico

pontos_de_entrega.remove('R') #Ponto inicial não permuta

# print (pontos_de_entrega) #Fim apenas didádico

#Quantidade de permutações possíveis dos pontos de entrega
qntde = fat(len(pontos_de_entrega))

#Todas as permutações possíveis
permutados = list(permutacao(pontos_de_entrega))

#Adicionar, novamente, após permutações, o restaurante
for rotas in permutados:
    #Adicionar elemento inicial (posição 0) e de retorno (posição final)
    rotas.insert(0, 'R')
    rotas.append('R')
    # print(rotas) #Fim apenas didádico

def distancias_em_lista(rotas): #Vai pegar todas as distâncias e calcular entre as sequências, de acordo com as coordenadas
    distancias = [] #Armazenar em uma lista a distância entre cada dois pontos
    for dronometros in range(len(rotas)-1):
        dij = 0
        #Cálculo da diferença entre uma coordenada e a seguinte (segue a lógica da 'Geometria do táxi'), em que:
        #G(A,B) = |Ai - Bi| + |Aj - Bj|
        dij += abs(coordenadas[rotas[dronometros]][0] - coordenadas[rotas[dronometros+1]][0]) + abs(coordenadas[rotas[dronometros]][1] - coordenadas[rotas[dronometros+1]][1])
        #Este valor será armazenado na lista previamente criada
        distancias.append(dij)
    return sum(distancias)

resultados = []
for rotas in permutados:
    dronometros = 0 #Gasto atual do percurso
    gasto_dronometros = 0 #Acúmulo do percurso
    #Uma nova variável receberá o retorno da função do cálculo das distâncias para cada rota
    distancia = distancias_em_lista(rotas)
    #O gasto atual do percurso será atualizado para a distância computada
    dronometros += distancia
    #Uma nova lista irá armazenar esses valores, um a um, mostrando o gasto de cada permutação possível
    resultados.append(distancia)
    # print(resultados) #Fim apenas didático
    for menor_dist in range(len(resultados)):
        #A cada iteração será computado o considerado mínimo até que haja atualização final
        if resultados[menor_dist] < resultados[gasto_dronometros]:
            gasto_dronometros = menor_dist #Atualização do valor
            #Para a sequência de pontos permutados com menor gasto de dronômetros, assume-se como menor rota 
        menor_rota = ''
        for rotas in permutados[gasto_dronometros]:
            menor_rota += str(rotas)

print(f"A matriz de entrada possui {qntde} rotas possíveis. O menor percurso possui como sequência os pontos: {menor_rota} de custo {resultados[gasto_dronometros]} dronômetros.")
