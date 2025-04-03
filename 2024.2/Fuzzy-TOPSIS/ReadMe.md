# Fuzzy-TOPSIS - Técnica para Ordenação de Preferências por Similaridade com a Solução Ideal, a partir da utilização

## Descrição
Este projeto implementa o método **Fuzzy-TOPSIS** (Technique for Order Preference by Similarity to Ideal Solution), uma técnica de análise de decisão multicritério. O objetivo é classificar alternativas com base em múltiplos critérios, considerando pesos diferentes para cada um. Esse método leva em consideração
também uma abordagem de trabalhar com linguagem natural para classificação dos pesos, sendo essa linguagem transformada em números fuzzy para execução do algoritmo.

## Autores
- **Cauê Marinho**
- **Matheus Nepomuceno**

## Como Usar

### Entrada de Dados
O código recebe uma entrada no formato JSON contendo:
- **method**: Nome do método ("Fuzzy_TOPSIS").
- **parameters**: Um dicionário contendo:
  - **alternatives**: Lista das alternativas.
  - **criteria**: Lista dos critérios.
  - **performance_matrix**: Matriz correspondente as alternativas e suas classificações em relação a cada critério em números fuzzy.
  - **criteria_types**: Especificação se o critério é de **custo (min)** ou **benefício (max)**.
  - **weights**: Pesos de cada critério.

#### Exemplo de Entrada:
```json
{
  "method": "Fuzzy_TOPSIS",
  "parameters": {
    "alternatives": ["F1", "F2", "F3"],
    "criteria": ["C1", "C2", "C3"],
    "performance_matrix": {
      "F1": [[0.6, 0.7, 0.8], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]],
      "F2": [[0.5, 0.6, 0.7], [0.3, 0.4, 0.5], [0.6, 0.7, 0.8]],
      "F3": [[0.7, 0.8, 0.9], [0.5, 0.6, 0.7], [0.8, 0.9, 1.0]]
    },
    "criteria_types": {
      "C1": "max",
      "C2": "min",
      "C3": "max"
    },
    "weights": {
      "C1": [0.3, 0.4, 0.5],
      "C2": [0.2, 0.3, 0.4],
      "C3": [0.4, 0.5, 0.6]
    }
  }
}
```

### Execução do Código
Para rodar o código, basta executar:
```python
from main import FuzzyTOPSIS

data = { # Dados no formato json }
result = process_fuzzy_topsis(data)
print(resultado)
```

### Saída Esperada
O código retorna um json contendo os resultados, os quais são:
- **proximities**: Proximidade das alternativas em relação a solução ideal positiva.
- **ranking**: Lista das alternativas ordenadas da melhor para pior escolha.
- **best alternative**: Melhor alternativa.
- **distances**: Dicionário que contém as distâncias de cada alternativa para as soluções ideais positivas e negativas.

#### Exemplo de Saída:
```json
{
  "method": "Fuzzy_TOPSIS",
  "results": {
    "proximities": {
      "F1": 0.72,
      "F2": 0.65,
      "F3": 0.80
    },
    "ranking": ["F3", "F1", "F2"],
    "best_alternative": "F3",
    "distances": {
      "F1": {
        "ideal": 0.28,
        "negative_ideal": 0.72
      },
      "F2": {
        "ideal": 0.35,
        "negative_ideal": 0.65
      },
      "F3": {
        "ideal": 0.20,
        "negative_ideal": 0.80
      }
    }
  }
}
```

## Licença
Este projeto está sob a licença MIT.