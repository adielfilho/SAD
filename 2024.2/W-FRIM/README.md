# Weighted Fuzzy Reference Ideal Method (W-FRIM)

Este projeto implementa o **Weighted Fuzzy Reference Ideal Method (W-FRIM)**, uma abordagem multicritério baseada em lógica fuzzy para auxiliar na **avaliação e ranqueamento de alternativas** considerando pesos de critérios, referências ideais e estruturas de preferência.

## 🧠 Como Funciona

O método recebe quatro conjuntos de dados:

1. **Matriz de decisão fuzzy** (`table1_fuzzy_decision_matrix.csv`)
2. **Faixas de valores e referências ideais** (`table2_range_reference_ideal.csv`)
3. **Lambdas de preferência para cada critério** (`table3_preference_structure.csv`)
4. **Pesos dos critérios** (`table4_criterion_weights.csv`)

Esses dados são processados para:

- Normalizar os valores fuzzy com base nas referências ideais;
- Ponderar os valores normalizados usando os pesos dos critérios;
- Calcular os índices relativos de cada alternativa;
- Gerar o ranqueamento das alternativas.

## 📁 Estrutura dos Arquivos

```
.
├── data/
│   ├── table1_fuzzy_decision_matrix.csv
│   ├── table2_range_reference_ideal.csv
│   ├── table3_preference_structure.csv
│   └── table4_criterion_weights.csv
├── main.py
└── README.md
```

## 📥 Instalação

Requisitos:
- Python 3.7+
- pandas
- numpy

Instale as dependências com:

```bash
pip install pandas numpy
```

## ▶️ Execução

Rode o script principal com:

```bash
python main.py
```

A saída incluirá:

- Matriz de decisão normalizada
- Matriz ponderada
- Índices relativos para cada alternativa
- Ranqueamento final

## 📌 Exemplo de Saída

```
Normalized Decision Matrix (N):
[[0.83 0.91 0.77]
 [0.62 0.80 0.70]
 [0.90 0.95 0.85]]

Weighted Normalized Decision Matrix (P):
[[0.25 0.36 0.23]
 [0.19 0.32 0.21]
 [0.27 0.38 0.28]]

Relative Indices for Alternatives:
Alternative A1: 0.621574
Alternative A2: 0.482113
Alternative A3: 0.841997

Ranking of Alternatives (Best First):
Rank 1: Alternative A3 (Relative Index = 0.841997)
Rank 2: Alternative A1 (Relative Index = 0.621574)
Rank 3: Alternative A2 (Relative Index = 0.482113)
```

## 🧪 Estrutura dos Dados

- **table1_fuzzy_decision_matrix.csv**:
  ```
  C1_l,C1_m,C1_u,C2_l,C2_m,C2_u,...
  3,4,5,2,3,4,...
  ```

- **table2_range_reference_ideal.csv**:
  ```
  Range_A_l,Range_A_m,Range_A_u,RefIdeal_C_l,RefIdeal_C_m,RefIdeal_C_u,RefIdeal_D_l,RefIdeal_D_m,RefIdeal_D_u
  ```

- **table3_preference_structure.csv**:
  ```
  Criterion,Lambda
  1,0.6
  ```

- **table4_criterion_weights.csv**:
  ```
  Criterion,Weight_l,Weight_m,Weight_u
  ```

## 🧠 Referência Teórica

A implementação do método está baseado no artigo W-FRIM: : A weighted fuzzy RIM approach.

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).