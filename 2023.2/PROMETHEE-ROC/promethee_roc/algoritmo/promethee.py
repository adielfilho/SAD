#Função para calcular os pesos substituos através do método ROC, recebe com atributo a lista contendo os critérios em ordem de importância
def roc(criterios):
    criterios_com_pesos = []
    somatorio = 0
    for i in range(len(criterios) - 1, -1, -1): #Loop for que percorre a lista dos critérios ao contrário para aplicar a função do método ROC
        criterios_com_pesos.append((f"{criterios[i]}", 1 / len(criterios) * (somatorio + 1 / (i + 1))))
        somatorio += 1 / (i + 1) #Somatório que leva em conta a posição do critério na ordem de importância dele
    criterios_com_pesos.reverse() #Inverte para caso de print para manter a ordem de importância dos critérios

    return criterios_com_pesos
#Função para calcular os índices de preferência entre cada tupla de alternativas utilizando a função limiar
def calcular_indices_preferencia(alternativa1, alternativa2, criterios, alternativas, dados):
    indice_preferencia = 0
    for j in range(len(criterios)):
        indice = 0

        valor_alternativa1 = float(dados[alternativas.index(alternativa1)][j])
        valor_alternativa2 = float(dados[alternativas.index(alternativa2)][j])

        if valor_alternativa1 > valor_alternativa2: #Caso o valor de um critério da alternativa 1 for maior que o da alternativa2 para o mesmo critério, a primeira é preferida em relação a segunda em um grau que é calculado nessa linha
            indice = 1
        else:
            indice = 0 #Atribui 0 para caso o valor de um critério da alternativa 1 for menor que o da alternativa 2, ou seja, não há preferência neste critério
        indice_preferencia += indice * criterios[j][1] #Leva em conta o peso de cada critério

    return indice_preferencia
#Função par calcular os fluxos de superação positivo, negativo e total de cada alternativa levando em conta os índices de preferência de cada uma
def calcular_fluxos(alternativas, criterios, dados):
    pares = [(a, b) for a in alternativas for b in alternativas if a != b] #Cria uma lista com todas as tuplas de alternativas possíveis para que possa ser aplicada a função calcular_indices_preferencia para cada
    todos_indices = {}
    todos_fluxos_positivos = {}
    todos_fluxos_negativos = {}

    for par in pares:
        indice_par = calcular_indices_preferencia(par[0], par[1], criterios, alternativas, dados)
        todos_indices[f"Indice({par[0]}, {par[1]})"] = indice_par

    for alternativa in alternativas:
        soma_indice_positivo = 0
        for par, indice in todos_indices.items():
            if par.startswith(f"Indice({alternativa}"):
                soma_indice_positivo += indice
        fluxo_positivo = 1 / (len(alternativas) - 1) * soma_indice_positivo #Cálculo fluxo de superação positivo
        todos_fluxos_positivos[alternativa] = fluxo_positivo

        soma_indice_negativo = 0
        for par, indice in todos_indices.items():
            if par.endswith(f"{alternativa})"):
                soma_indice_negativo += indice
        fluxo_negativo = 1 / (len(alternativas) - 1) * soma_indice_negativo #Cálculo fluxo de superação negativo
        todos_fluxos_negativos[alternativa] = fluxo_negativo

    todos_fluxos_totais = {}
    for alternativa in alternativas:
        todos_fluxos_totais[alternativa] = todos_fluxos_positivos[alternativa] - todos_fluxos_negativos[alternativa] #Cálculo fluxo de superação total

    return todos_fluxos_totais, todos_fluxos_positivos, todos_fluxos_negativos, todos_indices
#Função da saída do PROMETHEE I, retorna as relações entre cada alternativa, seja de preferência, indiferença ou imcoparabilidade
def classificacao_parcial(todos_fluxos_positivos, todos_fluxos_negativos, alternativas):
    pares = [(a, b) for a in alternativas for b in alternativas if a != b]
    classificacoes = []
    for par in pares:
        if (todos_fluxos_positivos[par[0]] > todos_fluxos_positivos[par[1]] and todos_fluxos_negativos[par[0]] < todos_fluxos_negativos[par[1]]) or \
                (todos_fluxos_positivos[par[0]] == todos_fluxos_positivos[par[1]] and todos_fluxos_negativos[par[0]] < todos_fluxos_negativos[par[1]]) or \
                (todos_fluxos_positivos[par[0]] > todos_fluxos_positivos[par[1]] and todos_fluxos_negativos[par[0]] == todos_fluxos_negativos[par[1]]):
            classificacoes.append(f"{par[0]} é preferível a {par[1]}")
        elif todos_fluxos_positivos[par[0]] == todos_fluxos_positivos[par[1]] and todos_fluxos_negativos[par[0]] == todos_fluxos_negativos[par[1]]:
            classificacoes.append(f"{par[0]} e {par[1]} são indiferentes")
            pares.remove((par[1], par[0]))
        elif (todos_fluxos_positivos[par[0]] > todos_fluxos_positivos[par[1]] and todos_fluxos_negativos[par[0]] > todos_fluxos_negativos[par[1]]) or \
                (todos_fluxos_positivos[par[0]] < todos_fluxos_positivos[par[1]] and todos_fluxos_negativos[par[0]] < todos_fluxos_negativos[par[1]]):
            classificacoes.append(f"{par[0]} e {par[1]} são incomparáveis")
            pares.remove((par[1], par[0]))

    return classificacoes
#Função da saída do PROMETHEE II, retorna a relação de preferência total entre todas alternativas
def classificacao_total(fluxos_totais):
    alternativas_ordenadas = sorted(fluxos_totais.items(), key=lambda x: x[1], reverse=True)

    return alternativas_ordenadas