## Topsis Sort B
##### O que é o TOPSIS-Sort-B
###### O TOPSIS-Sort-B é uma variação aprimorada do método TOPSIS-Sort, desenvolvido para lidar com problemas de classificação e ordenação de alternativas em múltiplos critérios. Neste método, são utilizados perfis de fronteira para determinar as classes de categorização e realizar a ordenação das alternativas de acordo com a proximidade de seus coeficientes de proximidade em relação aos perfis estabelecidos.

###### A principal inovação do TOPSIS-Sort-B é a abordagem de utilizar apenas perfis de fronteira de classe 1 em vez de perfis de limite superior e inferior para cada classe. Isso simplifica o processo de determinação dos perfis e evita possíveis reversões de classificação que podem ocorrer em métodos tradicionais de TOPSIS. Além disso, o TOPSIS-Sort-B inclui uma etapa para definir um domínio para cada critério e oferece uma opção de normalização de intervalo, o que é mais apropriado para situações em que os critérios possuem diferentes escalas ou domínios.

###### Ao adotar perfis de fronteira e introduzir a normalização de intervalo, o TOPSIS-Sort-B busca melhorar a consistência e a estabilidade das classificações obtidas, garantindo que a adição de novas alternativas ao problema não cause mudanças significativas na ordenação das alternativas existentes. Essa abordagem visa aprimorar a aplicação do método TOPSIS em problemas de classificação, tornando-o mais robusto e confiável para diferentes cenários de tomada de decisão

#### Etapas do cálculo do TOPSIS-Sort-B
##### 1. Determinar a matriz de decisão.
##### 2. **Estabelecer a matriz de perfil de limite.**
    1. Representa perfis hipotéticos com o melhor e o pior desempenho em cada critério.
##### 3. Determinar o domínio de cada critério, logo iremos obter os valores máximos e mínimos que podem ser alcançados por cada alternativa em seus critérios. Ponto **importante na solução ideia e anti-ideal.**
    1. Define os limites superior e inferior para cada critério.

##### 4. Estabelecer a matriz de decisão completa e normalizada.

##### 5. **Determinar a matriz de decisão ponderada e normalizada.**
    1. Normalização pelo Max
    2. Normalização de intervalo
##### 6. **Determine a solução ideal e anti-ideal.**                     
    
    a. Vetor com os melhores valores em cada critério
    b. Vetor com os piores valores
    
##### 7. **Calculo da distancia Euclidianas**  

    1. Distancia de cada alternativa
       b.  Distância das soluções ideais e anti-ideais

##### 8. **Calculo do coeficiente (CI)**                                          
    
    a. Calcular o coeficiente de proximidade de cada alternativa e perfil para ideal e anti-ideal
    
##### 9. **Classificação das alternativas**                                      
    1. Alternativas são ordenadas de acordo com os valores do coeficiente de Proximidade
    2. Alternativa CI que mais se aproxima da solução ideal será escolhido