import os
#1a
import pandas as pd
import matplotlib.pyplot as plt
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'CarDataset.xlsx')
data = pd.read_excel(DATA_PATH)
import pandas as pd 
import numpy as np
import math
import huffmancodec as huffc


#1b
dataMatrix = data.to_numpy()
#1c
min_value = np.uint16(0)
max_value = np.uint16(65535)
varNames=data.columns.values.tolist()
figure, axs = plt.subplots(3, 2, figsize=(15, 10))

#2

def compareMPG(dataMatrix, varNames):
    #MPG é o index 6 da lista
    MPG = dataMatrix[:,6]
    for i in range (6):
        plt.figure(1)
        plt.subplot(321+i)
        plt.scatter(dataMatrix[:,i], MPG, color = 'purple')
        plt.xlabel(varNames[i])
        plt.ylabel("MPG")
        plt.title("MPG vs. " + varNames[i])
        plt.subplots_adjust(hspace=0.99, wspace=0.3)   
    plt.tight_layout()
#3a
dataMatrix = dataMatrix.astype("uint16")
#3b
lists_by_variable = {variable: [] for variable in varNames}

#define o aflabeto de uma variavel ,em range(não usado)
def calculate_alphabet(target, name):
    max_value = float()
    min_value = float(0) 
    for value in target.values:
        if value > max_value:
            max_value = value
        if value < min_value:
            min_value = value          
    alphabet = list(range(min_value, max_value + 1))
    return alphabet
#4
#conta as ocorrencias
def ocorrencias (target, alfa):
    contador = alfa.copy()
    for i in target:
        contador[i] += 1
    return contador
#5a

def ocorrenciasPlot (target, alfa, name, tickInterval):
    contador = ocorrencias(target, alfa)
    #filtra se ocorrencias for 0 (como pedido)
    xAxis = [x for x in contador.keys() if contador[x] > 0]
    yAxis = []
    for i in xAxis:
        yAxis.append(contador[i])
        
    # O x_values é uma linha de valores para o eixo X sem espaços vazios
    x_values = np.arange(len(xAxis))
    plt.figure(2)
    plt.bar(x_values, yAxis, color = "red")
    plt.xlabel(name)
    plt.ylabel("Count")
    # xticks é usado para trocar as labels do x_values pelas do xAxis, tendo assim 
    # uma linha não interrompida de valores em x mas com as labels corretas do xAxis 
    tickPos = np.arange(0, len(xAxis), tickInterval)
    tickLabels = [xAxis[i] for i in tickPos]
  
    plt.xticks(tickPos, tickLabels)
    plt.axis("tight")
    plt.tight_layout()
   
#6
def binning (target, n, firstAlfa):
    # Encontra o valor máximo no array 'target'
    lastAlfa = np.max(target)
    # Cria um dicionário para rastrear as contagens de ocorrências de valores no intervalo
    targetAlfa = {key: 0 for key in range(0, lastAlfa + 1)}
    # Calcula as contagens de ocorrências
    ocorr = ocorrencias(target, targetAlfa)
    # Calcula o número de intervalos desejados
    binningN = len(list(ocorr.keys())) // n
    # Loop para criar os intervalos e substituir valores
    for i in range(binningN):
        binn = list(ocorr.keys())[i * n : (i+1) * n]
        # Substitui pelo valor mais comum dentro do intervalo
        replacement = max(ocorr, key = lambda k: ocorr[k] if k in binn else -1)
        # Cria uma máscara para selecionar elementos dentro do intervalo
        mask = (target >= np.min(binn)) & (target <= np.max(binn))
        # Substitui os elementos pela 'replacement' dentro do intervalo
        target[mask] = replacement
        # Retorna o array 'target' após o processo de binning
    return target

#define alfabeto em dicionario, para ser usado em ocorrencias
alfa = {key: 0 for key in range (min_value, max_value +1)}

def mediaBits (target, alfa):
    contador = ocorrencias(target, alfa)
    nAlfa = len([x for x in contador.values() if x > 0])
    return math.log2(nAlfa)

#ex 7a
def entropy(target, alfa):
    # H(X) = -ΣP(i)*log2(P(i))

    contador = ocorrencias(target, alfa)
    menor = min(target)
    maior = max(target)
    tamanho = len(target)   
    ent = 0
    for i in range(menor, maior + 1):
        if i in contador and contador[i] > 0:
            prob = contador[i] / tamanho
            ent += prob * math.log2(prob)    
    return -ent


#ex 8
def entropyHuff (target, alfa):
    codec = huffc.HuffmanCodec.from_data(target) 
    symbols, lenghts = codec.get_code_len()
    # Calcula as ocorrências dos símbolos
    ocorr = ocorrencias(target, alfa)
    # Calcula o tamanho dos dados de entrada
    tamanho = len(target)
    entropy = 0
    for idx in range(len(symbols)):
        prob = ocorr[symbols[idx]]/tamanho
        entropy += prob * lenghts[idx]
    return entropy

def varianceHuff(target, alfa):
    codec = huffc.HuffmanCodec.from_data(target) 
    symbols, lengths = codec.get_code_len()

    ocorr = ocorrencias(target, alfa)
    tamanho = len(target)
    # Cálculo da entropia
    entropy = 0
    for idx in range(len(symbols)):
        prob = ocorr[symbols[idx]] / tamanho
        entropy += prob * lengths[idx]
    # Cálculo da variância
    variance = 0
    for idx in range(len(symbols)):
        prob = ocorr[symbols[idx]] / tamanho
        # Calcula a diferença quadrática ponderada entre o comprimento e a entropia
        variance += prob * (lengths[idx] - entropy) ** 2
    return variance
#9
def pearson(MPG, target):
    return np.corrcoef(target, MPG)[0][1]


def infoMut(MPG, target, alfa):    
    #ocorrTarget = ocorrencias(target, alfa)
    #ocorrMPG = ocorrencias(MPG, alfa)
    # Calcula a entropia de MPG
    MPGEntropy = entropy(MPG, alfa)
    # Calcula a entropia do alvo (target)
    targetEntropy = entropy(target, alfa)
    # Calcula o tamanho do alvo (target)
    tamanho = len(target)
    # Encontra os valores únicos em MPG
    uniqueMPG = np.unique(MPG)
    # Encontra os valores únicos no alvo (target)
    uniqueTarget = np.unique(target)
    # Encontra os valores únicos no alvo (target)
    uniqueMPG = np.max(MPG) - np.min(MPG)
    # Calcula a faixa de valores no alvo (target)
    uniqueTarget = np.max(target) - np.min(target)
    # Calcula a matriz de probabilidade conjunta MPG-Target
    probMPGTarget = np.histogram2d(MPG, target, bins=(uniqueMPG, uniqueTarget +10))[0] / tamanho
    #Filtra os valores de probabilidade diferentes de zero
    nonzeroIdx = probMPGTarget != 0
    probMPGTarget = probMPGTarget[nonzeroIdx]
    # Calcula a entropia conjunta de MPG e Target
    MPGTargetEntropy = -np.sum(probMPGTarget * np.log2(probMPGTarget))
        
    return MPGEntropy + targetEntropy - MPGTargetEntropy
#indica a distância entre a MPGpred e MPG real(erro)
def MAE (MPG, target):
    target = np.array(target)
    MPG = np.array(MPG)
    return np.mean(np.abs(MPG-target))

#usa a formula obtida no exercicio 11, podendo remover uma variavel
def predictMPG (dataM, remove):
    rowSize = len(dataM[0])
    for i in remove: 
        dataM[i] = [0 for i in range(rowSize)]
    MPGpred = [-5.5241 - 0.146 * dataM[0][i] - 0.4909 * dataM[1][i] + 0.0026 * dataM[2][i] - 0.0045 * dataM[3][i] + 0.6725 * dataM[4][i] - 0.0059 * dataM[5][i] for i in range(rowSize)]
        
    return MPGpred
        

acceleration = np.copy(dataMatrix[:,0])
cylinders = np.copy(dataMatrix[:,1])
displacement = np.copy(dataMatrix[:,2])
horsepower = np.copy(dataMatrix[:,3])
model = np.copy(dataMatrix[:,4])
weight = np.copy(dataMatrix[:,5])
MPG = np.copy(dataMatrix[:,6])
compareMPG(dataMatrix, varNames)

#calcula ocorrencias de aceleracao
#da print as ocorrencias da aceleracao
acceleration_column = np.copy(dataMatrix[:, 0])
ocorrenciasPlot(acceleration_column, alfa, "acceleration", 1)
plt.show()

#6 a,b,c
#6 d
#6e
weight = binning(weight, 40, np.min(dataMatrix[:,5]))
displacement = binning(displacement, 5, np.min(dataMatrix[:,2]))
horsepower = binning(horsepower, 5, np.min(dataMatrix[:,3]))
ocorrenciasPlot(weight, alfa, "Weight (with binnig)", 7)
plt.show()
ocorrenciasPlot(displacement, alfa, "Displacement (with binnig)", 3)
plt.show()
ocorrenciasPlot(horsepower, alfa, "Horsepower (with binnig)", 3)
plt.show()

#matriz com os valores de weight displacement e horsepower apos binning
dataMatrixBinn = [acceleration, cylinders, displacement, horsepower, model, weight, MPG]

#7a
total_entropy = entropy(dataMatrix.reshape(-1), alfa)
IMarray = []
print(" \n")
for i in range(7):
    #7a
    print(varNames[i], ":")
    print("entropia normal após binning:", entropy(dataMatrixBinn[i], alfa))
    #8a
    huffEntropy = entropyHuff(dataMatrixBinn[i], alfa)
    print("entropia de huffman após binning", huffEntropy)
    #8apt2
    huffvariance = varianceHuff(dataMatrixBinn[i], alfa)
    print("variancia tamanho", huffvariance)
    #9
    print("coorelação de Pearson entre MPG e a variavel",pearson(MPG, dataMatrixBinn[i]))
    #10
    print("informação mútua da variavel",infoMut(MPG, dataMatrixBinn[i], alfa))
    print(" \n")
      
print("Entropia da matriz inteira antes do binning: ", entropy(np.reshape(dataMatrix, -1), alfa), "\n")
print("Entropia da matriz inteira depois do binning: ", entropy(np.reshape(dataMatrixBinn, -1), alfa), "\n")


    
#11a
MPGpred = predictMPG(dataMatrixBinn.copy(), [])
print("Erro de MPGpred com todas as variáveis: ", MAE(MPG, MPGpred), "MPG previsto: ", np.average(MPGpred))
#11c
MPGpred = predictMPG(dataMatrixBinn.copy(), [5])
print("Erro de MPGpred sem variável de maior MI: ", MAE(MPG, MPGpred), "MPG previsto: ", np.average(MPGpred))
#11d
MPGpred = predictMPG(dataMatrixBinn.copy(), [0])
print("Erro de MPGpred sem variável de menor MI: ", MAE(MPG, MPGpred), "MPG previsto: ", np.average(MPGpred))
