# TOPSIS - Técnica para Ordenação de Preferências por Similaridade com a Solução Ideal

## Descrição
Este projeto implementa o método **TOPSIS** (Technique for Order Preference by Similarity to Ideal Solution), uma técnica de análise de decisão multicritério. O objetivo é classificar alternativas com base em múltiplos critérios, considerando pesos diferentes para cada um.

## Autores
- **Mateus da Silva**
- **Lucas Luis**

## Requisitos
Antes de rodar o código, instale as dependências necessárias. Você pode fazer isso com o comando:
```bash
pip install numpy
```

## Como Usar

### Entrada de Dados
O código recebe uma entrada no formato JSON ou dicionário Python contendo:
- **method**: Nome do método ("TOPSIS").
- **parameters**: Um dicionário contendo:
  - **alternatives**: Lista das alternativas.
  - **criteria**: Lista dos critérios.
  - **performance_matrix**: Dicionário onde cada alternativa possui uma lista de valores para cada critério.
  - **criteria_types**: Especificação se o critério é de **custo (min)** ou **benefício (max)**.
  - **weights**: Pesos de cada critério.
  - **`distance_metric`** *(opcional)*: Define a métrica de distância a ser usada para calcular a proximidade das alternativas:
  - `"1"` → **Distância de Manhattan** (soma das diferenças absolutas entre os valores)
  - `"2"` *(padrão)* → **Distância Euclidiana** (raiz quadrada da soma dos quadrados das diferenças)
  - `"inf"` → **Distância de Chebyshev** (maior diferença absoluta entre os valores)

Se não especificado, o código usará **distância Euclidiana** (`"2"`) por padrão.


#### Exemplo de Entrada:
```json
{
  "method": "TOPSIS",
  "parameters": {
    "alternatives": ["A1", "A2", "A3"],
    "criteria": ["C1", "C2", "C3"],
    "performance_matrix": {
      "A1": [7, 9, 8],
      "A2": [6, 8, 7],
      "A3": [8, 7, 9]
    },
    "criteria_types": {
      "C1": "max",
      "C2": "max",
      "C3": "max"
    },
    "weights": {
      "C1": 0.5,
      "C2": 0.3,
      "C3": 0.2
    },
    "distance_metric": "2"
  }
}

```

### Execução do Código
Para rodar o código, basta executar:
```python
from main import TOPSIS

data = {  # Insira os dados conforme o formato acima }
topsis = TOPSIS(data)
resultado = topsis.calculate()
print(resultado)
```

### Saída Esperada
O código retorna um dicionário contendo:
- **positive_ideal_solution**: Solução ideal positiva.
- **negative_ideal_solution**: Solução ideal negativa.
- **distance_to_pis**: Distância de cada alternativa à solução ideal positiva.
- **distance_to_nis**: Distância de cada alternativa à solução ideal negativa.
- **topsis_score**: Coeficiente de proximidade.
- **ranking**: Lista das alternativas ordenadas.

#### Exemplo de Saída:
```json
{
  "method": "TOPSIS",
  "results": {
    "positive_ideal_solution": {
      "C1": 0.3277,
      "C2": 0.1938,
      "C3": 0.1292
    },
    "negative_ideal_solution": {
      "C1": 0.2458,
      "C2": 0.1508,
      "C3": 0.1005
    },
    "distance_to_pis": {        
      "A1": 0.0434,
      "A2": 0.0894,
      "A3": 0.0431
    },
    "distance_to_nis": {
      "A1": 0.0612,
      "A2": 0.0215,
      "A3": 0.0868
    },
    "topsis_score": {
      "A1": 0.5849,
      "A2": 0.1941,
      "A3": 0.6684
    },
    "ranking": [
      "A3",
      "A1",
      "A2"
    ]
  }
}
```

## Licença
Este projeto está sob a licença MIT.

