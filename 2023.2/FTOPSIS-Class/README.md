# FTOPSIS-Class

A biblioteca FTOPSIS-Class é uma implementação do algoritmo FTOPSIS (Fuzzy Technique for Order Preference by Similarity to Ideal Solution). Este algoritmo é usado para análise de decisão multicritério com dados fuzzy, ou seja, quando os valores dos critérios são imprecisos ou incertos. A biblioteca ajuda na normalização, ponderação e cálculo das soluções ideais, além de calcular distâncias e fornecer os resultados em um formato tabular.

## Autores do Projeto
- <a href='https://github.com/lucasccampos' target='_blank'>Lucas Campos</a>
- <a href='https://github.com/MatheusMalta002' target='_blank'>Matheus Malta</a>
- <a href='https://github.com/ArthurConegundes29102002' target='_blank'>Arthur Conegundes</a>
- <a href='https://github.com/IanFelipe215' target='_blank'>Ian Felipe</a>
- <a href='https://github.com/RodBC' target='_blank'>RodBC</a>


## Instalação

Você pode instalar a biblioteca utilizando pip:

```bash
pip install ftopsis-class
```

Esta biblioteca foi desenvolvida como parte de um projeto da cadeira de Sistemas de Apoio a Decisão no CIn-UFPE. Para mais informações sobre o método e a implementação, você pode consultar o artigo original:

<a href='https://www.sciencedirect.com/science/article/abs/pii/S0957417417306619' target=_blank>A fuzzy hybrid integrated framework for portfolio optimization in private banking</a>


## Métodos

### 1. normalize_matrix
  ```python
    normalize_matrix(matrix: pd.DataFrame, criteria_type: dict[str, CriteriaType]) -> pd.DataFrame
  ```

Normaliza a matriz de decisão com base nos tipos de critério (Benefício ou Custo) especificados. Retorna a matriz normalizada.

### 2. weigh_matrix
  ```python
      weigh_matrix(df_normalized_matrix: pd.DataFrame, df_vector_weights: pd.DataFrame) -> pd.DataFrame
  ````

Pondera a matriz normalizada com os pesos dos critérios. Retorna a matriz ponderada.

### 3. round_weighted_normalized_matrix
  ```python
    round_weighted_normalized_matrix(df_weighted_normalized_matrix: pd.DataFrame) -> pd.DataFrame
  ```
Arredonda os números na matriz ponderada e normalizada para 4 casas decimais.

### 4. ideal_solution
  ```python
    ideal_solution(df_profile_matrix: pd.DataFrame, profile_mapping: dict[int, str]) -> tuple[pd.DataFrame, pd.DataFrame]
  ```
Calcula as soluções ideais positivas e negativas com base na matriz de perfil fornecida e no mapeamento de perfil. Retorna as soluções ideais positivas e negativas.

### 5. distance_calculation
  ```python 
  distance_calculation(matrix: pd.DataFrame, df_positive_solution: pd.DataFrame, df_negative_solution: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]
  ```
Calcula as distâncias entre as alternativas e as soluções ideais positivas e negativas. Retorna as distâncias positivas e negativas.

### 6. proximity_coefficient
  ```python 
    proximity_coefficient(positive_distances: pd.DataFrame, negative_distances: pd.DataFrame) -> pd.DataFrame
  ```
Calcula o coeficiente de proximidade com base nas distâncias positivas e negativas. Retorna o coeficiente de proximidade.

### 7. euclidean_distance
  ```python 
    euclidean_distance(v1: list[float], v2: list[float]) -> list[float]
  ```

Calcula a distância euclidiana entre dois vetores.

## Exemplo de Uso

para uma experiência mais interativa recomendamos o uso desse arquivo collab -> https://colab.research.google.com/drive/1GLa4Qr3NAfs_kj7MJLjlGgWvd6zfWR8J?usp=sharing

```python
import pandas as pd
import numpy as np
from ftopsis_class import FTOPSISClass as ft
from ftopsis_class import CriteriaType

# Variáveis Linguísticas para avaliação alternativas
MR = np.array([0.0, 0.0, 2.5]) # Muito Ruim
R = np.array([0.0, 2.5, 5.0]) # Ruim
M = np.array([2.5, 5.0, 7.5]) # Medio
B = np.array([5.0, 7.5, 10.0]) # Bom
MB = np.array([7.5, 10.0, 10.0]) # Muito Bom

# Variáveis Linguísticas dos pesos dos critérios
NI = np.array([0.2, 0.2, 0.4]) # Nada Importante
PI = np.array([0.2, 0.4, 0.6]) # Pouco Importante
IM = np.array([0.4, 0.6, 0.8]) # Importancia Media
I = np.array([0.6, 0.8, 1.0]) # Importante
MI = np.array([0.8, 0.8, 1.0]) # Muito Importante

# Dados da matriz de decisão
dados_matriz_decisao = {
    "C1": [MB, B, M, R, MR, MB, MB, R, B],
    'C2': [MB, B, M, R, MR, R, MR, B, MR],
    'C3': [MB, B, M, R, MR, B, B, B, R],
    'C4': [MB, B, M, R, MR, MB, MB, B, MB]
}

matriz_decisao = pd.DataFrame(dados_matriz_decisao)

# Dados da matriz de perfil
dados_perfil = {
    "C1": [MB, B, R],
    'C2': [B, M, R],
    'C3': [B, M, MR],
    'C4': [MB, B, M]
}

matriz_perfil = pd.DataFrame(dados_perfil)

# Mapeamento do perfil
mapeamento_perfil = {0: 'Preferível', 1: 'Aceitável', 2: 'Inaceitável'}

# Pesos dos critérios
pesos = {
    "C1": [I],
    "C2": [IM],
    "C3": [IM],
    "C4": [I]
}
pesos = pd.DataFrame(pesos)

# Tipos de critérios
tipo_criterio = {"C1": CriteriaType.Benefit, "C2": CriteriaType.Benefit, 'C3': CriteriaType.Benefit, "C4": CriteriaType.Benefit}

# Normalizar matriz de decisão
matriz_normalizada = ft.normalize_matrix(matriz_decisao, tipo_criterio)

# Ponderar matriz de decisão
matriz_ponderada = ft.weigh_matrix(matriz_normalizada, pesos)

# Arredondar números para 4 casas decimais
matriz_decisao_normalizada_ponderada  = ft.round_weighted_normalized_matrix(matriz_ponderada)

# Normalizar matriz de perfil
matriz_perfil_normalizada = ft.normalize_matrix(matriz_perfil, tipo_criterio)

# Ponderar matriz de perfil
matriz_perfil_ponderada = ft.weigh_matrix(matriz_perfil_normalizada, pesos)

# Arredondar números para 4 casas decimais
matriz_perfil_normalizada_ponderada = ft.round_weighted_normalized_matrix(matriz_perfil_ponderada)

# Calcular soluções ideais
solucao_ideal_positiva, solucao_ideal_negativa = ft.ideal_solution(matriz_perfil_normalizada_ponderada, mapeamento_perfil)

# Calcular distâncias
distancia_positiva, distancia_negativa = ft.distance_calculation(matriz_decisao_normalizada_ponderada, solucao_ideal_positiva, solucao_ideal_negativa)

# Calcular coeficiente de proximidade
resultado = ft.proximity_coefficient(distancia_positiva, distancia_negativa)

# Definir fornecedores
fornecedores = ["Fornecedor 1", "Fornecedor 2", "Fornecedor 3", "Fornecedor 4"]

resultado.index=fornecedores

resultado
```

![image](https://github.com/lucasccampos/ftopsis_class/assets/104574086/ee609f37-0e99-4828-87a5-2e1fda4757bd)


## Limitações e Sugestões de Melhoria do Projeto

### 1. Refatoração para Código Mais Limpo
- Realizar uma revisão detalhada do código, identificando áreas que possam ser simplificadas, modularizadas ou melhor documentadas para garantir a clareza e legibilidade do código.

### 2. Utilização Exclusiva de Numpy para Cálculos de Matrizes
- Reescrever as operações de matriz para utilizar exclusivamente a biblioteca numpy, aproveitando sua eficiência computacional e otimização de desempenho em comparação com os dataframes pandas.

### 3. Implementação de uma Interface Usando Streamlit
- Seria legal desenvolver uma interface de usuário (como sugestão utilizando a biblioteca Streamlit) para oferecer uma experiência mais interativa e amigável para os usuários realizarem análises utilizando o algoritmo FTOPSIS.

### 4. Suporte para Inputs em Formato CSV
- Em relação aos inputs dados nas funções da biblioteca, percebemos que seria bastante útil padronizar a forma como as funções recebem os dados e criar uma funcionalidade para receber os inputs desses dados em formato CSV ao invés de somente dataframes e dicionários, permitindo aos usuários carregar facilmente conjuntos de dados existentes para análise através de uma interface desenvolvida com o Streamlit por exemplo.

### 5. Tratamento de Divisão por Zero
- Implementar tratamento para operações com número 0, evitando erros de divisão por zero e possibilitando a continuidade das operações mesmo em casos excepcionais.

### 6. Testagem com Casos mais Abrangentes
- Ampliar os testes realizados para além de números fuzzy trapezoidais e triangulares, a fim de garantir a robustez e generalização do algoritmo para diferentes tipos de números fuzzy.



