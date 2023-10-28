import pandas as pd
import random


def leArquivo():

    # Lista para armazenar as linhas do arquivo
    linhas = []

    # Abre o arquivo em modo binário e lê as linhas
    with open('dados/teste1.txt', 'rb') as arquivo:
        for linha in arquivo:
            linhas.append(linha.decode('utf-8', errors='ignore'))

    # Extrair os valores desejados
    virtual = int(linhas[0].split(': ')[1])
    fisica = int(linhas[1].split(': ')[1])
    quantidade = int(linhas[2])
    vetor = [int(valor) for valor in linhas[3:]]

    return virtual, fisica, quantidade, vetor

def otimo():
    virtual, fisica, quantidade, vetor = leArquivo()

    memoriaFisica = [-1] * fisica
    quantidadeDeSubstituicoes = 0

    for indice in range(len(vetor)):
        if vetor[indice] in memoriaFisica:
            continue
        else:
            quantidadeDeSubstituicoes += 1
            if -1 in memoriaFisica:
                memoriaFisica[memoriaFisica.index(-1)] = vetor[indice]
            else:
                paginas = vetor[indice+1:]
                # Encontre a página que não será usada por mais tempo
                paginaSubstituida = -1
                distanciaMaxima = -1
                for i in range(fisica):
                    page = memoriaFisica[i]
                    if page in paginas:
                        distance = paginas.index(page)
                        if distance > distanciaMaxima:
                            distanciaMaxima = distance
                            paginaSubstituida = i
                    else:
                        paginaSubstituida = i
                        break
                memoriaFisica[paginaSubstituida] = vetor[indice]

    #print(quantidadeDeSubstituicoes)
    return quantidadeDeSubstituicoes

def aleatorio():
    virtual, fisica, quantidade, vetor = leArquivo()

    memoriaFisica = [-1] * fisica
    quantidadeDeSubstituicoes = 0

    for indice in range(len(vetor)):
        if vetor[indice] in memoriaFisica:
            quantidadeDeSubstituicoes += 0
        else:
            quantidadeDeSubstituicoes += 1
            memoriaFisica[ random.randint(0, fisica-1)] = vetor[indice]

    #print(quantidadeDeSubstituicoes)
    return quantidadeDeSubstituicoes

def fifo():
    virtual, fisica, quantidade, vetor = leArquivo()

    memoriaFisica = [-1] * fisica
    inciceDeSubstituicao = 0
    quantidadeDeSubstituicoes = 0

    for indice in range(len(vetor)):
        if vetor[indice] in memoriaFisica:
            quantidadeDeSubstituicoes += 0
        else:
            quantidadeDeSubstituicoes += 1
            memoriaFisica[inciceDeSubstituicao] = vetor[indice]

            inciceDeSubstituicao += 1
            if inciceDeSubstituicao == fisica:
                inciceDeSubstituicao = 0

    #print(quantidadeDeSubstituicoes)
    return quantidadeDeSubstituicoes

def segndaChance():
    virtual, fisica, quantidade, vetor = leArquivo()

    memoriaFisica = [-1] * fisica
    controle = [0] * fisica
    inciceDeSubstituicao = 0
    quantidadeDeSubstituicoes = 0

    for indice in range(len(vetor)):
        if vetor[indice] in memoriaFisica:
            controle[memoriaFisica.index(vetor[indice])] = 1
        else:
            quantidadeDeSubstituicoes += 1

            while controle[inciceDeSubstituicao] == 1:
                controle[inciceDeSubstituicao] = 0
                inciceDeSubstituicao += 1
                if inciceDeSubstituicao == fisica:
                    inciceDeSubstituicao = 0

            memoriaFisica[inciceDeSubstituicao] = vetor[indice]

            inciceDeSubstituicao += 1
            if inciceDeSubstituicao == fisica:
                inciceDeSubstituicao = 0

    #print(quantidadeDeSubstituicoes)
    return quantidadeDeSubstituicoes

def lru(): # menos recentemente usada
    virtual, fisica, quantidade, vetor = leArquivo()

    memoriaFisica = [-1] * fisica
    controle = [-1] * fisica
    quantidadeDeSubstituicoes = -1

    for indice in range(len(vetor)):
        if vetor[indice] in memoriaFisica:
            controle[memoriaFisica.index(vetor[indice])] = indice

        else:
            inciceDeSubstituicao = controle.index(min(controle))
            quantidadeDeSubstituicoes += 1
            memoriaFisica[inciceDeSubstituicao] = vetor[indice]
            controle[inciceDeSubstituicao] = indice

    #print(quantidadeDeSubstituicoes)
    return quantidadeDeSubstituicoes

def NRU(): # não usada recentemente
    virtual, fisica, quantidade, vetor = leArquivo()

    memoriaFisica = [-1] * fisica
    bits_referencia = [0] * fisica
    bits_modificacao = [0] * fisica
    quantidadeDeSubstituicoes = 0

    for indice in range(len(vetor)):
        if vetor[indice] in memoriaFisica:
            # Defina o bit de referência para 1 para a página presente
            bits_referencia[memoriaFisica.index(vetor[indice])] = 1
        else:
            quantidadeDeSubstituicoes += 1

            # Verifique se alguma página deve ser removida
            page_to_replace = None
            i = 0
            while page_to_replace is None and i < fisica:
                if bits_referencia[i] == 0 and bits_modificacao[i] == 0:
                    page_to_replace = i
                i += 1

            if page_to_replace is None:
                i = 0
                while page_to_replace is None and i < fisica:
                    if bits_referencia[i] == 0 and bits_modificacao[i] == 1:
                        page_to_replace = i
                    i += 1

            if page_to_replace is None:
                i = 0
                while page_to_replace is None and i < fisica:
                    if bits_referencia[i] == 1 and bits_modificacao[i] == 0:
                        page_to_replace = i
                    i += 1

            if page_to_replace is None:
                i = 0
                while page_to_replace is None and i < fisica:
                    if bits_referencia[i] == 1 and bits_modificacao[i] == 1:
                        page_to_replace = i
                    i += 1

            if page_to_replace is not None:
                memoriaFisica[page_to_replace] = vetor[indice]
                bits_referencia[page_to_replace] = 0
                bits_modificacao[page_to_replace] = 0

    #print(quantidadeDeSubstituicoes)
    return quantidadeDeSubstituicoes

NRU()

_, _, quantidade, _ = leArquivo()
quantidadeSubstituicoesOtimo = otimo()
quantidadeSubstituicoesAleatorio = aleatorio()
quantidadeSubstituicoesFifo = fifo()
quantidadeSubstituicoesSegundaChance = segndaChance()
quantidadeSubstituicoesLRU = lru()
quantidadeSubstituicoesNRU = NRU()

print('\nAlgoritmo ótimo')
print('Quantidade de páginas substituídas: ',quantidadeSubstituicoesOtimo)
print('GAP para o algoritmo ótimo: ', (quantidade-quantidadeSubstituicoesOtimo)/(quantidade-quantidadeSubstituicoesOtimo)*100,'%')

print('\nAlgoritmo aleatório')
print('Quantidade de páginas substituídas: ',quantidadeSubstituicoesAleatorio)
print('GAP para o algoritmo ótimo: ', (quantidade- quantidadeSubstituicoesAleatorio)/(quantidade-quantidadeSubstituicoesOtimo)*100,'%')

print('\nAlgoritmo FIFO')
print('Quantidade de páginas substituídas: ',quantidadeSubstituicoesFifo)
print('GAP para o algoritmo ótimo: ', (quantidade- quantidadeSubstituicoesFifo)/(quantidade-quantidadeSubstituicoesOtimo)*100,'%')


print('\nAlgoritmo segunda chance')
print('Quantidade de páginas substituídas: ',quantidadeSubstituicoesSegundaChance)
print('GAP para o algoritmo ótimo: ', (quantidade- quantidadeSubstituicoesSegundaChance)/(quantidade-quantidadeSubstituicoesOtimo)*100,'%')


print('\nAlgoritmo LRU')
print('Quantidade de páginas substituídas: ',quantidadeSubstituicoesLRU)
print('GAP para o algoritmo ótimo: ', (quantidade- quantidadeSubstituicoesLRU)/(quantidade-quantidadeSubstituicoesOtimo)*100,'%')


print('\nAlgoritmo NRU')
print('Quantidade de páginas substituídas: ',quantidadeSubstituicoesNRU)
print('GAP para o algoritmo ótimo: ', (quantidade- quantidadeSubstituicoesNRU)/(quantidade-quantidadeSubstituicoesOtimo)*100,'%')
