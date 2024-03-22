import streamlit as st
import pandas as pd
import numpy as np
from topsis_sort_b import topsis_b_sort_profile_classification

def main():
    st.title("Topsis-Sort-B")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"]) # TODO: Validar

    if uploaded_file is not None:
        # Read the content of the uploaded file
        data = np.loadtxt(uploaded_file, delimiter=',', skiprows=1)
        uploaded_file.seek(0)
        first_line = uploaded_file.readline().decode().strip()

    # Dividir os nomes das colunas usando a vírgula como delimitador
        column_names = first_line.split(',')
        # Matriz de decisão 
        decision_matrix = data[:, 0:]
        num_columns = decision_matrix.shape[1]
        st.write('Perfil dominante')
        container = st.container()
        
        # Dicionário para armazenar os valores dos inputs
        inputs = {}

        # Cria os inputs dentro das colunas
        for i in range(num_columns):
            input_name = f"num{i + 1}"
            valor = st.number_input(f"Digite o número {i + 1}:", min_value=1, max_value=10, step=1, key=input_name)
            inputs[input_name] = valor

        st.write(f'Número de valores na Matriz de Domínio: {num_columns}')
        values = []
        for i in range(num_columns):
            value = st.slider(f'Valor {i+1}', 1, 100, 50)
            values.append(value)
        values = np.array(values)

        st.write(f'Número de pesos: {num_columns}')
        weights = []
        for i in range(num_columns):
            peso = st.slider(f'Peso {i+1}', 0.1, 1.0, 0.1)
            weights.append(peso)
        weights = np.array(weights)

        dominant_profiles = np.array([[inputs[f"num{i+1}"] for i in range(num_columns)]])
        domain_matrix = np.array([values for _ in range(2)])

        if st.button("Visualizar Resultados"):
            classification_result, best_solution, best_profile = topsis_b_sort_profile_classification(decision_matrix, domain_matrix, dominant_profiles, weights)
        
            indices_sorted = np.argsort(classification_result[:, 1])[::-1]
            indices_top_10 = indices_sorted[:5]
            classification_result_sorted = classification_result[indices_top_10]
            df_classification_result = pd.DataFrame(classification_result_sorted, columns=["Dominant Profile", "Approximation Coefficient"])
            
            st.write("Classification Result:")
            st.table(df_classification_result)
            
            df_best_solution = pd.DataFrame([best_solution], columns=[f"{column_names[i]}: {i}" for i in range(len(best_solution))])
            st.write("Best Solution:")
            st.table(df_best_solution.to_dict(orient='records'))

            st.write("Dominant Profile of the Best Solution:", best_profile)

    else:
        st.warning("Please upload a CSV file.")

if __name__ == "__main__":
    main()
