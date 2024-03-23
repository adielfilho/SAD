# Importa a biblioteca NumPy, que é utilizada para realizar operações matriciais eficientes em Python.
import numpy as np

#STEP 3
def determinar_dominio_dos_criterios(matriz_decisao):
    matriz_decisao = np.array(matriz_decisao)

    # Determinando os maiores valores possíveis para cada critério (solução ideal)
    maiores_valores = np.max(matriz_decisao, axis=0)
    # Os maiores valores representam as soluções ideais em cada critério, ou seja, o melhor valor que uma alternativa poderia alcançar em cada critério.

    # Determinando os menores valores possíveis para cada critério (solução não ideal)
    menores_valores = np.min(matriz_decisao, axis=0)
    # Os menores valores representam as soluções não ideais em cada critério, ou seja, o pior valor que uma alternativa poderia alcançar em cada critério.

    # Criando a matriz de domínio com os maiores e menores valores de cada critério
    matriz_dominio = np.vstack((maiores_valores, menores_valores))
    # A matriz de domínio é composta pelos maiores e menores valores de cada critério, onde a primeira linha representa os maiores valores (solução ideal) e a segunda linha representa os menores valores (solução não ideal).

    return matriz_dominio.tolist()


# STEP 4 
def criar_matriz_decisao_completa(matriz_decisao, perfis_centrais):
    # Concatenando a matriz de decisão com a matriz de domínio
    matriz_decisao_completa = matriz_decisao + perfis_centrais

    # A concatenação dessas duas matrizes resulta na matriz de decisão completa, onde cada elemento da matriz contém tanto o valor real do critério quanto seus limites de variação(mínimo e máximo). Esta matriz é usada posteriormente no cálculo das distâncias entre as alternativas e as soluções ideal e anti-ideal no método TOPSIS.
    return matriz_decisao_completa


# STEP 5
# STEP 5.1: Normalizar a Matriz de Decisão Completa
# Isso é necessário porque os critérios podem ter unidades diferentes, escalas diferentes ou variações de valores muito distintas, o que pode distorcer a análise se não forem tratados adequadamente.A normalização coloca todos os critérios em uma escala comum para que possam ser comparáveis de forma justa.
def normalizar_matriz_decisao_completa(matriz_decisao_completa):
    # Realizando a normalização por min-max
    valores_minimos = np.min(matriz_decisao_completa, axis=0)  # Calcula o valor mínimo ao longo de cada coluna
    valores_maximos = np.max(matriz_decisao_completa, axis=0)  # Calcula o valor máximo ao longo de cada coluna
    matriz_normalizada = (matriz_decisao_completa - valores_minimos) / (valores_maximos - valores_minimos)  # Aplica a fórmula min-max

    #  Retorna matriz de decisão completa normalizada.
    return matriz_normalizada.tolist()


def normalizar_pesos(pesos):
    #  Retorna pesos normalizados
    soma_pesos = np.sum(pesos)  # Calcula a soma dos pesos
    pesos_normalizados = pesos / soma_pesos  # Divide cada peso pela soma dos pesos
    return pesos_normalizados


# STEP 5.2: Calcular a Matriz de Decisão Completa Ponderada e Normalizada
def calcular_matriz_completa_ponderada_normalizada(matriz_normalizada, pesos):
    #matriz_normalizada = np.array(matriz_normalizada)
    # Multiplicando cada valor normalizado pelo peso correspondente do critério
    matriz_completa_ponderada_normalizada = matriz_normalizada * pesos

    # Retorna a matriz de decisão ponderada e normalizada
    return matriz_completa_ponderada_normalizada.tolist()


# STEP 6: Determine as soluções ideais e anti-ideais
def determinar_solucoes_ideais(matriz_ponderada_normalizada, criterios):
    solucao_ideal = np.copy(matriz_ponderada_normalizada[0]) # inicializa com a primeira linha
    solucao_anti_ideal = np.copy(matriz_ponderada_normalizada[0]) # inicializa com a primeira linha

    for i in range(1, len(matriz_ponderada_normalizada)):
        for j in range(len(matriz_ponderada_normalizada[i])):
            if criterios[j] is True:
                solucao_ideal[j] = max(solucao_ideal[j], matriz_ponderada_normalizada[i][j])
                solucao_anti_ideal[j] = min(solucao_anti_ideal[j], matriz_ponderada_normalizada[i][j])
            elif criterios[j] is False:
                solucao_ideal[j] = min(solucao_ideal[j], matriz_ponderada_normalizada[i][j])
                solucao_anti_ideal[j] = max(solucao_anti_ideal[j], matriz_ponderada_normalizada[i][j])

    return solucao_ideal, solucao_anti_ideal


# STEP 7: Calcular as distâncias euclidianas de cada alternativa e perfil para as soluções ideais e anti-ideais
def calcular_distancias_euclidianas(matriz_normalizada_ponderada, solucao_ideal, solucao_anti_ideal):
    # Calcula as distâncias euclidianas de cada alternativa e perfil para as soluções ideais e anti-ideais.

    distancias_ideal = np.sqrt(np.sum((matriz_normalizada_ponderada - solucao_ideal) ** 2, axis=1))
    # A distância euclidiana de cada alternativa para a solução ideal é calculada pela raiz quadrada da soma dos quadrados das diferenças entre os valores da alternativa e os valores ideais em cada critério.

    # Calcular as distâncias euclidianas para a solução anti-ideal
    distancias_anti_ideal = np.sqrt(np.sum((matriz_normalizada_ponderada - solucao_anti_ideal) ** 2, axis=1))
    # A distância euclidiana de cada alternativa para a solução anti-ideal é calculada da mesma forma, mas usando os valores anti-ideais em vez dos valores ideais.

    return distancias_ideal, distancias_anti_ideal


# STEP 8: Calcular o coeficiente de proximidade de cada alternativa para a solução ideal
def calcular_coeficiente_proximidade(distancia_ideal, distancia_anti_ideal):
    # Calcula o coeficiente de proximidade de cada alternativa para a solução ideal.
    coeficiente_proximidade = distancia_anti_ideal / (distancia_ideal + distancia_anti_ideal)
    # O coeficiente de proximidade é calculado como a razão entre a distância para a solução anti-ideal e a soma das distâncias para a solução ideal e a solução anti-ideal.

    return coeficiente_proximidade


# STEP 9: Classificar as alternativas da matriz e os perfis fazendo comparações entre seus coeficientes de proximidade
def classificar_alternativas(coeficientes_proximidade_alternativas, coeficientes_proximidade_perfis):
    coeficientes_proximidade_alternativas = np.array(coeficientes_proximidade_alternativas)
    coeficientes_proximidade_perfis = np.array(coeficientes_proximidade_perfis)
    classificacoes = []

    for cpa in coeficientes_proximidade_alternativas:
        diffs = np.abs(cpa - coeficientes_proximidade_perfis)
        min_diff_index = np.argmin(diffs)
        classificacoes.append(f'C{min_diff_index+1}')

    return classificacoes


# Função principal que executa todas as etapas do algoritmo TOPSIS
def topsis(matriz_decisao, pesos, perfis, criterios):
    # STEP 3
    dominio_dos_criterios = determinar_dominio_dos_criterios(matriz_decisao)
    
    # STEP 4
    matriz_decisao_completa = criar_matriz_decisao_completa(matriz_decisao, perfis)

    # STEP 5
    matriz_decisao_normalizada = normalizar_matriz_decisao_completa(matriz_decisao_completa)

    # STEP 5.2
    pesos_normalizados = normalizar_pesos(pesos)
    matriz_completa_ponderada_normalizada = calcular_matriz_completa_ponderada_normalizada(matriz_decisao_normalizada, pesos_normalizados)

    # STEP 6
    solucao_ideal, solucao_anti_ideal = determinar_solucoes_ideais(matriz_completa_ponderada_normalizada, criterios)

    # STEP 7
    tamanho_matriz_decisao = len(matriz_decisao)
    tamanho_matriz_perfil = len(perfis)
    
    # Dividindo matriz de decisão ponderada normalizada em matriz de decisão e matriz de perfil
    matriz_decisao_ponderada_normalizada = matriz_completa_ponderada_normalizada[:tamanho_matriz_decisao]
    matriz_perfil_ponderada_normalizada = matriz_completa_ponderada_normalizada[tamanho_matriz_decisao:tamanho_matriz_decisao+tamanho_matriz_perfil]

    # Calculando distancias ideais e anti-ideais
    distancias_alternativa_ideal, distancias_alternativa_anti_ideal = calcular_distancias_euclidianas(matriz_decisao_ponderada_normalizada, solucao_ideal, solucao_anti_ideal)

    distancias_perfil_ideal, distancias_perfil_anti_ideal = calcular_distancias_euclidianas(matriz_perfil_ponderada_normalizada, solucao_ideal, solucao_anti_ideal)

    # STEP 8
    coeficiente_proximidade_alternativa = calcular_coeficiente_proximidade(distancias_alternativa_ideal, distancias_alternativa_anti_ideal)
    
    coeficiente_proximidade_perfil = calcular_coeficiente_proximidade(distancias_perfil_ideal, distancias_perfil_anti_ideal.tolist())

    # STEP 9
    classificacao = classificar_alternativas(coeficiente_proximidade_alternativa, coeficiente_proximidade_perfil)

    print("Classificação:", classificacao)
    return classificacao

###############################################################################

# Exemplo de entrada manual
'''
matriz = [[8, 10, 6], [7, 6, 9], [10, 9, 9]]
pesos = [9, 8, 8]
perfis =[[10, 10, 9], [8, 7, 9], [7, 6, 6]]
criterios = [True, False, True]
'''	