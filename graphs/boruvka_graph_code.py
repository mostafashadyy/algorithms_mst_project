#boruvka
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Data for Boruvka
datasets = ['USAir97', 'G13', 'Trefethen_2000', 'LHR04C', 'amazon0302']
nodes = np.array([332, 800, 2000, 4101, 262111])
edges = np.array([2126, 1600, 21953, 82682, 1234877])
costs = np.array([17805.33, 15430.17, 240731.86, 992329.52, 22227561.72])

log_nodes = np.log10(nodes)
log_edges = np.log10(edges)
log_costs = np.log10(costs)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(log_nodes, log_edges, log_costs, marker='o', linestyle='--', color='black', label='Computational Complexity Growth')
point_colors = ['red', 'green', 'blue', 'orange', 'purple']
for i in range(len(datasets)):
    ax.scatter(log_nodes[i], log_edges[i], log_costs[i], color=point_colors[i], s=50, label=f'{datasets[i]}: {point_colors[i]}')

ax.set_xlabel('log(Number of Nodes)', labelpad=10)
ax.set_ylabel('log(Number of Edges)', labelpad=10)
ax.set_zlabel('log(Computational Cost)', labelpad=0)
ax.set_title("Empirical Runtime Growth of Borůvka’s Algorithm:  O(E log V)\nNodes vs Edges and Cost", pad=20)
ax.legend()
fig.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05)
plt.show()


