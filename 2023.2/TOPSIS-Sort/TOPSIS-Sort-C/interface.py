import streamlit as st
from topsis_sort_c import *
import pandas as pd
import ast

# Titulos da pagina
st.set_page_config(page_title="Topsis Sort C", page_icon=":space_invader:", layout="wide", initial_sidebar_state="expanded")
st.title('Algoritmo Topsis Sort-C')

# Criando barra lateral
sidebar = st.sidebar
# Adicionando opções para barra lateral
expander = sidebar.expander("Options", expanded=False)

with expander:
    sidebar.title("Entrada")
    # Adicionando botão de rádio para escolher o tipo de entrada
    input_type = sidebar.radio("Escolha o tipo de entrada", ("Entrada manual", "Upload de arquivo CSV"))
    if input_type == "Upload de arquivo CSV":
        # Adicionando botão de upload de arquivo CSV
        uploaded_file1 = sidebar.file_uploader("Arquivo CSV para Matriz")
        uploaded_file2 = sidebar.file_uploader("Arquivo CSV para os Perfis")
        uploaded_file3 = sidebar.file_uploader("Arquivo CSV para os Pesos")
        uploaded_file4 = sidebar.file_uploader("Arquivo CSV para os Critérios")
    elif input_type == "Entrada manual":
        # Adicionando campos de entrada para matriz, perfis, pesos e critério
        matriz_input = sidebar.text_input("Matriz")
        perfis_input = sidebar.text_input("Perfis")
        pesos_input = sidebar.text_input("Pesos")
        criterio_input = sidebar.text_input("Critérios")
    else:
        pass

matriz = perfis = pesos = criterio = None

# Verificando se os arquivos foram carregados ou os dados foram inseridos
if input_type == "Upload de arquivo CSV" and uploaded_file1 is not None and uploaded_file2 is not None and uploaded_file3 is not None and uploaded_file4 is not None:
    # Lendo os arquivos CSV e convertendo em dataframes
    df_matriz = pd.read_csv(uploaded_file1, header=None)
    df_perfis = pd.read_csv(uploaded_file2, header=None)
    df_pesos = pd.read_csv(uploaded_file3, header=None)
    df_criterio = pd.read_csv(uploaded_file4, header=None)
    matriz = df_matriz.values.tolist()
    perfis = df_perfis.values.tolist()
    pesos = df_pesos.values.tolist()
    criterio = df_criterio.values.tolist()[0]
elif input_type == "Entrada manual" and matriz_input and perfis_input and pesos_input and criterio_input:
    # Convertendo as entradas de string para listas
    matriz = ast.literal_eval(matriz_input)
    perfis = ast.literal_eval(perfis_input)
    pesos = ast.literal_eval(pesos_input)
    criterio = ast.literal_eval(criterio_input)
else:
    pass

if matriz and perfis and pesos and criterio:
    resultado = topsis(matriz, pesos, perfis, criterio)

    # Estilizando a saída da função topsis
    st.text('Classificação das alternativas da matriz de acordo com os perfis')

    cores = ['#01DF3A', '#DBA901', '#DF3A01']
    for i, item in enumerate(resultado):
        cor = cores[i % len(cores)]

        html = f"""
            <div style="
                font-size: 18px;
                color: {cor};
                border: 1px solid #ddd;
                padding: 10px;
                margin: 5px;
                border-radius: 12px;
                max-width: 300px;
            ">
                {item}
            </div>
        """

        st.write(html, unsafe_allow_html=True)
else:
    if input_type == "Entrada manual":
        st.error("Por favor, insira os dados manualmente.")
    elif input_type == "Upload de arquivo CSV":
        st.error("Por favor, insira os arquivos CSV.")
