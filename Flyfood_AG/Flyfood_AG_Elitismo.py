from random import random, randint, shuffle, sample
import tsplib95 as tsplib

#Leitura do arquivo

def leitura_arquivo(file_path): #Função padrão de leitura
    tsp = tsplib.load(file_path) #Recebe o arquivo .tsp
    coordenadas = [] #Informações são armazenadas em uma lista
    for i in range(1, tsp.dimension + 1):  
        pontos = tsp.node_coords[i] #As coordenadas são obtidas e passadas para a lista declarada
        coordenadas.append(pontos)
    cidades = {} #Cada ponto é uma chave e possui uma lista de dois valores chaveada
    for i, pontos in enumerate(coordenadas):
        cidades[i] = pontos
    return cidades

#População inicial

def populacao_inicial(lista, n_pop=20): #Vai gerar a primeira população
    populacao = []
    for _ in range(n_pop):
        permutacao = []
        for elemento in lista:
            permutacao.append(elemento)
        shuffle(permutacao) #Consiste em achar permutações aleatórias dos pontos de entrega
        populacao.append(permutacao)
    return populacao

#Função fitness

def distancias_em_lista(lista, cidades):
    distancias = [] #Vai pegar a distância de uma rota ponto a ponto e somar no final
    for i in range(len(lista)-1): #Pega a distância de um ponto até seu subsequente no eixo X e Y
        dij = ((cidades[lista[i]][0] - cidades[lista[i+1]][0])**2 + (cidades[lista[i]][1] - cidades[lista[i+1]][1])**2)**0.5
        distancias.append(dij)
    return sum(distancias)

def aptidao_individuo(individuo, cidades): #Para o PCV, a aptidão de um indivíduo (rota) é a sua distância
    return distancias_em_lista(individuo, cidades) #Quanto menor for sua rota, mais apto se torna

def aptidao_populacao(populacao, cidades):
    aptidoes = [] #Vai gerar uma lista com todas as aptidões de uma população
    for individuo in populacao:
        aptd = aptidao_individuo(individuo, cidades) #Faz a aptidão um a um e armazena em uma lista
        aptidoes.append(aptd)
    return aptidoes

#Seleção por torneio

def torneio(populacao, tamanho_torneio, cidades): #Triagem de indivíduos
    pais = []
    for _ in range(2): #Forma pares (pais) e seleciona aqueles com aptidão relevante em relação ao restante da população
        #Seleciona aleatoriamente um grupo de (tamanho_torneio) indivíduos da população
        torneio = sample(populacao, tamanho_torneio)
        #Compara a aptidão de cada indivíduo do torneio
        aptidoes_torneio = [aptidao_individuo(individuo, cidades) for individuo in torneio]
        #Seleciona o índice do indivíduo com a menor aptidão (mais apto)
        indice_melhor = aptidoes_torneio.index(min(aptidoes_torneio))
        #Adiciona o melhor indivíduo do torneio aos pais, pois serão usados para a reprodução da próxima geração
        pais.append(torneio[indice_melhor])
    return pais

#Crossover PMX (cruzamento pais e população)

def pmx(pai1, pai2):
    # Implementação do PMX crossover
    filho = [None] * len(pai1) #Filho é uma lista com tamanho igual a do pai
    #Seleciona duas posições aleatórias no cromossomo de cada pai (delimita seção a ser copiada)
    ponto1 = randint(0, len(pai1) - 1)
    ponto2 = randint(0, len(pai1) - 1)
    if ponto1 > ponto2:
        ponto1, ponto2 = ponto2, ponto1
    #Copia a seção do pai1 para o filho
    filho[ponto1:ponto2+1] = pai1[ponto1:ponto2+1]
    #Mapeia cada elemento da seção copiada para o seu correspondente no pai2
    for i in range(ponto1, ponto2+1):
        if pai2[i] not in filho[ponto1:ponto2+1]: #Verifica se o gene correspondente no pai2 ainda não foi mapeado para o filho
            j = i #índice do gene do pai1
            while filho[j] is not None: # Enquanto o gene mapeado para j no filho não for nulo (estiver já mapeado)
                j = pai1.index(pai2[j])
            filho[j] = pai2[i] #Encontra o índice do gene a partir do gene mapeado no pai2 e atualiza o valor de j com esse índice
    #Completa o filho com os elementos do pai2 que não estão na seção copiada
    for i in range(len(filho)):
        if filho[i] is None: #Verifica se o gene no índice i do filho ainda não foi mapeado para nenhum gene do pai1
            filho[i] = pai2[i] #Atribui o valor do gene correspondente no pai2 para o filho no índice i
    return filho

#Seleção de pais

def selecao_pais(populacao, tamanho_torneio, taxa_cruzamento, cidades):
    # Seleciona dois indivíduos para serem pais utilizando o método de torneio
    pais = torneio(populacao, tamanho_torneio, cidades)
    # Verifica se deve ocorrer o cruzamento
    if random() <= taxa_cruzamento: #Manter diversidade da geração
        filho1 = pmx(pais[0], pais[1]) 
        filho2 = pmx(pais[1], pais[0])
    else:
        filho1, filho2 = pais[0], pais[1]
    return [filho1, filho2]

#Mutação (indivíduo e população)

def mutacao_individuo(individuo, taxa_mutacao, cidades):
    filho_mutado = list(individuo) #Cria uma cópia do cromossomo do indivíduo passado
    for _ in range(len(individuo)):
        if random() <= taxa_mutacao:
            #Escolhe duas cidades aleatórias para trocar de posição
            c1, c2 = sample(range(len(cidades)), 2)
            filho_mutado[c1], filho_mutado[c2] = filho_mutado[c2], filho_mutado[c1] #Troca de posição das duas cidades selecionadas
    return filho_mutado

def mutacao_populacao(populacao, taxa_mutacao, cidades):
    for i, ind in enumerate(populacao): #Percorre cada indivíduo da população
        populacao[i] = mutacao_individuo(ind, taxa_mutacao, cidades) #Aplica a mutação em cada um deles
    return populacao #Retorna a população mutada

#Substituição geracional (seleção sobreviventes)

def selecao_sobreviventes(populacao, aptidao_populacao, filhos, aptidao_filhos):
    # Combine os indivíduos da população atual e os filhos gerados em uma única lista
    individuos = populacao + filhos
    aptidoes = aptidao_populacao + aptidao_filhos
    # Crie uma lista de índices para a lista de indivíduos
    indices = list(range(len(individuos)))
    # Ordene a lista combinada pelo valor da aptidão de cada indivíduo em ordem decrescente
    for i in range(len(individuos)):
        for j in range(i+1, len(individuos)):
            if aptidoes[j] < aptidoes[i]:
                aptidoes[i], individuos[i], indices[i] = aptidoes[j], individuos[j], indices[j]
                aptidoes[j], individuos[j], indices[j]= aptidoes[i], individuos[i], indices[i] 
    # Selecione os N indivíduos mais aptos da lista combinada
    selecionados = []
    for i in indices[:len(populacao)]:
        selecionados.append(individuos[i])
    aptidoes_selecionados = aptidoes[:len(populacao)]
    # Retorne a lista de indivíduos selecionados e a lista de aptidões correspondentes
    return selecionados, aptidoes_selecionados

#Evolução

def evolucao_ag(taxa_cruzamento, taxa_mutacao, torneio, cidades, n_geracoes):
    populacao = populacao_inicial(cidades)
    apt = aptidao_populacao(populacao, cidades) #População inicial e suas distâncias para saber aptidão de cada indivíduo
    for _ in range(n_geracoes):
        pais = selecao_pais(populacao, torneio, taxa_cruzamento, cidades)
        filhos = mutacao_populacao(populacao, taxa_mutacao, cidades)
        apt_filhos = aptidao_populacao(filhos, cidades)
        rota, custo = selecao_sobreviventes(pais, apt, filhos, apt_filhos)
    return rota, custo


def principal():
    cidades = leitura_arquivo("zi929.tsp")
    taxa_cruzamento = 0.9 #Cerca de 90% população é cruzada
    taxa_mutacao = 0.02 #Cerca de 2% dos genes de um indivíduo é mutado a cada geração
    torneio = 4
    n_geracoes = 100
    melhor_rota, aptd = evolucao_ag(taxa_cruzamento, taxa_mutacao, torneio, cidades, n_geracoes)
    menor_custo = min(aptd) #Menor valor dentro das aptidões
    indice_menor_custo = aptd.index(menor_custo) #Indivíduo que possui a menor aptidão (mais apto)
    melhor_rota = melhor_rota[indice_menor_custo]
    print(f"O menor percurso possui como sequência os pontos: {melhor_rota} de custo {menor_custo} dronômetros.")

principal()
