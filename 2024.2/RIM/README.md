# **📚 Implementação do Método RIM em Python**  

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python" alt="Python Version">
</div>  

---

## **🏛️ Instituição**  
**Universidade Federal de Pernambuco (UFPE)**  
**Centro de Informática (CIN)**  
**Disciplina: Sistemas de Apoio à Decisão (2024.2)**  

---

## **👥 Equipe**  
| **Discentes** | **Docente** |  **Monitores** |
|--------------|------------|--------------|
| Franklin Amaral | **Prof. Adiel Teixeira de Almeida Filho** |  Maria Paula Perrazo |
| Leonardo Bezerra | | Daniel Nascimento |
| Maíra Cabral | |  
| Pedro Henrique Medeiros | |  

---

## **📌 Sobre o Projeto**  
Este repositório contém a implementação em Python do **método RIM (Reference Ideal Method)**, uma técnica de apoio à decisão multicritério (MCDA) proposta por **Cables et al. (2016)**.  

O objetivo principal foi:  
✅ **Implementar** o método RIM em Python, seguindo a metodologia do artigo.  
✅ **Validar** os resultados comparando-os com os dados originais.  
✅ **Disponibilizar** uma biblioteca modular e de fácil uso para aplicação em problemas reais.  

---

## **🔍 Método RIM**  
O RIM é um método de decisão multicritério que:  
- **Classifica alternativas** com base em sua proximidade a um **ideal de referência** e distância de um **anti-ideal**.  
- Utiliza **pesos** para critérios, permitindo priorização conforme preferências do decisor.  
- Pode ser aplicado em áreas como **logística, saúde, transporte e meio ambiente**.  

---

## **⚙️ Funcionalidades da Biblioteca**  
✔ **Normalização de dados** (`normalize_with_ideal()`)  
✔ **Cálculo de distâncias** (`calculate_distances()`)  
✔ **Definição de pontos ideais/anti-ideais** (`calculate_indices()`)  
✔ **Ranqueamento de alternativas** (`ranking`)  
✔ **Matriz ponderada normalizada** (`weighted_matrix_dict`)  

---

## **📊 Resultados e Validação**  
- Os resultados foram **consistentes** com os do artigo original.  
- Pequenas divergências foram observadas devido a:  
  - Arredondamentos nos dados publicados.  
  - Diferenças na aplicação de pesos/normalização.  
- **Conclusão**: A implementação reproduziu corretamente o comportamento geral do método.  

---

## **🚀 Como Usar**  
1. **Clone o repositório**:  
   ```bash
   git clone https://github.com/adielfilho/SAD/tree/main/2024.2/RIM
   ```  
2. **Execute o script Python**:  
   ```python
   python rim_method.py
   ```  
3. **Insira seus dados** (matriz de decisão, pesos e critérios).  

---

## **🔧 Pontos de Melhoria Futura**  
🔹 Suporte a **diferentes medidas de distância** (Manhattan, Chebyshev).  
🔹 **Análise de sensibilidade** para variação de pesos.  
🔹 **Interface gráfica (GUI)** ou API para facilitar o uso.  
🔹 **Publicação no PyPI** para instalação via `pip`.  

---

## **📚 Referências**  
- **CABLES, E. et al.** (2016). *RIM – Reference Ideal Method in Multicriteria Decision Making*. Information Sciences.  
- **ONUT, S. et al.** (2015). *A decision support system based on RIM for multimodal transportation problems*.  

### **🌟 Contribuições são bem-vindas!**  
Sinta-se à vontade para abrir **issues** ou **pull requests** com melhorias.  

### Para mais informações acesse o documento completo do projeto em : <a href="https://docs.google.com/document/d/1-ldidP-jWfqh-dLNnGp1xGAKy0j3_Nzi/edit?tab=t.0"> Relatório do projeto</a>

