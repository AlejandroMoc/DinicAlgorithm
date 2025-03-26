#%%
import networkx as nx
import matplotlib.pyplot as plt
import collections
#-------------------------------------------------------------------------------------------------------------------
#%%
# Función para leer el grafo desde un archivo
def read_graph(grafoFile):
    with open(grafoFile, 'r') as file:
        lines = file.readlines()
        nodoInicio, nodoFinal, num_edges = map(int, lines[0].split())
        edges = [tuple(map(int, line.split())) for line in lines[1:]]

    graph = nx.DiGraph()
    graph.add_nodes_from(range(nodoInicio, nodoFinal + 1))
    graph.add_edges_from([(u, v, {'capacity': c, 'flow': 0}) for u, v, c in edges])

    return graph, nodoInicio, nodoFinal

archivoGrafo = "archivo.txt" 
grafo, nodoInicio, nodoFinal = read_graph(archivoGrafo)
#-------------------------------------------------------------------------------------------------------------------
# %%
#Dibujo del grafo original
labels = dict([(n, n) for n in grafo.nodes()])
# Asigna el color naranja a todos los nodos
colores_nodos = ['orange'] * len(grafo.nodes())
nx.draw(grafo, labels=labels, node_color=colores_nodos, with_labels=True)
plt.show()
#-------------------------------------------------------------------------------------------------------------------
# %%
#Calcular Los Niveles del Grafo
def calcularNiveles(graph, nodoInicio):
    levels = {nodoInicio: 0}
    queue = collections.deque([nodoInicio])

    while queue:
        current_node = queue.popleft()
        for successor in graph.successors(current_node):
            if successor not in levels:
                levels[successor] = levels[current_node] + 1
                queue.append(successor)

    return levels

levels = calcularNiveles(grafo, nodoInicio)
#-------------------------------------------------------------------------------------------------------------------
# %%
# Visualizar Grafo Niveles Originales
def visualizarNiveles(graph, levels):
    pos = nx.spring_layout(graph)
    node_colors = ['orange'] * len(graph.nodes())
    edge_labels = {(u, v): graph[u][v]['capacity'] for u, v in graph.edges()}
    
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.Oranges, font_size=14, width=2)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=11, font_color='blue')
    
    for node, (x, y) in pos.items():
        plt.text(x+0.08, y+0.08, f"Nivel: {levels[node]}", fontsize=12, ha='center', va='center', color='red')

    plt.show()

# Llama a la función con el grafo y niveles
visualizarNiveles(grafo, levels)
#-------------------------------------------------------------------------------------------------------------------
# %%
def visualizarGrafo(graph, levels=None, path=None, edge_color=None):
    pos = nx.spring_layout(graph)

    if levels:
        node_colors = [levels[node] for node in graph.nodes()]
        edge_labels = {(u, v): graph[u][v]['capacity'] for u, v in graph.edges()}
        nx.draw(graph, pos, with_labels=True, font_weight='', node_color=node_colors, cmap=plt.cm.Oranges, width=2, edge_color=edge_color)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    elif path:
        nx.draw(graph, pos, with_labels=True, font_weight='bold', edge_color=edge_color, width=2)
    else:
        edge_labels = {(u, v): graph[u][v]['capacity'] for u, v in graph.edges()}
        nx.draw(graph, pos, with_labels=True, font_weight='bold', width=2, edge_color=edge_color)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    plt.show()




# Función para realizar una búsqueda en anchura (BFS) en el grafo
def bfs(graph, source, target, path_color=None):
    visited = set()
    queue = collections.deque([(source, [source])])

    while queue:
        current_node, path = queue.popleft()
        visited.add(current_node)

        for successor in graph.successors(current_node):
            if successor not in visited and graph[current_node][successor]['capacity'] > 0:
                if successor == target:
                   if path_color:
                    visualizarGrafo(graph, path=path, edge_color=path_color)

                    return path + [successor]
                queue.append((successor, path + [successor]))

    return []

# Función para actualizar el flujo en el grafo
def update_flow(graph, path):
    min_capacity = min(graph[u][v]['capacity'] for u, v in zip(path[:-1], path[1:]))
    
    for u, v in zip(path[:-1], path[1:]):
        # Actualizar flujo en la dirección original
        graph[u][v]['capacity'] -= min_capacity
        graph[u][v]['flow'] += min_capacity

        # Verificar si la clave v existe en el diccionario graph
        if v in graph:
            # Verificar si la clave u existe en el diccionario graph[v]
            if u in graph[v]:
                # Actualizar capacidad en la dirección inversa
                graph[v][u]['capacity'] += min_capacity
                # Actualizar flujo en la dirección inversa
                graph[v][u]['flow'] -= min_capacity
            else:
                # Si la clave u no existe en graph[v], crear una nueva arista inversa
                graph.add_edge(v, u, capacity=min_capacity, flow=-min_capacity)

# Función principal para el algoritmo de Dinic
def dinic(graph, source, target):
    levels = calcularNiveles(graph, source)
    visualizarNiveles(graph, levels)

    while levels[target] is not None:
        path_color = iter(plt.cm.rainbow(i / len(graph.edges())) for i in range(len(graph.edges())))
        current_color = next(path_color)
        
        path = bfs(graph, source, target, path_color=current_color)

        if not path:
            break

        update_flow(graph, path)

        levels = calcularNiveles(graph, source)
        visualizarNiveles(graph, levels)





dinic(grafo, nodoInicio, nodoFinal)
#%%
#Grafo Final 
visualizarGrafo(grafo)
#-------------------------------------------------------------------------------------------------------------------
 #%%
