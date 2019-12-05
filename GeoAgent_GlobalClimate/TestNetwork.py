import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# l = a.size
# timelag = 4
# r=range(timelag,l)
# s=range(0,timelag)
# b=a[np.hstack([range(timelag,l),range(0,timelag)])]
# print(b.size)
# print(a)
# print(b)
# print(a*b)


# G = nx.Graph()
# G.add_node(1)
# G.add_edge(2, 3)
# print("输出全部节点：{}".format(G.nodes()))
# print("输出全部边：{}".format(G.edges()))
# print("输出全部边的数量：{}".format(G.number_of_edges()))
# nx.draw(G)
# plt.show()


# G = nx.DiGraph()
# G.add_node(1)
# G.add_node(2)
# G.add_nodes_from([3, 4, 5, 6])
# G.add_cycle([1, 2, 3, 4])
# G.add_edge(1, 3)
# G.add_edges_from([(3, 5), (3, 6), (6, 7)])
# print("输出全部节点：{}".format(G.nodes()))
# print("输出全部边：{}".format(G.edges()))
# print("输出全部边的数量：{}".format(G.number_of_edges()))
# nx.draw(G)
# plt.show()


# G = nx.cubical_graph()
# plt.subplot(121)
# nx.draw(G)
# plt.subplot(122)
# nx.draw(G, pos=nx.circular_layout(G), nodecolor='r', edge_color='b')
# plt.show()


# G = nx.path_graph(8)
# nx.draw(G)
# plt.show()


# G = nx.cycle_graph(24)
# pos = nx.spring_layout(G, iterations=200)
# nx.draw(G, pos, node_color=range(24), node_size=800, cmap=plt.cm.Blues)
# plt.show()


# G = nx.petersen_graph()
# plt.subplot(121)
# nx.draw(G, with_labels=True, font_weight='bold')
# plt.subplot(122)
# nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
# plt.show()



# import networkx as nx
# G = nx.Graph()
# # G.add_edge(1, 2)  # default edge data=1
# G.add_edge(2, 3, weight=0.9)  # specify edge data
# import math
# G.add_edge('y', 'x', function=math.cos)
# G.add_node(math.cos)  # any hashable can be a node
# elist = [(1, 2), (2, 3), (1, 4), (4, 2)]
# G.add_edges_from(elist)
# elist = [('a', 'b', 5.0), ('b', 'c', 3.0), ('a', 'c', 1.0), ('c', 'd', 7.3)]
# G.add_weighted_edges_from(elist)

import matplotlib.pyplot as plt
import networkx as nx

G = nx.star_graph(20)
pos = nx.spring_layout(G)
colors = range(20)
nx.draw(G, pos, node_color='#A0CBE2', edge_color=colors,
        width=4, edge_cmap=plt.cm.Blues, with_labels=False)
plt.show()
