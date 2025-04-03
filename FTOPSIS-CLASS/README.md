# FTOPSIS-Class

A biblioteca FTOPSIS-Class é uma implementação do algoritmo FTOPSIS (Fuzzy Technique for Order Preference by Similarity to Ideal Solution). Este algoritmo é usado para análise de decisão multicritério com dados fuzzy, ou seja, quando os valores dos critérios são imprecisos ou incertos. A biblioteca ajuda na normalização, ponderação e cálculo das soluções ideais, além de calcular distâncias e fornecer os resultados em um formato tabular.

## Autores do Projeto
<br>

| [<img src="https://github.com/luiz-linkezio.png" width=115><br><sub>Luiz Henrique</sub><br>](https://github.com/luiz-linkezio) <sub>Developer</sub><br> <sub>[Linkedin](https://www.linkedin.com/in/luiz-henrique-brito-4065761b0/)</sub><br> | [<img src="https://github.com/dev-joseronaldo.png" width=115><br><sub>José Ronaldo</sub><br>](https://github.com/Dev-JoseRonaldo) <sub>Developer</sub><br> <sub>[Linkedin](https://www.linkedin.com/in/josé-ronaldo-973a26236)</sub><br> | [<img src="https://github.com/Mariana-Marinho.png" width=115><br><sub>Mariana Marinho</sub><br>](https://github.com/Mariana-Marinho) <sub>Developer</sub><br> <sub>[Linkedin](https://www.linkedin.com/in/mariana--marinho/)</sub><br> | [<img src="https://github.com/vitoriabtriz.png" width=115><br><sub>Vitória Beatriz</sub><br>](https://github.com/vitoriabtriz) <sub>Developer</sub><br> <sub>[Linkedin](https://www.linkedin.com/in/vitoriabtriz/)</sub><br> | [<img src="https://github.com/gugaldox.png" width=115><br><sub>Aldo Lemos</sub><br>](https://github.com/gugaldox) <sub>Developer</sub><br> <sub>[Linkedin](https://www.linkedin.com/in/aldo-lemos-ba3331254/)</sub><br> | 
| :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
---



## Instalação (Download da biblioteca)

Você pode instalar a biblioteca utilizando pip:

```bash
pip install ftopsis-class
```

Esta biblioteca foi desenvolvida como parte de um projeto da cadeira de Sistemas de Apoio a Decisão no CIn-UFPE. Para mais informações sobre o método e a implementação, você pode consultar o artigo original:

<a href='https://www.sciencedirect.com/science/article/abs/pii/S0957417417306619' target=_blank>A fuzzy hybrid integrated framework for portfolio optimization in private banking</a>

## Instalação (Rodar localmente)

### Pré-requisitos
- Python 3.8+
- Pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório**:
   ```bash
   git clone git@github.com:adielfilho/SAD.git
   cd SAD/2024.2/FTOPSIS-Class
   
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
    # No Linux/Mac:
   source venv/bin/activate
    # No Windows:
   venv\Scripts\activate
   
3. Instale as dependências:
   ```bash
    pip install -r requirements.txt
  
4. Execute o sistema
   ```bash
   python3 main.py


> ### Personalização dos Arquivos de Entrada
> 
> É possível alterar os arquivos JSON de entrada editando o arquivo `main.py`:
> 
> ```python
> # Na função main(), procure por:
> file_path = 'data/json/trapezoidal_input.json'  # ← Altere este caminho
> 
> # Você pode substituir por:
> file_path = 'caminho/para/seu/arquivo.json'    # Caminho absoluto ou relativo
> ```
> 
> **Dicas importantes**:
> - O sistema detectará automaticamente se o JSON contém números triangulares (3 valores) ou trapezoidais (4 valores)
> - Ou seja, após a publicação da biblioteca, deve-se apenas fornecer o json de entrada que ela detectará automaticamente qual caso usar.
> - Mantenha a estrutura do JSON conforme os exemplos fornecidos na pasta `data/json`

   
## Estrutura do código


### `main.py` - Ponto de Entrada Principal

#### Responsabilidades:
- Coordenação do fluxo principal do programa
- Carregamento e processamento inicial dos dados

#### Principais Componentes:
```python
class FTOPSISProcessor:
    # Classe utilitária com operações comuns
    @staticmethod
    def load_json_data(file_path)  # Carrega arquivos JSON
    @staticmethod
    def print_results(result)      # Exibe resultados formatados
    @staticmethod
    def detect_fuzzy_type(data)    # Detecta tipo de número fuzzy

def trapezoidal_ftopsis_class(data)  # Fluxo para números trapezoidais
def triangular_ftopsis_class(data)   # Fluxo para números triangulares 
def main()                          # Função principal de execução
```

### `triangular_core.py`

#### Responsabilidades:
- Implementação do algoritmo FTOPSIS para números fuzzy triangulares

#### Principais Componentes:
```python
class CriteriaType(Enum):
    """Enumera os tipos de critérios"""
    Cost = 0    # Para critérios de custo (menor é melhor)
    Benefit = 1 # Para critérios de benefício (maior é melhor)

class FTOPSISClass:
    """Implementação completa do FTOPSIS para números triangulares"""

    @staticmethod
    def normalize_matrix(matrix, criteria_type):
        """
        Normaliza a matriz de decisão conforme o tipo de critério
        - Para critérios Benefit: divide cada valor pelo máximo da coluna
        - Para critérios Cost: divide o mínimo da coluna por cada valor
        Retorna: DataFrame normalizado
        """

    @staticmethod
    def weigh_matrix(df_normalized_matrix, df_vector_weights):
        """
        Aplica os pesos à matriz normalizada
        - Multiplica cada valor pelo peso correspondente
        - Arredonda os resultados para 4 casas decimais
        Retorna: DataFrame ponderado
        """

    @staticmethod
    def round_weighted_normalized_matrix(df_weighted_matrix):
        """
        Arredonda os valores da matriz ponderada
        - Padroniza a precisão numérica
        Retorna: DataFrame com valores arredondados
        """

    @staticmethod
    def ideal_solution(df_profile_matrix, profile_mapping):
        """
        Calcula as soluções ideais positiva e negativa
        - Baseado no mapeamento de perfis
        Retorna: Tuple (DataFrame solução positiva, DataFrame solução negativa)
        """

    @staticmethod
    def distance_calculation(matrix, df_positive, df_negative):
        """
        Calcula distâncias euclidianas para ambas as soluções ideais
        - Distância para a solução ideal positiva
        - Distância para a solução ideal negativa
        Retorna: Tuple (DataFrame distâncias positivas, DataFrame distâncias negativas)
        """

    @staticmethod
    def euclidean_distance(v1, v2):
        """
        Calcula distância euclidiana entre dois vetores
        - Implementação vetorizada com numpy
        Retorna: Lista de distâncias calculadas
        """

    @staticmethod
    def proximity_coefficient(positive_dist, negative_dist):
        """
        Calcula coeficiente de proximidade relativa
        - Fórmula: CC = negative_dist / (positive_dist + negative_dist)
        - Determina a classificação final
        Retorna: DataFrame com resultados finais
        """
```
### `trapezoidal_core.py`

#### Responsabilidades:
- Implementação do algoritmo FTOPSIS para números fuzzy trapezoidais

#### Principais Componentes:
```python
class CriteriaType(Enum):
    """Enumera os tipos de critérios"""
    BENEFIT = 1  # Critérios onde maior é melhor
    COST = 0     # Critérios onde menor é melhor

class FuzzyNumber:
    """Representação de números fuzzy trapezoidais"""
    
    def __init__(self, a1: float, a2: float, a3: float, a4: float):
        """
        Inicializa número trapezoidal com:
        - a1: limite inferior esquerdo
        - a2: limite superior esquerdo 
        - a3: limite superior direito
        - a4: limite inferior direito
        """
    
    def distance(self, other: 'FuzzyNumber') -> float:
        """Calcula distância euclidiana entre dois números trapezoidais"""

class FTOPSISClass:
    """Implementação completa do FTOPSIS para números trapezoidais"""

    def __init__(self, linguistic_terms, weights, criteria_type,
                 elements, criteria, fuzzy_decision_matrix, reference_matrix):
        """
        Inicializa o processador FTOPSIS com:
        - linguistic_terms: Dicionário de termos linguísticos
        - weights: Pesos para cada critério
        - criteria_type: Tipo de cada critério (BENEFIT/COST)
        - elements: Lista de elementos a avaliar
        - criteria: Lista de critérios
        - fuzzy_decision_matrix: Matriz de decisão fuzzy
        - reference_matrix: Matriz de referência para perfis
        """

    def _normalize_criteria(self, values: List[FuzzyNumber], criterion: str) -> List[FuzzyNumber]:
        """
        Normaliza valores para um critério específico
        - BENEFIT: divide pelo valor máximo
        - COST: divide o valor mínimo por cada valor
        Retorna: Lista de FuzzyNumbers normalizados
        """

    def normalize_matrix(self) -> Dict:
        """
        Normaliza toda a matriz de decisão
        - Aplica pesos aos valores normalizados
        Retorna: Dicionário com valores normalizados e ponderados
        """

    def calculate_closeness(self) -> Dict:
        """
        Calcula coeficientes de proximidade para todos os elementos
        - Calcula distâncias para soluções ideais
        - Computa CC = d- / (d+ + d-)
        Retorna: Dicionário com CCs para cada perfil
        """

    def classify_funds(self) -> Dict:
        """
        Classifica elementos baseado nos coeficientes de proximidade
        - Seleciona perfil com maior CC para cada elemento
        Retorna: Dicionário com (perfil, CC) para cada elemento
        """

    def run(self) -> Tuple[Dict, Dict]:
        """
        Executa o fluxo completo do FTOPSIS
        Retorna: Tupla com (coeficientes, classificação)
        """
```


## Exemplo de Entrada (Triangular)

### Estrutura do JSON de Entrada
```json
{
  "linguistic_variables_alternatives": {
    "MR": [0.0, 0.0, 2.5],
    "R": [0.0, 2.5, 5.0],
    "M": [2.5, 5.0, 7.5],
    "B": [5.0, 7.5, 10.0],
    "MB": [7.5, 10.0, 10.0]
  },
  "linguistic_variables_weights": {
    "NI": [0.2, 0.2, 0.4],
    "PI": [0.2, 0.4, 0.6],
    "IM": [0.4, 0.6, 0.8],
    "I": [0.6, 0.8, 1.0],
    "MI": [0.8, 0.8, 1.0]
  },
  "decision_matrix": {
    "C1": ["MB", "B", "M", "R", "MR", "MB", "MB", "R", "B"],
    "C2": ["MB", "B", "M", "R", "MR", "R", "MR", "B", "MR"],
    "C3": ["MB", "B", "M", "R", "MR", "B", "B", "B", "R"],
    "C4": ["MB", "B", "M", "R", "MR", "MB", "MB", "B", "MB"]
  },
  "profile_matrix": {
    "C1": ["MB", "B", "R"],
    "C2": ["B", "M", "R"],
    "C3": ["B", "M", "MR"],
    "C4": ["MB", "B", "M"]
  },
  "profile_mapping": {
    "0": "Preferível",
    "1": "Aceitável",
    "2": "Inaceitável"
  },
  "weights": {
    "C1": ["I"],
    "C2": ["IM"],
    "C3": ["IM"],
    "C4": ["I"]
  },
  "criteria_type": {
    "C1": "Benefit",
    "C2": "Benefit",
    "C3": "Benefit",
    "C4": "Benefit"
  },
  "alternatives": [
    "Fornecedor 1", "Fornecedor 2", "Fornecedor 3",
    "Fornecedor 4", "Fornecedor 5", "Fornecedor 6",
    "Fornecedor 7", "Fornecedor 8", "Fornecedor 9"
  ]
}
```

## Exemplo de Saída (Triangular)

### Estrutura do JSON de Resultados
```json
{
  "results": {
    "Fornecedor 1": {
      "scores": {
        "Preferível": 0.8937556705796293,
        "Aceitável": 0.6960279609553498,
        "Inaceitável": 0.1062443294203707
      },
      "classification": "Preferível"
    },
    "Fornecedor 2": {
      "scores": {
        "Preferível": 0.8261102660508366,
        "Aceitável": 0.8151905914802051,
        "Inaceitável": 0.17388973394916343
      },
      "classification": "Preferível"
    },
    "Fornecedor 3": {
      "scores": {
        "Preferível": 0.4060976520273939,
        "Aceitável": 0.6156653142793894,
        "Inaceitável": 0.5939023479726061
      },
      "classification": "Aceitável"
    },
    // ... outros
  }
}

```

## Exemplo de Entrada (Trapezoidal)

### Estrutura do JSON de Entrada
```json
{
  "linguistic_variables_alternatives": {
    "VL": [0.0, 0.0, 0.1, 0.2],
    "L": [0.1, 0.2, 0.3, 0.4],
    "M": [0.3, 0.4, 0.5, 0.6],
    "H": [0.5, 0.6, 0.7, 0.8],
    "VH": [0.7, 0.8, 0.9, 1.0]
  },
  "linguistic_variables_weights": {
    "U": [0.0, 0.0, 0.1, 0.2],
    "MI": [0.1, 0.2, 0.3, 0.4],
    "I": [0.3, 0.4, 0.5, 0.6],
    "VI": [0.5, 0.6, 0.7, 0.8],
    "EI": [0.7, 0.8, 0.9, 1.0]
  },
  "decision_matrix": {
    "C1": ["VL", "VL", "L", "L", "M", "M", "H", "H", "VH", "VH"],
    "C2": ["VL", "VL", "VL", "VL", "VL", "VL", "H", "L", "VL", "VH"],
    "C3": ["H", "VH", "H", "VH", "VH", "VH", "VH", "VL", "VH", "L"],
    "C4": ["VL", "VL", "L", "L", "M", "M", "H", "H", "VH", "VH"],
    "C5": ["VH", "VH", "H", "H", "M", "M", "L", "L", "VL", "VL"],
    "C6": ["VL", "VL", "L", "L", "M", "M", "H", "H", "VH", "VH"],
    "C7": ["M", "M", "M", "M", "VH", "VH", "VH", "H", "H", "VH"]
  },
  "profile_matrix": {
    "C1": ["L", "L", "H", "VH"],
    "C2": ["VL", "VL", "VL", "VL"],
    "C3": ["VL", "L", "H", "VH"],
    "C4": ["VL", "L", "H", "VH"],
    "C5": ["VH", "H", "L", "VL"],
    "C6": ["VL", "L", "H", "VH"],
    "C7": ["H", "H", "L", "VL"]
  },
  "profile_mapping": {
    "0": "Conservative",
    "1": "Moderate",
    "2": "Bold",
    "3": "Aggressive"
  },
  "weights": {
    "C1": ["I"],
    "C2": ["I"],
    "C3": ["I"],
    "C4": ["I"],
    "C5": ["I"],
    "C6": ["I"],
    "C7": ["I"]
  },
  "criteria_type": {
    "C1": "Benefit",
    "C2": "Benefit",
    "C3": "Benefit",
    "C4": "Benefit",
    "C5": "Benefit",
    "C6": "Benefit",
    "C7": "Benefit"
  },
  "alternatives": [
    "Fornecedor 1", "Fornecedor 2", "Fornecedor 3",
    "Fornecedor 4", "Fornecedor 5", "Fornecedor 6",
    "Fornecedor 7", "Fornecedor 8", "Fornecedor 9",
    "Fornecedor 10"
  ]
}

```

## Exemplo de Saída (Trapezoidal)

### Estrutura do JSON de Resultados
```json
{
  "Fornecedor 1": {
    "scores": {
      "Conservative": 0.7924779185497123,
      "Moderate": 0.7316338477777367,
      "Bold": 0.2764522872002296,
      "Aggressive": 0.20752208145028767
    },
    "classification": "Conservative"
  },
  "Fornecedor 2": {
    "scores": {
      "Conservative": 0.7502583468121905,
      "Moderate": 0.6926263567079421,
      "Bold": 0.29903545546785604,
      "Aggressive": 0.24974165318780955
    },
    "classification": "Conservative"
  },
  "Fornecedor 3": {
    "scores": {
      "Conservative": 0.6844564478029598,
      "Moderate": 0.8324520673822401,
      "Bold": 0.43294774451407736,
      "Aggressive": 0.3155435521970403
    },
    "classification": "Moderate"
  },
  // ... outros
}

```