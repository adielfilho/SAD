import pandas as pd
from tkinter import *
from tkinter import filedialog  # Importa a biblioteca filedialog para abrir uma janela de seleção de arquivo

# Importando a função promethee do módulo functions
from functions import promethee

# Função para centralizar a janela
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x_offset = (window.winfo_screenwidth() - width) // 2
    y_offset = (window.winfo_screenheight() - height) // 2
    window.geometry(f"+{x_offset}+{y_offset}")

# Função para fechar a janela após clicar em "Confirmar"
def close_window(window):
    window.destroy()

def pop_window():
    # Criar nova janela para digitar q e p
    input_window = Toplevel(root)
    input_window.title("Entrada de Variáveis")
    input_window.geometry("300x120")
    center_window(input_window)

    return input_window

# Função para processar o clique dos botões
def process_button_click(tipo):
    if tipo == 2 or tipo == 3:
        # Criar nova janela para digitar q
        input_window = pop_window()
        label_q = Label(input_window, text="Valor de q:")
        label_q.pack()
        q_entry = Entry(input_window)
        q_entry.pack()

        # Botão para confirmar e processar
        confirm_button = Button(input_window, text="Confirmar", command=lambda: process_with_variables(tipo, q_entry.get(), None, input_window))
        confirm_button.pack()

    elif tipo == 4 or tipo == 5:
        input_window = pop_window()
        label_q = Label(input_window, text="Valor de q:")
        label_q.pack()
        q_entry = Entry(input_window)
        q_entry.pack()

        label_p = Label(input_window, text="Valor de p:")
        label_p.pack()
        p_entry = Entry(input_window)
        p_entry.pack()

        # Botão para confirmar e processar
        confirm_button = Button(input_window, text="Confirmar", command=lambda: process_with_variables(tipo, q_entry.get(), p_entry.get(), input_window))
        confirm_button.pack()

    elif tipo == 6:
        input_window = pop_window()
        label_q = Label(input_window, text="Valor de q:")
        label_q.pack()
        q_entry = Entry(input_window)
        q_entry.pack()

        # Botão para confirmar e processar
        confirm_button = Button(input_window, text="Confirmar", command=lambda: process_with_variables(tipo, q_entry.get(), None, input_window))
        confirm_button.pack()
    else:
        # Chamada da função promethee
        q, p = 0 , 0
        phi = promethee(df, pesos, tipo, q, p)
        
        # Atualiza o DataFrame com os resultados
        new_df = df.copy(deep=True)
        new_df.loc[:, 'Fluxo'] = list(phi)
        # Atualiza o Text Widget com o DataFrame
        output_text.delete(1.0, END)
        output_text.insert(END, new_df)

# Função para processar após a entrada das variáveis
def process_with_variables(tipo, q, p, window):
    q = int(q)
    if p:
        p = int(p)
    else:
        p = None

    # Chamada da função promethee
    phi = promethee(df, pesos, tipo, q, p)
    
    # Atualiza o DataFrame com os resultados
    new_df = df.copy(deep=True)
    new_df.loc[:, 'Fluxo'] = list(phi)
    
    # Atualiza o Text Widget com o DataFrame
    output_text.delete(1.0, END)
    output_text.insert(END, new_df)

    # Fecha a janela de entrada de variáveis
    close_window(window)

def import_excel():
    global linhas
    global colunas
    global pesos
    global dados
    global df
    # Abre uma janela de seleção de arquivo para o usuário escolher o arquivo Excel
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])

    if file_path:
        # Carrega os dados do arquivo Excel selecionado
        excel_data = pd.read_excel(file_path)
        print(excel_data)
    
        # Pega o Df do excel e o trata para pegar a lista de critérios, problemas, pesos, etc
        excel_data['Unnamed: 0'] = excel_data['Unnamed: 0'].fillna(0)
        linhas = list(excel_data['Unnamed: 0'])
        linhas = [x for x in linhas if x != 0]
        colunas = excel_data.columns.values[1:]
        pesos = list(excel_data.iloc[len(linhas)][1:])
        
        dados = []
        for i in range(len(linhas)):
            sub_data = list(excel_data.iloc[i][1:])
            dados.append(sub_data)
        
        df = pd.DataFrame(data=dados,index=linhas,columns=colunas)

        return df

# Criando a janela principal
root = Tk()
root.title("Análise Promethee")
root.geometry("600x400")

# Centralizar a janela principal
center_window(root)

# Criando um frame para os botões
button_frame = Frame(root)
button_frame.pack()

# Criando os botões com opções correspondentes
button_texts = ["Usual Criterion", "U-shape Criterion", "V-shape Criterion", "Level Criterion", "Level Criterion", "Gaussian Criterion"]
buttons = []
for i, text in enumerate(button_texts, start=1):
    button = Button(button_frame, text=text, command=lambda i=i: process_button_click(i))
    button.grid(row=0, column=i-1)
    buttons.append(button)

# Adicionando o botão para importar uma planilha Excel
import_button = Button(root, text="Importar Excel", command=import_excel)
import_button.pack(side=BOTTOM)  # Coloca o botão na parte inferior da tela

# Text Widget para mostrar o DataFrame
output_text = Text(root, height=10, width=50)
output_text.pack(fill=BOTH, expand=True)

root.mainloop()
