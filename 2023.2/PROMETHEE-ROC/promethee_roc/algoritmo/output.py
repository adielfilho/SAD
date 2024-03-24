import numpy as np
import matplotlib.pyplot as plt

def print_resultado(nodes, data):
    print_graph_classificacao_total(nodes)
    print_table_classificacao_parcial(data, "Classificação Parcial")
    plt.tight_layout()  # Ajusta automaticamente o layout para evitar sobreposição
    plt.show()

def print_graph_classificacao_total(nodes):
    num_nodes = len(nodes)

    x = np.ones(num_nodes)
    y = np.arange(num_nodes, 0, -1)

    # Calcula os limites mínimo e máximo para x e y
    min_x, max_x = np.min(x) - 1, np.max(x) + 1
    min_y, max_y = np.min(y) - 1, np.max(y) + 1

    # Tamanho da figura com base nos limites das coordenadas
    width = max_x - min_x
    height = max_y - min_y

    plt.figure(figsize=(width, height))

    for i in range(1, len(x)):
        plt.plot([x[i - 1], x[i]], [y[i - 1], y[i]], color='black', zorder=1)

    plt.scatter(x, y, s=500, color='lightblue', zorder=2)

    padding = 0.2
    for i, node in enumerate(nodes):
        plt.text(x[i] + padding, y[i], node, horizontalalignment='left', verticalalignment='center', color='black')

    plt.title("Classificação Total")

    plt.xlim(min_x - padding, max_x + padding)
    plt.ylim(min_y - padding, max_y + padding)

    plt.gca().set_aspect('equal', adjustable='box')

    plt.axis('off')

def print_table_classificacao_parcial(data, title):
    fig, ax = plt.subplots()
    ax.axis('off')

    table = ax.table(cellText=[[row] for row in data],
                     colLabels=[title],
                     loc='center',
                     cellLoc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)

    plt.title(title)