# Universidade Federal Rural de Pernambuco
# Bacharelado em Sistemas de Informação
# Raquel Silva dos Santos
# Projeto Interdisciplinar para Sistemas de Informação II: Algoritmo de força bruta (VA1) - Flyfood

#Função de permutação de pontos
def permutacao(lista):
    if len(lista) == 0: #Caso base 1: lista vazia
        return []
    if len(lista) == 1: #Caso base 2: lista de apenas um elemento
        return [lista]
    matriz_aux = []
    for i, el_verificando in enumerate(lista):
        #Lista auxiliar com o elemento x travado e as permutações
        el_sem_verificacao = lista[:i] + lista[i+1:]
        for p in permutacao(el_sem_verificacao):
            matriz_aux.append([el_verificando] + p)
            return matriz_aux

coordenadas = {} 
pontos_de_entrega = [] 


entrada = open("matrix.txt", 'r') #Leitura da entrada (arquivo)
linhas, colunas = map(int, entrada.readline().split()) #Separação de linhas e colunas

for l in range(linhas):
    linha = entrada.readline().split()
    for c in range(colunas):
        if linha[c] != '0':
            pontos_de_entrega.append(linha[c])
            coordenadas[linha[c]] = (l, c)


entrada.close() #Fecha-se o arquivo de entrada

# print(coordenadas)

pontos_de_entrega.remove('R') #Ponto inicial não permuta

# print (pontos_de_entrega)

menor_custo = float('inf') #Menor uso de dronometros

permutados = list(permutacao(pontos_de_entrega))

for rotas in permutados:
    rotas.append('R')
    rotas.insert(0, 'R')

for rotas in permutados:
    dronometros_gastos = 0
    dronometros = 0

    for dronometros in range(len(rotas)-1):
        di = abs(coordenadas[rotas[dronometros]][0] - coordenadas[rotas[dronometros+1]][0])
        dj = abs(coordenadas[rotas[dronometros]][1] - coordenadas[rotas[dronometros+1]][1])
        dronometros_gastos += di + dj
        dronometros += 1

    if dronometros_gastos < menor_custo:
        menor_custo = dronometros_gastos
        percurso = rotas

print(' '.join(percurso[1:-1]), menor_custo)
