# Weighted Fuzzy Reference Ideal Method (W-FRIM)

Este projeto implementa o **Weighted Fuzzy Reference Ideal Method (W-FRIM)**, uma abordagem multicritério baseada em lógica fuzzy para auxiliar na **avaliação e ranqueamento de alternativas** considerando pesos de critérios, referências ideais e estruturas de preferência.

## Como Funciona

O método recebe um único arquivo JSON contendo:

- **Critérios**
- **Alternativas** com valores fuzzy por critério
- **Faixas de valores esperados** por critério
- **Referências ideais fuzzy**
- **Estrutura de preferência (λ)** por critério
- **Pesos fuzzy** por critério

Esses dados são processados para:

- Normalizar os valores fuzzy com base nas referências ideais;
- Ponderar os valores normalizados usando os pesos dos critérios;
- Calcular os índices relativos de cada alternativa;
- Gerar o ranqueamento das alternativas.


## Estrutura dos Arquivos

```
.
├── data/
│   ├── input.json
├── main.py
└── README.md
```

## Instalação

Requisitos:
- Python 3.7+

## Execução

Rode o script principal com:

```bash
python main.py
```

## Exemplo de Entrada (`input.json`)

```json
{
  "method": "W-FRIM",
  "parameters": {
    "criteria": ["C1", "C2", "C3", "C4", "C5", "C6"],
    "performance_matrix": [
      {
        "name": "A1",
        "values": {
          "C1": [3.3712, 3.44, 3.5088],
          "C2": [2.9890, 3.05, 3.1110],
          "C3": [12.6518, 12.91, 13.1682],
          "C4": [0.5350, 0.546, 0.5569],
          "C5": [0.1274, 0.13, 0.1326],
          "C6": [1.0141, 1.0348, 1.0555]
        }
      }
      // ...
    ],
    "range": {
      "C1": [[2.4304, 2.4800, 2.5296], [3.9396, 4.0200, 4.1004]]
      // ...
    },
    "reference_ideal": {
      "C1": [[3.4300, 3.500, 3.5700], [3.9396, 4.0200, 4.1004]]
      // ...
    },
    "preferences": {
      "C1": 1,
      "C2": 1,
      // ...
    },
    "weights": {
      "C1": [0.1568, 0.1600, 0.1632],
      // ...
    }
  }
}
```

## Exemplo de Saída (`output.json`)

```json
{
  "method": "W-FRIM",
  "results": {
    "ranking": ["A8", "A2", "A4", "A5", "A7", "A9", "A10", "A1", "A3", "A6", "A11"],
    "scores": {
      "A1": 0.379715,
      "A2": 0.539774,
      "A3": 0.377886,
      "A4": 0.493291,
      "A5": 0.460452,
      "A6": 0.358407,
      "A7": 0.441508,
      "A8": 0.577422,
      "A9": 0.416644,
      "A10": 0.413317,
      "A11": 0.208098
    },
    "normalized_weights": {
      "A1": {
        "C1": 0.13986,
        "C2": 0.120719,
        "C3": 0.13683,
        "C4": 0.118757,
        "C5": 0.02649,
        "C6": 0.125826
      },
      // ...
    }
  }
}
```

## Referência Teórica

A implementação do método está baseado no artigo W-FRIM: A weighted fuzzy RIM approach.

## Autores
Victoria Pantoja - vpa@cin.ufpe.br