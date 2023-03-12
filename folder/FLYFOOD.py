# Universidade Federal Rural de Pernambuco
# Bacharelado em Sistemas de Informação
# Raquel Silva dos Santos
# Projeto Interdisciplinar para Sistemas de Informação II: Algoritmo de força bruta (VA1) - Flyfood
# Versão comentada e sem tempo de execução

pontos_de_entrega = [] #Lista que guardará os pontos de entrega

#Função de permutação
def permutacao(lista): #Age em uma lista de entrada, nesse caso, os pontos da matriz
    if len(lista) <= 1: #Caso base: Não há permutação a ser realizada
        return [lista]
    #Passo recursivo:
    aux_list = [] #É uma lista auxiliar que guardará todas permutações dos elementos da matriz (pontos)
    for indice, elemento in enumerate(lista): #Vai passar por todos os índices da lista de entrada e seus respectivos elementos
        restantes = lista[:indice] + lista[indice+1:] #O restante da lista (exceção do que está travado) será atribuída a uma nova variável
        for p in permutacao(restantes):
            aux_list.append([elemento]+p)
    return aux_list

#Leitura da entrada (arquivo)
entrada = open("matrix.txt", 'r')

#Separação do número de linhas e colunas (Matriz ij)
i, j = [int(x) for x in entrada.readline().split()]

#Dicionário que guarda os pontos de entrega com suas coordenadas
coordenadas = {}

#Manipulação das linhas e colunas para retirar os '0' e pegar as coordenadas dos pontos
for l in range(i):
    linha = entrada.readline().split() #Devolve em lista
    for c in range(j):
        if linha[c] != 'R' and linha[c] != '0': #Ponto 'R' não permuta
            pontos_de_entrega.append(linha[c])
        if linha[c] != '0':
            coordenadas[linha[c]] = (l, c)

#Fecha-se o arquivo de entrada
entrada.close() 

# print(coordenadas) #Fim apenas didádico

# print (pontos_de_entrega) #Fim apenas didádico

#Todas as permutações possíveis
permutados = permutacao(pontos_de_entrega)
# print(permutados)

def distancias_em_lista(lista): #Vai pegar todas as distâncias e calcular entre as sequências, de acordo com as coordenadas
    distancias = [] #Armazenar em uma lista a distância entre cada dois pontos
    for dronometros in range(len(lista)-1):
        dij = 0
            #Cálculo da diferença entre uma coordenada e a seguinte (segue a lógica da 'Geometria do táxi'), em que:
            #G(A,B) = |Ai - Bi| + |Aj - Bj|
        di = abs(coordenadas[lista[dronometros]][0] - coordenadas[lista[dronometros+1]][0])
        dj = abs(coordenadas[lista[dronometros]][1] - coordenadas[lista[dronometros+1]][1])
        dij += di + dj
            #Este valor será armazenado na lista previamente criada
        distancias.append(dij)
    return sum(distancias)

resultados = []
for rotas in permutados:
    #Adicionar, novamente, após permutações, o restaurante
    #Adicionar elemento inicial (posição 0) e de retorno (posição final)
    rotas.insert(0, 'R')
    rotas.append('R')
    # print(rotas) #Fim apenas didádico
    #Uma nova variável receberá o retorno da função do cálculo das distâncias para cada rota
    distancia = distancias_em_lista(rotas)
    #Uma nova lista irá armazenar esses valores, um a um, mostrando o gasto de cada permutação possível
    resultados.append(distancia)
    # print(resultados) #Fim apenas didático)
    menor_gasto = min(resultados) #Busca o menor valor na lista de resultados
    trilha_economica = resultados.index(menor_gasto) #Procura a sequência de pontos que possui o menor valor
    menor_rota = ''.join(str(rotas) for rotas in permutados[trilha_economica]) #Recuperar o menor valor e a rota em permutados que está relacionado a ele, convertendo para string
                          
print(f"O menor percurso possui como sequência os pontos: {menor_rota} de custo {menor_gasto} dronômetros.")
