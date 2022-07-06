import numpy as np
import rotate_matrix as rm
from copy import deepcopy

#Func auxiliar, só pra melhorar legibilidade.

def getMinValue(linha):
    return min(linha)

#STEP 1 redução de linha.


def rowReduction(matriz):
    for linha in matriz:
        menor_valor = getMinValue(linha)

        for elemento in range(0,len(linha)):
            linha[elemento] -= menor_valor
    return matriz

#STEP 2 , redução de colunas

def columnReduction(matriz):
    ordemMatriz = len(matriz)
    linha = 0
    valoresColuna = []
    result = []
    while linha != ordemMatriz:
        for elemento in range(0,len(matriz)):
            valoresColuna.append(matriz[elemento][linha])     #Separou em arrays de coluna
        menor_valor = getMinValue(valoresColuna)    #menor valor da coluna
        for item in range(0,len(matriz)):
            valoresColuna[item] -= menor_valor
        result.append(valoresColuna)
        valoresColuna = []
        linha += 1
    return rotateMatrix(result)


#Roda a matriz, de forma que as linhas passam a ser colunas, porém segue a ordem:
#1 coluna vira a 1 linha e assim por diante.

def rotateMatrix(matriz):
    matrizResult = []
    matrizLib = rm.anti_clockwise(matriz) # Pega a matriz invertida 90°

    for item in matrizLib:
        x = []
        for i in range(len(item)-1,-1,-1):  # Inverte as linhas da matriz, pra ficar tipo 180° em relação aos 90°
            x.append(item[i])
        matrizResult.append(x)
        x = []
    return matrizResult

    # return rm.clockwise(matriz)
        


#Func auxiliar, retorna a quantidade de zeros em uma lista
def checarLinha(linha):
    quantZeros = 0
    for item in linha:
        if item == 0:
            quantZeros += 1
    return quantZeros

#Dado uma lista, retorna o maior valor. Se a lista for vazia retorna "Acabou"
def getHigher(lista):
    if not lista:
        return "Acabou"
    else:
        maiorValor = max(lista)
        return maiorValor

#Conta quantos zeros há em cada linha e cada coluna
#Retorna uma tupla no formato (quantDeZeros,indexNaLista,1 se for linha e 2 se for coluna)
def updateZeros(matriz):    

    zerosLeft = []
    # Iterar sobre as linhas
    for i in range(0,len(matriz)):
        # zerosInRowByOrder.append((checarLinha(matriz[i]),i))
        zerosLeft.append(((checarLinha(matriz[i]),i,1)))
    
    # Iterar sobre colunas
    x = rotateMatrix(matriz)

    for i in range(0,len(x)):
        # zerosInColumnByOrder.append((checarLinha(x[i]),i))
        zerosLeft.append(((checarLinha(x[i]),i,2)))

    return zerosLeft


def setLines(matriz):   #Retorna uma tupla dos index de ([linhasmarcadas],[colunasmarcadas])

    matrizEntrada = matriz
    zerosLeft = updateZeros(matrizEntrada)
    linesAlreadySet = []
    columnsAlreadySet = []
    o = getHigher(zerosLeft)


    while o != "Acabou":

        if o[2] == 1:    #Se o "o" for uma linha
            if o[0] != 0: 
                linesAlreadySet.append(o[1])
            matrizEntrada = np.delete(matrizEntrada,o[1],0)
            matrizEntrada = matrizEntrada.tolist()
        if o[2] == 2:
            if o[0] != 0:
                columnsAlreadySet.append(o[1])
            matrizEntrada = np.delete(matrizEntrada,o[1],1) #Deleta a linha com ajuda do numpy
            matrizEntrada = matrizEntrada.tolist() #Transforma a arraynumpy numa lista python.
        
        o = getHigher(updateZeros(matrizEntrada))
    return (linesAlreadySet,columnsAlreadySet)


def getMinNumberNotMarked(matriz,listasDeMarcados):
    matrizEntrada = matriz
    linhasMarcadas = listasDeMarcados[0]
    colunasMarcadas = listasDeMarcados[1]

    #ApagarLinhas
    for l in linhasMarcadas:
        matrizEntrada = np.delete(matrizEntrada,l,0)
        matrizEntrada = matrizEntrada.tolist()
    for c in colunasMarcadas:
        matrizEntrada = np.delete(matrizEntrada,c,1)
        matrizEntrada = matrizEntrada.tolist()
    
    return (min(min(matrizEntrada)),matrizEntrada) #Retorna o menor valor, e os valores não marcados.
    
def whichListIsLarger(list1,list2):
    tamanhoDasLinhas = [(len(list1)),len(list2)]
    tamanho = max(tamanhoDasLinhas)
    return (tamanho,tamanhoDasLinhas.index(tamanho)) #Retorna tamanho da maior lista, e 1 se for a primeira/ 2 se for a segunda.


def correctIndex(entrada,entrada2):
    result = True
    for item in entrada2:
        if item not in entrada[0]:
            result = False
    return result

#STEP 3


#Resultado do step 2 ja é o step 3 .

#STEP 4
def createAditionalZeros(matriz,listasDeMarcados):

    matrizEntrada = matriz

    menorValor = getMinNumberNotMarked(matrizEntrada,listasDeMarcados)[0]
    valoresNaoMarcados = getMinNumberNotMarked(matrizEntrada,listasDeMarcados)[1]

    doubleMarked = []

    linhasMarcadas = listasDeMarcados[0]
    colunasMarcadas = listasDeMarcados[1]

    # Definindo os valores "cruzados"
    maiorLista = whichListIsLarger(linhasMarcadas,colunasMarcadas)

    if maiorLista[1] == 1:
        for linhas in linhasMarcadas:
            for colunas in colunasMarcadas:
                doubleMarked.append((linhas,colunas)) #Index dos valores marcados
    if maiorLista[1] == 2:
        for colunas in colunasMarcadas:
            for linhas in linhasMarcadas:
                doubleMarked.append((linhas,colunas)) #Index dos valores marcados
    
    valoresMarcadosNaLista = []
    for valores in doubleMarked:
        valoresMarcadosNaLista.append(matrizEntrada[valores[0]][valores[1]])

    #Agora reconstruir a matriz original para retorna-la
    
#Menor valor, e valores cruzados definidos, agora vou diminuir o menor de todos que não foram cortados
# E somar aos cruzados.

    for x in range(0,len(valoresMarcadosNaLista)):
        for h in range(0,len(matrizEntrada)):

            if valoresMarcadosNaLista[x] in matrizEntrada[h]:
                index = matrizEntrada[h].index(valoresMarcadosNaLista[x])
                matrizEntrada[h][index] = valoresMarcadosNaLista[x] + menorValor

    
    

    for i in range(0,len(valoresNaoMarcados)):

        for itemi in valoresNaoMarcados[i]:
            for j in range(0,len(matrizEntrada)):

                if itemi in matrizEntrada[j]:
                    index = matrizEntrada[j].index(itemi)
                    matrizEntrada[j][index] = itemi - menorValor
    return matrizEntrada



def checkColumnsInPositionIndex(PositionIndex,column):
    for i in PositionIndex:
        if i[1] == column:
            return False
    return True


def optimalAssignment(entrada,matrizResult,formaDoOutput=None):
    matrizEntrada = entrada
    matrizResultado = matrizResult
    colunas = []
    indices = []

    resultado = []

    for linha in range(0,len(matrizResultado)):
        for coluna in range(0,len(matrizResultado[linha])):
            if matrizResultado[linha][coluna] == 0:
                if coluna not in colunas:
                    colunas.append(coluna)
                    indices.append((linha,coluna))


    for p in range(0,len(indices)):
        linha = (indices[p][0])
        coluna = (indices[p][1])
        resultado.append(matrizEntrada[linha][coluna])

    if formaDoOutput == None:
        return sum(resultado)
    else:
        return indices
        


#step 4 volta 1 matriz
#step2 volta 1 matriz e step 3 volta os indices


def elegibleToStepFour(entrada,lista):
    x = len(lista[0]) + len(lista[1])
    y = len(entrada)

    if x < y:
        return True
    else:
        return False

def main(Entrada):
    # STEP 1  ROW MINIMA
    step1 = rowReduction(Entrada)
    # STEP 2
    step2 = columnReduction(step1)
    copyStep2 = deepcopy(step2)
    # STEP 3
    step3 = setLines(step2)

    
    if (elegibleToStepFour(Entrada,step3)):
        step4 = createAditionalZeros(copyStep2,step3)
        step5 = optimalAssignment(Entrada,step4)
    else:
        step5 = optimalAssignment(Entrada,step2,"indices")

    # STEP 4
    print(step5)
    return step5

Entrada = [
    #j1 j2 j3 j4
    [82,83,69,92],  #w1
    [77,37,49,92],  #w2
    [11,69,5,86],   #w3
    [8,9,98,23]     #w4
]


main(Entrada)


