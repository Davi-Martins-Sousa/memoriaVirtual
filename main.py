import pandas as pd
import random
import tkinter as tk
import time
from tkinter import ttk
from tkinter import messagebox

quantidadeSubstituicoesOtimo = 0
passo = 0


def leArquivo(arquivo):

    # Lista para armazenar as linhas do arquivo
    linhas = []

    # Abre o arquivo em modo binário e lê as linhas
    with open('dados/{}'.format(arquivo), 'rb') as arquivo:
        for linha in arquivo:
            linhas.append(linha.decode('utf-8', errors='ignore'))

    # Extrair os valores desejados
    virtual = int(linhas[0].split(': ')[1])
    fisica = int(linhas[1].split(': ')[1])
    quantidade = int(linhas[2])
    vetor = [int(valor) for valor in linhas[3:]]

    return virtual, fisica, quantidade, vetor

def otimo(arquivo,botao):
    _, fisica, quantidade, vetor = leArquivo(arquivo)

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

        if botao != 0:
            atualizar_resultados(quantidade,quantidadeDeSubstituicoes)
        if botao == 2:
            time.sleep(1)
        
    if botao == 0:
        return quantidadeDeSubstituicoes

def aleatorio(arquivo,botao):
    global passo
    _, fisica, quantidade, vetor = leArquivo(arquivo)

    memoriaFisica = [-1] * fisica
    quantidadeDeSubstituicoes = 0

    for indice in range(len(vetor)):
        if vetor[indice] in memoriaFisica:
            quantidadeDeSubstituicoes += 0
        else:
            quantidadeDeSubstituicoes += 1
            memoriaFisica[ random.randint(0, fisica-1)] = vetor[indice]
        atualizar_resultados(quantidade,quantidadeDeSubstituicoes)

        if botao == 2:
            time.sleep(1)
        
       

def fifo(arquivo,botao):
    _, fisica, quantidade, vetor = leArquivo(arquivo)

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

        atualizar_resultados(quantidade,quantidadeDeSubstituicoes)

        if botao == 2:
            time.sleep(1)

def segndaChance(arquivo,botao):
    _, fisica, quantidade, vetor = leArquivo(arquivo)

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
        
        atualizar_resultados(quantidade,quantidadeDeSubstituicoes)

        if botao == 2:
            time.sleep(1)

def lru(arquivo,botao):# menos recentemente usada
    _, fisica, quantidade, vetor = leArquivo(arquivo)

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

        atualizar_resultados(quantidade,quantidadeDeSubstituicoes)

        if botao == 2:
            time.sleep(1)

def NRU(arquivo,botao): # não usada recentemente
    _, fisica, quantidade, vetor = leArquivo(arquivo)

    memoriaFisica = [-1] * fisica
    bits_referencia = [0] * fisica
    bits_modificacao = [0] * fisica
    quantidadeDeSubstituicoes = 0

    for indice in range(len(vetor)):
        if vetor[indice] in memoriaFisica:
            bits_referencia[memoriaFisica.index(vetor[indice])] = 1
        else:
            quantidadeDeSubstituicoes += 1

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

        atualizar_resultados(quantidade,quantidadeDeSubstituicoes)

        if botao == 2:
            time.sleep(1)

def atualizar_resultados(quantidade, quantidade_substituicoes_algo):
    global quantidadeSubstituicoesOtimo 
    gap = (quantidade - quantidade_substituicoes_algo) / (quantidade - quantidadeSubstituicoesOtimo) * 100
    resultado_label.config(text=f"Quantidade de páginas substituídas: {quantidade_substituicoes_algo}\nGAP para o algoritmo ótimo: {gap:.2f}%")
    root.update_idletasks()

# Função para executar o algoritmo escolhido
def executar_algoritmo(botao):
    global quantidadeSubstituicoesOtimo 
    arquivo = arquivo_entry.get()
    algoritmo = algoritmo_combobox.get()

    _, _, quantidade, _ = leArquivo(arquivo)
    if quantidadeSubstituicoesOtimo == 0:
        quantidadeSubstituicoesOtimo = otimo(arquivo,0)

    if algoritmo == "Ótimo":
        otimo(arquivo,botao)
    elif algoritmo == "Aleatório":
        aleatorio(arquivo,botao)
    elif algoritmo == "FIFO":
        fifo(arquivo,botao)
    elif algoritmo == "Segunda Chance":
        segndaChance(arquivo,botao)
    elif algoritmo == "LRU":
        lru(arquivo,botao)
    elif algoritmo == "NRU":
        NRU(arquivo,botao)
    else:
        messagebox.showerror("Erro", "Algoritmo não reconhecido")
        return

    #gap = (quantidade - quantidade_substituicoes) / (quantidade - quantidadeSubstituicoesOtimo) * 100

    #resultado_label.config(text=f"Quantidade de páginas substituídas: {quantidade_substituicoes}\nGAP para o algoritmo ótimo: {gap:.2f}%")

# Configuração da janela principal
root = tk.Tk()
root.title("Simulação de Algoritmos de Substituição de Páginas")
root.geometry("400x300")  # Define o tamanho inicial da janela

# Estilo para os widgets
style = ttk.Style()
style.configure('TLabel', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12))
style.configure('TEntry', font=('Arial', 12))
style.configure('TCombobox', font=('Arial', 12))

# Cor de fundo da janela
root.configure(bg='#f0f0f0')

# Cor de fundo dos widgets
widget_bg_color = '#e0e0e0'

# Entrada para o nome do arquivo
arquivo_label = tk.Label(root, text="Nome do arquivo:")
arquivo_label.pack()
arquivo_entry = tk.Entry(root)
arquivo_entry.pack()

# Combobox para escolher o algoritmo
algoritmo_label = tk.Label(root, text="Escolha o algoritmo:")
algoritmo_label.pack()
algoritmo_combobox = ttk.Combobox(root, values=["Ótimo", "Aleatório", "FIFO", "Segunda Chance", "LRU", "NRU"])
algoritmo_combobox.pack()

# Botão para simular passo-a-passo,
#executar_1_button = tk.Button(root, text="Executar 1", command=lambda: executar_algoritmo(1))
#executar_1_button.pack()

# Botão para simular em tempo real
executar_2_button = tk.Button(root, text="Executar 2", command=lambda: executar_algoritmo(2))
executar_2_button.pack()

# Botão para simulação completa,
executar_3_button = tk.Button(root, text="Executar 3", command=lambda: executar_algoritmo(3))
executar_3_button.pack()

# Label para exibir o resultado
resultado_label = tk.Label(root, text="")
resultado_label.pack()

root.mainloop()