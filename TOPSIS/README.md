# TOPSIS - Técnica para Ordenação de Preferências por Similaridade com a Solução Ideal

## Descrição
Este projeto implementa o método **TOPSIS** (Technique for Order Preference by Similarity to Ideal Solution), uma técnica de análise de decisão multicritério. O objetivo é classificar alternativas com base em múltiplos critérios, considerando pesos diferentes para cada um.

## Autores
- **Mateus da Silva**
- **Lucas Luis**

## Requisitos
Antes de rodar o código, instale as dependências necessárias. Você pode fazer isso com o comando:
```bash
pip install -r requirements.txt
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

#### Exemplo de Entrada:
```json
{
  "method": "TOPSIS",
  "parameters": {
    "alternatives": ["Palio", "HB20", "Corolla"],
    "criteria": ["Consumo", "Conforto", "Preço", "Reputação"],
    "performance_matrix": {
      "Palio": [15, 6, 25000, 7],
      "HB20": [12, 7, 35000, 7],
      "Corolla": [10, 9, 55000, 8]
    },
    "criteria_types": {"Consumo": "min", "Conforto": "max", "Preço": "min", "Reputação": "max"},
    "weights": {"Consumo": 0.3, "Conforto": 0.05, "Preço": 0.6, "Reputação": 0.05}
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
    "positive_ideal_solution": {"Consumo": 10.0, "Conforto": 9.0, "Preço": 25000.0, "Reputação": 8.0},
    "negative_ideal_solution": {"Consumo": 15.0, "Conforto": 6.0, "Preço": 55000.0, "Reputação": 7.0},
    "distance_to_pis": {"Palio": 0.7, "HB20": 0.5, "Corolla": 0.3},
    "distance_to_nis": {"Palio": 0.3, "HB20": 0.5, "Corolla": 0.7},
    "topsis_score": {"Palio": 0.3, "HB20": 0.5, "Corolla": 0.7},
    "ranking": ["Corolla", "HB20", "Palio"]
  }
}
```

## Licença
Este projeto está sob a licença MIT.
