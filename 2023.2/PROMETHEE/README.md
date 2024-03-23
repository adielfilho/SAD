Esse código também foi upado como uma biblioteca, pode ser acessado através do link:

https://pypi.org/project/Promethee/1.0/

Instale com o pip:

`pip install Promethee==1.0`

importe com o código:

`from Promethee import promethee`

----------------------------------------------------------------------------------------------------------------------

O executável do código está dentro da pasta 'PROMETHEEII'.
Essa aplicação executa o algoritmo de PROMETHEE II para ordenar problemas com base em critérios e fornecer um ranking.
Ao executá-lo, é necessário importar uma planilha excel com os valores de critério e de problemas, seguindo o seguinte padrão (no repositório já tem uma planilha exemplo):

  
|    | C1 | C2 | C3  |
|----|----|----|-----|
| D1 | 6  | 7  | 10  |
| D2 | 9  | 8  | 9   |
| D3 | 8  | 2  | 8   |
| D4 | 7  | 8  | 5   |
| D5 | 1  | 10 | 10  |
| D6 | 8  | 3  | 8   |
| D7 | 6  | 10 | 9   |
| D8 | 1  | 2  | 6   |
|    | 0.4| 0.5| 0.1 |


Onde c1, c2, c3 são os critéirios escolhidos, d1, d2, d3 são os problemas escolhidos, e na linha logo abaixo do ultimo problema deve ser 
colocado os valores dos pesos na ordem de cada critério. (a planilha no repositório traz um exemplo de como o modelo deve ser)

Após a importação da planilha, basta selecionar qual o função que prefere utilizar, entre elas estão:

1. Usual Criterion
2.U-shape Criterion
3. V-shape Criterion
4. Level Criterion
5. V-Shape with indiference criterion
6. Gaussion Criterion

A aplicação retornará na tela cada problema com os seus respectivos valores de fluxo líquido.

## Limitações e Melhorias

Uma limitação desse código é que a função de preferência é aplicada a todos os critérios, não sendo possível escolher uma por critério. Além disso, é possível a implementação
futura do Beta-Promethee, uma melhoria no Promethee II, onde há uma otimização no processo de escolha de critérios.
