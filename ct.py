# %%
import networkx as nx
import matplotlib.pyplot as plt

# %%
G = nx.DiGraph()
G.add_nodes_from([1, 2, 3, 4, 5])
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)])

# %%
labels = {}
labels[1] = r"$a$"
labels[2] = r"$b$"
labels[3] = r"$c$"
labels[4] = r"$d"
labels[5] = r"$e"
pos = nx.spring_layout(G)

nx.draw(G, pos, labels=dict([(n + 1, n + 1) for n in range(5)]))

# %%
path = nx.shortest_path(G, source=1, target=5, method='dijkstra')

ncolors = []
for e in G.edges():
    if e in zip(path, path[1:]):
        ncolors.append("red")
    else:
        ncolors.append("black")

nx.draw(G, pos, edge_color=ncolors, labels=labels)

plt.show()
# %%
